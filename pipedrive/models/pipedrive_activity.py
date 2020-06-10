# -*- coding: utf-8 -*-
#https://developers.pipedrive.com/docs/api/v1/#!/Activities
from odoo import api, fields, models, tools
import json
import boto3
from botocore.exceptions import ClientError

import logging
_logger = logging.getLogger(__name__)

class PipedriveActivity(models.Model):
    _name = 'pipedrive.activity'
    _description = 'Pipedrive Activity'

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
    public_description = fields.Text(
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
            pipedrive_activity_vals = {
                'done': data['current']['done'],
                'subject': data['current']['subject'],
                'public_description': data['current']['public_description']
            }
            #type
            if data['current']['type']!=None:
                pipedrive_activity_type_ids = self.env['pipedrive.activity.type'].sudo().search([('key_string', '=', data['current']['type'])])
                if len(pipedrive_activity_type_ids)==0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.activity.type) key_string=' + str(data['current']['type'])
                else:
                    pipedrive_activity_vals['pipedrive_activity_type_id'] = pipedrive_activity_type_ids[0].id
            #due_date
            if data['current']['due_date']!=None:
                pipedrive_activity_vals['due_date'] = data['current']['due_date']
            #marked_as_done_time
            if data['current']['marked_as_done_time']!=None:
                pipedrive_activity_vals['marked_as_done_time'] = data['current']['marked_as_done_time']
            # user_id
            if data['current']['user_id'] > 0:
                pipedrive_user_ids = self.env['pipedrive.user'].sudo().search([('id', '=', data['current']['user_id'])])
                if len(pipedrive_user_ids) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.user) user_id=' + str(data['current']['user_id'])
                else:
                    pipedrive_activity_vals['pipedrive_user_id'] = pipedrive_user_ids[0].id
            # org_id
            if data['current']['org_id'] != None:
                if data['current']['org_id'] > 0:
                    pipedrive_organization_ids = self.env['pipedrive.organization'].sudo().search([('id', '=', data['current']['org_id'])])
                    if len(pipedrive_organization_ids) == 0:
                        result_message['delete_message'] = False
                        result_message['errors'] = True
                        result_message['return_body'] = 'No existe el (pipedrive.organization) org_id=' + str(data['current']['org_id'])
                    else:
                        pipedrive_activity_vals['pipedrive_organization_id'] = pipedrive_organization_ids[0].id
            # person_id
            if data['current']['person_id'] > 0:
                pipedrive_person_ids = self.env['pipedrive.person'].sudo().search([('id', '=', data['current']['person_id'])])
                if len(pipedrive_person_ids) == 0:
                    result_message['delete_message'] = False
                    result_message['errors'] = True
                    result_message['return_body'] = 'No existe el (pipedrive.person) person_id=' + str(data['current']['person_id'])
                else:
                    pipedrive_activity_vals['pipedrive_person_id'] = pipedrive_person_ids[0].id
            #deal_id
            if data['current']['deal_id'] != None:
                if data['current']['deal_id'] > 0:
                    pipedrive_deal_ids = self.env['pipedrive.deal'].sudo().search([('id', '=', data['current']['deal_id'])])
                    if len(pipedrive_deal_ids) == 0:
                        result_message['delete_message'] = False
                        result_message['errors'] = True
                        result_message['return_body'] = 'No existe el (pipedrive.deal) deal_id=' + str(data['current']['deal_id'])
                    else:
                        pipedrive_activity_vals['pipedrive_deal_id'] = pipedrive_deal_ids[0].id
        # all operations (if errors False)
        if result_message['errors'] == False:
            # create-update (pipedrive.activity)
            pipedrive_activity_ids = self.env['pipedrive.activity'].sudo().search([('id', '=', data['current']['id'])])
            if len(pipedrive_activity_ids) == 0:
                pipedrive_activity_vals['id'] = data['current']['id']
                pipedrive_activity_id = self.env['pipedrive.activity'].sudo().create(pipedrive_activity_vals)
            else:
                pipedrive_activity_id = pipedrive_activity_ids[0]
                pipedrive_activity_id.write(pipedrive_activity_vals)
            # mail_activity_id
            if pipedrive_activity_id.pipedrive_deal_id.lead_id.id>0:
                #ir_model
                ir_model_ids = self.env['ir.model'].sudo().search([('model', '=', 'crm.lead')])
                if len(ir_model_ids)>0:
                    ir_model_id = ir_model_ids[0]
                    #vals
                    mail_activity_vals = {
                        'summary': pipedrive_activity_id.subject,
                        'done': pipedrive_activity_id.done,
                        'note': pipedrive_activity_id.public_description,
                        'date_deadline': pipedrive_activity_id.due_date,
                        'res_model_id': ir_model_id.id,
                        'res_id': pipedrive_activity_id.pipedrive_deal_id.lead_id.id
                    }
                    #date_done
                    if pipedrive_activity_id.done==True:
                        if pipedrive_activity_id.marked_as_done_time!=False:
                            mail_activity_vals['date_done'] = pipedrive_activity_id.marked_as_done_time
                    #activity_type_id
                    if pipedrive_activity_id.pipedrive_activity_type_id.id>0:
                        if pipedrive_activity_id.pipedrive_activity_type_id.mail_activity_type_id.id > 0:
                            mail_activity_vals['activity_type_id'] = pipedrive_activity_id.pipedrive_activity_type_id.mail_activity_type_id.id
                    #user_id
                    if pipedrive_activity_id.pipedrive_user_id.id>0:
                        if pipedrive_activity_id.pipedrive_user_id.user_id.id > 0:
                            mail_activity_vals['user_id'] = pipedrive_activity_id.pipedrive_user_id.user_id.id
                    # create-update (mail.activity)
                    if pipedrive_activity_id.mail_activity_id.id == 0:
                        mail_activity_obj = self.env['mail.activity'].sudo().create(mail_activity_vals)
                        pipedrive_activity_id.mail_activity_id = mail_activity_obj.id
                    else:
                        pipedrive_activity_id.mail_activity_id.write(mail_activity_vals)
        # return
        return result_message

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
                    if result_message['delete_message'] == True:
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_pipedrive_activity_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )