# -*- coding: utf-8 -*-
#https://developers.pipedrive.com/docs/api/v1/#!/Organizations
from odoo import api, fields, models, tools
import json
import boto3
from botocore.exceptions import ClientError

import logging
_logger = logging.getLogger(__name__)

class PipedriveOrganization(models.Model):
    _name = 'pipedrive.organization'
    _description = 'Pipedrive Organization'

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
            #vals
            pipedrive_organization_vals = {
                'name': data['current']['name']
            }
            #fields_need_check
            fields_need_check = ['address', 'address_street_number', 'address_route', 'address_locality', 'address_country', 'address_postal_code']
            for field_need_check in fields_need_check:
                if field_need_check in data['current']:
                    if data['current'][field_need_check]==None:
                        pipedrive_organization_vals[field_need_check] = False
                    else:
                        pipedrive_organization_vals[field_need_check] = data['current'][field_need_check]
            #pipedrive_user_id
            if data['current']['owner_id']>0:
                pipedrive_user_ids = self.env['pipedrive.user'].sudo().search([('id', '=', data['current']['owner_id'])])
                if len(pipedrive_user_ids)== 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.user) owner_id=' + str(data['current']['owner_id'])
                else:
                    pipedrive_organization_vals['pipedrive_user_id'] = pipedrive_user_ids[0].id
        # all operations (if errors False)
        if result_message['errors'] == False:
            # create-update (pipedrive.organization)
            pipedrive_organization_ids = self.env['pipedrive.organization'].sudo().search([('id', '=', data['current']['id'])])
            if len(pipedrive_organization_ids) == 0:
                pipedrive_organization_vals['id'] = data['current']['id']
                pipedrive_organization_id = self.env['pipedrive.organization'].sudo().create(pipedrive_organization_vals)
            else:
                pipedrive_organization_id = pipedrive_organization_ids[0]
                pipedrive_organization_id.write(pipedrive_organization_vals)
            # partner_id
            res_partner_vals = {
                'company_type': 'company',
                'name': pipedrive_organization_id.name
            }
            #address
            if pipedrive_organization_id.address!=False:
                res_partner_vals['street'] = pipedrive_organization_id.address
                #address_street_number
                if pipedrive_organization_id.address_street_number!=False:
                    res_partner_vals['street'] += ' '+str(pipedrive_organization_id.address_street_number)
            #address_locality
            if pipedrive_organization_id.address_locality!=False:
                res_partner_vals['city'] = pipedrive_organization_id.address_locality
            #address_postal_code
            if pipedrive_organization_id.address_postal_code!=False:
                res_partner_vals['zip'] = pipedrive_organization_id.address_postal_code
                #search
                res_city_zip_ids = self.env['res.city.zip'].sudo().search([('name', '=', res_partner_vals['zip'])])
                if len(res_city_zip_ids)>0:
                    res_city_zip_id = res_city_zip_ids[0]
                    res_partner_vals['state_id'] = res_city_zip_id.city_id.state_id.id
                    res_partner_vals['country_id'] = res_city_zip_id.city_id.country_id.id
            # user_id
            if pipedrive_organization_id.pipedrive_user_id.id > 0:
                if pipedrive_organization_id.pipedrive_user_id.user_id.id > 0:
                    res_partner_vals['user_id'] = pipedrive_organization_id.pipedrive_user_id.user_id.id
            # create-update (res.partner)
            if pipedrive_organization_id.partner_id.id == 0:
                res_partner_obj = self.env['res.partner'].sudo().create(res_partner_vals)
                pipedrive_organization_id.partner_id = res_partner_obj.id
            else:
                pipedrive_organization_id.partner_id.write(res_partner_vals)
        #return
        return result_message

    @api.model
    def cron_sqs_pipedrive_organization(self):
        _logger.info('cron_sqs_pipedrive_organization')
        sqs_pipedrive_organization_url = tools.config.get('sqs_pipedrive_organization_url')
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
                    #operations
                    _logger.info('result_message')
                    _logger.info(result_message)
                    # remove_message
                    if result_message['delete_message'] == True:
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_pipedrive_organization_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )