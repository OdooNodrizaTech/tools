# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#https://developers.pipedrive.com/docs/api/v1/#!/Currencies
from odoo import api, fields, models
from pipedrive.client import Client

import logging
_logger = logging.getLogger(__name__)


class PipedriveCurrency(models.Model):
    _name = 'pipedrive.currency'
    _description = 'Pipedrive Currency'

    external_id = fields.Integer(
        string='External Id'
    )
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

    @api.model
    def action_item(self, data):
        vals = {
            'external_id': data['id'],
            'code': data['code'],
            'name': data['name'],
            'symbol': data['symbol']
        }
        # currency_id
        res_currency_ids = self.env['res.currency'].search(
            [
                ('name', '=', data['code'])
            ]
        )
        if res_currency_ids:
            vals['currency_id'] = res_currency_ids[0].id
        # search
        pipedrive_currency_ids = self.env['pipedrive.currency'].search(
            [
                ('external_id', '=', vals['external_id'])
            ]
        )
        if len(pipedrive_currency_ids) == 0:
            pipedrive_currency_obj = self.env['pipedrive.currency'].sudo().create(vals)
        else:
            pipedrive_currency_id = pipedrive_currency_ids[0]
            pipedrive_currency_id.write(vals)

    @api.model
    def cron_pipedrive_currency_exec(self):
        _logger.info('cron_pipedrive_currency_exec')

        # params
        pipedrive_domain = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_domain'))
        pipedrive_api_token = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_api_token'))
        # api client
        client = Client(domain=pipedrive_domain)
        client.set_api_token(pipedrive_api_token)
        # get_info
        response = client._get(client.BASE_URL + 'currencies')
        if 'success' in response:
            if response['success']:
                for data_item in response['data']:
                    self.action_item(data_item)
