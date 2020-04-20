# -*- coding: utf-8 -*-
{
    'name': 'Odoo Git',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'views/git_repository_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,    
}