# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import werkzeug

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.website_mail.controllers.main import _message_post_helper

import logging
_logger = logging.getLogger(__name__)

class GitRepositoryController(http.Controller):
    
    @http.route("/git/<uuid>", type='http', auth="user", website=True)
    def oniad_address_view(self, *args, **kwargs):
        if 'uuid' not in kwargs:
            return request.render('website.404')
        else:
            git_repository_ids = request.env['git.repository'].sudo().search([('uuid', '=', kwargs['uuid'])])
            if len(git_repository_ids)==0:
                return request.render('website.404')
            else:
                git_repository_id = git_repository_ids[0]
                #odoo_reboot
                odoo_reboot = False
                #params
                if 'odoo_reboot' in kwargs:
                    if str(kwargs['odoo_reboot'])=="1":
                        odoo_reboot = True
                #action_clone
                git_repository_id.action_clone(odoo_reboot)
                #return                
                return request.render('website.404')                                        