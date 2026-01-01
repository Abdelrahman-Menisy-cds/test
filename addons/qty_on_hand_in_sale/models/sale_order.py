""" Initialize Sale Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
import itertools


class SaleOrderLine(models.Model):
    """
        Inherit Sale Order Line:
         -
    """
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty', 'route_id')
    def _onchange_route_id(self):
        """ route_id """
        for rec in self:
            if rec.order_id.warehouse_id:
                str1 = ''
                if rec.product_id:
                    quants = self.env['stock.quant'].search([
                        ('location_id', 'in', rec.order_id.warehouse_id.view_location_id.child_ids.ids),
                        ('product_id', '=', rec.product_id.id),
                        ('on_hand', '=', True)])
                    availble_quantity = sum(quants.mapped('available_quantity'))
                    if availble_quantity >= rec.product_uom_qty:
                        pass
                    else:
                        quants = self.env['stock.quant'].search([
                            ('product_id', '=', rec.product_id.id),
                            ('on_hand', '=', True)])

                        # Get full location paths
                        final_locations = []
                        for quant in quants:
                            # Get complete location path from root to current location
                            location_path = quant.location_id.complete_name
                            final_locations.append(location_path)

                        availble_quantity = quants.mapped('available_quantity')
                        qty = sum(quants.mapped('available_quantity'))
                        if qty <= 0:
                            return {
                                'warning': {
                                    'title': _("Warning !"),
                                    'message': _(str1)
                                }
                            }

                        else:
                            coombine_list = []
                            for i, (a, b) in enumerate(zip(final_locations, availble_quantity)):
                                coombine_list.append(a + ' : ')
                                coombine_list.append(str(b))
                            final_list = [i + j for i, j in zip(coombine_list[::2], coombine_list[1::2])]
                            str1 = '\n'.join(str(e) for e in final_list)

                            return {
                                'warning': {
                                    'title': _("Warning !"),
                                    'message': _(str1)
                                }
                            }

