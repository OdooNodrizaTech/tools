# -*- coding: utf-8 -*-
#https://developers.pipedrive.com/docs/api/v1/#!/Users
from odoo import api, fields, models
from pipedrive.client import Client

import logging
_logger = logging.getLogger(__name__)

class PipedriveUser(models.Model):
    _name = 'pipedrive.user'
    _description = 'Pipedrive User'

    external_id = fields.Integer(
        string='External Id'
    )
    name = fields.Char(
        string='Name'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency Id'
    )
    email = fields.Char(
        string='Email'
    )
    phone = fields.Char(
        string='Phone'
    )
    is_admin = fields.Boolean(
        string='Is admin'
    )
    activated = fields.Boolean(
        string='Activated'
    )
    timezone_name = fields.Char(
        string='Timezone Name'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User Id'
    )

    @api.model
    def action_item(self, data):
        vals = {
            'external_id': data['id'],
            'name': data['name'],
            'email': data['email'],
            'phone': data['phone'],
            'is_admin': data['is_admin'],
            'activated': data['activated'],
            'timezone_name': data['timezone_name']
        }
        #currency_id
        res_currency_ids = self.env['res.currency'].search([('name', '=', data['default_currency'])])
        if len(res_currency_ids)>0:
            vals['currency_id'] = res_currency_ids[0].id
        #search
        pipedrive_user_ids = self.env['pipedrive.user'].search([('external_id', '=', vals['external_id'])])
        if len(pipedrive_user_ids)==0:
            pipedrive_user_obj = self.env['pipedrive.user'].sudo().create(vals)
        else:
            pipedrive_user_id = pipedrive_user_ids[0]
            pipedrive_user_id.write(vals)

    @api.model
    def cron_pipedrive_user_exec(self):
        _logger.info('cron_pipedrive_user_exec')
        # params
        pipedrive_domain = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_domain'))
        pipedrive_api_token = str(self.env['ir.config_parameter'].sudo().get_param('pipedrive_api_token'))
        # api client
        client = Client(domain=pipedrive_domain)
        client.set_api_token(pipedrive_api_token)
        # get_info
        response = client.users.get_all_users()
        if 'success' in response:
            if response['success']==True:
                for data_item in response['data']:
                    self.action_item(data_item)