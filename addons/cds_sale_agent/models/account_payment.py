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


class AccountPayment(models.Model):
    _inherit = "account.payment"

    employee_id = fields.Many2one('hr.employee', 'Sales Agent',related='partner_id.sale_employee_id',store=True)

    # @api.depends('partner_id')
    # def _partner_agent(self):
    #     for rec in self:
    #         if rec.partner_id and rec.partner_id.sale_employee_id:
    #             rec.employee_id = rec.partner_id.sale_employee_id

