# -*- coding: utf-8 -*-
#https://developers.pipedrive.com/docs/api/v1/#!/Persons
from odoo import api, fields, models, tools
import json
import boto3
from botocore.exceptions import ClientError

import logging
_logger = logging.getLogger(__name__)

class PipedrivePerson(models.Model):
    _name = 'pipedrive.person'
    _description = 'Pipedrive Person'

    name = fields.Char(
        string='Name'
    )
    first_name = fields.Char(
        string='First Name'
    )
    last_name = fields.Char(
        string='Last Name'
    )
    phone = fields.Char(
        string='Phone'
    )
    email = fields.Char(
        string='Email'
    )
    pipedrive_organization_id = fields.Many2one(
        comodel_name='pipedrive.organization',
        string='Pipedrive Organization Id'
    )
    pipedrive_user_id = fields.Many2one(
        comodel_name='pipedrive.user',
        string='Pipedrive User Id'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id'
    )

    @api.model
    def action_item(self, data):
        _logger.info('action_item')
        _logger.info(data)
        #result_message
        result_message = {
            'statusCode': 200,
            'return_body': 'OK',
            'message': data
        }
        #operations
        if data['meta']['action'] in ['updated', 'added']:
            #vals
            pipedrive_person_vals = {
                'name': data['current']['name'],
                'first_name': data['current']['first_name'],
                'last_name': data['current']['last_name']
            }
            #phone
            if 'phone' in data['current']:
                if len(data['current']['phone'])>0:
                    for phone_item in data['current']['phone']:
                        if phone_item['primary']==True:
                            pipedrive_person_vals['phone'] = phone_item['value']
            #email
            if 'email' in data['current']:
                if len(data['current']['email'])>0:
                    for email_item in data['current']['email']:
                        if email_item in['primary']==True:
                            pipedrive_person_vals['email'] = email_item in['value']
            #pipedrive_organization_id
            if data['current']['org_id']>0:
                pipedrive_organization_ids = self.env['pipedrive.organization'].sudo().search([('id', '=', data['current']['org_id'])])
                if len(pipedrive_organization_ids)>0:
                    pipedrive_person_vals['pipedrive_organization_id'] = pipedrive_organization_ids[0].id
            #pipedrive_user_id
            if data['current']['owner_id']>0:
                pipedrive_user_ids = self.env['pipedrive.user'].sudo().search([('id', '=', data['current']['owner_id'])])
                if len(pipedrive_user_ids)>0:
                    pipedrive_person_vals['pipedrive_user_id'] = pipedrive_user_ids[0].id
        #create-update (pipedrive.person)
        pipedrive_person_ids = self.env['pipedrive.person'].search([('id', '=', data['current']['id'])])
        if len(pipedrive_person_ids) == 0:
            pipedrive_person_vals['id'] = data['current']['id']
            pipedrive_person_id = self.env['pipedrive.person'].sudo().create(pipedrive_person_vals)
        else:
            pipedrive_person_id = pipedrive_person_ids[0]
            pipedrive_person_id.write(pipedrive_person_vals)
        #partner_id
        res_partner_vals = {
            'name': pipedrive_person_id.name,
            'phone': pipedrive_person_id.phone,
            'email': pipedrive_person_id.email
        }
        #parent_id
        if pipedrive_person_id.pipedrive_organization_id.id>0:
            if pipedrive_person_id.pipedrive_organization_id.partner_id.id>0:
                res_partner_vals['parent_id'] = pipedrive_person_id.pipedrive_organization_id.partner_id.id
        #user_id
        if pipedrive_person_id.pipedrive_user_id.id>0:
            if pipedrive_person_id.pipedrive_user_id.user_id.id>0:
                res_partner_vals['user_id'] = pipedrive_person_id.pipedrive_user_id.user_id.id
        #create-update (res.partner)
        if pipedrive_person_id.partner_id.id==0:
            res_partner_obj = self.env['res.partner'].sudo().create(res_partner_vals)
            pipedrive_person_id.partner_id = res_partner_obj.id
        else:
            pipedrive_person_id.partner_id.write(res_partner_vals)
        #return
        return result_message

    @api.model
    def cron_sqs_pipedrive_person(self):
        _logger.info('cron_sqs_pipedrive_person')
        sqs_pipedrive_person_url = tools.config.get('sqs_pipedrive_person_url')
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
                QueueUrl=sqs_pipedrive_person_url,
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
                    #operations
                    _logger.info('result_message')
                    _logger.info(result_message)
                    # remove_message
                    if result_message['statusCode'] == 200:
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_pipedrive_person_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )