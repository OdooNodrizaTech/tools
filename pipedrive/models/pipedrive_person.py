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

    external_id = fields.Integer(
        string='External Id'
    )
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

    @api.one
    def check_res_partner(self):
        _logger.info('check_res_partner')
        # partner_id
        vals = {
            'type': 'contact',
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }
        # parent_id
        if self.pipedrive_organization_id.id > 0:
            if self.pipedrive_organization_id.partner_id.id > 0:
                vals['parent_id'] = self.pipedrive_organization_id.partner_id.id
        # user_id
        if self.pipedrive_user_id.id > 0:
            if self.pipedrive_user_id.user_id.id > 0:
                vals['user_id'] = self.pipedrive_user_id.user_id.id
        # create-update (res.partner)
        if self.partner_id.id == 0:
            res_partner_obj = self.env['res.partner'].sudo().create(vals)
            self.partner_id = res_partner_obj.id
        else:
            self.partner_id.write(vals)

    @api.model
    def create(self, values):
        return_item = super(PipedrivePerson, self).create(values)
        # operations
        return_item.check_res_partner()
        # return
        return return_item

    @api.one
    def write(self, vals):
        return_write = super(PipedrivePerson, self).write(vals)
        # operations
        if 'partner_id' not in vals:
            self.check_res_partner()
        # return
        return return_write

    @api.model
    def action_item(self, data):
        _logger.info('action_item')
        _logger.info(data)
        #result_message
        result_message = {
            'delete_message': True,
            'errors': False,
            'return_body': 'OK',
            'message': data
        }
        #operations
        if data['meta']['action'] not in ['updated', 'added']:
            result_message['errors'] = True
            result_message['return_body'] = 'El action '+str(data['meta']['action'] )+' no tien que realizar ninguna accion'
        else:
            #vals
            vals = {
                'external_id': data['current']['id'],
                'name': data['current']['name'],
                'first_name': data['current']['first_name'],
                'last_name': data['current']['last_name']
            }
            #phone
            if 'phone' in data['current']:
                if len(data['current']['phone'])>0:
                    for phone_item in data['current']['phone']:
                        if phone_item['primary']==True:
                            vals['phone'] = phone_item['value']
            #email
            if 'email' in data['current']:
                if len(data['current']['email'])>0:
                    for email_item in data['current']['email']:
                        if email_item in['primary']==True:
                            vals['email'] = email_item in['value']
            #pipedrive_organization_id
            if data['current']['org_id']!=None:
                if data['current']['org_id']>0:
                    pipedrive_organization_ids = self.env['pipedrive.organization'].sudo().search([('external_id', '=', data['current']['org_id'])])
                    if len(pipedrive_organization_ids)==0:
                        result_message['delete_message'] = False
                        result_message['errors'] = True
                        result_message['return_body'] = 'No existe el (pipedrive.organization) org_id='+str(data['current']['org_id'])
                    else:
                        vals['pipedrive_organization_id'] = pipedrive_organization_ids[0].id
            #pipedrive_user_id
            if data['current']['owner_id']>0:
                pipedrive_user_ids = self.env['pipedrive.user'].sudo().search([('external_id', '=', data['current']['owner_id'])])
                if len(pipedrive_user_ids)==0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.user) owner_id='+str(data['current']['owner_id'])
                else:
                    vals['pipedrive_user_id'] = pipedrive_user_ids[0].id
        # all operations (if errors False)
        if result_message['errors'] == False:
            #create-update (pipedrive.person)
            pipedrive_person_ids = self.env['pipedrive.person'].sudo().search([('external_id', '=', vals['external_id'])])
            if len(pipedrive_person_ids) == 0:
                pipedrive_person_id = self.env['pipedrive.person'].sudo().create(vals)
            else:
                pipedrive_person_id = pipedrive_person_ids[0]
                pipedrive_person_id.write(vals)
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
                    if result_message['delete_message'] == True:
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_pipedrive_person_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )