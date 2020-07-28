# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from .googleanalytics_webservice import GoogleanalyticsWebservice
from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta

import odoo

_logger = logging.getLogger(__name__)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


class GoogleanalyticsResultGeneral(models.Model):
    _name = 'googleanalytics.result.general'
    _description = 'Googleanalytics Result General'

    medium = fields.Char(
        string='medium'
    )
    pageviews = fields.Integer(
        string='pageviews'
    )
    keyword = fields.Char(
        string='keyword'
    )
    campaign = fields.Char(
        string='campaign'
    )
    sessions = fields.Integer(
        string='sessions'
    )
    deviceCategory = fields.Char(
        string='deviceCategory'
    )
    goal1ConversionRate = fields.Float(
        string='goal1ConversionRate'
    )
    goal6ConversionRate = fields.Float(
        string='goal6ConversionRate'
    )
    newUsers = fields.Integer(
        string='newUsers'
    )
    webPropertyId = fields.Char(
        string='webPropertyId'
    )
    cityId = fields.Char(
        string='cityId'
    )
    source = fields.Char(
        string='source'
    )
    goal1Completions = fields.Integer(
        string='goal1Completions'
    )
    goal6Completions = fields.Integer(
        string='goal6Completions'
    )
    sessionDuration = fields.Float(
        string='sessionDuration'
    )
    bounceRate = fields.Float(
        string='bounceRate'
    )
    profileName = fields.Char(
        string='profileName'
    )
    date = fields.Date(
        string='date'
    )
    profileId = fields.Integer(
        string='profileId'
    )
    users = fields.Integer(
        string='users'
    )
    timeOnPage = fields.Float(
        string='timeOnPage'
    )
    uniqueEvents = fields.Integer(
        string='uniqueEvents'
    )
    accountId = fields.Integer(
        string='accountId'
    )

    @api.model
    def get_day_info(self, date, profile_id):
        _logger.info(date)
        _logger.info(profile_id)
        # GoogleanalyticsWebservice
        key_file_location = odoo.tools.config.get('googleanalytics_api_key_file')
        googleanalytics_webservice = GoogleanalyticsWebservice(key_file_location)
        # define
        metrics = ['ga:users', 'ga:newUsers', 'ga:sessions', 'ga:sessionDuration',
                   'ga:bounceRate', 'ga:pageviews', 'ga:timeOnPage',
                   'ga:goalXXCompletions', 'ga:goalXXConversionRate', 'ga:uniqueEvents']
        dimensions = ['ga:date', 'ga:source', 'ga:medium', 'ga:campaign',
                      'ga:keyword', 'ga:cityId', 'ga:deviceCategory']
        # replace_xx_metrics
        metrics_xx_by_profile = {
            '15181752': 6,  # todocesped
            '46640523': 1,  # arelux
            '85831272': 1,  # oniup
            '138471441': 1  # oniad
        }
        metrics_new = []

        for metric_key in metrics:
            if 'XX' not in metric_key:
                metrics_new.append(metric_key)
            else:
                metrics_xx_profile = str(metrics_xx_by_profile[str(profile_id)])
                metric_new_key = str(metric_key)
                metric_new_key = metric_new_key.replace('XX', metrics_xx_profile)
                metrics_new.append(metric_new_key)

        metrics = metrics_new
        # search
        ids = self.env['googleanalytics.result.general'].sudo().search(
            [
                ('date', '=', str(date)),
                ('profileId', '=', str(profile_id))
            ]
        )
        if len(ids) == 0:
            try:
                results = googleanalytics_webservice.get_results(
                    profile_id,
                    date,
                    date,
                    metrics,
                    dimensions
                )
                if 'rows' in results:
                    if len(results['rows']) > 0:
                        for row in results['rows']:
                            count = 0
                            vals = {
                                'webPropertyId':
                                    results['profileInfo']['webPropertyId'],
                                'profileId':
                                    results['profileInfo']['profileId'],
                                'profileName':
                                    results['profileInfo']['profileName'],
                                'accountId':
                                    results['profileInfo']['accountId']
                            }
                            for columnHeader in results['columnHeaders']:
                                # row_value
                                row_value = str(row[count])
                                # data
                                columnHeaderName = str(columnHeader['name'])
                                columnHeaderName = columnHeaderName.replace('ga:', '')

                                columnHeaderDataType = str(columnHeader['dataType'])
                                # pre_item
                                vals[columnHeaderName] = ''
                                # fix
                                if row_value == '(none)' or row_value == '(not set)':
                                    row_value = ''
                                # ga:source
                                if columnHeaderName == 'source':
                                    row_value = row_value.replace('(', '').replace(')', '')
                                # ga:date
                                if columnHeaderName == 'date':
                                    new_row_value = '%s-%s-%s' % (
                                        row_value[0:4],
                                        row_value[4:6],
                                        row_value[6:8]
                                    )
                                    row_value = new_row_value
                                # types
                                if columnHeaderDataType == 'INTEGER':
                                    vals[columnHeaderName] = int(row_value)
                                elif columnHeaderDataType == 'STRING':
                                    vals[columnHeaderName] = str(row_value)
                                elif columnHeaderDataType == 'PERCENT':
                                    vals[columnHeaderName] = row_value
                                elif columnHeaderDataType == 'TIME':
                                    vals[columnHeaderName] = row_value
                                # count
                                count += 1
                            # add_item
                            self.env['googleanalytics.result.general'].sudo().create(vals)
            except:
                _logger.info('se ha producido un error')

    @api.model
    def cron_get_yesterday_info(self):
        _logger.info('cron_get_yesterday_info')
        # vars
        profile_ids = str(self.env['ir.config_parameter'].sudo().get_param(
            'googleanalytics_api_profile_ids'
        )).split(',')
        current_date = datetime.today()
        date_yesterday = current_date + relativedelta(days=-1)
        # config
        for profile_id in profile_ids:
            self.get_day_info(date_yesterday.strftime("%Y-%m-%d"), profile_id)

    @api.model
    def cron_get_all_year_info(self):
        _logger.info('cron_get_all_year_info')
        # vars
        profile_ids = str(self.env['ir.config_parameter'].sudo().get_param(
            'googleanalytics_api_profile_ids'
        )).split(',')
        end_date = datetime.today()
        start_date = datetime(end_date.year, 1, 1)
        date_item = start_date
        # operations
        while date_item.strftime("%Y-%m-%d") != end_date.strftime("%Y-%m-%d"):
            for profile_id in profile_ids:
                self.get_day_info(date_item.strftime("%Y-%m-%d"), profile_id)
            # increase
            date_item = date_item + relativedelta(days=1)
