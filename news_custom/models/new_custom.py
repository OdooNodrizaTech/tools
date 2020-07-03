# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class NewCustom(models.Model):
    _name = 'new.custom'
    _description = 'New Custom'
    _order = 'date asc'    
    name = fields.Char(        
        string='Nombre'
    )
    active = fields.Boolean(
        string='Activo',
        default=True 
    )        
    description = fields.Html(        
        string='Descripcion'
    )
    date = fields.Date(        
        string='Fecha'
    )
    date_read = fields.Date(   
        compute='_date_read',     
        string='Fecha lectura',
        store=False
    )
    
    @api.model        
    def _date_read(self):
        for new_custom_item in self:
            new_custom_item.date_read = ''            
            
            new_custom_user_ids = self.env['new.custom.user'].search([('new_custom_id', '=', new_custom_item.id), ('user_id', '=', self.env.uid)])
            if new_custom_user_ids!=False:
                for new_custom_user_id in new_custom_user_ids:
                    if new_custom_user_id.id>0:
                        new_custom_item.date_read = new_custom_user_id.create_date                
    
    @api.model
    def get_records_unread_total(self):
        new_custom_user_ids_real = []
        new_custom_user_ids = self.env['new.custom.user'].search([('user_id', '=', self.env.uid)])
        if new_custom_user_ids!=False:
            for new_custom_user_id in new_custom_user_ids:
                new_custom_user_ids_real.append(new_custom_user_id.new_custom_id.id)            
                        
        new_custom_ids = self.env['new.custom'].search([('active', '=', True),('id', 'not in', new_custom_user_ids_real)])
        
        res = {
            'total': len(new_custom_ids),
        }        
        return res
    
    @api.one
    def action_mark_as_read(self):
        if self.date_read==False:
            new_custom_user_vals = {
                'user_id': self.env.uid,
                'new_custom_id': self.id,                                                         
            }
            new_custom_user_obj = self.env['new.custom.user'].sudo().create(new_custom_user_vals)
        
        return True                
                                                                                
    @api.model
    def get_last_record_unread(self):
        res = {
            'action': False,
            'record_unread': False,
        }
        new_custom_user_ids_real = []
        new_custom_user_ids = self.env['new.custom.user'].search([('user_id', '=', self.env.uid)])
        if new_custom_user_ids!=False:
            for new_custom_user_id in new_custom_user_ids:
                new_custom_user_ids_real.append(new_custom_user_id.new_custom_id.id)
        
        new_custom_ids = self.env['new.custom'].search([('active', '=', True),('id', 'not in', new_custom_user_ids_real)])
        if new_custom_ids!=False:
            res_obj = False  
            for new_custom_id in new_custom_ids:
                if new_custom_id.id>0:              
                    res_obj = new_custom_ids[0]
                    
            if res_obj!=False:                                
                res['record_unread'] = {
                    'id': res_obj.id,
                    'name': res_obj.name,
                    'date': res_obj.date,
                    'date_read': res_obj.date_read,
                    'description': res_obj.description,                                
                }
            else:
                action_act_window_ids = self.env['ir.actions.act_window'].search([('res_model', '=', 'new.custom')])
                _logger.info(action_act_window_ids)
                if action_act_window_ids!=False:
                    for action_act_window_id in action_act_window_ids:
                        res['action'] = {
                            'id': action_act_window_id.id,                            
                        }         
                        
                _logger.info(res)                                                                                                               
                                                                
        return res                                                            