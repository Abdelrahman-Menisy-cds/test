# -*- coding: utf-8 -*-
# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    internal_transfer_id = fields.Many2one(
        'stock.picking',
        string='Internal Transfer',
        domain="[('state', '=', 'done'), ('picking_type_code', '=', 'internal')]",
        help='Select an internal transfer in Done status to copy products from it',
        copy=False,
        tracking=True
    )

    @api.onchange('internal_transfer_id')
    def _onchange_internal_transfer_id(self):
        """When internal transfer is selected, populate order lines with its products"""
        if self.internal_transfer_id and self.state in ['draft', 'sent']:
            self._populate_lines_from_internal_transfer()

    def _populate_lines_from_internal_transfer(self):
        """Populate order lines from the selected internal transfer"""
        if not self.internal_transfer_id:
            return

        # Clear existing order lines
        self.order_line = [(5, 0, 0)]  # Clear all lines

        # Add lines from internal transfer
        for move in self.internal_transfer_id.move_ids:
            if move.state == 'done' and move.product_id:
                line_vals = {
                    'product_id': move.product_id.id,
                    'product_uom_qty': move.product_uom_qty,
                    'product_uom': move.product_uom.id,
                    'price_unit': move.product_id.list_price or 0.0,
                    'name': move.product_id.name_get()[0][1],
                    'order_id': self.id,
                }
                self.order_line = [(0, 0, line_vals)]

    @api.constrains('internal_transfer_id')
    def _check_internal_transfer_unique(self):
        """Ensure the same internal transfer is not used in multiple sales orders"""
        for order in self:
            if order.internal_transfer_id:
                existing_orders = self.search([
                    ('id', '!=', order.id),
                    ('internal_transfer_id', '=', order.internal_transfer_id.id),
                    ('state', 'not in', ['cancel'])
                ])
                if existing_orders:
                    raise ValidationError(_(
                        'The internal transfer "%s" is already referenced in another sales order (%s). '
                        'Each internal transfer can only be linked to one sales order.'
                    ) % (order.internal_transfer_id.name, existing_orders[0].name))

    def action_confirm(self):
        """Override to validate internal transfer before confirmation"""
        for order in self:
            if order.internal_transfer_id:
                # Check if internal transfer is still in done state
                if order.internal_transfer_id.state != 'done':
                    raise UserError(_(
                        'Cannot confirm sales order. The internal transfer "%s" is not in Done state.'
                    ) % order.internal_transfer_id.name)
                
                # Check if internal transfer has moves
                if not order.internal_transfer_id.move_ids:
                    raise UserError(_(
                        'Cannot confirm sales order. The internal transfer "%s" has no product moves.'
                    ) % order.internal_transfer_id.name)
        
        return super().action_confirm()

    def write(self, vals):
        """Prevent changing internal transfer if order is confirmed"""
        if 'internal_transfer_id' in vals and vals.get('internal_transfer_id'):
            for order in self:
                if order.state in ['sale', 'done']:
                    raise UserError(_(
                        'Cannot change the internal transfer once the sales order is confirmed.'
                    ))
        return super().write(vals)
