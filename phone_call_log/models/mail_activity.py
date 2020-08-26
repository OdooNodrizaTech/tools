# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    phone_call_type = fields.Selection(
        selection=[
            (1, 'Incoming'),
            (2, 'Outgoing'),
            (3, 'Missed'),
            (4, 'Voicemail'),
            (5, 'Rejected'),
            (6, 'Refused'),
        ],
        string='Phone Call Type'
    )