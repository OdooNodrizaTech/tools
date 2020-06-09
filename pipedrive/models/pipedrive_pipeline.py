# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedrivePipeline(models.Model):
    _name = 'pipedrive.pipeline'
    _description = 'Pipedrive Pipeline'

    name = fields.Char(
        string='Name'
    )
    active = fields.Boolean(
        string='Active'
    )
    deal_probability = fields.Boolean(
        string='Deal Probability'
    )
    selected = fields.Boolean(
        string='Selected'
    )
    type = fields.Selection(
        selection=[
            ('lead', 'Lead'),
            ('opportunity', 'Oportunidad')
        ],
        string='Type',
        default='lead'
    )

'''
{
    "id": 1,
    "name": "Leads",
    "url_title": "Leads",
    "order_nr": 1,
    "active": true,
    "deal_probability": false,
    "add_time": "2020-05-13 21:23:22",
    "update_time": "2020-06-04 07:02:35",
    "selected": true
}
'''