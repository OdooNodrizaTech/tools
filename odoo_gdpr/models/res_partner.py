# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
        
    not_allow_marketing_mails = fields.Boolean(
        string="Not allow marketing mails"
    )                                                                                                     