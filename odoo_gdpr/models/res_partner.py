# -*- coding: utf-8 -*-
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
        
    not_allow_marketing_mails = fields.Boolean(
        string="No permite emails de marketing"
    )                                                                                                     