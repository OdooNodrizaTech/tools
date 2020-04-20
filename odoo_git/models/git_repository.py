# -*- coding: utf-8 -*-
from odoo import api, fields, models
import odoo

from datetime import datetime
import uuid
#need
import git
import time
import zipfile
#import os
import subprocess

import logging
_logger = logging.getLogger(__name__)

class GirRepository(models.Model):
    _name = 'git.repository'
    _description = 'Git Repository'
    
    name = fields.Char(        
        string='Nombre'
    )
    uuid = fields.Char(        
        string='Uuid'
    )
    git_author_id = fields.Many2one(
        comodel_name='git.author',
        string='Git Author'
    )
    url = fields.Char(        
        string='Url',
        help='Similar to https://github.com/oca/repository.git'
    )    
    path = fields.Char(        
        string='Path',
        help='Similar to /home/ubuntu/odoo_addons/oca/web'
    )
    branch = fields.Char(        
        string='Branch',
        help='Similar to 10.0'
    )
    exclude = fields.Text(        
        string='Exclude'
    )
    #extra urls
    odoo_url = fields.Char(        
        compute='_get_odoo_url',
        string='Odoo Url',
        store=False
    )
    odoo_url_odoo_reboot = fields.Char(        
        compute='_get_odoo_url',
        string='Odoo Url (odoo reboot)',
        store=False
    )
    
    @api.one        
    def _get_odoo_url(self):
        web_base_url = str(self.env['ir.config_parameter'].sudo().get_param('web.base.url'))        
        #operations            
        for obj in self:
            if obj.id>0:                
                obj.odoo_url = str(web_base_url)+'/git/'+str(obj.uuid)
                obj.odoo_url_odoo_reboot = str(web_base_url)+'/git/'+str(obj.uuid)+'?odoo_reboot=1'
    
    @api.model
    def create(self, values):
        return_object = super(GirRepository, self).create(values)
        return_object.uuid = uuid.uuid4()
        return return_object
        
    @api.one
    def action_clone(self, odoo_reboot=False):
        if self.path==False or self.url==False or self.branch==False:
            _logger.info('Fields required: paht, url, branch')
        else:
            #save.log
            git_repository_log_vals = {
                'git_repository_id': self.id,
                'odoo_reboot': odoo_reboot,
                'date_start': fields.datetime.now(),
                'date_end': fields.datetime.now(),
            }
            git_repository_log_obj = self.env['git.repository.log'].create(git_repository_log_vals)
            #action_real
            _logger.info('action_real')
            #arglist = '10.0 git@github.com:OdooNodrizaTech/website.git /home/ubuntu/odoo_addons/ont/website True'
            arglist = str(self.branch)+' '+str(self.url)+' '+str(self.path)+ ' '+str(odoo_reboot)
            bashCommand = "sh /home/ubuntu/odoo_addons/odoo_git.sh " + arglist
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            _logger.info('output')
            _logger.info(output)
            _logger.info('error')
            _logger.info(error)
            #save_log (update date_end)
            git_repository_log_obj.date_end = fields.datetime.now()