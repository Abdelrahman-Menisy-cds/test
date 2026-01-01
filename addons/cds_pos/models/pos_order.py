# -*- coding: utf-8 -*-

#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Ragab Deaf (<ragabdeaf93@outlook.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.

from odoo import fields, models, api
from odoo.osv.expression import AND
from datetime import datetime 
from collections import defaultdict
from dateutil.relativedelta import relativedelta

class  PosOrder(models.Model):
    _inherit = 'pos.order'
    
    pos_refund_period = fields.Integer(string='Refund Period', related='config_id.refund_period', readonly=True)
    
    def _export_for_ui(self, order):
        fields = super()._export_for_ui(order)
        fields['pos_refund_period'] = order.pos_refund_period
        return fields
    # override search_paid_order_ids method to add load days domain
    @api.model
    def search_paid_order_ids(self, config_id, domain, limit, offset):
        """Search for 'paid' orders that satisfy the given domain, limit and offset."""
        default_domain = [('state', '!=', 'draft'), ('state', '!=', 'cancel')]
        pos_config = self.env['pos.config'].browse(config_id)
        # We will add a domain to filter the orders that are older than the limit date.
        if pos_config.enable_load_pos_orders_days and pos_config.load_pos_orders_days > 0:
            limit_date = datetime.today() - relativedelta(days=pos_config.load_pos_orders_days)
            date_domain = [('date_order', '>=', limit_date)]
            if domain == []:
                real_domain = AND([date_domain, default_domain])
            else:
                real_domain = AND([domain, date_domain, default_domain])
        else:
            if domain == []:
                real_domain = default_domain
            else:
                real_domain = AND([domain, default_domain])
        orders = self.search(real_domain, limit=limit, offset=offset)
        # We clean here the orders that does not have the same currency.
        # As we cannot use currency_id in the domain (because it is not a stored field),
        # we must do it after the search.

        orders = orders.filtered(lambda order: order.currency_id == pos_config.currency_id)
        orderlines = self.env['pos.order.line'].search(['|', ('refunded_orderline_id.order_id', 'in', orders.ids), ('order_id', 'in', orders.ids)])

        # We will return to the frontend the ids and the date of their last modification
        # so that it can compare to the last time it fetched the orders and can ask to fetch
        # orders that are not up-to-date.
        # The date of their last modification is either the last time one of its orderline has changed,
        # or the last time a refunded orderline related to it has changed.
        orders_info = defaultdict(lambda: datetime.min)
        for orderline in orderlines:
            key_order = orderline.order_id.id if orderline.order_id in orders \
                            else orderline.refunded_orderline_id.order_id.id
            if orders_info[key_order] < orderline.write_date:
                orders_info[key_order] = orderline.write_date
        totalCount = self.search_count(real_domain)
        return {'ordersInfo': list(orders_info.items())[::-1], 'totalCount': totalCount}
