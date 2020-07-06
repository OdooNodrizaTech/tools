# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools

import logging
_logger = logging.getLogger(__name__)

class PhoneCallLog(models.Model):
    _name = 'phone.call.log'
    _description = 'Phone Call Log'

    phone_call_log_file_id = fields.Many2one(
        comodel_name='phone.call.log.file',
        string='Phone Call Log File'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User'
    )
    number = fields.Char(
        string='Number'
    )
    duration = fields.Integer(
        string='Duration'
    )
    date = fields.Datetime(
        string='Date'
    )
    type = fields.Selection(
        selection=[
            (1, 'Incoming'),
            (2, 'Outgoing'),
            (3, 'Missed'),
            (4, 'Voicemail'),
            (5, 'Rejected'),
            (6, 'Refused'),
        ],
        string='Type'
    )
    presentation = fields.Selection(
        selection=[
            (1, 'Allowed'),
            (2, 'Restricted'),
            (3, 'Unknown'),
            (4, 'Payphone'),
        ],
        string='Presentation'
    )
    contact_name = fields.Char(
        string='CONTACT NAME'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead Id'
    )
    mail_message_id = fields.Many2one(
        comodel_name='mail.message',
        string='Mail Message id'
    )

    @api.model
    def create(self, values):
        return_object = super(PhoneCallLog, self).create(values)
        #operations
        if return_object.number!=False:
            if '+' not in return_object.number:
                res_country_ids = self.env['res.country'].search([('phone_code', '=', 34)])
                if len(res_country_ids)>0:
                    code_res_country_id = res_country_ids[0].id
                #number
                number = return_object.number
            else:
                res_country_ids = self.env['res.country'].search([('phone_code', '=', return_object.number[1:3])])
                if len(res_country_ids)>0:
                    code_res_country_id = res_country_ids[0].id
                #number
                number = return_object.number[3:]
            #phone_is_mobile
            phone_is_mobile = True
            if number[0:1]!='6':
                phone_is_mobile = False
            #search
            if phone_is_mobile==True:
                res_partner_ids = self.env['res.partner'].search([('mobile_code_res_country_id', '=', code_res_country_id),('mobile', '=', number)])
            else:
                res_partner_ids = self.env['res.partner'].search([('phone_code_res_country_id', '=', code_res_country_id),('phone', '=', number)])
            #items
            if len(res_partner_ids)>0:
                return_object.partner_id = res_partner_ids[0].id
                #search_lead_id
                crm_lead_ids = self.env['crm.lead'].search([('partner_id', '=', return_object.partner_id.id)])
                if len(crm_lead_ids)>0:
                    #update lead_id
                    return_object.lead_id = crm_lead_ids[0].id
                    #get mail_message_subtype
                    mail_message_subtype_ids = self.env['mail.message.subtype'].search([('is_phone_call', '=', True)])
                    if len(mail_message_subtype_ids)>0:
                        #mail_message_without_parent_ids
                        mail_message_without_parent_ids = self.env['mail.message'].search(
                            [
                                ('parent_id', '=', False),
                                ('res_id', '=', return_object.lead_id),
                                ('model', '=', 'crm.lead')
                            ]
                        )
                        if len(mail_message_without_parent_ids)>0:
                            #create mail_message
                            mail_message_obj = self.env['mail.message'].sudo(return_object.user_id).create({
                                'parent_id': mail_message_without_parent_ids[0].id,
                                'subtype_id': mail_message_subtype_ids[0].id,
                                'res_id': return_object.lead_id,
                                'record_name': return_object.lead_id.name,
                                'date': return_object.date,
                                'model': 'crm.lead',
                                'message_type': 'notification',
                                'duration': return_object.duration,
                                'body': '<div><b>Actividad realizada</b>: Llamada</div><p><br></p>',
                                'phone_call_type': return_object.type
                            })
                            #update mail_message_id
                            return_object.mail_message_id = mail_message_obj.id
        #return
        return return_object