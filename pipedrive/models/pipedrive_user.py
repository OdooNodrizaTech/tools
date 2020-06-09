# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedriveUser(models.Model):
    _name = 'pipedrive.user'
    _description = 'Pipedrive User'

    name = fields.Char(
        string='Name'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency Id'
    )
    email = fields.Char(
        string='Email'
    )
    phone = fields.Char(
        string='Phone'
    )
    is_admin = fields.Boolean(
        string='Is admin'
    )
    activated = fields.Boolean(
        string='Activated'
    )
    timezone_name = fields.Char(
        string='Timezone Name'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User Id'
    )

'''
{
    "id": 11451374,
    "name": "TUUP",
    "default_currency": "EUR",
    "locale": "es_ES",
    "email": "servicios@tuup.es",
    "phone": "+34667637701",
    "created": "2020-05-14 09:19:49",
    "modified": "2020-06-08 10:13:51",
    "lang": 6,
    "active_flag": true,
    "is_admin": 1,
    "last_login": "2020-06-08 10:13:51",
    "signup_flow_variation": "signup_service",
    "has_created_company": true,
    "role_id": 1,
    "activated": true,
    "timezone_name": "Europe/Madrid",
    "timezone_offset": "+01:00",
    "icon_url": "https://d3myhnqlqw2314.cloudfront.net/profile_120x120_11451374_947f9957d2eb3cd06cddb67fa36c29b6.jpg",
    "is_you": true
}
'''