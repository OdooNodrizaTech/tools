# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class CesceSaleMotiveSituation(models.Model):
    _name = 'cesce.sale.motive.situation'
    _description = 'Cesce Motivos Situacion Ventas'    
    
    code = fields.Char(        
        string='Codigo'
    )
    name = fields.Char(        
        string='Nombre'
    )                                       