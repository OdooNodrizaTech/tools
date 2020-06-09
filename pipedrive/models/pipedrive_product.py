# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedriveProduct(models.Model):
    _name = 'pipedrive.product'
    _description = 'Pipedrive Product'

    name = fields.Char(
        string='Name'
    )
    code = fields.Char(
        string='Code'
    )
    description = fields.Text(
        string='Description'
    )
    tax = fields.Monetary(
        string='Tax'
    )
    price = fields.Monetary(
        string='Price'
    )
    cost = fields.Monetary(
        string='Cost'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency Id'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product Id'
    )
'''
{
    "id": 4,
    "name": "Importación Base de Datos",
    "code": "IMPORTDB",
    "description": null,
    "unit": "",
    "tax": 21,
    "category": "15",
    "active_flag": true,
    "selectable": true,
    "first_char": "i",
    "visible_to": "3",
    "owner_id": {
        "id": 11451374,
        "name": "TUUP",
        "email": "servicios@tuup.es",
        "has_pic": 1,
        "pic_hash": "947f9957d2eb3cd06cddb67fa36c29b6",
        "active_flag": true,
        "value": 11451374
    },
    "files_count": null,
    "followers_count": 0,
    "add_time": "2020-06-04 07:40:23",
    "update_time": "2020-06-08 12:09:31",
    "prices": [
        {
            "id": 4,
            "product_id": 4,
            "price": 100,
            "currency": "EUR",
            "cost": 0,
            "overhead_cost": null
        }
    ]
}
'''