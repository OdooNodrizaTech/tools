# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

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