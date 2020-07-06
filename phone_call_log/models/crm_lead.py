# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    phone_call_log_count = fields.Integer(
        compute='_compute_phone_call_log_count',
        string="Expediciones",
    )

    def _compute_phone_call_log_count(self):
        for item in self:
            item.phone_call_log_count = len(self.env['phone.call.log'].search([('lead_id', '=', self.id)]))