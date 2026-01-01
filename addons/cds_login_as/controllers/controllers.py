# -*- coding: utf-8 -*-

##############################################################################
#
#
#    Copyright (C) 2019-TODAY .
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################


from odoo import http
from odoo.http import request
import werkzeug
from odoo.service import db, security
from odoo.addons.web.controllers.home import Home


class CdsLoginAsController(Home):
    @http.route('/web/cds_login_as/<int:user_id>', auth='public')
    def cds_web_login_as(self, user_id, **kw):
        uid = request.env.user.id
        if request.env.user._is_system():
            request.session['original_loginas_uid'] = uid
            uid = request.session.uid = user_id
            # request.env['res.users'].clear_caches()
            request.session.session_token = security.compute_session_token(
                request.session, request.env)

        return werkzeug.utils.redirect(self._login_redirect(uid))

    @http.route('/web/cds_login_back', auth='public')
    def cds_web_login_back(self, **kw):
        uid = request.env.user.id
        if request.session.get('original_loginas_uid'):
            original_uid = request.session.get('original_loginas_uid')
            request.session['original_loginas_uid'] = False
            request.session.uid = original_uid
            request.session.session_token = security \
                .compute_session_token(request.session,
                                       http.request.env)
            redirect = '/web'
            return request.redirect(redirect)
