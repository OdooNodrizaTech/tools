# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CesceWebserviceError(models.Model):
    _name = 'cesce.webservice.error'
    _description = 'Cesce Webservice Error'
    
    code = fields.Char(
        string='Code'
    )
    name = fields.Char(
        string='Name'
    )
    area = fields.Selection(
        selection=[
            ('none', 'None'),
            ('security', 'Security'),
            ('risk', 'Risk')
        ],
        string='Area'
    )
