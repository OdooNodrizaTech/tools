# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CescePaymentTerm(models.Model):
    _name = 'cesce.payment.term'
    _description = 'Cesce Payment Term'

    code = fields.Char(
        string='Code'
    )
    name = fields.Char(
        string='Name'
    )
