# -*- coding: utf-8 -*-
{
    'name': 'Ir Attachment S3',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'external_dependencies': {
        'python3' : ['boto'],
    },
    'depends': ['base'],
    'data': [
        'data/ir_cron.xml',
        'data/ir_configparameter_data.xml',
    ],
    'installable': True,
    'auto_install': False,    
}