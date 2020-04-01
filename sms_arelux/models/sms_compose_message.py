# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class SmsComposeMessage(models.Model):
    _name = 'sms.compose.message'
    _description = 'SMS Compose Message'
    
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Pais'
    )
    mobile = fields.Char(
        string='Mobile'
    )
    message = fields.Text(
        string='Mensaje'
    )
    sender = fields.Char(
        string='Sender'
    )
    model = fields.Char(
        string='Message Id'
    )    
    res_id = fields.Integer(
        string='Related Document ID'
    )
    sms_template_id = fields.Many2one(
        comodel_name='sms.template',
        string='Plantilla SMS'
    )
    action_send = fields.Boolean(
        string='Action Send'
    )        
    
    @api.multi
    def send_sms_action(self):
        self.send_message()                
    
    @api.multi
    def send_message(self):        
        for wizard_item in self:
            model_id = self.env['ir.model'].search([('model', '=', wizard_item.model)])[0]
        
            mobile = self.mobile.strip()
            if '+' in str(mobile):
                mobile = mobile.replace('+'+str(wizard_item.country_id.phone_code), '')
                
            mobile = mobile.replace(' ', '')
        
            sms_message_vals = {
                'country_id': wizard_item.country_id.id,
                'mobile': mobile,
                'message': wizard_item.message,
                'sender': wizard_item.sender,
                'model_id': model_id.id,
                'res_id': wizard_item.res_id,
                'user_id': self.env.user.id                                                          
            }                        
            sms_message_obj = self.env['sms.message'].sudo(self.env.user.id).create(sms_message_vals)        
            return_action_send = sms_message_obj.action_send()
            #Fix list
            if isinstance(return_action_send, (list,)):
                return_action_send = return_action_send[0]
                            
            wizard_item.action_send = return_action_send
                                    
            if wizard_item.action_send==True:            
                #update_sale_order
                if wizard_item.model=='sale.order':
                    sale_order_id = self.env['sale.order'].search([('id', '=', wizard_item.res_id)])[0]
                    #date_order_send_sms
                    if sale_order_id.date_order_send_sms==False:
                        sale_order_id.date_order_send_sms = fields.datetime.now()
                    #change_to_sale state
                    if sale_order_id.state=='draft':
                        sale_order_id.state = 'sent'
                        
                #mail_message_note
                mail_message_body = '<b>SMS</b><br/>'+str(sms_message_obj.message)
                mail_message_body = mail_message_body.replace('\n', '<br/>')
                
                mail_message_vals = {
                    'subtype_id': 2,
                    'body': mail_message_body,
                    'record_name': 'SMS',
                    'date': fields.datetime.now(),
                    'res_id': wizard_item.res_id,
                    'model': wizard_item.model,
                    'message_type': 'comment',                                                         
                }                        
                mail_message_obj = self.env['mail.message'].sudo(self.env.user.id).create(mail_message_vals)
                        
        return {'type': 'ir.actions.act_window_close'}
        
    #------------------------------------------------------
    # Template methods
    #------------------------------------------------------

    @api.multi
    @api.onchange('sms_template_id')
    def onchange_sms_template_id_wrapper(self):
        self.ensure_one()
        values = self.onchange_sms_template_id(self.sms_template_id.id, self.model, self.res_id)['value']
        for fname, value in values.iteritems():
            setattr(self, fname, value)

    @api.multi
    def onchange_sms_template_id(self, sms_template_id, model, res_id):
        if sms_template_id:
            values = self.generate_sms_for_composer(sms_template_id, [res_id])[res_id]            
        else:
            default_values = self.with_context(default_model=model, default_res_id=res_id).default_get(['model', 'res_id','sender', 'message'])
            values = dict((key, default_values[key]) for key in ['sender', 'message'] if key in default_values)
        
        if values.get('message'):
            values['message'] = cleanhtml(values['message'])

        # This onchange should return command instead of ids for x2many field.
        # ORM handle the assignation of command list on new onchange (api.v8),
        # this force the complete replacement of x2many field with
        # command and is compatible with onchange api.v7
        values = self._convert_to_write(values)

        return {'value': values}

    @api.multi
    def render_message(self, res_ids):
        """Generate template-based values of wizard, for the document records given
        by res_ids. This method is meant to be inherited by email_template that
        will produce a more complete dictionary, using Jinja2 templates.

        Each template is generated for all res_ids, allowing to parse the template
        once, and render it multiple times. This is useful for mass mailing where
        template rendering represent a significant part of the process.

        Default recipients are also computed, based on mail_thread method
        message_get_default_recipients. This allows to ensure a mass mailing has
        always some recipients specified.

        :param browse wizard: current mail.compose.message browse record
        :param list res_ids: list of record ids

        :return dict results: for each res_id, the generated template values for
                              sender, message, email_from and reply_to
        """
        self.ensure_one()
        multi_mode = True
        if isinstance(res_ids, (int, long)):
            multi_mode = False
            res_ids = [res_ids]

        senders = self.render_template(self.sender, self.model, res_ids)
        messages = self.render_template(self.message, self.model, res_ids, post_process=True)        
        results = dict.fromkeys(res_ids, False)
        for res_id in res_ids:
            results[res_id] = {
                'sender': senders[res_id],
                'message': messages[res_id],
            }

        # generate template-based values
        if self.sms_template_id:
            sms_template_values = self.generate_sms_for_composer(self.sms_template_id.id, res_ids, fields=[])
        else:
            sms_template_values = {}

        for res_id in res_ids:
            sms_template_values[res_id] = dict()
            sms_template_values[res_id].update(results[res_id])

        return multi_mode and sms_template_values or sms_template_values[res_ids[0]]
    
    @api.model
    def generate_sms_for_composer(self, sms_template_id, res_ids, fields=None):
        """ Call sms_template.generate_sms(), get fields relevant for
            sms.compose.message"""
        multi_mode = True
        if isinstance(res_ids, (int, long)):
            multi_mode = False
            res_ids = [res_ids]

        if fields is None:
            fields = ['sender', 'message']
        returned_fields = fields
        values = dict.fromkeys(res_ids, False)

        sms_template_values = self.env['sms.template'].with_context(tpl_partners_only=True).browse(sms_template_id).generate_sms(res_ids, fields=fields)
        for res_id in res_ids:
            res_id_values = dict((field, sms_template_values[res_id][field]) for field in returned_fields if sms_template_values[res_id].get(field))
            res_id_values['message'] = res_id_values.pop('message', '')
            values[res_id] = res_id_values

        return multi_mode and values or values[res_ids[0]]
    
    @api.model
    def render_template(self, template, model, res_ids, post_process=False):
        return self.env['sms.template'].render_template(template, model, res_ids, post_process=post_process)                                                                                                                                                                       