# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

from googleanalytics_webservice import GoogleanalyticsWebservice

class GoogleanalyticsResultBeahavior(models.Model):
    _name = 'googleanalytics.result.beahavior'
    _description = 'Googleanalytics Result Beahavior'
    
    landingPagePath = fields.Char(        
        string='landingPagePath'
    )
    sessionDuration = fields.Float(        
        string='sessionDuration'
    )
    pageviews = fields.Integer(        
        string='pageviews'
    )
    exits = fields.Integer(        
        string='exits'
    )
    sessions = fields.Integer(        
        string='sessions'
    )
    webPropertyId = fields.Char(        
        string='webPropertyId'
    )
    pagePath = fields.Char(        
        string='pagePath'
    )
    eventCategory = fields.Char(        
        string='eventCategory'
    )
    totalEvents = fields.Integer(        
        string='totalEvents'
    )
    eventAction = fields.Char(        
        string='eventAction'
    )
    userType = fields.Char(        
        string='userType'
    )
    bounceRate = fields.Float(        
        string='bounceRate'
    )
    entrances = fields.Integer(        
        string='entrances'
    )
    profileName = fields.Char(        
        string='profileName'
    )
    date = fields.Date(        
        string='date'
    )
    profileId = fields.Char(        
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
    def cron_get_previous_day_info(self):
        current_date = datetime.today()        
        _logger.info('cron_get_previous_day_info')
        #start
        key_file_location = odoo.tools.config.get('googleanalytics_api_key_file')
        googleanalytics_webservice = GoogleanalyticsWebservice(key_file_location)
        #vars
        profile_id = str(15181752)
        metrics = ['ga:users', 'ga:sessions', 'ga:sessionDuration', 'ga:bounceRate', 'ga:pageviews', 'ga:timeOnPage', 'ga:totalEvents', 'ga:uniqueEvents', 'ga:entrances', 'ga:exits']
        dimensions = ['ga:date', 'ga:userType', 'ga:landingPagePath', 'ga:pagePath', 'ga:eventCategory', 'ga:eventAction', 'ga:eventLabel']          
        start_date = '2019-08-01'
        end_date = '2019-08-01'
        #search_previous
        googleanalytics_result_beahavior_ids = self.env['googleanalytics.result.beahavior'].sudo().search(
            [
                ('date', '=', str(start_date)),
                ('profileId', '=', str(profile_id))
            ]
        )
        if len(googleanalytics_result_beahavior_ids)==0:        
            results = googleanalytics_webservice.get_results(profile_id, start_date, end_date, metrics, dimensions)
            if 'rows' in results:
                if len(results['rows'])>0:
                    for row in results['rows']:
                        count = 0
                        #vals
                        googleanalytics_result_beahavior_vals = {
                            'webPropertyId': str(results['profileInfo']['webPropertyId']),
                            'profileId': str(results['profileInfo']['profileId']),
                            'profileName': str(results['profileInfo']['profileName']),
                            'accountId': str(results['profileInfo']['accountId'])
                        }
                        for columnHeader in results['columnHeaders']:
                            #row_value 
                            row_value = str(row[count])
                            #data
                            columnHeaderName = str(columnHeader['name'])
                            columnHeaderName = columnHeaderName.replace('ga:', '')
                            
                            columnHeaderDataType = str(columnHeader['dataType'])
                            #pre_item
                            googleanalytics_result_beahavior_vals[columnHeaderName] = ''
                            #fix
                            if row_value=='(none)' or row_value=='(not set)':
                                row_value = ''
                            #ga:source
                            if columnHeaderName=='source':
                                row_value = row_value.replace('(', '').replace(')', '')
                            #ga:date
                            if columnHeaderName=='date':
                                new_row_value = str(row_value[0:4])+'-'+str(row_value[4:6])+'-'+str(row_value[6:8])
                                row_value = new_row_value
                            #types
                            if columnHeaderDataType=='INTEGER':
                                googleanalytics_result_beahavior_vals[columnHeaderName] = int(row_value)
                            elif columnHeaderDataType=='STRING':
                                googleanalytics_result_beahavior_vals[columnHeaderName] = str(row_value)
                            elif columnHeaderDataType=='PERCENT':
                                googleanalytics_result_beahavior_vals[columnHeaderName] = row_value
                            elif columnHeaderDataType=='TIME':
                                googleanalytics_result_beahavior_vals[columnHeaderName] = row_value
                            #count
                            count += 1
                        #remove eventLabel
                        if 'eventLabel' in googleanalytics_result_beahavior_vals:
                            del googleanalytics_result_beahavior_vals['eventLabel']                                                 
                        #add_item
                        googleanalytics_result_beahavior_obj = self.env['googleanalytics.result.beahavior'].sudo().create(googleanalytics_result_beahavior_vals)                                        