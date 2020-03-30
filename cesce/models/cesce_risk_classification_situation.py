# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class CesceRiskClassificationSituation(models.Model):
    _name = 'cesce.risk.classification.situation'
    _description = 'Cesce Riesgo Clasificacion Situacion'    
    
    code = fields.Char(        
        string='Codigo'
    )
    name = fields.Char(        
        string='Nombre'
    )                                       