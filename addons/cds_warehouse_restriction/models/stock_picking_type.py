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


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    can_validate_own_transfers = fields.Boolean(string="Can Validate Own Transfers", default=False)

    @api.model
    def action_view_picking_type(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            'stock.stock_picking_type_action')
        if self.with_user(1).env.user.has_group(
                'cds_warehouse_restriction.group_restrict_view_stock_operations'):
            domain = [('id', 'in',
                       self.with_user(1).env.user.allow_picking_type_ids.ids)]
            action['domain'] = domain
        return action

