# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools
from dateutil.relativedelta import relativedelta

import os
import sys
import subprocess
from optparse import OptionParser
from datetime import datetime 

import boto
from boto.s3.key import Key

import zipfile

import logging
_logger = logging.getLogger(__name__)

class S3Model(models.Model):
    _name = 's3.model'
    _description = 'S3 Model'                                
          
    def upload_to_s3(self, source_path, destination_filename, bucket_name, remove_file=True, public_read=False):
        return_url_s3 = False
        # Amazon S3 settings.
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_REGION_NAME = tools.config.get('aws_region_name')
        AWS_BUCKET_NAME = bucket_name                
        conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(AWS_BUCKET_NAME)
        k = Key(bucket)
        k.key = destination_filename
        size = k.set_contents_from_filename(source_path)
        
        if size>0:
            if remove_file==True:
                os.remove(source_path)
            
            if public_read==True:
                k.set_acl('public-read')            
            
            return_url_s3 = "https://s3-"+str(AWS_REGION_NAME)+".amazonaws.com/%s/%s" % (AWS_BUCKET_NAME, destination_filename)
        else:
            _logger.info('Error al subir')            
            
        return return_url_s3                            
    
    def remove_to_s3(self, destination_folder, bucket_name):
        # Amazon S3 settings.
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_BUCKET_NAME = bucket_name                
        conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(AWS_BUCKET_NAME)
        k = Key(bucket)
        #list-delete all
        destination_folder2 = destination_folder[1:-1]
        
        for i in bucket.list():
            split_key = i.key.rsplit('/', 1)
            key_folder = split_key[0] 
            key_file = split_key[1]
            
            if key_file!="":            
                if key_folder==destination_folder2:
                    #delete file in folder                    
                    k.key = i.key
                    k.delete()                    
        #delete empty folder
        k.key = destination_folder            
        k.delete()                            
                                                                           