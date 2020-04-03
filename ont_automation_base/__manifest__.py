# -*- coding: utf-8 -*-
{
    'name': 'Ont Automation Base',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/automation_view.xml',
    ],    
    'installable': True,
    'auto_install': False,    
}