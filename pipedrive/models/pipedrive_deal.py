# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# https://developers.pipedrive.com/docs/api/v1/#!/Deals
from odoo import api, fields, models, tools, _
from pipedrive.client import Client
import json
import boto3
from botocore.exceptions import ClientError

import logging
_logger = logging.getLogger(__name__)


class PipedriveDeal(models.Model):
    _name = 'pipedrive.deal'
    _description = 'Pipedrive Deal'

    external_id = fields.Integer(
        string='External Id'
    )
    title = fields.Char(
        string='Title'
    )
    value = fields.Float(
        string='Value'
    )
    active = fields.Boolean(
        string='Active'
    )
    status = fields.Selection(
        selection=[
            ('open', 'Abierto'),
            ('won', 'Ganado'),
            ('lost', 'Perdido'),
            ('deleted', 'Eliminado')
        ],
        string='Status',
        default='open'
    )
    probability = fields.Integer(
        string='Probability'
    )
    expected_close_date = fields.Date(
        string='Expected Close Date'
    )
    pipedrive_person_id = fields.Many2one(
        comodel_name='pipedrive.person',
        string='Pipedrive Peron Id'
    )
    pipedrive_organization_id = fields.Many2one(
        comodel_name='pipedrive.organization',
        string='Pipedrive Organization Id'
    )
    pipedrive_user_id = fields.Many2one(
        comodel_name='pipedrive.user',
        string='Pipedrive User Id'
    )
    pipedrive_pipeline_id = fields.Many2one(
        comodel_name='pipedrive.pipeline',
        string='Pipedrive Pipeline Id'
    )
    pipedrive_stage_id = fields.Many2one(
        comodel_name='pipedrive.stage',
        string='Pipedrive Stage Id'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead Id'
    )

    @api.multi
    def check_crm_lead(self):
        _logger.info('check_crm_lead')
        self.ensure_one()
        # partner_id
        if self.pipedrive_person_id:
            if self.pipedrive_person_id.partner_id:
                self.partner_id = self.pipedrive_person_id.partner_id.id
                # lead_id
                vals = {
                    'active': self.active,
                    'type': self.pipedrive_pipeline_id.type,
                    'name': self.title,
                    'partner_id': self.partner_id.id,
                    'planned_revenue': self.value,
                    'probability': self.probability
                }
                # email_from
                if self.partner_id.email:
                    vals['email_from'] = self.partner_id.email
                # phone
                if self.partner_id.phone:
                    vals['phone'] = self.partner_id.phone
                # mobile
                if self.partner_id.mobile:
                    vals['mobile'] = self.partner_id.mobile
                # date_deadline
                if self.expected_close_date:
                    vals['date_deadline'] = self.expected_close_date
                # stage_id
                if self.pipedrive_stage_id.stage_id:
                    vals['stage_id'] = self.pipedrive_stage_id.stage_id.id
                # user_id
                if self.pipedrive_user_id:
                    if self.pipedrive_user_id.user_id:
                        vals['user_id'] = self.pipedrive_user_id.user_id.id
                # create-update (crm.lead)
                if self.lead_id.id == 0:
                    crm_lead_obj = self.env['crm.lead'].sudo().create(vals)
                    self.lead_id = crm_lead_obj.id
                else:
                    self.lead_id.write(vals)

    @api.model
    def create(self, values):
        return_item = super(PipedriveDeal, self).create(values)
        # operations
        return_item.check_crm_lead()
        # return
        return return_item

    @api.one
    def write(self, vals):
        return_write = super(PipedriveDeal, self).write(vals)
        # operations
        allow_check = True
        keys_need_check = ['lead_id', 'partner_id']
        for key_need_check in keys_need_check:
            if key_need_check in vals:
                allow_check = False

        if allow_check:
            self.check_crm_lead()
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
                'title': data['current']['title'],
                'value': data['current']['value'],
                'active': data['current']['active'],
                'status': data['current']['status'],
                'probability': data['current']['probability']
            }
            #expected_close_date
            if data['current']['expected_close_date'] != None:
                vals['expected_close_date'] = data['current']['expected_close_date']
            # person_id
            if data['current']['person_id'] != None:
                if data['current']['person_id'] > 0:
                    items = self.env['pipedrive.person'].sudo().search(
                        [
                            ('external_id', '=', data['current']['person_id'])
                        ]
                    )
                    if len(items) == 0:
                        result_message['delete_message'] = False
                        result_message['errors'] = True
                        result_message['return_body'] = \
                            _('No existe el (pipedrive.person) person_id=%s') \
                            % data['current']['person_id']
                    else:
                        vals['pipedrive_person_id'] = items[0].id
            # org_id
            if data['current']['org_id'] != None:
                if data['current']['org_id'] > 0:
                    items = self.env['pipedrive.organization'].sudo().search(
                        [
                            ('external_id', '=', data['current']['org_id'])
                        ]
                    )
                    if len(items) == 0:
                        result_message['delete_message'] = False
                        result_message['errors'] = True
                        result_message['return_body'] = \
                            _('No existe el (pipedrive.organization) org_id=%s') \
                            % data['current']['org_id']
                    else:
                        vals['pipedrive_organization_id'] = items[0].id
            # user_id
            if data['current']['user_id'] > 0:
                items = self.env['pipedrive.user'].sudo().search(
                    [
                        ('external_id', '=', data['current']['user_id'])
                    ]
                )
                if len(items) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = \
                        _('No existe el (pipedrive.user) user_id=%s') \
                        % data['current']['user_id']
                else:
                    vals['pipedrive_user_id'] = items[0].id
            # pipeline_id
            if data['current']['pipeline_id'] > 0:
                items = self.env['pipedrive.pipeline'].sudo().search(
                    [
                        ('external_id', '=', data['current']['pipeline_id'])
                    ]
                )
                if len(items) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = \
                        _('No existe el (pipedrive.pipeline) pipeline_id=%s') \
                        % data['current']['pipeline_id']
                else:
                    vals['pipedrive_pipeline_id'] = items[0].id
            # stage_id
            if data['current']['stage_id'] > 0:
                items = self.env['pipedrive.stage'].sudo().search(
                    [
                        ('external_id', '=', data['current']['stage_id'])
                    ]
                )
                if len(items) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = \
                        _('No existe el (pipedrive.stage) stage_id=%s') \
                        % data['current']['stage_id']
                else:
                    vals['pipedrive_stage_id'] = items[0].id
        # all operations (if errors False)
        if not result_message['errors']:
            # create-update (pipedrive.deal)
            items = self.env['pipedrive.deal'].sudo().search(
                [
                    ('external_id', '=', vals['external_id'])
                ]
            )
            if len(items) == 0:
                self.env['pipedrive.deal'].sudo().create(vals)
            else:
                pipedrive_deal_id = items[0]
                pipedrive_deal_id.write(vals)
        # return
        return result_message

    @api.model
    def cron_pipedrive_deal_exec(self):
        _logger.info('cron_pipedrive_deal_exec')
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
        response = client.deals.get_all_deals()
        if 'success' in response:
            if response['success']:
                for data_item in response['data']:
                    #keys_need_check
                    keys_need_check = ['person_id', 'org_id', 'user_id']
                    for key_need_check in keys_need_check:
                        if key_need_check in data_item:
                            if data_item[key_need_check] != None:
                                if 'id' in data_item[key_need_check]:
                                    data_item[key_need_check] = data_item[key_need_check]['id']
                                else:
                                    data_item[key_need_check] = None
                            else:
                                data_item[key_need_check] = None
                    # action_item
                    self.action_item({
                        'current': data_item,
                        'meta': {
                            'action': 'updated'
                        }
                    })

    @api.model
    def cron_sqs_pipedrive_deal(self):
        _logger.info('cron_sqs_pipedrive_deal')
        sqs_pipedrive_deal_url = tools.config.get('sqs_pipedrive_deal_url')
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
                QueueUrl=sqs_pipedrive_deal_url,
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
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_pipedrive_deal_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
