# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime

from ..cesce.web_service import CesceWebService
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cesce_sale_state = fields.Selection(
        selection=[
            ('none', 'Ninguno'),
            ('sale_sent', 'Venta enviada'),
            ('sale_ok', 'Venta ok'),
            ('sale_error', 'Venta error')
        ],
        string='Cesce Sale State',
        default='none'
    )
    cesce_error = fields.Char(
        string='Cesce Error'
    )
    partner_vat = fields.Char(
        compute='_compute_get_partner_vat',
        string='VAT',
        store=False
    )
    invoice_id_date = fields.Date(
        compute='_compute_get_invoice_id_date',
        string='Invoice date',
        store=False
    )
    invoice_id_amount_total = fields.Monetary(
        compute='_compute_get_invoice_id_amount_total',
        string='Amount invoice total',
        store=False
    )
    invoice_id_amount_untaxed = fields.Monetary(
        compute='_compute_get_invoice_id_amount_untaxed',
        string='Invoice amount untaxed',
        store=False
    )
    partner_id_credit_limit = fields.Monetary(
        compute='_compute_get_partner_id_credit_limit',
        string='Credit limit',
        store=False
    )

    @api.multi
    @api.depends('partner_id')
    def _compute_get_partner_vat(self):
        self.partner_vat = self.partner_id.vat

    @api.multi
    @api.depends('invoice_id')
    def _compute_get_invoice_id_date(self):
        self.invoice_id_date = self.invoice_id.date

    @api.multi
    @api.depends('invoice_id')
    def _compute_get_invoice_id_amount_total(self):
        self.invoice_id_amount_total = self.invoice_id.amount_total

    @api.multi
    @api.depends('invoice_id')
    def _compute_get_invoice_id_amount_untaxed(self):
        self.invoice_id_amount_untaxed = self.invoice_id.amount_untaxed

    @api.multi
    @api.depends('partner_id')
    def _compute_get_partner_id_credit_limit(self):
        self.partner_id_credit_limit = self.partner_id.credit_limit

    @api.model
    def cron_cesce_sale_generate_file(self):
        current_date = datetime.today()
        start_date = current_date + relativedelta(months=-1, day=1)
        end_date = datetime(
            start_date.year,
            start_date.month,
            1
        ) + relativedelta(months=1, days=-1)
        items = self.env['account.move.line'].search(
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
        if items:
            cesce_web_service = CesceWebService(self.env.user.company_id, self.env)
            for item in items:
                if item.invoice_id.date_invoice \
                        != item.invoice_id.date_due:
                    res = cesce_web_service.generate_cesce_sale(
                        item
                    )
                    if not res['errors']:
                        item.cesce_sale_state = 'sale_sent'
                    else:
                        _logger.info(res)

    @api.model
    def cron_cesce_sale_check_file_out(self):
        cesce_web_service = CesceWebService(self.env.user.company_id, self.env)
        # errors
        cesce_web_service.cesce_sale_error()
        # file_out
        cesce_web_service.cesce_sale_out()
        # review with cesce_sale_state=sale_sent,sale_error
        items = self.env['account.move.line'].search(
            [
                ('cesce_sale_state', 'in', ('sale_sent', 'sale_error'))
            ]
        )
        if items:
            _logger.info('revisar estos ids')
            _logger.info(items)
