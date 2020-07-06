# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class MailMessageSubtype(models.Model):
    _inherit = 'mail.message.subtype'

    is_phone_call = fields.Boolean(
        string='Is phone call?',
        default=False
    )