# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class AutomationLog(models.Model):
    _name = 'automation.log'
    _description = 'Automation Log'
    
    model = fields.Char(        
        string='Model'
    )
    res_id = fields.Integer(        
        string='Related document'
    )
    category = fields.Selection(
        selection=[
            ('account_invoice','Account Invoice'),
            ('crm_lead','Crm Lead'),
            ('survey_user_input','Survey User Input'),                          
        ],
        string='Categoria'
    )    
    action = fields.Char(        
        string='Accion'
    )