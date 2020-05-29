# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import odoo

import logging
_logger = logging.getLogger(__name__)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

from googleanalytics_webservice import GoogleanalyticsWebservice

class GoogleanalyticsResultCampaign(models.Model):
    _name = 'googleanalytics.result.campaign'
    _description = 'Googleanalytics Result Campaign'
    
    sessionDuration = fields.Float(        
        string='sessionDuration'
    )
    landingPagePath = fields.Char(        
        string='landingPagePath'
    )
    adGroup = fields.Char(        
        string='adGroup'
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
    webPropertyId = fields.Char(        
        string='webPropertyId'
    )
    totalEvents = fields.Integer(        
        string='totalEvents'
    )
    entrances = fields.Integer(        
        string='entrances'
    )
    source = fields.Char(        
        string='source'
    )
    medium = fields.Char(        
        string='medium'
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
    exits = fields.Integer(        
        string='exits'
    )
    uniqueEvents = fields.Integer(        
        string='uniqueEvents'
    )
    accountId = fields.Integer(        
        string='accountId'
    )

    @api.multi
    def cron_get_previous_day_info(self, cr=None, uid=False, context=None):
        current_date = datetime.today()
        _logger.info('cron_get_previous_day_info')
        # start
        key_file_location = odoo.tools.config.get('googleanalytics_api_key_file')
        googleanalytics_webservice = GoogleanalyticsWebservice(key_file_location)
        # vars
        profile_id = str(15181752)
        metrics = ['ga:users', 'ga:sessions', 'ga:sessionDuration', 'ga:bounceRate', 'ga:pageviews', 'ga:timeOnPage', 'ga:totalEvents', 'ga:uniqueEvents', 'ga:entrances', 'ga:exits']
        dimensions = ['ga:date', 'ga:landingPagePath', 'ga:adGroup', 'ga:campaign', 'ga:source', 'ga:medium', 'ga:keyword']
        start_date = '2019-08-01'
        end_date = '2019-08-01'
        # search_previous
        googleanalytics_result_campaign_ids = self.env['googleanalytics.result.campaign'].sudo().search(
            [
                ('date', '=', str(start_date)),
                ('profileId', '=', str(profile_id))
            ]
        )
        if len(googleanalytics_result_campaign_ids) == 0:
            results = googleanalytics_webservice.get_results(profile_id, start_date, end_date, metrics, dimensions)
            if 'rows' in results:
                if len(results['rows'])>0:
                    for row in results['rows']:
                        _logger.info('row')
                        _logger.info(row)
                        _logger.info(row2)