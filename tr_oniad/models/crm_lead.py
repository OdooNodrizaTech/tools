# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models

import requests
import json

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    tracking_profile_uuid = fields.Char(
        string='Tracking Profile Uuid',
        readonly=True
    )
    tracking_cookie_uuid = fields.Char(
        string='Tracking Cookie Uuid',
        readonly=True
    )
    tracking_user_uuid = fields.Char(
        string='Tracking User Uuid',
        readonly=True
    )
    tracking_session_uuid = fields.Char(
        string='Tracking Session Uuid',
        readonly=True
    )

    @api.multi
    def tracking_session_addProperties(self):
        self.ensure_one()
        if self.tracking_profile_uuid and self.tracking_session_uuid:
            headers = {
                'Content-type': 'application/json',
                'origin': 'erp.arelux.com',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
            }
            data = {
                "profile_uuid": str(self.tracking_profile_uuid),
                "properties": {
                    "lead_id": self.id
                }
            }
            url = 'https://tr.oniad.com/api/session/%s/addProperties' % self.tracking_session_uuid
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers)
                return response.status_code
            except:
                return 500

    @api.model
    def cron_odoo_tr_oniad_api_call_update_session_data(self):
        _logger.info('cron_odoo_tr_oniad_api_call_update_session_data')
        items = self.env['crm.lead.account.invoice.report'].search(
            [
                ('amount_untaxed_total_out_invoice', '>', 0),
                ('lead_id.tracking_session_uuid', '!=', False),
                ('lead_id.tracking_profile_uuid', '!=', False)                
            ]
        )
        if items:
            for item in items:
                amount_untaxed = item.amount_untaxed_total_out_invoice-item.amount_untaxed_total_out_refund
                margin = item.margin_total_out_invoice-item.margin_total_out_refund                
                # api_call tr.oniad.com
                headers = {
                    'Content-type': 'application/json', 
                    'origin': 'erp.arelux.com', 
                    'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
                }
                data = {
                    "profile_uuid": str(item.lead_id.tracking_profile_uuid),
                    "properties": {
                        "amount_untaxed_invoices": amount_untaxed,
                        "margin_invoices": margin
                    }
                }
                url = 'https://tr.oniad.com/api/session/%s/addProperties' % item.lead_id.tracking_session_uuid
                try:
                    response = requests.post(url, data=json.dumps(data), headers=headers)
                    # logger
                    if response.status_code != 200:
                        _logger.info(response.status_code)
                        _logger.info(response.json())
                    # return
                    return response.status_code
                except:
                    return 500
