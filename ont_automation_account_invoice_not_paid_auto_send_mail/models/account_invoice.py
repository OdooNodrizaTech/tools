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
    def account_invoice_not_paid_auto_send_mail_item_real(self, mail_template_id, author_id):                
        return_item = super(AccountInvoice, self).account_invoice_not_paid_auto_send_mail_item_real(mail_template_id, author_id)
        #save_log
        automation_log_vals = {                    
            'model': 'account.invoice',
            'res_id': self.id,
            'category': 'account_invoice',
            'action': 'send_mail_not_paid',                                                                                                                                                                                           
        }
        automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        #return
        return return_item