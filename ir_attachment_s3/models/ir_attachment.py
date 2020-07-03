# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

import odoo
import os
import unidecode

import logging
_logger = logging.getLogger(__name__)

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    
    @api.multi
    def unlink(self):
        ir_attachment_s3_bucket_name = self.env['ir.config_parameter'].sudo().get_param('ir_attachment_s3_bucket_name')
        #operations
        for item in self:
            if item.type=='url':
                if 'amazonaws.com' in item.url:
                    destination_filename = 'ir_attachments/'+str(item.res_model)+'/'+str(item.res_id)+'/'+str(item.name.encode('ascii', 'ignore').decode('ascii'))
                    self.env['s3.model'].sudo().remove_to_s3(destination_filename, ir_attachment_s3_bucket_name)
                
        return models.Model.unlink(self)    
                    
    @api.one        
    def upload_to_s3(self):
        db_name = odoo.tools.config.get('db_name')
        source_path = '/var/lib/odoo/.local/share/Odoo/filestore/'+str(db_name)+'/'+str(self.store_fname)
        destination_filename = 'ir_attachments/'+str(self.res_model)+'/'+str(self.res_id)+'/'+str(self.name.encode('ascii', 'ignore').decode('ascii'))
        ir_attachment_s3_bucket_name = self.env['ir.config_parameter'].sudo().get_param('ir_attachment_s3_bucket_name')
        
        if isinstance(destination_filename, unicode):
            destination_filename = unidecode.unidecode(destination_filename)        
        
        if not os.path.exists(source_path):
            self.unlink()
        else:
            return_url_s3 = self.env['s3.model'].sudo().upload_to_s3(source_path, destination_filename, ir_attachment_s3_bucket_name, False, True)
            
            if return_url_s3!=False:
                self.type = 'url'
                self.url = return_url_s3
                
    @api.multi    
    def cron_action_s3_upload_ir_attachments(self, cr=None, uid=False, context=None):            
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