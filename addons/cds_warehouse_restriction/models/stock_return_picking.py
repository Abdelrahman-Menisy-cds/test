# -*- coding: utf-8 -*-

#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_return(self):
        """Override to add validation for return quantities on sales orders."""
        # Check if the picking is related to a sales order
        picking = self.picking_id
        if picking.picking_type_code == 'outgoing' and picking.sale_id:
            self._validate_sale_return_quantities()
        
        return super(StockReturnPicking, self)._create_return()
    
    def _validate_sale_return_quantities(self):
        """Validate that return quantities do not exceed delivered quantities for sales orders."""
        picking = self.picking_id
        
        # Dictionary to track total returned quantities per sale line
        returned_qty_per_sale_line = {}
        
        # Get all previous returns for this picking
        previous_returns = self.env['stock.picking'].search([
            ('return_id', '=', picking.id),
            ('state', 'not in', ['draft', 'cancel'])
        ])
        
        # Calculate already returned quantities per sale line
        for return_pick in previous_returns:
            for move in return_pick.move_ids:
                if move.sale_line_id and move.state not in ['cancel', 'draft']:
                    sale_line_id = move.sale_line_id.id
                    if sale_line_id not in returned_qty_per_sale_line:
                        returned_qty_per_sale_line[sale_line_id] = 0.0
                    returned_qty_per_sale_line[sale_line_id] += move.product_uom_qty
        
        # Check if current return quantities would exceed delivered quantities
        for return_line in self.product_return_moves:
            move = return_line.move_id
            if not move.sale_line_id:
                continue

            sale_line = move.sale_line_id
            sale_line_id = sale_line.id
            
            # Get delivered quantity for this sale line
            delivered_qty = move.quantity
            
            # Get previously returned quantity
            previously_returned_qty = returned_qty_per_sale_line.get(sale_line_id, 0.0)
            
            # Current return quantity
            current_return_qty = return_line.quantity
            
            # Total return quantity (previous + current)
            total_return_qty = previously_returned_qty + current_return_qty
            
            # Compare with delivered quantity
            if float_compare(total_return_qty, delivered_qty, precision_rounding=move.product_uom.rounding) > 0:
                raise ValidationError(_(
                    "You cannot return more than the delivered quantity for product '%(product)s' in sale order '%(order)s'.\n"
                    "Delivered: %(delivered)s, Previously returned: %(prev_returned)s, Current return: %(current)s"
                ) % {
                    'product': move.product_id.display_name,
                    'order': sale_line.order_id.name,
                    'delivered': delivered_qty,
                    'prev_returned': previously_returned_qty,
                    'current': current_return_qty,
                })
