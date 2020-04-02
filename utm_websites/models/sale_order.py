# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    utm_website_id = fields.Many2one(
        comodel_name='utm.website',        
        string='Sitio web'
    )