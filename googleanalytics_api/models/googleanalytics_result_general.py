# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

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