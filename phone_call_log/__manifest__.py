# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
{
    'name': 'Phone Call Log',
    'version': '12.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'mail_activity_done'],
    'data': [
        'data/ir_cron.xml',
        'views/mail_activity_type_view.xml',
        'views/phone_call_log_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
}