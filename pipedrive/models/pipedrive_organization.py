# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# https://developers.pipedrive.com/docs/api/v1/#!/Organizations
from odoo import api, fields, models, tools, _
from pipedrive.client import Client
import json
import boto3

import logging
_logger = logging.getLogger(__name__)


class PipedriveOrganization(models.Model):
    _name = 'pipedrive.organization'
    _description = 'Pipedrive Organization'

    external_id = fields.Integer(
        string='External Id'
    )
    name = fields.Char(
        string='Name'
    )
    address = fields.Char(
        string='Address'
    )
    address_street_number = fields.Char(
        string='Address Street Number'
    )
    address_route = fields.Char(
        string='Address Route'
    )
    address_locality = fields.Char(
        string='Address Locality'
    )
    address_country = fields.Char(
        string='Address Country'
    )
    address_postal_code = fields.Char(
        string='Address Postal Code'
    )
    pipedrive_user_id = fields.Many2one(
        comodel_name='pipedrive.user',
        string='Pipedrive User Id'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id'
    )

    @api.multi
    def check_res_partner(self):
        _logger.info('check_res_partner')
        self.ensure_one()
        # partner_id
        vals = {
            'type': 'contact',
            'name': self.name
        }
        # address
        if self.address:
            vals['street'] = self.address
            # address_street_number
            if self.address_street_number:
                vals['street'] += ' ' + str(self.address_street_number)
        # address_locality
        if self.address_locality:
            vals['city'] = self.address_locality
        # address_postal_code
        if self.address_postal_code:
            vals['zip'] = self.address_postal_code
            # search
            items = self.env['res.city.zip'].sudo().search(
                [
                    ('name', '=', vals['zip'])
                ]
            )
            if items:
                res_city_zip_id = items[0]
                vals['state_id'] = res_city_zip_id.city_id.state_id.id
                vals['country_id'] = res_city_zip_id.city_id.country_id.id
        # user_id
        if self.pipedrive_user_id:
            if self.pipedrive_user_id.user_id:
                vals['user_id'] = self.pipedrive_user_id.user_id.id
        # create-update (res.partner)
        if self.partner_id.id == 0:
            res_partner_obj = self.env['res.partner'].sudo().create(vals)
            self.partner_id = res_partner_obj.id
        else:
            self.partner_id.write(vals)

    @api.model
    def create(self, values):
        return_item = super(PipedriveOrganization, self).create(values)
        # operations
        return_item.check_res_partner()
        # return
        return return_item

    @api.one
    def write(self, vals):
        return_write = super(PipedriveOrganization, self).write(vals)
        # operations
        self.check_res_partner()
        # return
        return return_write

    @api.model
    def action_item(self, data):
        _logger.info('action_item')
        _logger.info(data)
        # result_message
        result_message = {
            'delete_message': True,
            'errors': False,
            'return_body': 'OK',
            'message': data
        }
        # operations
        if data['meta']['action'] not in ['updated', 'added']:
            result_message['errors'] = True
            result_message['return_body'] = \
                _('El action %s no tien que realizar ninguna accion') \
                % data['meta']['action']
        else:
            # vals
            vals = {
                'external_id': data['current']['id'],
                'name': data['current']['name']
            }
            # fields_need_check
            fields_need_check = [
                'address', 'address_street_number',
                'address_route', 'address_locality',
                'address_country', 'address_postal_code']
            for field_need_check in fields_need_check:
                if field_need_check in data['current']:
                    if data['current'][field_need_check] is None:
                        vals[field_need_check] = False
                    else:
                        vals[field_need_check] = data['current'][field_need_check]
            # pipedrive_user_id
            if data['current']['owner_id'] > 0:
                items = self.env['pipedrive.user'].sudo().search(
                    [
                        ('external_id', '=', data['current']['owner_id'])
                    ]
                )
                if len(items) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = \
                        _('No existe el (pipedrive.user) owner_id=%s') \
                        % data['current']['owner_id']
                else:
                    vals['pipedrive_user_id'] = items[0].id
        # all operations (if errors False)
        if not result_message['errors']:
            # create-update (pipedrive.organization)
            items = self.env['pipedrive.organization'].sudo().search(
                [
                    ('external_id', '=', vals['external_id'])
                ]
            )
            if len(items) == 0:
                self.env['pipedrive.organization'].sudo().create(vals)
            else:
                pipedrive_organization_id = items[0]
                pipedrive_organization_id.write(vals)
        # return
        return result_message

    @api.model
    def cron_pipedrive_organization_exec(self):
        _logger.info('cron_pipedrive_organization_exec')
        # params
        pipedrive_domain = str(self.env['ir.config_parameter'].sudo().get_param(
            'pipedrive_domain'
        ))
        pipedrive_api_token = str(self.env['ir.config_parameter'].sudo().get_param(
            'pipedrive_api_token'
        ))
        # api client
        client = Client(domain=pipedrive_domain)
        client.set_api_token(pipedrive_api_token)
        # get_info
        response = client.organizations.get_all_organizations()
        if 'success' in response:
            if response['success']:
                for data_item in response['data']:
                    data_item['owner_id'] = data_item['owner_id']['id']
                    # action_item
                    self.action_item({
                        'current': data_item,
                        'meta': {
                            'action': 'updated'
                        }
                    })

    @api.model
    def cron_sqs_pipedrive_organization(self):
        _logger.info('cron_sqs_pipedrive_organization')
        sqs_pipedrive_organization_url = tools.config.get(
            'sqs_pipedrive_organization_url'
        )
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
        # boto3
        sqs = boto3.client(
            'sqs',
            region_name=AWS_SMS_REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        # Receive message from SQS queue
        total_messages = 10
        while total_messages > 0:
            response = sqs.receive_message(
                QueueUrl=sqs_pipedrive_organization_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                MessageAttributeNames=['All']
            )
            if 'Messages' in response:
                total_messages = len(response['Messages'])
            else:
                total_messages = 0
            # continue
            if 'Messages' in response:
                for message in response['Messages']:
                    # message_body
                    message_body = json.loads(message['Body'])
                    # fix message
                    if 'Message' in message_body:
                        message_body = json.loads(message_body['Message'])
                    # result_message
                    result_message = self.action_item(message_body)
                    # operations
                    _logger.info('result_message')
                    _logger.info(result_message)
                    # remove_message
                    if result_message['delete_message']:
                        sqs.delete_message(
                            QueueUrl=sqs_pipedrive_organization_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
