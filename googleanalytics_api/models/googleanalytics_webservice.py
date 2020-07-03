# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models
import datetime, os, codecs, pysftp
from dateutil.relativedelta import relativedelta
#need
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class GoogleanalyticsWebservice():

    def __init__(self, key_file_location):
        scope = 'https://www.googleapis.com/auth/analytics.readonly'
        # Authenticate and construct service.
        self.service = self.get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location
        )
        
    def get_service(self, api_name, api_version, scopes, key_file_location):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_location, scopes=scopes)    
        # Build the service object.
        service = build(api_name, api_version, credentials=credentials)    
        return service
        
    def get_results_real(self, profile_id, start_date, end_date,  metrics, dimensions, start_index):
        return self.service.data().ga().get(
                ids='ga:' + profile_id,
                start_date=start_date,
                end_date=end_date,
                metrics=",".join(metrics),
                dimensions=",".join(dimensions),
                start_index=start_index,
                max_results=1000
            ).execute()
            
    def get_results(self, profile_id, start_date, end_date, metrics, dimensions):
        start_index = 1
        #result = get_results_real(profile_id, '7daysAgo', 'yesterday',  metrics, dimensions, start_index)
        result = self.get_results_real(profile_id, start_date, end_date,  metrics, dimensions, start_index)
        result_return = result
        
        if 'totalResults' in result:
            if result['totalResults']>result['itemsPerPage']:
                while result['totalResults']>start_index:
                    start_index += result['itemsPerPage']  
                    result = self.get_results_real(profile_id, start_date, end_date,  metrics, dimensions, start_index)
                    #rows
                    if 'rows' in result:
                        for row in result['rows']:
                            result_return['rows'].append(row)
                
        return result_return