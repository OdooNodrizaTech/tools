# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

import pytz
from datetime import datetime
import xml.etree.ElementTree as ET
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


class PhoneCallLogFile(models.Model):
    _name = 'phone.call.log.file'
    _description = 'Phone Call Log File'

    google_drive_file_id = fields.Char(
        string='Google Drive File Id',
        required=True
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        required=True
    )
    phone_call_log_count = fields.Integer(
        compute='_compute_phone_call_log_count',
        string="Phone Call Logs",
    )

    def _compute_phone_call_log_count(self):
        for item in self:
            item.phone_call_log_count = len(self.env['phone.call.log'].search(
                [
                    ('phone_call_log_file_id', '=', self.id)
                ]
            ))

    @api.multi
    def action_read_google_drive_file_id_multi(self):
        for item in self:
            item.action_read_google_drive_file_id()

    @api.one
    def action_read_google_drive_file_id(self):
        _logger.info(self.google_drive_file_id)
        # define
        keys_call = ['number', 'duration', 'type', 'presentation', 'subscription_id', 'post_dial_digits', 'subscription_component_name', 'readable_date', 'contact_name']
        url = "https://drive.google.com/uc?id=%s&export=download" % self.google_drive_file_id
        response = urlopen(url).read()
        tree = ET.fromstring(response)
        call_items = tree.findall('call')
        # info
        timezone_utc = pytz.timezone('UTC')
        timezone_user_id = pytz.timezone(self.user_id.tz)
        # operations
        _logger.info('Total elementos=%s' % len(call_items))
        if len(call_items) > 0:
            for call_item in call_items:
                call_item_array = {}
                for key_call in keys_call:
                    try:
                        call_item_array[key_call] = call_item.get(key_call)
                    except:
                        call_item_array[key_call] = None
                # change type
                if call_item_array['type'] != None:
                    call_item_array['type'] = int(call_item_array['type'])
                # change duration
                if call_item_array['duration'] != None:
                    call_item_array['duration'] = int(call_item_array['duration'])
                # change presentation
                if call_item_array['presentation'] != None:
                    call_item_array['presentation'] = int(call_item_array['presentation'])
                # date_convert
                readable_date_timezone_user_id = datetime.strptime(call_item_array['readable_date'], '%Y/%m/%d %H:%M:%S')
                readable_date_timezone_user_id = timezone_user_id.localize(readable_date_timezone_user_id)
                # convert_to_timezone_utc
                readable_date_timezone_utc = readable_date_timezone_user_id.astimezone(timezone_utc)
                # search
                phone_call_log_ids = self.env['phone.call.log'].search(
                    [
                        ('phone_call_log_file_id', '=', self.id),
                        ('date', '=', readable_date_timezone_utc.strftime('%Y/%m/%d %H:%M:%S')),
                        ('number', '=', call_item_array['number']),
                    ]
                )
                if len(phone_call_log_ids) == 0:
                    # phone_call_log_vars
                    vals = {
                        'phone_call_log_file_id': self.id,
                        'user_id': self.user_id.id,
                        'number': call_item_array['number'],
                        'duration': call_item_array['duration'],
                        'date': readable_date_timezone_utc.strftime('%Y/%m/%d %H:%M:%S'),
                        'type': call_item_array['type'],
                        'presentation': call_item_array['presentation']
                    }
                    # contact_name
                    if call_item_array['contact_name']!='(Unknown)':
                        vals['contact_name'] = call_item_array['contact_name']
                    # create
                    self.env['phone.call.log'].sudo().create(vals)

    @api.model
    def cron_phone_call_log_files(self):
        _logger.info('cron_phone_call_log_files')
        # all
        phone_call_log_file_ids = self.env['phone.call.log.file'].search(
            [
                ('id', '>', 0)
            ]
        )
        if phone_call_log_file_ids:
            for phone_call_log_file_id in phone_call_log_file_ids:
                phone_call_log_file_id.action_read_google_drive_file_id()
