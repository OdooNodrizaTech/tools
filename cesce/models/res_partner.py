# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, fields, _
from odoo.exceptions import Warning as UserError


from ..cesce.web_service import CesceWebService
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cesce_amount_requested = fields.Integer(
        string='Cesce Importe solicitado'
    )
    cesce_risk_state = fields.Selection(
        selection=[
            ('none', 'Ninguno'),
            ('classification_sent', 'Clasificacion enviada'),
            ('classification_ok', 'Clasificacion ok'),
            ('classification_error', 'Clasificacion error'),
            ('canceled_sent', 'Cancelacion enviada'),
            ('canceled_ok', 'Cancelacion ok'),
            ('canceled_error', 'Cancelacion error')
        ],
        string='Estado',
        default='none',
        track_visibility='onchange'
    )
    cesce_error = fields.Char(
        string='Cesce Error'
    )
    cesce_risk_classification_count = fields.Integer(
        compute='_compute_cesce_risk_classification_count',
        string="Cesce clasificaciones de riesgo"
    )

    @api.one
    def write(self, vals):
        allow_write = True
        # vat
        if 'vat' in vals:
            if vals['vat']:
                vals['vat'] = vals['vat'].upper()
        # credit_limit
        if 'credit_limit' in vals:
            if vals['credit_limit'] < 0:
                allow_write = False
                raise UserError(_('El Limite de credito NO puede ser < 0'))
        # allow_write
        if allow_write:
            return_write = super(ResPartner, self).write(vals)
        # operations
        if allow_write:
            if 'credit_limit' in vals:
                #  Solo se notificara cuando el estado sea algo que haya venido
                #  de Cesce (bien sea porque nos han dado riesgo o porque lo han
                #  actualizado a 0 -denegado o nos han dado riesgo aunque sea menos
                #  de lo que hemos pedido-)
                if self.cesce_risk_state in \
                        ['classification_ok', 'classification_error', 'canceled_ok']:
                    if self.user_id:
                        if self.user_id.partner_id.id != self._uid:
                            items = self.env['mail.message'].sudo().search(
                                [
                                    ('model', '=', 'res.partner'),
                                    ('res_id', '=', self.id),
                                    ('message_type', '=', 'notification')
                                ],
                                order='date desc',
                                limit=2
                            )
                            if items:
                                for item in items:
                                    mail_message_need_starred = False
                                    if item.tracking_value_ids:
                                        for value_id in item.tracking_value_ids:
                                            if value_id.field == 'credit_limit':
                                                if value_id.old_value_monetary \
                                                        != value_id.new_value_monetary:
                                                    mail_message_need_starred = True
                                    # mail_message_need_starred
                                    if mail_message_need_starred:
                                        # previously_insert (very strange)
                                        previously_insert = False
                                        for s_p_id in item.starred_partner_ids:
                                            if s_p_id.id == self.user_id.partner_id.id:
                                                previously_insert = True
                                        # insert
                                        if not previously_insert:
                                            item.starred_partner_ids = \
                                                [(4, self.user_id.partner_id.id)]
        # return
        return return_write

    @api.multi
    def _compute_cesce_risk_classification_count(self):
        crc_data = self.env['cesce.risk.classification'].read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'],
            ['partner_id']
        )
        mapped_data = dict(
            [
                (
                    crc in['partner_id'][0],
                    crc in['partner_id_count']
                )
                for crc in crc_data
            ]
        )
        for partner in self:
            partner.cesce_risk_classification_count = \
                mapped_data.get(partner.id, 0)

    @api.model
    def cron_cesce_risk_classification_check_file_out(self):
        cesce_web_service = CesceWebService(self.env.user.company_id, self.env)
        # errors
        cesce_web_service.partner_classifications_error()
        # file_out
        cesce_web_service.partner_classifications_out()
        # review with cesce_risk_state=classification_sent,classification_error
        res_partner_ids = self.env['res.partner'].search(
            [
                ('cesce_risk_state', 'in',
                 ('classification_sent', 'classification_error')
                 )
            ]
        )
        if res_partner_ids:
            _logger.info('revisar estos ids')
            _logger.info(res_partner_ids)

    @api.multi
    def action_partner_classification_sent(self):
        self.ensure_one()
        if self.id > 0:
            allow_action = True

            if self.cesce_amount_requested == 0:
                allow_action = False
                raise UserError(
                    _('Es necesario definir una importe '
                      'solicitado para Cesce para poder tramitar '
                      'la solicitud de riesgo'))
            elif not self.vat:
                allow_action = False
                raise UserError(_('Es necesario definir un NIF/CIF'))
            elif self.country_id.id == 0:
                allow_action = False
                raise UserError(_('Es necesario definir un pais'))
            elif self.state_id.id == 0:
                allow_action = False
                raise UserError(_('Es necesario definir una provincia'))
            elif not self.zip:
                allow_action = False
                raise UserError(_('Es necesario definir un codigo postal'))
            elif not self.city:
                allow_action = False
                raise UserError(_('Es necesario definir una ciudad'))
            elif not self.street:
                allow_action = False
                raise UserError(_('Es necesario definir una direccion'))

            if allow_action:
                cesce_web_service = CesceWebService(self.env.user.company_id, self.env)
                return_action = cesce_web_service.generate_partner_classification(self)

                if not return_action['errors']:
                    self.cesce_risk_state = 'classification_sent'
                else:
                    raise UserError(return_action['error'])

                return True

    @api.multi
    def action_partner_canceled_sent(self):
        _logger.info('action_partner_canceled_sent')
        self.ensure_one()
        return True
