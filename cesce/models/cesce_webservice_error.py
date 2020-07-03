# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class CesceWebserviceError(models.Model):
    _name = 'cesce.webservice.error'
    _description = 'Cesce Webservice Error'    
    
    code = fields.Char(        
        string='Codigo'
    )
    name = fields.Char(        
        string='Mensaje'
    )
    area = fields.Selection(
        selection=[
            ('none','Ninguna'), 
            ('security','Seguridad'),
            ('risk','Riesgos')                          
        ],
        string='Area'
    )                                           