# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

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