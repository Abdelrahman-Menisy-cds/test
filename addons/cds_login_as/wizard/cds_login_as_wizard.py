# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class CdsLoginAsWizard(models.TransientModel):
    _name = 'cds.login.as.wizard'
    _description = 'Login As Wizard'
    user_id = fields.Many2one('res.users', 'User', required=True)

    def action_login_as(self):
        user_id = self.user_id
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/cds_login_as/%s' % (
                user_id.id),
            'target': 'self',
        }
