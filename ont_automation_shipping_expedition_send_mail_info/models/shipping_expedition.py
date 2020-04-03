# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import decimal

class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'

    @api.one 
    def action_send_mail_info_real(self):                
        return_item = super(ShippingExpedition, self).action_send_mail_info_real()
        #save_log
        automation_log_vals = {                    
            'model': 'shipping.expedition',
            'res_id': self.id,
            'category': 'shipping_expedition',
            'action': 'send_mail_info',                                                                                                                                                                                           
        }
        automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        #return
        return return_item