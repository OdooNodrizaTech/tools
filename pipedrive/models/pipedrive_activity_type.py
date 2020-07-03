# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#https://developers.pipedrive.com/docs/api/v1/#!/ActivityTypes
from odoo import api, fields, models
from pipedrive.client import Client

import logging
_logger = logging.getLogger(__name__)

class PipedriveActivityType(models.Model):
    _name = 'pipedrive.activity.type'
    _description = 'Pipedrive Activity Type'

    external_id = fields.Integer(
        string='External Id'
    )
    name = fields.Char(
        string='Name'
    )
    key_string = fields.Char(
        string='Key String'
    )
    mail_activity_type_id = fields.Many2one(
        comodel_name='mail.activity.type',
        string='Mail Activity Type Id'
    )

    @api.model
    def action_item(self, data):
        vals = {
            'external_id': data['id'],
            'name': data['name'],
            'key_string': data['key_string']
        }
        # search
        pipedrive_activity_type_ids = self.env['pipedrive.activity.type'].search([('external_id', '=', vals['external_id'])])
        if len(pipedrive_activity_type_ids) == 0:
            pipedrive_currency_obj = self.env['pipedrive.activity.type'].sudo().create(vals)
        else:
            pipedrive_activity_type_id = pipedrive_activity_type_ids[0]
            pipedrive_activity_type_id.write(vals)

    @api.model
    def cron_pipedrive_activity_type_exec(self):
        _logger.info('cron_pipedrive_activity_type_exec')
        # params
        pipedrive_domain = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_domain'))
        pipedrive_api_token = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_api_token'))
        # api client
        client = Client(domain=pipedrive_domain)
        client.set_api_token(pipedrive_api_token)
        # get_info
        response = client._get(client.BASE_URL + 'activityTypes')
        if 'success' in response:
            if response['success']==True:
                for data_item in response['data']:
                    self.action_item(data_item)