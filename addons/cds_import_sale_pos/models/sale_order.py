from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'pos.load.mixin']
    
    refund_pos_order_line_ids = fields.One2many('pos.order.line', 'refund_sale_order_id', string="Order lines Transfered to Point of Sale", readonly=True)
    refund_pos_order_count = fields.Integer(string='Pos Order Count', compute='_count_refund_pos_order', readonly=True)

    def _count_refund_pos_order(self):
        for order in self:
            linked_orders = order.refund_pos_order_line_ids.mapped('order_id')
            order.refund_pos_order_count = len(linked_orders)

    def action_view_refund_pos_order(self):
        self.ensure_one()
        linked_orders = self.refund_pos_order_line_ids.mapped('order_id')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Linked POS Orders'),
            'res_model': 'pos.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', linked_orders.ids)],
        }




class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = ['sale.order.line', 'pos.load.mixin']

    pos_refund_line_ids = fields.One2many(
        'pos.order.line', 
        'refund_sale_order_line_id', 
        string='POS Refund Lines',
        help='POS order lines that refund this sale order line.'
    )
    
    pos_refunded_qty = fields.Float(
        string='POS Refunded Quantity',
        compute='_compute_pos_refunded_qty',
        store=True,
        digits='Product Unit of Measure',
        help='Total quantity refunded through POS orders for this sale order line.'
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append('pos_refunded_qty')
        return fields

    @api.depends('pos_refund_line_ids', 'pos_refund_line_ids.qty')
    def _compute_pos_refunded_qty(self):
        """
        Compute the total refunded quantity from POS order lines
        that reference this sale order line.
        """
        for line in self:
            # Sum the absolute quantities (POS refunds are typically negative)
            line.pos_refunded_qty = sum(abs(pos_line.qty) for pos_line in line.pos_refund_line_ids)


    def _get_refund_sale_order_fields(self):
        field_names = super()._get_sale_order_fields()
        field_names.append('pos_refunded_qty')
        return field_names

    def read_refund_converted(self):
        field_names = self._get_refund_sale_order_fields()
        results = []
        for sale_line in self:
            if sale_line.product_type:
                product_uom = sale_line.product_id.uom_id
                sale_line_uom = sale_line.product_id.uom_id
                item = sale_line.read(field_names, load=False)[0]
                if sale_line.product_id.tracking != 'none':
                    item['lot_names'] = sale_line.move_ids.move_line_ids.lot_id.mapped('name')
                    item['lot_qty_by_name'] = {line.lot_id.name: line.quantity for line in sale_line.move_ids.move_line_ids}
                if product_uom == sale_line_uom:
                    results.append(item)
                    continue
                item['product_uom_qty'] = self._convert_qty(sale_line, item['product_uom_qty'], 's2p')
                item['qty_delivered'] = self._convert_qty(sale_line, item['qty_delivered'], 's2p')
                item['qty_invoiced'] = self._convert_qty(sale_line, item['qty_invoiced'], 's2p')
                item['qty_to_invoice'] = self._convert_qty(sale_line, item['qty_to_invoice'], 's2p')
                item['pos_refunded_qty'] = self._convert_qty(sale_line, item['pos_refunded_qty'], 's2p')
                item['price_unit'] = sale_line_uom._compute_price(item['price_unit'], product_uom)
                results.append(item)

            elif sale_line.display_type == 'line_note':
                if results:
                    if results[-1].get('customer_note'):
                        results[-1]['customer_note'] += "--" + sale_line.name
                    else:
                        results[-1]['customer_note'] = sale_line.name


        return results