# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import  fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    phone_call_log_count = fields.Integer(
        compute='_compute_phone_call_log_count',
        string="Phone Calls",
    )

    def _compute_phone_call_log_count(self):
        for partner in self:
            partner.phone_call_log_count = len(self.env['phone.call.log'].search([('partner_id', 'child_of', partner.ids)]))