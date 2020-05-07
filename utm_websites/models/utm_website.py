# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class UtmWebsite(models.Model):
    _name = 'utm.website'
    _description = 'Utm website'
    
    name = fields.Char(        
        string='Nombre'
    )
    url = fields.Char(        
        string='Url'
    )
    mail_template_id = fields.Many2one(
        comodel_name='mail.template',        
        string='Mail Template Id'
    )                                