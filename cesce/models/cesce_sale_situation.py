# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CesceSaleSituation(models.Model):
    _name = 'cesce.sale.situation'
    _description = 'Cesce Situacion Ventas'
    
    code = fields.Char(
        string='Code'
    )
    name = fields.Char(
        string='Name'
    )
