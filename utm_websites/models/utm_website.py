# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class UtmWebsite(models.Model):
    _name = 'utm.website'
    _description = 'Utm website'
    
    name = fields.Char(        
        string='Name'
    )
    url = fields.Char(        
        string='Url'
    )
    mail_template_id = fields.Many2one(
        comodel_name='mail.template',        
        string='Mail Template Id'
    )
