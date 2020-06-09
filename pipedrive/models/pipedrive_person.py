# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedrivePerson(models.Model):
    _name = 'pipedrive.person'
    _description = 'Pipedrive Person'

    name = fields.Char(
        string='Name'
    )
    first_name = fields.Char(
        string='First Name'
    )
    last_name = fields.Char(
        string='Last Name'
    )
    phone = fields.Char(
        string='Phone'
    )
    email = fields.Char(
        string='Email'
    )
    pipedrive_organization_id = fields.Many2one(
        comodel_name='pipedrive.organization',
        string='Pipedrive Organization Id'
    )
    pipedrive_user_id = fields.Many2one(
        comodel_name='pipedrive.user',
        string='Pipedrive User Id'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id'
    )

'''
{
    "id": 1,
    "company_id": 7498904,
    "owner_id": {
        "id": 11451374,
        "name": "TUUP",
        "email": "servicios@tuup.es",
        "has_pic": 1,
        "pic_hash": "947f9957d2eb3cd06cddb67fa36c29b6",
        "active_flag": true,
        "value": 11451374
    },
    "org_id": {
        "name": "Ejemplo 1",
        "people_count": 1,
        "owner_id": 11451374,
        "address": null,
        "active_flag": false,
        "cc_email": "tuup@pipedrivemail.com",
        "value": 1
    },
    "name": "Ejemplo 1",
    "first_name": "Ejemplo",
    "last_name": "1",
    "open_deals_count": 0,
    "related_open_deals_count": 0,
    "closed_deals_count": 0,
    "related_closed_deals_count": 0,
    "participant_open_deals_count": 0,
    "participant_closed_deals_count": 0,
    "email_messages_count": 0,
    "activities_count": 0,
    "done_activities_count": 0,
    "undone_activities_count": 0,
    "files_count": 0,
    "notes_count": 0,
    "followers_count": 1,
    "won_deals_count": 0,
    "related_won_deals_count": 0,
    "lost_deals_count": 0,
    "related_lost_deals_count": 0,
    "active_flag": true,
    "phone": [
        {
            "label": "work",
            "value": "666666222",
            "primary": true
        }
    ],
    "email": [
        {
            "label": "work",
            "value": "prueba@ejemplo.es",
            "primary": true
        }
    ],
    "first_char": "e",
    "update_time": "2020-06-04 10:20:49",
    "add_time": "2020-06-04 07:38:27",
    "visible_to": "3",
    "picture_id": null,
    "next_activity_date": null,
    "next_activity_time": null,
    "next_activity_id": null,
    "last_activity_id": null,
    "last_activity_date": null,
    "last_incoming_mail_time": null,
    "last_outgoing_mail_time": null,
    "label": null,
    "org_name": "Ejemplo 1",
    "owner_name": "TUUP",
    "cc_email": "tuup@pipedrivemail.com"
}
'''