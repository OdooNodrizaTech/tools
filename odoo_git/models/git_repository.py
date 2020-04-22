# -*- coding: utf-8 -*-
from odoo import api, fields, models
import odoo

from datetime import datetime
import uuid
#need
import os
import time
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
        compute='_get_url',
        string='Url',
        help='Similar to https://github.com/oca/repository.git',
        store=False
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
    shell_command_without_odoo_reboot = fields.Text(        
        compute='_get_shell_command_without_odoo_reboot',
        string='Shell command',
        store=False
    )
    shell_command_with_odoo_reboot = fields.Text(        
        compute='_get_shell_command_with_odoo_reboot',
        string='Shell command',
        store=False
    )    
        
    @api.one        
    def _get_url(self):
        web_base_url = str(self.env['ir.config_parameter'].sudo().get_param('web.base.url'))        
        #operations            
        if self.id>0:
            if self.git_author_id.id>0 and self.name!=False:
                if self.git_author_id.url!=False:
                    self.url = self.git_author_id.url+'/'+str(self.name)+'.git'
    
    @api.one        
    def _get_odoo_url(self):
        web_base_url = str(self.env['ir.config_parameter'].sudo().get_param('web.base.url'))        
        #operations            
        if self.id>0:                
            self.odoo_url = str(web_base_url)+'/git/'+str(self.uuid)
            self.odoo_url_odoo_reboot = str(web_base_url)+'/git/'+str(self.uuid)+'?odoo_reboot=1'
                
    @api.model
    def define_url_log_finish(self, git_repository_log_id=0):
        web_base_url = str(self.env['ir.config_parameter'].sudo().get_param('web.base.url'))
        return web_base_url+'/git/'+str(self.uuid)+'/log/'+str(git_repository_log_id)+'/finish'
    
    @api.one        
    def _get_shell_command_without_odoo_reboot(self):            
        if self.id>0:
            self.shell_command_without_odoo_reboot = self._get_shell_command(False, 0)[0]
    
    @api.one        
    def _get_shell_command_with_odoo_reboot(self):            
        if self.id>0:
            self.shell_command_with_odoo_reboot = self._get_shell_command(True, 0)[0]                
                        
    @api.one        
    def _get_shell_command(self, odoo_reboot=False, git_repository_log_id=0):
        if self.id>0:
            #exclude
            exclude = '.git'
            if self.exclude!=False:
                exclude+=','+str(self.exclude)
            #arglist            
            arglist = str(self.branch)+' '+str(self.url)+' '+str(self.path)+ ' '+str(odoo_reboot)+' '+str(exclude)
            #url
            if git_repository_log_id>0:
                url = self.define_url_log_finish(git_repository_log_id)
                arglist+= ' '+str(url)
            #return        
            return "sh /home/ubuntu/odoo_addons/odoo_git.sh " + arglist
    
    @api.model
    def create(self, values):
        return_object = super(GirRepository, self).create(values)
        return_object.uuid = uuid.uuid4()
        return return_object
    
    @api.one
    def action_clone_real(self, odoo_reboot=False, git_repository_log_id=0):
        bashCommand = self._get_shell_command(odoo_reboot, git_repository_log_id)[0]        
        shellscript = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        stdout, stderr = shellscript.communicate()
        #return
        return {
            'output': stdout,
            'error': stderr
        }
        
    @api.one
    def action_clone(self, odoo_reboot=False):
        if self.path==False or self.url==False or self.branch==False:
            _logger.info('Fields required: paht, url, branch')
        else:
            #save.log
            git_repository_log_vals = {
                'git_repository_id': self.id,
                'odoo_reboot': odoo_reboot,
                'date_start': fields.datetime.now()
            }
            git_repository_log_obj = self.env['git.repository.log'].create(git_repository_log_vals)
            #action_real
            '''
            bashCommand = self._get_shell_command(odoo_reboot, git_repository_log_obj.id)[0]        
            shellscript = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            stdout, stderr = shellscript.communicate()
            _logger.info({'output': stdout,'error': stderr})
            '''
            return_action = self.action_clone_real(odoo_reboot, git_repository_log_obj.id)[0]
            _logger.info(return_action)            