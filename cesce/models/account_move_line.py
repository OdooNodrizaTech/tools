# -*- coding: utf-8 -*-
from openerp import api, models, fields

import logging
_logger = logging.getLogger(__name__)

from dateutil.relativedelta import relativedelta
from datetime import datetime

from ..cesce.web_service import CesceWebService

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    cesce_sale_state = fields.Selection(
        selection=[
            ('none','Ninguno'), 
            ('sale_sent','Venta enviada'), 
            ('sale_ok','Venta ok'),
            ('sale_error','Venta error')                         
        ],
        string='Cesce Venta Estado',
        default='none'
    )
    partner_vat = fields.Char(
        compute='_get_partner_vat',
        string='DNI',
        store=False
    )
    invoice_id_date = fields.Date(
        compute='_get_invoice_id_date',
        string='Fecha factura',
        store=False        
    )
    invoice_id_amount_total = fields.Monetary(
        compute='_get_invoice_id_amount_total',
        string='Importe factura',
        store=False        
    )
    invoice_id_amount_untaxed = fields.Monetary(
        compute='_get_invoice_id_amount_untaxed',
        string='Importe imponible factura',
        store=False        
    )    
    partner_id_credit_limit = fields.Monetary(
        compute='_get_partner_id_credit_limit',
        string='Credito concedido',
        store=False        
    )    
    
    @api.one        
    def _get_partner_vat(self):                              
        self.partner_vat = self.partner_id.vat
            
    @api.one        
    def _get_invoice_id_date(self):                              
        self.invoice_id_date = self.invoice_id.date
            
    @api.one        
    def _get_invoice_id_amount_total(self):                              
        self.invoice_id_amount_total = self.invoice_id.amount_total
            
    @api.one        
    def _get_invoice_id_amount_untaxed(self):                              
        self.invoice_id_amount_untaxed = self.invoice_id.amount_untaxed
            
    @api.one        
    def _get_partner_id_credit_limit(self):                              
        self.partner_id_credit_limit = self.partner_id.credit_limit
        
    @api.multi    
    def cron_cesce_sale_generate_file(self, cr=None, uid=False, context=None):
        _logger.info('cron_cesce_sale_generate_file')                                
        
        current_date = datetime.today()
        start_date = current_date + relativedelta(months=-1, day=1)
        end_date = datetime(start_date.year, start_date.month, 1) + relativedelta(months=1, days=-1)                
        
        account_move_line_ids = self.env['account.move.line'].search(
            [
                ('journal_id', '=', 1),
                ('account_id', '=', 193),
                ('debit', '>', 0),            
                ('invoice_id.date_invoice', '>=', start_date.strftime("%Y-%m-%d")),
                ('invoice_id.date_invoice', '<=', end_date.strftime("%Y-%m-%d")),
                ('invoice_id.invoice_with_risk', '=', True),                
                ('cesce_sale_state', '=', 'none')
            ]
        )        
        if len(account_move_line_ids)>0:
            cesce_web_service = CesceWebService(self.env.user.company_id, self.env)
            
            for account_move_line_id in account_move_line_ids:
                if account_move_line_id.invoice_id.date_invoice!=account_move_line_id.invoice_id.date_due:                   
                    return_generate_cesce_sale = cesce_web_service.generate_cesce_sale(account_move_line_id)
                
                    if return_generate_cesce_sale['errors']==False:
                        account_move_line_id.cesce_sale_state = 'sale_sent'
                    else:
                        _logger.info(return_generate_cesce_sale)                                        
        
    @api.multi    
    def cron_cesce_sale_check_file_out(self, cr=None, uid=False, context=None):
        _logger.info('cron_cesce_sale_check_file_out')        
        #webservice
        cesce_web_service = CesceWebService(self.env.user.company_id, self.env)        
        #errors
        cesce_web_service.cesce_sale_error()        
        #file_out
        cesce_web_service.cesce_sale_out()
        #review with cesce_sale_state=sale_sent,sale_error
        account_move_line_ids = self.env['account.move.line'].search([('cesce_sale_state', 'in', ('sale_sent','sale_error'))])
        if len(account_move_line_ids)>0:
            _logger.info('revisar estos ids')
            _logger.info(account_move_line_ids)
            
    @api.one    
    def action_send_cesce_sale_error_message_slack(self, vals):
        return True                                                                                               