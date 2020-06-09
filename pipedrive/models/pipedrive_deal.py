# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedriveDeal(models.Model):
    _name = 'pipedrive.deal'
    _description = 'Pipedrive Deal'

    title = fields.Char(
        string='Title'
    )
    active = fields.Boolean(
        string='Active'
    )
    status = fields.Selection(
        selection=[
            ('open', 'Abierto'),
            ('won', 'Ganado'),
            ('lost', 'Perdido'),
            ('deleted', 'Eliminado')
        ],
        string='Status',
        default='open'
    )
    pipedrive_person_id = fields.Many2one(
        comodel_name='pipedrive.person',
        string='Pipedrive Peron Id'
    )
    pipedrive_organization_id = fields.Many2one(
        comodel_name='pipedrive.organization',
        string='Pipedrive Organization Id'
    )
    pipedrive_user_id = fields.Many2one(
        comodel_name='pipedrive.user',
        string='Pipedrive User Id'
    )
    pipedrive_pipeline_id = fields.Many2one(
        comodel_name='pipedrive.pipeline',
        string='Pipedrive Pipeline Id'
    )
    pipedrive_stage_id = fields.Many2one(
        comodel_name='pipedrive.stage',
        string='Pipedrive Stage Id'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead Id'
    )

'''
{
    "id": 2,
    "value": 0,
    "currency": "EUR",
    "add_time": "2020-06-09 10:58:39",
    "update_time": "2020-06-09 10:58:39",
    "stage_change_time": null,
    "active": true,
    "deleted": false,
    "status": "open",
    "probability": null,
    "next_activity_date": null,
    "next_activity_time": null,
    "next_activity_id": null,
    "last_activity_id": null,
    "last_activity_date": null,
    "lost_reason": null,
    "visible_to": "3",
    "close_time": null,
    "pipeline_id": 1,
    "won_time": null,
    "first_won_time": null,
    "lost_time": null,
    "products_count": 0,
    "files_count": 0,
    "notes_count": 0,
    "followers_count": 1,
    "email_messages_count": 0,
    "activities_count": 0,
    "done_activities_count": 0,
    "undone_activities_count": 0,
    "participants_count": 1,
    "expected_close_date": null,
    "last_incoming_mail_time": null,
    "last_outgoing_mail_time": null,
    "label": null,
    "stage_order_nr": 0,
    "person_name": "Ejemplo 1",
    "org_name": null,
    "next_activity_subject": null,
    "next_activity_type": null,
    "next_activity_duration": null,
    "next_activity_note": null,
    "formatted_value": "0 €",
    "weighted_value": 0,
    "formatted_weighted_value": "0 €",
    "weighted_value_currency": "EUR",
    "rotten_time": null,
    "owner_name": "TUUP",
    "cc_email": "tuup+deal2@pipedrivemail.com",
    "org_hidden": false,
    "person_hidden": false
}
'''