# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#https://developers.pipedrive.com/docs/api/v1/#!/Stages
from odoo import api, fields, models
from pipedrive.client import Client

import logging
_logger = logging.getLogger(__name__)


class PipedriveStage(models.Model):
    _name = 'pipedrive.stage'
    _description = 'Pipedrive Stage'

    external_id = fields.Integer(
        string='External Id'
    )
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

    @api.model
    def action_item(self, data):
        vals = {
            'external_id': data['id'],
            'name': data['name'],
            'deal_probability': data['deal_probability']
        }
        # pipedrive_pipeline_id
        pipedrive_pipeline_ids = self.env['pipedrive.pipeline'].search(
            [
                ('external_id', '=', data['pipeline_id'])
            ]
        )
        if pipedrive_pipeline_ids:
            vals['pipedrive_pipeline_id'] = pipedrive_pipeline_ids[0].id
        # search
        pipedrive_stage_ids = self.env['pipedrive.stage'].search(
            [
                ('external_id', '=', vals['external_id'])
            ]
        )
        if len(pipedrive_stage_ids) == 0:
            pipedrive_stage_obj = self.env['pipedrive.stage'].sudo().create(vals)
        else:
            pipedrive_stage_id = pipedrive_stage_ids[0]
            pipedrive_stage_id.write(vals)

    @api.model
    def cron_pipedrive_stage_exec(self):
        _logger.info('cron_pipedrive_stage_exec')
        # params
        pipedrive_domain = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_domain'))
        pipedrive_api_token = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_api_token'))
        # api client
        client = Client(domain=pipedrive_domain)
        client.set_api_token(pipedrive_api_token)
        # get_info
        response = client._get(client.BASE_URL + 'stages')
        if 'success' in response:
            if response['success']:
                for data_item in response['data']:
                    self.action_item(data_item)
