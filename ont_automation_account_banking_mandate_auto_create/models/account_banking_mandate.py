# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning
from datetime import datetime

class AccountBankingMandate(models.Model):
    _inherit = 'account.banking.mandate'            
    
    @api.model
    def create(self, values):
        return_create = super(AccountBankingMandate, self).create(values)
        #operations
        if self.auto_create==True:
            #save_log
            automation_log_vals = {                    
                'model': 'account.banking.mandate',
                'res_id': self.id,
                'category': 'account_banking_mandate',
                'action': 'create',                                                                                                                                                                                           
            }
            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        #return        
        return return_create
    
    @api.model
    def validate(self):
        return_create = super(AccountBankingMandate, self).validate()
        #operations
        if return_create==True:
            if self.auto_create==True:
                #save_log
                automation_log_vals = {                    
                    'model': 'account.banking.mandate',
                    'res_id': self.id,
                    'category': 'account_banking_mandate',
                    'action': 'validate',                                                                                                                                                                                           
                }
                automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        #return        
        return return_create                    
                                                                        