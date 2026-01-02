# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    internal_transfer_id = fields.Many2one(
        'stock.picking', 
        string='Internal Transfer',
        domain="[('picking_type_id.code', '=', 'internal'), ('state', '=', 'done')]",
        help='Select an Internal Transfer in Done status to auto-add its products to this Sales Order'
    )

    @api.onchange('internal_transfer_id')
    def _onchange_internal_transfer_id(self):
        """When internal transfer is selected, add its products to the order lines"""
        if self.internal_transfer_id:
            # Check if this internal transfer is already used in another sale order
            existing_so = self.search([
                ('internal_transfer_id', '=', self.internal_transfer_id.id),
                ('id', '!=', self.id if self.id else False),
                ('state', 'not in', ['cancel', 'draft'])
            ])
            if existing_so:
                raise UserError(_(
                    'This Internal Transfer is already linked to Sales Order %s. '
                    'Each Internal Transfer can only be linked to one Sales Order.'
                ) % existing_so.name)

            # Clear existing order lines
            self.order_line = False

            # Add products from internal transfer
            for move in self.internal_transfer_id.move_lines:
                if move.product_id and move.product_qty > 0:
                    # Get the sales price from product
                    price = move.product_id.lst_price
                    if self.pricelist_id:
                        price = self.pricelist_id.with_context(
                            uom=move.product_uom.id
                        ).get_product_price(
                            move.product_id, 
                            move.product_qty, 
                            self.partner_id
                        )

                    self.order_line.create({
                        'order_id': self.id,
                        'product_id': move.product_id.id,
                        'product_uom_qty': move.product_qty,
                        'product_uom': move.product_uom.id,
                        'price_unit': price,
                        'name': move.product_id.name,
                    })

    @api.constrains('internal_transfer_id')
    def _check_internal_transfer_unique(self):
        """Ensure each internal transfer is only used once"""
        for order in self:
            if order.internal_transfer_id:
                existing_so = self.search([
                    ('internal_transfer_id', '=', order.internal_transfer_id.id),
                    ('id', '!=', order.id),
                    ('state', 'not in', ['cancel'])
                ])
                if existing_so:
                    raise ValidationError(_(
                        'This Internal Transfer is already linked to Sales Order %s. '
                        'Each Internal Transfer can only be linked to one Sales Order.'
                    ) % existing_so.name)

    def action_confirm(self):
        """Override to validate internal transfer before confirming"""
        if self.internal_transfer_id:
            # Check if internal transfer is in done state
            if self.internal_transfer_id.state != 'done':
                raise UserError(_('Cannot confirm Sales Order. The selected Internal Transfer must be in Done state.'))
            
            # Check if quantities match
            for move in self.internal_transfer_id.move_lines:
                order_line = self.order_line.filtered(lambda l: l.product_id == move.product_id)
                if not order_line:
                    raise UserError(_('Product %s from Internal Transfer is missing in Sales Order lines.') % move.product_id.name)
                if order_line.product_uom_qty != move.product_qty:
                    raise UserError(_(
                        'Quantity mismatch for product %s. '
                        'Internal Transfer: %s, Sales Order: %s'
                    ) % (move.product_id.name, move.product_qty, order_line.product_uom_qty))
        
        return super().action_confirm()
