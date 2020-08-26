# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    is_phone_call = fields.Boolean(
        string='Is phone call?',
        default=False
    )