# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class CesceFileCheck(models.Model):
    _name = 'cesce.file.check'
    _description = 'Cesce File Check'    
    
    folder = fields.Char(        
        string='Folder'
    )
    file = fields.Char(        
        string='File'
    )                                       