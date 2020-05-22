# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools

import os
import unidecode

import boto3
from botocore.exceptions import ClientError

import logging
_logger = logging.getLogger(__name__)

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'    
    
    @api.multi
    def unlink(self):        
        #operations
        for item in self:
            if item.type=='url':
                if item.url!=False:
                    if 'amazonaws.com' in item.url:
                        item.remove_to_s3()
        #return                
        return models.Model.unlink(self)    
    
    @api.one        
    def remove_to_s3(self):
        destination_filename = 'ir_attachments/' + str(self.res_model) + '/' + str(self.res_id) + '/' + str(self.name.encode('ascii', 'ignore').decode('ascii'))
        #decode
        if isinstance(destination_filename, str):
            decoded = False
        else:
            destination_filename = unicode_or_str.decode(destination_filename)
            decoded = True
        # Amazon S3 settings.
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_REGION_NAME = tools.config.get('aws_region_name')
        AWS_BUCKET_NAME = self.env['ir.config_parameter'].sudo().get_param('ir_attachment_s3_bucket_name')
        #destination_filename
        s3_key = destination_filename[1:-1]
        #client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
            region_name=AWS_REGION_NAME
        )
        #new
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=s3_key)
                    
    @api.one        
    def upload_to_s3(self):
        #define
        db_name = tools.config.get('db_name')
        source_path = '/var/lib/odoo/.local/share/Odoo/filestore/'+str(db_name)+'/'+str(self.store_fname)
        destination_filename = 'ir_attachments/'+str(self.res_model)+'/'+str(self.res_id)+'/'+str(self.name.encode('ascii', 'ignore').decode('ascii'))
        #define AWS
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_REGION_NAME = tools.config.get('aws_region_name')
        AWS_BUCKET_NAME = self.env['ir.config_parameter'].sudo().get_param('ir_attachment_s3_bucket_name')
        #decode
        if isinstance(destination_filename, str):
            decoded = False
        else:
            destination_filename = unicode_or_str.decode(destination_filename)
            decoded = True        
        #operations
        if not os.path.exists(source_path):
            self.unlink()
        else:            
            #define S3
            upload_to_s3 = False
            #client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID, 
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                region_name=AWS_REGION_NAME
            )                
            try:
                with open(source_path, "rb") as f:
                    #s3_client.upload_fileobj(f, AWS_BUCKET_NAME, destination_filename)
                    s3_client.upload_fileobj(f, AWS_BUCKET_NAME, destination_filename, ExtraArgs={'ACL':'public-read'})
                    upload_to_s3 = True            
            except ClientError as e:
                _logger.info(e)
                upload_to_s3 = False            
            #operatons
            if upload_to_s3==True:                
                #update
                self.type = 'url'
                self.url = "https://s3-"+str(AWS_REGION_NAME)+".amazonaws.com/%s/%s" % (AWS_BUCKET_NAME, destination_filename)                
            else:
                _logger.info('Error al subir')         
                
    @api.model    
    def cron_action_s3_upload_ir_attachments(self):            
        ir_attachment_ids = self.env['ir.attachment'].search(
            [
                ('type', '=', 'binary'),
                ('res_model', '!=', False),
                ('res_id', '>', 0)
            ],
            limit=1000
        )                
        if len(ir_attachment_ids)>0:
            for ir_attachment_id in ir_attachment_ids:
                ir_attachment_id.upload_to_s3()                            