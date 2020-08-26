# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models, tools

import pytz
from datetime import datetime
import xml.etree.ElementTree as ET
_logger = logging.getLogger(__name__)


class PhoneCallLogFile(models.Model):
    _name = 'phone.call.log.file'
    _description = 'Phone Call Log File'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Name',
        required=True
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('assign', 'Asignado'),
            ('done', 'Hecho'),
        ],
        string='State',
        default='draft'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User'
    )
    phone_call_log_count = fields.Integer(
        compute='_compute_phone_call_log_count',
        string="Phone Call Logs",
    )

    def _compute_phone_call_log_count(self):
        for item in self:
            item.phone_call_log_count = len(
                self.env['phone.call.log'].search(
                    [
                        ('phone_call_log_file_id', '=', self.id)
                    ]
                )
            )

    @api.multi
    def action_assign_multi(self):
        for item in self:
            if item.state == 'draft':
                phone_call_log_phone_ids = self.env['phone.call.log.phone'].search(
                    [
                        ('phone', '=', self.name),
                    ]
                )
                if phone_call_log_phone_ids:
                    phone_call_log_phone_id = phone_call_log_phone_ids[0]
                    item.user_id = phone_call_log_phone_id.user_id.id
                    item.state = 'assign'

    @api.multi
    def action_read_file_multi(self):
        for item in self:
            if item.state == 'assign':
                item.action_read_file()

    @api.model
    def create(self, values):
        res = super(PhoneCallLogFile, self).create(values)
        res.action_assign_multi()
        res.action_read_file_multi()
        return res

    @api.one
    def action_read_file(self):
        if self.state == 'assign':
            attachment_ids = self.env['ir.attachment'].search(
                [
                    ('res_model', '=', self._name),
                    ('res_id', '=', self.id),
                ]
            )
            if attachment_ids:
                attachment_id = attachment_ids[0]
                # define
                keys_call = [
                    'number', 'duration', 'type', 'presentation', 'subscription_id',
                    'post_dial_digits', 'subscription_component_name',
                    'readable_date', 'contact_name'
                ]
                url_file = '/var/lib/odoo/.local/share/Odoo/filestore/%s/%s' % (
                    tools.config.get('db_name'),
                    attachment_id.store_fname
                )
                tree = ET.parse(url_file)
                call_items = tree.findall('call')
                # info
                tz_utc = pytz.timezone('UTC')
                tz_user_id = pytz.timezone(self.user_id.tz)
                # operations
                _logger.info('Total elementos=%s' % len(call_items))
                if call_items:
                    phone_call_log_ids = self.env['phone.call.log'].search(
                        [
                            ('phone_call_log_file_id', '=', self.id)
                        ]
                    )
                    phone_call_logs = {}
                    if phone_call_log_ids:
                        for item in phone_call_log_ids:
                            # number
                            if item.number not in phone_call_logs:
                                phone_call_logs[item.number] = {}
                            # date
                            if item.date not in phone_call_logs[item.number]:
                                phone_call_logs[item.number][item.date] = item
                    # call_items
                    for call_item in call_items:
                        item = {}
                        for key_call in keys_call:
                            try:
                                item[key_call] = call_item.get(key_call)
                            except:
                                item[key_call] = None
                        # search lenght (prevent 1004, etc)
                        if len(item['number']) > 4:
                            # change type
                            if item['type'] is not None:
                                item['type'] = int(item['type'])
                            # change duration
                            if item['duration'] is not None:
                                item['duration'] = "{0:.2f}".format(
                                    (float(item['duration'])/60)
                                )
                            # change presentation
                            if item['presentation'] is not None:
                                item['presentation'] = int(item['presentation'])
                            # date_convert
                            date_tz_user_id = datetime.strptime(
                                item['readable_date'], '%Y/%m/%d %H:%M:%S'
                            )
                            date_tz_user_id = tz_user_id.localize(date_tz_user_id)
                            # convert_to_timezone_utc
                            date_tz_utc = date_tz_user_id.astimezone(tz_utc)
                            # search
                            key_date = date_tz_utc.strftime('%Y-%m-%d %H:%M:%S')
                            item_find = False
                            if item['number'] in phone_call_logs:
                                if key_date in phone_call_logs[item['number']]:
                                    item_find = True
                            # operations
                            if item_find:
                                call_log = phone_call_logs[item['number']][key_date]
                                call_log.operations_item()
                            else:
                                # vars
                                vars = {
                                    'phone_call_log_file_id': self.id,
                                    'user_id': self.user_id.id,
                                    'number': item['number'],
                                    'duration': item['duration'],
                                    'date':
                                        date_tz_utc.strftime('%Y/%m/%d %H:%M:%S'),
                                    'type': item['type'],
                                    'presentation': item['presentation']
                                }
                                # contact_name
                                if item['contact_name'] != '(Unknown)':
                                    vars['contact_name'] = item['contact_name']
                                # create
                                self.env['phone.call.log'].sudo().create(vars)
                    # done
                    self.state = 'done'

    @api.multi
    def cron_phone_call_log_files(self, cr=None, uid=False, context=None):
        _logger.info('cron_phone_call_log_files')
        # all
        file_ids = self.env['phone.call.log.file'].search(
            [
                ('state', '=', 'draft')
            ]
        )
        if file_ids:
            file_ids.action_assign_multi()
            for file_id in file_ids:
                if file_id.state == 'assign':
                    file_id.action_read_file()
