# -*- coding: utf-8 -*-
#https://developers.pipedrive.com/docs/api/v1/#!/Pipelines
from odoo import api, fields, models
from pipedrive.client import Client

import logging
_logger = logging.getLogger(__name__)

class PipedrivePipeline(models.Model):
    _name = 'pipedrive.pipeline'
    _description = 'Pipedrive Pipeline'

    external_id = fields.Integer(
        string='External Id'
    )
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

    @api.model
    def action_item(self, data):
        vals = {
            'external_id': data['id'],
            'name': data['name'],
            'active': data['active'],
            'deal_probability': data['deal_probability'],
            'selected': data['selected']
        }
        # search
        pipedrive_pipeline_ids = self.env['pipedrive.pipeline'].search([('external_id', '=', vals['external_id'])])
        if len(pipedrive_pipeline_ids) == 0:
            pipedrive_pipeline_obj = self.env['pipedrive.pipeline'].sudo().create(vals)
        else:
            pipedrive_pipeline_id = pipedrive_pipeline_ids[0]
            pipedrive_pipeline_id.write(vals)

    @api.model
    def cron_pipedrive_pipeline_exec(self):
        _logger.info('cron_pipedrive_pipeline_exec')
        # params
        pipedrive_domain = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_domain'))
        pipedrive_api_token = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_api_token'))
        # api client
        client = Client(domain=pipedrive_domain)
        client.set_api_token(pipedrive_api_token)
        # get_info
        response = client.pipelines.get_all_pipelines()
        if 'success' in response:
            if response['success'] == True:
                for data_item in response['data']:
                    self.action_item(data_item)