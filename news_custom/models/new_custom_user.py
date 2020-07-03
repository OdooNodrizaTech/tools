# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class NewCustomUser(models.Model):
    _name = 'new.custom.user'
    _description = 'New Custom User'
    
    new_custom_id = fields.Many2one(
        comodel_name='new.custom',
        string='New Custom'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuario'
    )                                        