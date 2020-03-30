# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)

class CesceRiskClassification(models.Model):
    _name = 'cesce.risk.classification'
    _description = 'Cesce Risk Classification'
    _inherit = ['mail.thread']    
    
    name = fields.Char(        
        compute='_get_name',
        string='Nombre',
        store=False
    )
    
    @api.one        
    def _get_name(self):            
        for obj in self:
            obj.name = obj.code_cesce
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto'
    )
    code_cesce = fields.Char(        
        string='Codigo Cesce'
    )
    num_sup_cesce = fields.Integer(        
        string='Num suplemento Cesce'
    )
    nombre_deudor = fields.Char(        
        string='Nombre deudor'
    )
    codigo_fiscal = fields.Char(        
        string='Codigo fiscal'
    )   
    codigo_deudor_cesce = fields.Char(        
        string='Codigo deudor Cesce'
    )
    grupo_riesgo_deudor = fields.Integer(        
        string='Grupo riesgo deudor'
    )
    mercado = fields.Selection(
        selection=[
            ('inside','Interior'), 
            ('outside','Exterior')                          
        ],
        string='Mercado'
    )
    pais_provincia = fields.Char(        
        string='Pais - Provincia'
    )
    importe_solicitado = fields.Float(        
        string='Importe solicitado'
    )
    importe_concedido = fields.Float(        
        string='Importe concedido'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda'
    )    
    plazo_solicitado = fields.Integer(        
        string='Plazo solicitado'
    )
    plazo_concedido = fields.Integer(        
        string='Plazo concedido'
    )
    condicion_pago = fields.Integer(        
        string='Condicion pago'
    )
    tipo_movimiento = fields.Char(        
        string='Tipo movimiento'
    )
    cesce_risk_classification_situation_id = fields.Many2one(
        comodel_name='cesce.risk.classification.situation',        
        string='Situacion',
    )
    fecha_solicitud = fields.Date(        
        string='Fecha solicitud'
    )
    fecha_efecto = fields.Date(        
        string='Fecha efecto'
    )
    fecha_anulacion = fields.Date(        
        string='Fecha anulacion'
    )
    fecha_validez = fields.Date(        
        string='Fecha validez'
    )
    motivo_validez = fields.Integer(        
        string='Motivo validez'
    )
    riesgo_comercial = fields.Float(        
        string='Riesgo comercial'
    )
    riesgo_politico = fields.Float(        
        string='Riesgo politico'
    )
    avalistas = fields.Boolean(        
        string='Avalistas'
    )
    cesce_risk_classification_motive_id = fields.Many2one(
        comodel_name='cesce.risk.classification.motive',        
        string='Motivo clasificacion',
    )
    codigo_deudor_interno = fields.Char(        
        string='Codigo deudor interno'
    ) 
    fecha_renovacion = fields.Date(        
        string='Fecha renovacion'
    )
    
    @api.multi    
    def cron_cesce_risk_classification_cambiar_fecha_renovacion(self, cr=None, uid=False, context=None):
        current_date = datetime.today()
        start_date = current_date
        end_date = start_date + relativedelta(months=-2)
        
        cesce_risk_classification_ids = self.env['cesce.risk.classification'].search(
            [
                ('fecha_renovacion', '<=', end_date.strftime("%Y-%m-%d")),
                ('partner_id.credit_limit', '>', 0),
                ('partner_id.cesce_risk_state', '=', 'classification_ok')
            ]
        )
        if len(cesce_risk_classification_ids)>0:
            for cesce_risk_classification_id in cesce_risk_classification_ids:
                fecha_renovacion_split = cesce_risk_classification_id.fecha_renovacion.split('-')
                year_next = int(fecha_renovacion_split[0])+1
                fecha_renovacion_new = str(year_next)+'-'+fecha_renovacion_split[1]+'-'+fecha_renovacion_split[2]
                cesce_risk_classification_id.fecha_renovacion = fecha_renovacion_new                  
    
    @api.multi    
    def cron_cesce_risk_classification_fecha_renovacion(self, cr=None, uid=False, context=None):
        current_date = datetime.today()
        start_date = current_date
        end_date = start_date + relativedelta(days=-30)
        
        start_date_account_invoice = current_date + relativedelta(months=-6)
        end_date_account_invoice = current_date                
        
        cesce_risk_classification_ids = self.env['cesce.risk.classification'].search(
            [
                ('fecha_renovacion', '>=', start_date.strftime("%Y-%m-%d")),
                ('fecha_renovacion', '<=', end_date.strftime("%Y-%m-%d")),
                ('partner_id.active', '=', True),
                ('partner_id.cesce_risk_state', 'in', ('classification_sent','classification_ok','classification_error'))
            ]
        )
        if len(cesce_risk_classification_ids)>0:
            for cesce_risk_classification_id in cesce_risk_classification_ids:
                account_invoice_amount_untaxed_sum = 0
                account_invoice_ids = self.env['account.invoice'].search(
                    [
                        ('partner_id', '=', cesce_risk_classification_id.partner_id.id),
                        ('date_invoice', '>=', start_date_account_invoice.strftime("%Y-%m-%d")),
                        ('date_invoice', '<=', end_date_account_invoice.strftime("%Y-%m-%d")),
                        ('state', '!=', 'draft'),
                        ('type', '=', 'out_invoice')
                    ]
                )
                if len(account_invoice_ids)>0:
                    for account_invoice_id in account_invoice_ids:
                        account_invoice_amount_untaxed_sum += account_invoice_id.amount_untaxed                
                #slack_message
                slack_message_vals = {
                    'msg': 'El contacto '+str(cesce_risk_classification_id.partner_id.name)+' ('+str(cesce_risk_classification_id.partner_id.vat)+') ha tenido una facturacion de '+str(account_invoice_amount_untaxed_sum)+' en los ultimos 6 meses',
                    'model': 'res.partner',
                    'res_id': cesce_risk_classification_id.partner_id.id,
                    'channel': self.env['ir.config_parameter'].sudo().get_param('slack_oniad_log_channel'),                                                         
                }                        
                slack_message_obj = self.env['slack.message'].sudo().create(slack_message_vals)                         
                                                                   