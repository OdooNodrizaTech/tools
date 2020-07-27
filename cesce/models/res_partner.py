# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from odoo.exceptions import Warning


from ..cesce.web_service import CesceWebService


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
                raise Warning("El Limite de credito NO puede ser < 0")                                
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
                if self.cesce_risk_state in ['classification_ok', 'classification_error', 'canceled_ok']:
                    if self.user_id:
                        if self.user_id.partner_id.id != self._uid:
                            ids = self.env['mail.message'].sudo().search(
                                [
                                    ('model', '=', 'res.partner'),
                                    ('res_id', '=', self.id),
                                    ('message_type', '=', 'notification')
                                ],
                                order='date desc',
                                limit=2
                            )
                            if ids:
                                for mm_id in ids:
                                    mail_message_need_starred = False
                                    if mm_id.tracking_value_ids:
                                        for tracking_value_id in mm_id.tracking_value_ids:
                                            if tracking_value_id.field == 'credit_limit':
                                                if tracking_value_id.old_value_monetary \
                                                        != tracking_value_id.new_value_monetary:
                                                    mail_message_need_starred = True
                                    # mail_message_need_starred
                                    if mail_message_need_starred:
                                        # previously_insert (very strange)
                                        previously_insert = False
                                        for starred_partner_id in mm_id.starred_partner_ids:
                                            if starred_partner_id.id == self.user_id.partner_id.id:
                                                previously_insert = True
                                        # insert
                                        if not previously_insert:
                                            mm_id.starred_partner_ids = [(4, self.user_id.partner_id.id)]
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
            partner.cesce_risk_classification_count = mapped_data.get(partner.id, 0)            
    
    @api.model
    def cron_cesce_risk_classification_check_file_out(self):
        _logger.info('cron_cesce_risk_classification_check_file_out')
        # webservice
        cesce_web_service = CesceWebService(self.env.user.company_id, self.env)        
        # errors
        cesce_web_service.partner_classifications_error()        
        # file_out
        cesce_web_service.partner_classifications_out()        
        # review with cesce_risk_state=classification_sent,classification_error
        res_partner_ids = self.env['res.partner'].search(
            [
                ('cesce_risk_state', 'in', ('classification_sent', 'classification_error'))
            ]
        )
        if res_partner_ids:
            _logger.info('revisar estos ids')
            _logger.info(res_partner_ids)
    
    @api.one
    def action_partner_classification_sent(self):
        if self.id>0:
            allow_action = True
            
            if self.cesce_amount_requested == 0:
                allow_action = False
                raise Warning("Es necesario definir una importe solicitado "
                              "para Cesce para poder tramitar la solicitud de riesgo")
            elif not self.vat:
                allow_action = False
                raise Warning("Es necesario definir un NIF/CIF")
            elif self.country_id.id == 0:
                allow_action = False
                raise Warning("Es necesario definir un pais")
            elif self.state_id.id == 0:
                allow_action = False
                raise Warning("Es necesario definir una provincia")
            elif not self.zip:
                allow_action = False
                raise Warning("Es necesario definir un codigo postal")
            elif not self.city:
                allow_action = False
                raise Warning("Es necesario definir una ciudad")
            elif not self.street:
                allow_action = False
                raise Warning("Es necesario definir una direccion")
            
            if allow_action:
                cesce_web_service = CesceWebService(self.env.user.company_id, self.env)
                return_action = cesce_web_service.generate_partner_classification(self)
                
                if not return_action['errors']:
                    self.cesce_risk_state = 'classification_sent'
                else:
                    raise Warning(return_action['error'])
                
                return True

    @api.one
    def action_partner_canceled_sent(self):
        _logger.info('action_partner_canceled_sent')
        return True                                                                                                                                                          