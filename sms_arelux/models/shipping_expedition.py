# -*- coding: utf-8 -*-
from openerp import _, api, exceptions, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'        
    
    date_send_sms_info = fields.Datetime(
        string='Fecha SMS info'
    )
    
    @api.one    
    def action_custom_send_sms_info_slack(self):
        return True
    
    @api.one
    def action_send_sms_info(self, sms_template_id=False):
        if sms_template_id!=False:
            states_skip = ['error', 'generate','canceled', 'delivered']
            if self.state not in states_skip:        
                if self.date_send_sms_info==False:
                    if self.delegation_name!=False and self.delegation_phone!=False:
                        allow_send_sms = True
                        
                        if self.partner_id.mobile==False:
                            allow_send_sms = False
                            
                        if allow_send_sms==True and self.partner_id.mobile_code_res_country_id==False:
                            allow_send_sms = False
                            
                        if allow_send_sms==True:
                            sms_template_item = self.env['sms.template'].search([('id', '=', sms_template_id)])[0]                                
                            sms_compose_message_vals = {
                                'model': 'shipping.expedition',
                                'res_id': self.id,
                                'country_id': self.partner_id.mobile_code_res_country_id.id,
                                'mobile': self.partner_id.mobile,
                                'sms_template_id': sms_template_id
                            }
                            #Fix user_id
                            if self.user_id.id>0:
                                self.env.user.id = self.user_id.id
                                sms_compose_message_obj = self.env['sms.compose.message'].sudo(self.env.user.id).create(sms_compose_message_vals)
                            else:
                                sms_compose_message_obj = self.env['sms.compose.message'].sudo().create(sms_compose_message_vals)
                                
                            return_onchange_sms_template_id = sms_compose_message_obj.onchange_sms_template_id(sms_template_item.id, 'shipping.expedition', self.id)
                            
                            sms_compose_message_obj.update({
                                'sender': return_onchange_sms_template_id['value']['sender'],
                                'message': return_onchange_sms_template_id['value']['message']                                                     
                            })
                            sms_compose_message_obj.send_sms_action()
                            
                            if sms_compose_message_obj.action_send==True:
                                #save_log
                                arelux_automation_log_vals = {                    
                                    'model': 'shipping.expedition',
                                    'res_id': self.id,
                                    'category': 'shipping_expedition',
                                    'action': 'send_sms',                                                                                                                                                                                           
                                }
                                arelux_automation_log_obj = self.env['arelux.automation.log'].sudo().create(arelux_automation_log_vals)
                                #other                                                                                                                                                         
                                self.date_send_sms_info = datetime.today()
                                self.action_custom_send_sms_info_slack()#Fix Slack                                                
                                            
            return True
            
    @api.multi    
    def cron_shipping_expedition_cbl_send_sms_info(self, cr=None, uid=False, context=None):
        cbl_expedition_sms_info_template_id = self.env['ir.config_parameter'].sudo().get_param('cbl_expedition_sms_info_template_id')
        
        shipping_expedition_ids = self.env['shipping.expedition'].search(
            [
                ('carrier_id.carrier_type', '=', 'cbl'),
                ('state', 'not in', ('error', 'generate','canceled', 'delivered')),
                ('date_send_sms_info', '=', False),
                ('delegation_name', '!=', False),
                ('delegation_phone', '!=', False),
                ('partner_id.mobile', '!=', False),
                ('partner_id.mobile', 'not like', '+'),
                ('partner_id.mobile_code_res_country_id', '!=', False),
            ]
        )
        if len(shipping_expedition_ids)>0:
            for shipping_expedition_id in shipping_expedition_ids:
                shipping_expedition_id.action_send_sms_info(cbl_expedition_sms_info_template_id)                                
        
    @api.one    
    def action_generate_shipping_expedition_link_tracker(self):
        return super(ShippingExpedition, self).action_generate_shipping_expedition_link_tracker()
    
    @api.one 
    def cron_shipping_expedition_txt_send_sms_info_item(self, template_id):
        #Fix link_tracker_id
        if self.link_tracker_id.id==0:
            res = self.action_generate_shipping_expedition_link_tracker()
            
        self.action_send_sms_info(template_id)
    
    @api.multi
    def cron_shipping_expedition_txt_send_sms_info(self, cr=None, uid=False, context=None):
        txt_expedition_sms_info_template_id = self.env['ir.config_parameter'].sudo().get_param('txt_expedition_sms_info_template_id')
        
        shipping_expedition_ids = self.env['shipping.expedition'].search(
            [
                ('carrier_id.carrier_type', '=', 'txt'),
                ('state', 'not in', ('error', 'generate','canceled', 'delivered')),
                ('date_send_sms_info', '=', False),
                ('delegation_name', '!=', False),
                ('delegation_phone', '!=', False),
                ('partner_id.mobile', '!=', False),
                ('partner_id.mobile_code_res_country_id', '!=', False),
            ]
        )
        if len(shipping_expedition_ids)>0:
            for shipping_expedition_id in shipping_expedition_ids:
                shipping_expedition_id.cron_shipping_expedition_txt_send_sms_info_item(txt_expedition_sms_info_template_id)                                                                                                                                                                                                                                                    