# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from dateutil.relativedelta import relativedelta

import os
from datetime import datetime 

import boto3
from botocore.exceptions import ClientError

import logging
_logger = logging.getLogger(__name__)

class S3Model(models.Model):
    _name = 's3.model'                                
          
    def upload_to_s3(self, source_path, destination_filename, bucket_name, remove_file=True, public_read=False):
        return_url_s3 = False
        # Amazon S3 settings.
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_REGION_NAME = tools.config.get('aws_region_name')
        AWS_BUCKET_NAME = bucket_name
        #define
        return_url_s3 = None
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
                if public_read==True:
                    s3_client.upload_fileobj(f, AWS_BUCKET_NAME, destination_filename, ExtraArgs={'ACL':'public-read'})
                else:
                    s3_client.upload_fileobj(f, AWS_BUCKET_NAME, destination_filename)
                #set
                upload_to_s3 = True            
        except ClientError as e:
            _logger.info(e)
            upload_to_s3 = False            
        #operatons
        if upload_to_s3==True:
            #remove_file
            if remove_file==True:
                os.remove(source_path)                
            #return_url_s3
            return_url_s3 = "https://s3-"+str(AWS_REGION_NAME)+".amazonaws.com/%s/%s" % (AWS_BUCKET_NAME, destination_filename)                
        else:
            _logger.info('Error al subir')         
        #return
        return return_url_s3                            
    
    def remove_to_s3(self, destination_folder, bucket_name):
        # Amazon S3 settings.
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_REGION_NAME = tools.config.get('aws_region_name')
        AWS_BUCKET_NAME = bucket_name
        #destination_filename
        destination_filename = destination_folder[1:-1]
        #client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
            region_name=AWS_REGION_NAME
        )
        #new
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=destination_folder)