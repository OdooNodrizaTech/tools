# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CesceSaleMotiveSituation(models.Model):
    _name = 'cesce.sale.motive.situation'
    _description = 'Cesce Motivos Situacion Ventas'
    
    code = fields.Char(
        string='Code'
    )
    name = fields.Char(
        string='Name'
    )
