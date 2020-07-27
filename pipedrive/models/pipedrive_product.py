# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#https://developers.pipedrive.com/docs/api/v1/#!/Products
from odoo import api, fields, models
from pipedrive.client import Client

import logging
_logger = logging.getLogger(__name__)


class PipedriveProduct(models.Model):
    _name = 'pipedrive.product'
    _description = 'Pipedrive Product'

    external_id = fields.Integer(
        string='External Id'
    )
    name = fields.Char(
        string='Name'
    )
    code = fields.Char(
        string='Code'
    )
    description = fields.Text(
        string='Description'
    )
    tax = fields.Float(
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

    @api.model
    def action_item(self, data):
        vals = {
            'external_id': data['id'],
            'name': data['name'],
            'code': data['code'],
            'description': data['description'],
            'tax': data['tax']
        }
        # price data
        if 'prices' in data:
            if len(data['prices'])>0:
                data_price_0 = data['prices'][0]
                vals['price'] = data_price_0['price']
                vals['cost'] = data_price_0['cost']
                # currency_id
                res_currency_ids = self.env['res.currency'].search(
                    [
                        ('name', '=', data_price_0['currency'])
                    ]
                )
                if res_currency_ids:
                    vals['currency_id'] = res_currency_ids[0].id
        # search
        pipedrive_product_ids = self.env['pipedrive.product'].search(
            [
                ('external_id', '=', vals['external_id'])
            ]
        )
        if len(pipedrive_product_ids) == 0:
            pipedrive_product_obj = self.env['pipedrive.product'].sudo().create(vals)
        else:
            pipedrive_product_id = pipedrive_product_ids[0]
            pipedrive_product_id.write(vals)

    @api.model
    def cron_pipedrive_product_exec(self):
        _logger.info('cron_pipedrive_product_exec')
        # params
        pipedrive_domain = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_domain'))
        pipedrive_api_token = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_api_token'))
        # api client
        client = Client(domain=pipedrive_domain)
        client.set_api_token(pipedrive_api_token)
        # get_info
        response = client.products.get_all_products()
        if 'success' in response:
            if response['success']:
                for data_item in response['data']:
                    self.action_item(data_item)
