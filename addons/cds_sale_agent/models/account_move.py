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


class AccountMove(models.Model):
    _inherit = "account.move"

    employee_id = fields.Many2one('hr.employee', 'Sales Agent',)

    @api.onchange('partner_id')
    def _onchange_partner_agent(self):
        self.ensure_one()
        if self.partner_id and self.partner_id.sale_employee_id and self.move_type in ['out_invoice','out_refund']:
            self.employee_id = self.partner_id.sale_employee_id




