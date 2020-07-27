# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, tools
from datetime import datetime
from dateutil.relativedelta import relativedelta

import json
import boto3

import logging
_logger = logging.getLogger(__name__)


class DatalakeLog(models.Model):
    _name = 'datalake.log'
    _description = 'Datalake Log'

    @api.model
    def cron_generate_ses_google_analytics_reports_yesterday(self):
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        ir_cf = self.env['ir.config_parameter']
        ses_datalake_test = str(ir_cf.sudo().get_param('ses_datalake_test'))

        sns_arns_google_analytics_reports = ir_cf.sudo().get_param(
            'sns_arns_google_analytics_reports'
        ).split(',')
        google_analytics_reports_profile_ids = ir_cf.sudo().get_param(
            'google_analytics_reports_profile_ids'
        ).split(',')
        current_date = datetime.today()
        sns_date = current_date + relativedelta(days=-1)
        
        sns_client = boto3.client('sns',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='eu-west-1'
        )
        for sns_arn in sns_arns_google_analytics_reports:
            for profile_id in google_analytics_reports_profile_ids:
                # test
                test = False
                if ses_datalake_test or ses_datalake_test == 'True':
                    test = True
                # publish
                message = {
                    'test': test,
                    'profile_id': profile_id,
                    'date': sns_date.strftime("%Y-%m-%d")
                }
                response = sns_client.publish(
                    TopicArn=sns_arn,
                    Message=json.dumps(message)
                )
                _logger.info(message)
                _logger.info(response)
    
    @api.model
    def cron_generate_ses_google_analytics_reports_all_year(self):
        end_date = datetime.today()
        start_date = datetime(end_date.year,1, 1)                
        
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')                
        ses_datalake_test = str(self.env['ir.config_parameter'].sudo().get_param('ses_datalake_test'))

        sns_arns_google_analytics_reports = self.env['ir.config_parameter'].sudo().get_param(
            'sns_arns_google_analytics_reports'
        ).split(',')
        google_analytics_reports_profile_ids = self.env['ir.config_parameter'].sudo().get_param(
            'google_analytics_reports_profile_ids'
        ).split(',')
        sns_client = boto3.client('sns',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='eu-west-1'
        )
        sns_date = start_date

        while sns_date.strftime("%Y-%m-%d") != end_date.strftime("%Y-%m-%d"):
            sns_date = sns_date + relativedelta(days=1)

            for sns_arn in sns_arns_google_analytics_reports:
                for profile_id in google_analytics_reports_profile_ids:
                    # test
                    test = False
                    if ses_datalake_test or ses_datalake_test == 'True':
                        test = True
                    # publish
                    message = {
                        'test': test,
                        'profile_id': profile_id,
                        'date': sns_date.strftime("%Y-%m-%d")
                    }
                    response = sns_client.publish(
                        TopicArn=sns_arn,
                        Message=json.dumps(message)
                    )
                    _logger.info(message)
                    _logger.info(response)
