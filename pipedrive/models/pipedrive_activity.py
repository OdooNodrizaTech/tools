# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class PipedriveActivity(models.Model):
    _name = 'pipedrive.activity'
    _description = 'Pipedrive Activity'

    type = fields.Selection(
        selection=[
            ('call', 'Lead'),
            ('videollamada', 'Videollamada'),
            ('meeting', 'Reunion'),
            ('email', 'Email'),
            ('demo', 'Presentacion'),
            ('deadline', 'Plazo'),
            ('lunch', 'Almuerzo'),
            ('task >', 'Tarea')
        ],
        string='Type',
        default='call'
    )
    pipedrive_user_id = fields.Many2one(
        comodel_name='pipedrive.user',
        string='Pipedrive User Id'
    )
    done = fields.Boolean(
        string='Done'
    )
    due_date = fields.Date(
        string='Due Date'
    )
    subject = fields.Char(
        string='Subject'
    )
    public_description = fields.Text(
        string='Public Description'
    )
    pipedrive_organization_id = fields.Many2one(
        comodel_name='pipedrive.organization',
        string='Pipedrive Organization Id'
    )
    pipedrive_person_id = fields.Many2one(
        comodel_name='pipedrive.person',
        string='Pipedrive Person Id'
    )
    pipedrive_deal_id = fields.Many2one(
        comodel_name='pipedrive.deal',
        string='Pipedrive Deal Id'
    )
    mail_activity_id = fields.Many2one(
        comodel_name='mail.activity',
        string='Mail Activity Id'
    )

'''
{
    "id": 1,
    "company_id": 7498904,
    "user_id": 11451374,
    "done": false,
    "type": "call",
    "reference_type": null,
    "reference_id": null,
    "conference_meeting_client": null,
    "conference_meeting_url": null,
    "due_date": "2020-06-09",
    "due_time": "",
    "duration": "",
    "busy_flag": null,
    "add_time": "2020-06-09 11:04:16",
    "marked_as_done_time": "",
    "last_notification_time": null,
    "last_notification_user_id": null,
    "notification_language_id": 6,
    "subject": "xxxx",
    "public_description": "",
    "calendar_sync_include_context": null,
    "location": null,
    "org_id": null,
    "person_id": null,
    "deal_id": null,
    "lead_id": null,
    "lead_title": "",
    "active_flag": true,
    "update_time": "2020-06-09 11:04:16",
    "update_user_id": null,
    "gcal_event_id": null,
    "google_calendar_id": null,
    "google_calendar_etag": null,
    "source_timezone": null,
    "rec_rule": null,
    "rec_rule_extension": null,
    "rec_master_activity_id": null,
    "conference_meeting_id": null,
    "note": null,
    "created_by_user_id": 11451374,
    "location_subpremise": null,
    "location_street_number": null,
    "location_route": null,
    "location_sublocality": null,
    "location_locality": null,
    "location_admin_area_level_1": null,
    "location_admin_area_level_2": null,
    "location_country": null,
    "location_postal_code": null,
    "location_formatted_address": null,
    "attendees": null,
    "participants": null,
    "series": null,
    "org_name": null,
    "person_name": null,
    "deal_title": null,
    "owner_name": "TUUP",
    "person_dropbox_bcc": null,
    "deal_dropbox_bcc": null,
    "assigned_to_user_id": 11451374,
    "file": null
}
'''