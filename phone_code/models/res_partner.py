# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields
from openerp.exceptions import Warning, ValidationError

import re

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    phone_code_res_country_id = fields.Many2one(
        comodel_name='res.country', 
        string='Telefono - Pais'
    )    
    phone_code = fields.Selection(
        selection='_get_phone_code',
        compute='_get_phone_code_res_country_id',
        string='Telefono - Pais'
    )
    mobile_code_res_country_id = fields.Many2one(
        comodel_name='res.country', 
        string='Movil - Pais'
    )    
    mobile_code = fields.Selection(
        selection='_get_mobile_code',
        compute='_get_mobile_code_res_country_id',
        string='Movil - Pais'
    )                     
    
    @api.model
    def create(self, values):
        record = super(ResPartner, self).create(values)
        #phone_code
        if 'phone_code' not in values or values['phone_code']==False:
            if record.country_id.id>0:
                record.phone_code_res_country_id = record.country_id.id
                record.phone_code = record.country_id.phone_code
        
        #mobile_code
        if 'mobile_code' not in values or values['mobile_code']==False:
            if record.country_id.id>0:
                record.mobile_code_res_country_id = record.country_id.id
                record.mobile_code = record.country_id.phone_code
        #return                        
        return record                        
    
    @api.multi
    def _get_phone_code_res_country_id(self):
        for partner in self:
            if partner.phone_code_res_country_id.id>0:
                partner.phone_code = partner.phone_code_res_country_id.phone_code                    
    
    def _get_phone_code(self):
        phone_codes = []
        res_country_ids = self.env['res.country'].search([('id', '>', 0) ])
        if len(res_country_ids)>0:
            for res_country_id in res_country_ids:
                if res_country_id.phone_code>0:
                    name_item = str(res_country_id.phone_code)+' - '+str(res_country_id.name)
                    phone_codes.append((res_country_id.phone_code, name_item))
        
        return phone_codes
        
    @api.multi
    def _get_mobile_code_res_country_id(self):
        for partner in self:
            if partner.mobile_code_res_country_id.id>0:
                partner.mobile_code = partner.mobile_code_res_country_id.phone_code                    
    
    def _get_mobile_code(self):
        phone_codes = []
        res_country_ids = self.env['res.country'].search([('id', '>', 0) ])
        if len(res_country_ids)>0:
            for res_country_id in res_country_ids:
                if res_country_id.phone_code>0:
                    name_item = str(res_country_id.phone_code)+' - '+str(res_country_id.name)
                    phone_codes.append((res_country_id.phone_code, name_item))
        
        return phone_codes                                                           
    
    @api.one
    def write(self, vals):
        #ckeck_phone_code
        if 'phone_code' in vals:
            res_country_ids = self.env['res.country'].search([('phone_code', '=', vals['phone_code'])])
            if len(res_country_ids)>0:
                res_country_id = res_country_ids[0]
                vals['phone_code_res_country_id'] = res_country_id.id                    
        #ckeck_mobile_code
        if 'mobile_code' in vals:
            res_country_ids = self.env['res.country'].search([('phone_code', '=', vals['mobile_code'])])
            if len(res_country_ids)>0:
                res_country_id = res_country_ids[0]
                vals['mobile_code_res_country_id'] = res_country_id.id                    
        #return                                                        
        return super(ResPartner, self).write(vals)