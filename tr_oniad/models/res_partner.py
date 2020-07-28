# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
import requests
import json

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

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
    def tracking_user_identify(self):
        self.ensure_one()
        if self.tracking_user_uuid and self.tracking_profile_uuid:
            headers = {
                'Content-type': 'application/json',
                'origin': 'erp.arelux.com',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; '
                    'rv:68.0) Gecko/20100101 Firefox/68.0'
            }
            data = {
                "profile_uuid": str(self.tracking_profile_uuid),
                "identity": str(self.id)
            }
            url = 'https://tr.oniad.com/api/user/%s/identify' \
                  % self.tracking_user_uuid
            try:
                response = requests.post(
                    url,
                    data=json.dumps(data),
                    headers=headers
                )
                return response.status_code
            except:
                return 500
