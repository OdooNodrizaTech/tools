# -*- coding: utf-8 -*-
from openerp import api, models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
        
    not_allow_marketing_mails = fields.Boolean(
        string="No permite emails de marketing"
    )                                                                                                     