# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
import odoo

from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class GirAuthor(models.Model):
    _name = 'git.author'
    _description = 'Git Author'
    
    name = fields.Char(        
        string='Nombre'
    )    
    url = fields.Char(        
        string='Url',
        help='Similar to https://github.com/oca'
    )    