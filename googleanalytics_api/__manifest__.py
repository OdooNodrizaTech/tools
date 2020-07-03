# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Googleanalytics Api',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'external_dependencies': {
        'python3': ['google-api-python-client', 'oauth2client'],
    },
    'depends': ['base'],
    'data': [
        'data/ir_cron.xml',
        'data/ir_configparameter_data.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,    
}