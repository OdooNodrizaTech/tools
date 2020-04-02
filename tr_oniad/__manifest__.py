# -*- coding: utf-8 -*-
{
    'name': 'Tr Oniad',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'crm', 'sale'],
    'data': [
        'data/ir_cron.xml',
        'views/crm_lead.xml',
        'views/sale_order.xml',
        'views/res_partner.xml'
    ],
    'installable': True,
    'auto_install': False,    
}