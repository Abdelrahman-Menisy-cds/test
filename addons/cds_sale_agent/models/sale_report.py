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


class SaleReport(models.Model):
    _inherit = "sale.report"

    employee_id = fields.Many2one('hr.employee', 'Sales Agent', readonly=True)

    def _group_by_sale(self):
        group = super()._group_by_sale()
        group += ', s.employee_id'
        return group

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['employee_id'] = "s.employee_id"
        return res





