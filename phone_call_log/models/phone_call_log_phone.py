# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PhoneCallLogPhone(models.Model):
    _name = 'phone.call.log.phone'
    _description = 'Phone Call Log Phone'
    _rec_name = 'phone'

    phone = fields.Char(
        string='Phone',
        required=True
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        required=True
    )
