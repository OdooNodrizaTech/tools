# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    utm_website_id = fields.Many2one(
        comodel_name='utm.website',
        string='Utm website'
    )
