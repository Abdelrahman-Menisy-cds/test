# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import models, fields, api
from odoo.tools import SQL

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    employee_id = fields.Many2one('hr.employee', string='Sales Agent')


    def _select(self) -> SQL:
        return SQL("%s, move.employee_id as employee_id", super()._select())