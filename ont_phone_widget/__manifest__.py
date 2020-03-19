# -*- coding: utf-8 -*-
{
    'name': 'Ont Phone Widget',
    'version': "10.0.1.0.0,    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'views/resources.xml',
        'web_phone.xml',
    ],
    'installable': True,
    'auto_install': False,
    'qweb': ['static/src/xml/*.xml'],    
}