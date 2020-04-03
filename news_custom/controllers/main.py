# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2015-2016 Juris Malinens (port to v9)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http

class NewsCustomController(http.Controller):

    @http.route('/news_custom/get_records_unread_total/', type='json', auth='public')
    def get_records_unread_total(self, **kw):
        res = http.request.env['new.custom'].get_records_unread_total()
        return res
        
    @http.route('/news_custom/get_last_record_unread/', type='json', auth='public')
    def get_last_record_unread(self, **kw):
        res = http.request.env['new.custom'].get_last_record_unread()
        return res        
