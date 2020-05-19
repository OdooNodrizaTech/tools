# -*- coding: utf-8 -*-
import werkzeug

from odoo import fields, http, _
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class GitRepositoryController(http.Controller):
                
    @http.route("/git/<uuid>/log/<id>/finish", type='http', auth="public", methods=['GET'], website=True)
    def git_repository_log_finish_item(self, *args, **kwargs):
        if 'uuid' not in kwargs:
            return request.render('website.404')
        else:
            git_repository_ids = request.env['git.repository'].sudo().search([('uuid', '=', kwargs['uuid'])])
            if len(git_repository_ids)==0:
                return request.render('website.404')
            else:
                git_repository_id = git_repository_ids[0]
                #id
                if 'id' not in kwargs:
                    return request.render('website.404')
                else:
                    git_repository_log_ids = request.env['git.repository.log'].sudo().search([('git_repository_id', '=', git_repository_id.id),('id', '=', kwargs['id'])])
                    if len(git_repository_log_ids)==0:
                        return request.render('website.404')
                    else:
                        git_repository_log_id = git_repository_log_ids[0]
                        #action_finish
                        git_repository_log_id.action_finish()
                        #return                
                        return request.render('website.404')                                                        