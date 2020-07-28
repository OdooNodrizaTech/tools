# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# https://developers.pipedrive.com/docs/api/v1/#!/Activities
from odoo import api, fields, models, tools, _
from pipedrive.client import Client
import json
import boto3
from botocore.exceptions import ClientError

import logging
_logger = logging.getLogger(__name__)


class PipedriveActivity(models.Model):
    _name = 'pipedrive.activity'
    _description = 'Pipedrive Activity'

    external_id = fields.Integer(
        string='External Id'
    )
    pipedrive_activity_type_id = fields.Many2one(
        comodel_name='pipedrive.activity.type',
        string='Pipedrive Activity Type Id'
    )
    pipedrive_user_id = fields.Many2one(
        comodel_name='pipedrive.user',
        string='Pipedrive User Id'
    )
    done = fields.Boolean(
        string='Done'
    )
    due_date = fields.Date(
        string='Due Date'
    )
    marked_as_done_time = fields.Date(
        string='Marked as done time'
    )
    subject = fields.Char(
        string='Subject'
    )
    public_description = fields.Html(
        string='Public Description'
    )
    pipedrive_organization_id = fields.Many2one(
        comodel_name='pipedrive.organization',
        string='Pipedrive Organization Id'
    )
    pipedrive_person_id = fields.Many2one(
        comodel_name='pipedrive.person',
        string='Pipedrive Person Id'
    )
    pipedrive_deal_id = fields.Many2one(
        comodel_name='pipedrive.deal',
        string='Pipedrive Deal Id'
    )
    mail_activity_id = fields.Many2one(
        comodel_name='mail.activity',
        string='Mail Activity Id'
    )

    @api.multi
    def check_mail_activity(self):
        _logger.info('check_mail_activity')
        self.ensure_one()
        # mail_activity_id
        allow_create = False
        if self.pipedrive_deal_id.lead_id:
            allow_create = True
            items = self.env['ir.model'].sudo().search(
                [
                    ('model', '=', 'crm.lead')
                ]
            )
            vals = {
                'res_model_id': items[0].id,
                'res_id': self.pipedrive_deal_id.lead_id.id
            }
        elif self.pipedrive_deal_id.lead_id.id == 0 and self.pipedrive_person_id:
            allow_create = True
            items = self.env['ir.model'].sudo().search(
                [
                    ('model', '=', 'res.partner')
                ]
            )
            vals = {
                'res_model_id': items[0].id,
                'res_id': self.pipedrive_person_id.partner_id.id
            }
        # operations
        if allow_create:
            vals['summary'] = self.subject
            vals['done'] = self.done
            vals['note'] = self.public_description
            vals['date_deadline'] = self.due_date
            # date_done
            if self.done:
                if self.marked_as_done_time:
                    vals['date_done'] = self.marked_as_done_time
            # activity_type_id
            if self.pipedrive_activity_type_id:
                if self.pipedrive_activity_type_id.mail_activity_type_id:
                    vals['activity_type_id'] = self.pipedrive_activity_type_id.mail_activity_type_id.id
            # user_id
            if self.pipedrive_user_id:
                if self.pipedrive_user_id.user_id:
                    vals['user_id'] = self.pipedrive_user_id.user_id.id
            # create-update (mail.activity)
            if self.mail_activity_id.id == 0:
                mail_activity_obj = self.env['mail.activity'].sudo().create(vals)
                self.mail_activity_id = mail_activity_obj.id
            else:
                self.mail_activity_id.write(vals)

    @api.model
    def create(self, values):
        return_item = super(PipedriveActivity, self).create(values)
        # operations
        return_item.check_mail_activity()
        # return
        return return_item

    @api.one
    def write(self, vals):
        return_write = super(PipedriveActivity, self).write(vals)
        # operations
        self.check_mail_activity()
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
                _('El action %s no tiene que realizar ninguna accion') \
                % data['meta']['action']
        else:
            # vals
            vals = {
                'external_id': data['current']['id'],
                'done': data['current']['done'],
                'subject': data['current']['subject'],
                'public_description': data['current']['public_description']
            }
            # type
            if data['current']['type'] != None:
                items = self.env['pipedrive.activity.type'].sudo().search(
                    [
                        ('key_string', '=', data['current']['type'])
                    ]
                )
                if len(items) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = \
                        _('No existe el (pipedrive.activity.type) key_string=%s') \
                        % data['current']['type']
                else:
                    vals['pipedrive_activity_type_id'] = items[0].id
            # due_date
            if data['current']['due_date'] != None:
                vals['due_date'] = data['current']['due_date']
            # marked_as_done_time
            if data['current']['marked_as_done_time'] != None:
                if data['current']['marked_as_done_time'] != '':
                    vals['marked_as_done_time'] = data['current']['marked_as_done_time']
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
            # deal_id
            if data['current']['deal_id'] != None:
                if data['current']['deal_id'] > 0:
                    items = self.env['pipedrive.deal'].sudo().search(
                        [
                            ('external_id', '=', data['current']['deal_id'])
                        ]
                    )
                    if len(items) == 0:
                        result_message['delete_message'] = False
                        result_message['errors'] = True
                        result_message['return_body'] = \
                            _('No existe el (pipedrive.deal) deal_id=%s') \
                            % data['current']['deal_id']
                    else:
                        vals['pipedrive_deal_id'] = items[0].id
        # all operations (if errors False)
        if not result_message['errors']:
            # create-update (pipedrive.activity)
            items = self.env['pipedrive.activity'].sudo().search(
                [
                    ('external_id', '=', vals['external_id'])
                ]
            )
            if len(items) == 0:
                self.env['pipedrive.activity'].sudo().create(vals)
            else:
                pipedrive_activity_id = items[0]
                pipedrive_activity_id.write(vals)
        # return
        return result_message

    @api.model
    def cron_pipedrive_activity_exec(self):
        _logger.info('cron_pipedrive_activity_exec')
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
        response = client.activities.get_all_activities()
        if 'success' in response:
            if response['success']:
                for data_item in response['data']:
                    # keys_need_check
                    keys_need_check = ['owner_id']
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
    def cron_sqs_pipedrive_activity(self):
        _logger.info('cron_sqs_pipedrive_activity')
        sqs_pipedrive_activity_url = tools.config.get('sqs_pipedrive_activity_url')
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
                QueueUrl=sqs_pipedrive_activity_url,
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
                            QueueUrl=sqs_pipedrive_activity_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
