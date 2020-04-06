# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import decimal

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one 
    def action_auto_create(self):                
        return_item = super(AccountInvoice, self).action_auto_create()
        #save_log
        automation_log_vals = {                    
            'model': 'account.invoice',
            'res_id': self.id,
            'category': 'account_invoice',
            'action': 'create',                                                                                                                                                                                           
        }
        automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        #return
        return return_item
        
    @api.one 
    def action_auto_open(self):                
        return_item = super(AccountInvoice, self).action_auto_open()
        #save_log
        automation_log_vals = {                    
            'model': 'account.invoice',
            'res_id': self.id,
            'category': 'account_invoice',
            'action': 'valid',                                                                                                                                                                                           
        }
        automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        #return
        return return_item        