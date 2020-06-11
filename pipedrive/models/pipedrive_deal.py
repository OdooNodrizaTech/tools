# -*- coding: utf-8 -*-
#https://developers.pipedrive.com/docs/api/v1/#!/Deals
from odoo import api, fields, models, tools
import json
import boto3
from botocore.exceptions import ClientError

import logging
_logger = logging.getLogger(__name__)

class PipedriveDeal(models.Model):
    _name = 'pipedrive.deal'
    _description = 'Pipedrive Deal'

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

    @api.one
    def check_crm_lead(self):
        _logger.info('check_crm_lead')
        # partner_id
        if self.pipedrive_person_id.id > 0:
            if self.pipedrive_person_id.partner_id.id > 0:
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
                if self.partner_id.email != False:
                    vals['email_from'] = self.partner_id.email
                # phone
                if self.partner_id.phone != False:
                    vals['phone'] = self.partner_id.phone
                # mobile
                if self.partner_id.mobile != False:
                    vals['mobile'] = self.partner_id.mobile
                # date_deadline
                if self.expected_close_date != False:
                    vals['date_deadline'] = self.expected_close_date
                # stage_id
                if self.pipedrive_stage_id.stage_id.id > 0:
                    vals['stage_id'] = self.pipedrive_stage_id.stage_id.id
                # user_id
                if self.pipedrive_user_id.id > 0:
                    if self.pipedrive_user_id.user_id.id > 0:
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
            result_message['return_body'] = 'El action ' + str(data['meta']['action']) + ' no tien que realizar ninguna accion'
        else:
            # vals
            vals = {
                'title': data['current']['title'],
                'value': data['current']['value'],
                'active': data['current']['active'],
                'status': data['current']['status'],
                'probability': data['current']['probability']
            }
            #expected_close_date
            if data['current']['expected_close_date']!=None:
                vals['expected_close_date'] = data['current']['expected_close_date']
            #person_id
            if data['current']['person_id'] > 0:
                pipedrive_person_ids = self.env['pipedrive.person'].sudo().search([('id', '=', data['current']['person_id'])])
                if len(pipedrive_person_ids) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.person) person_id=' + str(data['current']['person_id'])
                else:
                    vals['pipedrive_person_id'] = pipedrive_person_ids[0].id
            #org_id
            if data['current']['org_id']!=None:
                if data['current']['org_id'] > 0:
                    pipedrive_organization_ids = self.env['pipedrive.organization'].sudo().search([('id', '=', data['current']['org_id'])])
                    if len(pipedrive_organization_ids) == 0:
                        result_message['delete_message'] = False
                        result_message['errors'] = True
                        result_message['return_body'] = 'No existe el (pipedrive.organization) org_id=' + str(data['current']['org_id'])
                    else:
                        vals['pipedrive_organization_id'] = pipedrive_organization_ids[0].id
            #user_id
            if data['current']['user_id']>0:
                pipedrive_user_ids = self.env['pipedrive.user'].sudo().search([('id', '=', data['current']['user_id'])])
                if len(pipedrive_user_ids) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.user) user_id=' + str(data['current']['user_id'])
                else:
                    vals['pipedrive_user_id'] = pipedrive_user_ids[0].id
            #pipeline_id
            if data['current']['pipeline_id'] > 0:
                pipedrive_pipeline_ids = self.env['pipedrive.pipeline'].sudo().search([('id', '=', data['current']['pipeline_id'])])
                if len(pipedrive_pipeline_ids) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.pipeline) pipeline_id=' + str(data['current']['pipeline_id'])
                else:
                    vals['pipedrive_pipeline_id'] = pipedrive_pipeline_ids[0].id
            # stage_id
            if data['current']['stage_id'] > 0:
                pipedrive_stage_ids = self.env['pipedrive.stage'].sudo().search([('id', '=', data['current']['stage_id'])])
                if len(pipedrive_stage_ids) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.stage) stage_id=' + str(data['current']['stage_id'])
                else:
                    vals['pipedrive_stage_id'] = pipedrive_stage_ids[0].id
        # all operations (if errors False)
        if result_message['errors'] == False:
            # create-update (pipedrive.deal)
            pipedrive_deal_ids = self.env['pipedrive.deal'].sudo().search([('id', '=', data['current']['id'])])
            if len(pipedrive_deal_ids) == 0:
                vals['id'] = data['current']['id']
                pipedrive_deal_id = self.env['pipedrive.deal'].sudo().create(vals)
            else:
                pipedrive_deal_id = pipedrive_deal_ids[0]
                pipedrive_deal_id.write(vals)
        # return
        return result_message

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
                    if result_message['delete_message'] == True:
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_pipedrive_deal_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )