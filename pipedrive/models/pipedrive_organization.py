# -*- coding: utf-8 -*-
#https://developers.pipedrive.com/docs/api/v1/#!/Organizations
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedriveOrganization(models.Model):
    _name = 'pipedrive.organization'
    _description = 'Pipedrive Organization'

    name = fields.Char(
        string='Name'
    )
    address = fields.Char(
        string='Address'
    )
    address_street_number = fields.Char(
        string='Address Street Number'
    )
    address_route = fields.Char(
        string='Address Route'
    )
    address_locality = fields.Char(
        string='Address Locality'
    )
    address_country = fields.Char(
        string='Address Country'
    )
    address_postal_code = fields.Char(
        string='Address Postal Code'
    )
    pipedrive_user_id = fields.Many2one(
        comodel_name='pipedrive.user',
        string='Pipedrive User Id'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id'
    )

    @api.model
    def cron_sqs_pipedrive_organization(self):
        _logger.info('cron_sqs_pipedrive_organization')

'''
{
    "id": 2,
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
    "name": "Demostraciones S.L",
    "open_deals_count": 0,
    "related_open_deals_count": 0,
    "closed_deals_count": 0,
    "related_closed_deals_count": 0,
    "email_messages_count": 0,
    "people_count": 1,
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
    "category_id": null,
    "picture_id": null,
    "country_code": null,
    "first_char": "d",
    "update_time": "2020-06-04 14:32:04",
    "add_time": "2020-06-04 10:21:51",
    "visible_to": "3",
    "next_activity_date": null,
    "next_activity_time": null,
    "next_activity_id": null,
    "last_activity_id": null,
    "last_activity_date": null,
    "label": null,
    "address": "Avenida de las Pruebas 1, Zaragoza",
    "address_subpremise": "3",
    "address_street_number": "1",
    "address_route": "Avenida Alcalde Ramón Sainz de Varanda",
    "address_sublocality": null,
    "address_locality": "Zaragoza",
    "address_admin_area_level_1": "Aragón",
    "address_admin_area_level_2": "Zaragoza",
    "address_country": "España",
    "address_postal_code": "50009",
    "address_formatted_address": "Av. Alcalde Ramón Sainz de Varanda, 1, 3, 50009 Zaragoza, España",
    "89a1b8d03112f1b63eab112c7c46c69c73ae7334": null,
    "owner_name": "TUUP",
    "cc_email": "tuup@pipedrivemail.com"
}
'''