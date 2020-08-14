# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CesceSale(models.Model):
    _name = 'cesce.sale'
    _description = 'Cesce Sale'

    account_move_line_id = fields.Many2one(
        comodel_name='account.move.line',
        string='Codigo Operacion Cesce'
    )
    nif_filial = fields.Char(
        string='Nif filial'
    )
    numero_interno_factura = fields.Char(
        string='Numero interno factura'
    )
    fecha_movimiento = fields.Date(
        string='Fecha movimiento'
    )
    num_sumplemento_cesce = fields.Integer(
        string='Numero suplemento cesce'
    )
    nif_deudor = fields.Char(
        string='Nif deudor'
    )
    codigo_deudor_cesce = fields.Integer(
        string='Codigo deudor cesce'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Codigo deudor interno'
    )
    fecha_factura = fields.Date(
        string='Fecha factura'
    )
    fecha_vencimiento = fields.Date(
        string='Fecha vencimiento'
    )
    importe_credito = fields.Float(
        string='Importe credito'
    )
    account_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Codigo factura'
    )
    cesce_sale_situation_id = fields.Many2one(
        comodel_name='cesce.sale.situation',
        string='Situacion'
    )
    cesce_sale_motive_situation_id = fields.Many2one(
        comodel_name='cesce.sale.motive.situation',
        string='Motivo situacion'
    )
    percent_riesgo_comercial = fields.Float(
        string='% Riesgo comercial'
    )
    percent_tasa_rrcc = fields.Float(
        string='% Tasa RRCC'
    )
    prima_rrcc = fields.Float(
        string='Prima RRCC'
    )
    percent_riesgo_politico = fields.Float(
        string='% Riesgo politico'
    )
    percent_tasa_rrpp = fields.Float(
        string='% Tasa RRPP'
    )
    prima_rrpp = fields.Float(
        string='Prima RRPP'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Divisa importe'
    )
    nif_cedente = fields.Char(
        string='Nif cedente'
    )
    fecha_adquisicion = fields.Date(
        string='Fecha adquisicion'
    )
    id_interno_factura_cliente = fields.Char(
        string='Id interno factura cliente'
    )
