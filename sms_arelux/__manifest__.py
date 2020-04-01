# -*- coding: utf-8 -*-
{
    'name': 'SMS Arelux',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'external_dependencies': {
        'python' : ['boto3', 'phonenumbers'],
    },
    'depends': ['base', 'sale', 'shipping_expedition'],
    'data': [
        'data/ir_cron.xml',
        'data/ir_configparameter_data.xml',
        'views/sale_order_view.xml',
        'views/sms_message_view.xml',
        'views/shipping_expedition_view.xml',
        'wizard/sms_compose_message_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,    
}