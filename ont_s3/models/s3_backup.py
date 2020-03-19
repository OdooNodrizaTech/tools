# -*- coding: utf-8 -*-
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

class S3Backup(models.Model):
    _name = 's3.backup'                                
   
    @api.multi       
    def zipfiles(self, destination_name):
        addons_path = tools.config.get('addons_path').split(",")
        destination_path = os.path.abspath(destination_name)        
        addons_path.append('/var/lib/odoo/.local/share/')#Fix add filestore
        
        with zipfile.ZipFile(destination_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for addon_path in addons_path:
                for dirname, subdirs, files in os.walk(addon_path):
                    # zf.write(dirname) # not needed
                    for filename in files:
                        filepath = os.path.join(dirname, filename)
                        if filepath != destination_path:
                            zf.write(filepath)                                                           
        
    @api.multi    
    def cron_action_s3_backup_log_generate(self, cr=None, uid=False, context=None):
        log_file = "/var/log/odoo/odoo-server.log"        
        #destination_filename
        now = datetime.now()
        hour = str(now.hour).zfill(2)
        
        filename = "odoo-server-%s-00-00.log" % (hour)
                        
        AWS_BACKUP_PATH = self.env['ir.config_parameter'].sudo().get_param('ont_s3_backup_log_path')                
        date_test = datetime.today().strftime('%Y/%m/%d')
        destination_filename = AWS_BACKUP_PATH+date_test+"/"+filename
        #upload_to_s3
        self.env['s3.model'].sudo().upload_to_s3(log_file, destination_filename, None)
        #empty_log_file
        open(log_file, 'w').close()
        #remove_to_s3       
        start_date = datetime.today() + relativedelta(days=-4)        
        destination_folder = AWS_BACKUP_PATH+start_date.strftime("%Y/%m/%d")+"/"
        self.env['s3.model'].sudo().remove_to_s3(destination_folder, None)
                                       
    @api.multi    
    def cron_action_s3_backup_files_generate(self, cr=None, uid=False, context=None):                       
        FILENAME_BACKUP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/files_backups"
        
        if not os.path.exists(FILENAME_BACKUP_PATH):
            os.makedirs(FILENAME_BACKUP_PATH)
        
        now = datetime.now()
        hour = str(now.hour).zfill(2)
        
        filename = "odoo-%s-00-00.zip" % (hour)            
        zip_filename = r'%s/%s' % (FILENAME_BACKUP_PATH, filename)
        
        self.zipfiles(zip_filename)                                    
        #destination_filename                
        AWS_BACKUP_PATH = self.env['ir.config_parameter'].sudo().get_param('ont_s3_backup_files_path')                
        date_test = datetime.today().strftime('%Y/%m/%d')
        destination_filename = AWS_BACKUP_PATH+date_test+"/"+filename
        #upload_to_s3        
        self.env['s3.model'].sudo().upload_to_s3(zip_filename, destination_filename, None)
        #remove_to_s3       
        start_date = datetime.today() + relativedelta(days=-4)        
        destination_folder = AWS_BACKUP_PATH+start_date.strftime("%Y/%m/%d")+"/"
        self.env['s3.model'].sudo().remove_to_s3(destination_folder, None)                                                                                                   