# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CesceRiskClassificationSituation(models.Model):
    _name = 'cesce.risk.classification.situation'
    _description = 'Cesce Riesgo Clasificacion Situacion'    
    
    code = fields.Char(        
        string='Code'
    )
    name = fields.Char(        
        string='Name'
    )
