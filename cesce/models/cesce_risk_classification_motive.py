# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CesceRiskClassificationMotive(models.Model):
    _name = 'cesce.risk.classification.motive'
    _description = 'Cesce Riesgo Classification Motive'

    code = fields.Char(
        string='Code'
    )
    name = fields.Char(
        string='Name'
    )
