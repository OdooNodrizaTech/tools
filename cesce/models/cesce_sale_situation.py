# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class CesceSaleSituation(models.Model):
    _name = 'cesce.sale.situation'
    _description = 'Cesce Situacion Ventas'    
    
    code = fields.Char(        
        string='Codigo'
    )
    name = fields.Char(        
        string='Nombre'
    )                                       