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


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    def get_route_domain(self):
        domain = [('product_selectable', '=', True)]
        if self.env.user.has_group(
                'cds_warehouse_restriction.group_restrict_stock_routes'):
            domain += [('id', 'in', self.env.user.allowed_route_ids.ids)]
        return domain

    route_id = fields.Many2one(
        'stock.route', string='Preferred Route',
        domain=get_route_domain)

    # @api.model
    # def action_view_allowed_replenish(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id(
    #         'stock.action_orderpoint_replenish')
    #     if self.with_user(1).env.user.has_group(
    #             'cds_warehouse_restriction.action_orderpoint_allowed_replenish'):
    #         domain = [('route_id', 'in',
    #                    self.with_user(1).env.user.allowed_route_ids.ids)]
    #         action['domain'] = domain
    #     return action


    def _get_orderpoint_action(self):
        action = super(StockWarehouseOrderpoint, self)._get_orderpoint_action()
        if self.env.user.has_group(
                'cds_warehouse_restriction.group_restrict_stock_routes') :
            action['domain'] = [('route_id', 'in',
                       self.env.user.allowed_route_ids.ids)]
        else:
            action['domain'] = []
        return action
