# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedriveCurrency(models.Model):
    _name = 'pipedrive.currency'
    _description = 'Pipedrive Currency'

    code = fields.Char(
        string='Code'
    )
    name = fields.Char(
        string='Name'
    )
    symbol = fields.Char(
        string='Symbol'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency Id'
    )

'''
{
    "id": 2,
    "code": "AFN",
    "name": "Afghanistan Afghani",
    "decimal_points": 2,
    "symbol": "AFN",
    "active_flag": true,
    "is_custom_flag": false
}
'''