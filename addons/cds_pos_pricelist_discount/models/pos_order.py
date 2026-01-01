# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)

# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies

# of the Software or modified copies of the Software.

# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    total_discount_amount = fields.Float(string='Total Discount Amount', readonly=True, compute='_compute_total_discount_amount', store=True)
    total_without_discount = fields.Float(string='Total Without Discount', readonly=True, compute='_compute_total_without_discount', store=True)
    
    @api.depends('amount_total', 'total_discount_amount')
    def _compute_total_without_discount(self):
        for order in self:
            order.total_without_discount = order.amount_total + order.total_discount_amount
    
    @api.depends('lines.discount_amount')
    def _compute_total_discount_amount(self):
        for order in self:
            order.total_discount_amount = sum(order.lines.mapped('discount_amount'))
    
class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    discount_amount = fields.Float(string='Discount Amount', readonly=True, compute='_compute_discount_amount', store=True)
    
    @api.depends('price_unit', 'qty', 'discount')
    def _compute_discount_amount(self):
        for line in self:
            line.discount_amount = line.price_unit * line.qty * line.discount / 100