# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class CesceRiskClassificationMotive(models.Model):
    _name = 'cesce.risk.classification.motive'
    _description = 'Cesce Riesgo Classification Motive'    
    
    code = fields.Char(        
        string='Nombre'
    )
    name = fields.Char(        
        string='Nombre'
    )                                       