# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'News Custom',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'views/news_custom.xml',        
        'security/ir.model.access.csv',
        'web_news_custom.xml',
    ],
    'installable': True,
    'auto_install': False,
    'qweb': ['static/src/xml/*.xml'],    
}