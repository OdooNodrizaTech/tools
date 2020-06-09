# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedriveStage(models.Model):
    _name = 'pipedrive.stage'
    _description = 'Pipedrive Stage'

    name = fields.Char(
        string='Name'
    )
    deal_probability = fields.Integer(
        string='Deal Probability'
    )
    pipedrive_pipeline_id = fields.Many2one(
        comodel_name='pipedrive.pipeline',
        string='Pipedrive Pipeline Id'
    )
    stage_id = fields.Many2one(
        comodel_name='crm.stage',
        string='Stage Id'
    )

'''
{
    "id": 1,
    "order_nr": 0,
    "name": "No Contactado",
    "active_flag": true,
    "deal_probability": 10,
    "pipeline_id": 1,
    "rotten_flag": false,
    "rotten_days": null,
    "add_time": "2020-05-14 09:19:55",
    "update_time": "2020-06-08 11:52:11",
    "pipeline_name": "Leads",
    "pipeline_deal_probability": false
}
'''