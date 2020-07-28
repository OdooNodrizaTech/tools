# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tracking_profile_uuid = fields.Char(
        string='Tracking Profile Uuid',
        readonly=True
    )
    tracking_cookie_uuid = fields.Char(
        string='Tracking Cookie Uuid',
        readonly=True
    )
    tracking_user_uuid = fields.Char(
        string='Tracking User Uuid',
        readonly=True
    )
    tracking_session_uuid = fields.Char(
        string='Tracking Session Uuid',
        readonly=True
    )
