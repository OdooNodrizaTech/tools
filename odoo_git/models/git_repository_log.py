# -*- coding: utf-8 -*-
from odoo import api, fields, models
import odoo

from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class GirRepositoryLog(models.Model):
    _name = 'git.repository.log'
    _description = 'Git Repository Log'
        
    git_repository_id = fields.Many2one(
        comodel_name='git.repository',
        string='Git Repository'
    )    
    odoo_reboot = fields.Boolean(        
        string='Odoo Reboot'
    )
    date_start = fields.Datetime(        
        string='Date Start'
    )
    date_end = fields.Datetime(        
        string='Date End'
    )