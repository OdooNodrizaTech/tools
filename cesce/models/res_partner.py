# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

from ..cesce.web_service import CesceWebService

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    cesce_amount_requested = fields.Integer(        
        string='Cesce Importe solicitado'
    )
    cesce_risk_state = fields.Selection(
        selection=[
            ('none','Ninguno'), 
            ('classification_sent','Clasificacion enviada'), 
            ('classification_ok','Clasificacion ok'),
            ('classification_error','Clasificacion error'), 
            ('canceled_sent','Cancelacion enviada'),
            ('canceled_ok','Cancelacion ok'),
            ('canceled_error','Cancelacion error')             
        ],
        string='Estado',
        default='none',
        track_visibility='onchange'
    )
    cesce_error = fields.Char(
        string='Cesce Error'
    )
    cesce_risk_classification_count = fields.Integer(compute='_compute_cesce_risk_classification_count', string="Cesce clasificaciones de riesgo")
    
    @api.one
    def write(self, vals):
        allow_write = True
        #vat
        if 'vat' in vals:
            if vals['vat']!=False:
                vals['vat'] = vals['vat'].upper()
        #credit_limit
        if 'credit_limit' in vals:            
            if vals['credit_limit']<0:
                allow_write = False
                raise Warning("El Limite de credito NO puede ser < 0")                                
        #allow_write                                        
        if allow_write==True:                        
            return_write = super(ResPartner, self).write(vals)
        #operations
        if allow_write==True:
            if 'credit_limit' in vals:            
                if vals['credit_limit']>=0:
                    if self.user_id.id>0:
                        if self.user_id.partner_id.id!=self._uid:
                            mail_message_ids = self.env['mail.message'].sudo().search(
                                [
                                    ('model', '=', 'res.partner'),
                                    ('res_id', '=', self.id),
                                    ('message_type', '=', 'notification')
                                ], order='date desc', limit=2
                            )
                            if len(mail_message_ids)>0:
                                for mail_message_id in mail_message_ids:
                                    mail_message_need_starred = False
                                    if len(mail_message_id.tracking_value_ids)>0:
                                        for tracking_value_id in mail_message_id.tracking_value_ids:
                                            if tracking_value_id.field=='credit_limit':
                                                if tracking_value_id.old_value_monetary!=tracking_value_id.new_value_monetary:
                                                    mail_message_need_starred = True
                                    #mail_message_need_starred
                                    if mail_message_need_starred==True:
                                        #previously_insert (very strange)
                                        previously_insert = False
                                        for starred_partner_id in mail_message_id.starred_partner_ids:
                                            if starred_partner_id.id==self.user_id.partner_id.id:
                                                previously_insert = True
                                        #insert
                                        if previously_insert==False:
                                            mail_message_id.starred_partner_ids = [(4, self.user_id.partner_id.id)]            
        #return
        return return_write
    
    @api.multi
    def _compute_cesce_risk_classification_count(self):
        cesce_risk_classification_data = self.env['cesce.risk.classification'].read_group([('partner_id', 'in', self.ids)], ['partner_id'], ['partner_id'])
        mapped_data = dict([(cesce_risk_classification['partner_id'][0], cesce_risk_classification['partner_id_count']) for cesce_risk_classification in cesce_risk_classification_data])
        for partner in self:
            partner.cesce_risk_classification_count = mapped_data.get(partner.id, 0)            
    
    @api.multi    
    def cron_cesce_risk_classification_check_file_out(self, cr=None, uid=False, context=None):
        _logger.info('cron_cesce_risk_classification_check_file_out')
        #webservice
        cesce_web_service = CesceWebService(self.env.user.company_id, self.env)        
        #errors
        cesce_web_service.partner_classifications_error()        
        #file_out
        cesce_web_service.partner_classifications_out()        
        #review with cesce_risk_state=classification_sent,classification_error
        res_partner_ids = self.env['res.partner'].search([('cesce_risk_state', 'in', ('classification_sent', 'classification_error'))])
        if len(res_partner_ids)>0:
            _logger.info('revisar estos ids')
            _logger.info(res_partner_ids)
    
    @api.one
    def action_partner_classification_sent(self):
        if self.id>0:
            allow_action = True
            
            if self.cesce_amount_requested==0:
                allow_action = False
                raise Warning("Es necesario definir una importe solicitado para Cesce para poder tramitar la solicitud de riesgo")
            elif self.vat==False:
                allow_action = False
                raise Warning("Es necesario definir un NIF/CIF")
            elif self.country_id.id==0:
                allow_action = False
                raise Warning("Es necesario definir un pais")
            elif self.state_id.id==0:
                allow_action = False
                raise Warning("Es necesario definir una provincia")
            elif self.zip==False:
                allow_action = False
                raise Warning("Es necesario definir un codigo postal")
            elif self.city==False:
                allow_action = False
                raise Warning("Es necesario definir una ciudad")
            elif self.street==False:
                allow_action = False
                raise Warning("Es necesario definir una direccion")
            
            if allow_action==True: 
                cesce_web_service = CesceWebService(self.env.user.company_id, self.env)
                return_action = cesce_web_service.generate_partner_classification(self)
                
                if return_action['errors']==False:
                    self.cesce_risk_state = 'classification_sent'
                else:
                    raise Warning(return_action['error'])
                
                return True
                                                    
    @api.one
    def action_partner_canceled_sent(self):
        _logger.info('action_partner_canceled_sent')
        _logger.info('Generamos el archivo .txt y lo enviamos a cesce para despues cambiar el estado de cesce_risk_state=canceled_sent')
        return True                                                                                                                                                          