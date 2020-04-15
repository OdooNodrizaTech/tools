# -*- coding: utf-8 -*-
{
    'name': 'Googleanalytics Api',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'external_dependencies': {
        'python' : ['google-api-python-client', 'oauth2client'],
    },
    'depends': ['base'],
    'data': [
        'data/ir_cron.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,    
}