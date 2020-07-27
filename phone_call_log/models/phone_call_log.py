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
        string='Contact name'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )
    mail_activity_id = fields.Many2one(
        comodel_name='mail.activity',
        string='Mail Activity id'
    )

    @api.model
    def create(self, values):
        return_object = super(PhoneCallLog, self).create(values)
        # operations
        if return_object.number:
            if '+' not in return_object.number:
                if return_object.user_id.partner_id.country_id:
                    prefix_number = return_object.user_id.partner_id.country_id.phone_code
                else:
                    prefix_number = return_object.user_id.company_id.country_id.phone_code
                # number
                number = return_object.number
            else:
                prefix_number = return_object.number[1:3]
                number = return_object.number[3:]
            # phone_is_mobile
            phone_is_mobile = True
            if number[0:1] != '6':
                phone_is_mobile = False
            # search
            number_need_check = '+'+str(prefix_number)+str(number)
            if phone_is_mobile:
                res_partner_ids = self.env['res.partner'].search(
                    [
                        ('mobile', '=', number_need_check)
                    ]
                )
            else:
                res_partner_ids = self.env['res.partner'].search(
                    [
                        ('phone', '=', number_need_check)
                    ]
                )
            # items
            if res_partner_ids:
                return_object.partner_id = res_partner_ids[0].id
                # get mail_activity_type
                mail_activity_type_ids = self.env['mail.activity.type'].search(
                    [
                        ('is_phone_call', '=', True)
                    ]
                )
                if mail_activity_type_ids:
                    ir_model_ids = self.env['ir.model'].sudo().search(
                        [
                            ('model', '=', 'res.partner')
                        ]
                    )
                    if ir_model_ids:
                        # create mail_activity
                        vals = {
                            'activity_type_id': mail_activity_type_ids[0].id,
                            'date_deadline': return_object.date,
                            'date_done': return_object.date,
                            'user_id': return_object.user_id.id,
                            'res_model_id': ir_model_ids[0].id,
                            'res_id': return_object.partner_id.id,
                            'res_name': return_object.partner_id.name,
                            'duration': return_object.duration,
                            'automated': True,
                            'done': True,
                            'active': False,
                            'phone_call_type': return_object.type
                        }
                        mail_activity_obj = self.env['mail.activity'].sudo(return_object.user_id.id).create(vals)
                        # update mail_activity_id
                        return_object.mail_activity_id = mail_activity_obj.id
        # return
        return return_object
