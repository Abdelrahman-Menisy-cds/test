# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)

# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies

# of the Software or modified copies of the Software.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    internal_transfer_id = fields.Many2one(
        'stock.picking',
        string='Internal Transfer',
        domain="[('state', '=', 'done'), ('picking_type_id.code', '=', 'internal')]",
        help='Select an Internal Transfer in Done status to auto-add its products to this Sales Order',
        copy=False,
        tracking=True
    )

    @api.onchange('internal_transfer_id')
    def _onchange_internal_transfer_id(self):
        """When internal transfer is selected, add its products to the order lines"""
        if self.internal_transfer_id and self.state in ['draft', 'sent']:
            self._add_internal_transfer_products()

    def _add_internal_transfer_products(self):
        """Add products from internal transfer to sales order lines"""
        if not self.internal_transfer_id:
            return

        # Clear existing order lines if any
        self.order_line = [(5, 0, 0)]

        # Add products from internal transfer
        for move in self.internal_transfer_id.move_ids_without_package:
            if move.state == 'done' and move.product_qty > 0:
                self.order_line = [(0, 0, {
                    'product_id': move.product_id.id,
                    'product_uom_qty': move.product_qty,
                    'product_uom': move.product_uom.id,
                    'price_unit': move.product_id.list_price or 0.0,
                    'name': move.product_id.display_name,
                    'tax_id': [(6, 0, move.product_id.taxes_id.ids)],
                })]

    @api.constrains('internal_transfer_id')
    def _check_internal_transfer_unique(self):
        """Prevent using the same internal transfer in multiple sales orders"""
        for order in self:
            if order.internal_transfer_id:
                existing_orders = self.search([
                    ('id', '!=', order.id),
                    ('internal_transfer_id', '=', order.internal_transfer_id.id),
                    ('state', 'not in', ['cancel'])
                ])
                if existing_orders:
                    raise ValidationError(_(
                        'This Internal Transfer is already linked to Sales Order %s. '
                        'You cannot use the same Internal Transfer in multiple Sales Orders.'
                    ) % existing_orders[0].name)

    def action_confirm(self):
        """Override to validate internal transfer before confirmation"""
        for order in self:
            if order.internal_transfer_id:
                # Check if internal transfer is still in done state
                if order.internal_transfer_id.state != 'done':
                    raise ValidationError(_(
                        'The Internal Transfer %s is not in Done state. '
                        'Please select a valid Internal Transfer.'
                    ) % order.internal_transfer_id.name)
                
                # Check if products are still available
                for move in order.internal_transfer_id.move_ids_without_package:
                    if move.state != 'done' or move.product_qty <= 0:
                        raise ValidationError(_(
                            'Some products in Internal Transfer %s are not valid. '
                            'Please check the transfer details.'
                        ) % order.internal_transfer_id.name)

        return super().action_confirm()

    def write(self, vals):
        """Prevent changing internal transfer if order is confirmed"""
        if 'internal_transfer_id' in vals and self.state in ['sale', 'done']:
            old_transfer = self.internal_transfer_id
            new_transfer = self.env['stock.picking'].browse(vals['internal_transfer_id']) if vals['internal_transfer_id'] else False
            
            if old_transfer != new_transfer:
                raise ValidationError(_(
                    'You cannot change the Internal Transfer once the Sales Order is confirmed.'
                ))
        
        return super().write(vals)
