# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from dateutil.relativedelta import relativedelta
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

import urllib2
import json
import gzip
import io
import unidecode

import logging
_logger = logging.getLogger(__name__)

#https://docs.aws.amazon.com/sns/latest/dg/sms_stats_usage.html

class SmsMessage(models.Model):
    _name = 'sms.message'
    _description = 'SMS Message'
    
    name = fields.Char(        
        compute='_get_name',
        string='Nombre',
        store=False
    )
    
    @api.one        
    def _get_name(self):            
        for obj in self:
            obj.name = obj.message_id
    
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Pais'
    )
    mobile = fields.Char(
        string='Mobile'
    )
    message = fields.Text(
        string='Mensaje'
    )
    sender = fields.Char(
        string='Sender'
    )
    message_id = fields.Char(
        string='Message Id'
    )
    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Modelo'
    )
    res_id = fields.Integer(
        string='Related Document ID'
    )
    state = fields.Selection(
        selection=[ 
            ('delivery','Entregado'), 
            ('failed','Error'),                         
        ],
        default='delivery',
        string='Estado', 
    )
    delivery_status = fields.Char(
        string='Delivery Status'
    )
    price = fields.Float(
        string='Precio'
    )
    part_number = fields.Integer(
        string='Part Number'
    )
    total_parts = fields.Integer(
        string='Total Parts'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Comercial'
    )
    
    @api.model
    def create(self, values):
        #replace accents unidecode
        if 'message' in values:            
            values['message'] = unidecode.unidecode(values['message'])
        
        return super(SmsMessage, self).create(values)
    
    @api.one    
    def action_send_error_sms_message_message_slack(self, res):
        return                                        
    
    @api.one                               
    def action_send_real(self):
        # Create an SNS client
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
        
        try:
            res_return = {
                'send': True,                
                'error': ''
            }
            client = boto3.client(
                "sns",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_SMS_REGION_NAME
            )
            # Send your sms message.
            phone_number_full = "+"+str(self.country_id.phone_code)+str(self.mobile)            
                        
            response = client.publish(
                PhoneNumber=phone_number_full,
                Message=str(self.message),
                #Sender=self.sender
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': self.sender
                    }
                }
            )                        
            
            #Fix MessageId
            if 'MessageId' in response:
                self.message_id = response['MessageId']
            else:
                res_return['send'] = False
                res_return['error'] = response
                
            return res_return                
                                                                                    
        except ClientError as e:
            res_return = {
                'send': False,                
                'error': ''
            }
                     
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                res_return['error'] = "User already exists"
            else:
                #res_return['error'] = e
                res_return['error'] = 'Client error'
                                                
            return res_return
            
    @api.one                               
    def action_send(self):
        if 'False' in self.message:
            res_to_slack = {
                'send': False,                
                'error': 'El mensaje contiene False'
            }
        
            self.state = 'failed'
            self.action_send_error_sms_message_message_slack(res_to_slack)
            
            return False
        else:
            return_action = self.action_send_real()#Fix only return
            #Fix list
            if isinstance(return_action, (list,)):
                return_action = return_action[0]        
            #slack_message
            if return_action['send']==False:
                res_to_slack = return_action
                self.state = 'failed'                    
                self.action_send_error_sms_message_message_slack(res_to_slack)
                    
            return return_action['send']                                            
    
    def s3_line_sms_message(self, line):
        line_split = line.split(',')
        sms_message_ids = self.env['sms.message'].search([('message_id', '=', line_split[1])])
        if len(sms_message_ids)>0:
            sms_message_id = sms_message_ids[0]
            if sms_message_id.price==False:            
                #state
                delivery_status = line_split[4]
                if "accepted" not in delivery_status:                                                                                
                    sms_message_id.state = 'failed'
                #other_fields
                sms_message_id.delivery_status = line_split[4]
                sms_message_id.price = line_split[5]
                sms_message_id.part_number = line_split[6]
                sms_message_id.total_parts = line_split[7]
                                    
    @api.multi    
    def cron_sms_usage_reports(self, cr=None, uid=False, context=None):
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        bucket_sms_report = 'sms-report-arelux'
        
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='eu-west-1'
        )        
        all_objects = s3.list_objects(Bucket=bucket_sms_report)        
        if len(all_objects['Contents'])>0:                                    
            for content in all_objects['Contents']:
                obj = s3.get_object(
                    Bucket=bucket_sms_report, 
                    Key=content['Key']
                )
                obj_gzip = False                
                
                if obj['ContentType']=='text/plain':
                    if 'ContentEncoding' in obj:
                        if obj['ContentEncoding']=='gzip':
                            obj_gzip = True
                            
                            return_presigned_url = s3.generate_presigned_url(
                                'get_object', 
                                Params = {
                                    'Bucket': bucket_sms_report, 
                                    'Key': content['Key']
                                }, 
                                ExpiresIn = 100
                            )
                            
                            page=urllib2.urlopen(return_presigned_url)
                            gzip_filehandle=gzip.GzipFile(fileobj=io.BytesIO(page.read()))
                            content_file = gzip_filehandle.readlines()
                            
                            count_lines = 0
                            for content_file_line in content_file:
                                if count_lines>0:
                                    self.s3_line_sms_message(content_file_line)
                                    
                                count_lines += 1                    
                    #read_file
                    if obj_gzip==False:        
                        count_lines = 0
                        for line in obj['Body']._raw_stream:
                            if count_lines>0:
                                self.s3_line_sms_message(line)
                                                        
                            count_lines += 1                                                                    