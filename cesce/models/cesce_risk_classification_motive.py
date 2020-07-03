# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

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