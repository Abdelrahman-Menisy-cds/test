from odoo import _, api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    refund_sale_order_count = fields.Integer(string='Refund Sale Order Count', compute='_count_refund_sale_order_count', readonly=True)

    def _count_refund_sale_order_count(self):
        for order in self:
            order.refund_sale_order_count = len(order.lines.mapped('refund_sale_order_id'))

    def _compute_order_name(self, session=None):
        if len(self.lines.mapped('refund_sale_order_id')) != 0:
            return _('%(refunded_sale_order)s REFUND', refunded_sale_order=','.join(self.lines.mapped('refund_sale_order_id').mapped('name')))
        return super(PosOrder, self)._compute_order_name(session)

    def action_view_refund_sale_order(self):
        self.ensure_one()
        linked_orders = self.lines.mapped('refund_sale_order_id')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Linked Sale Orders'),
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', linked_orders.ids)],
        }

    def _get_fields_for_order_line(self):
        fields = super(PosOrder, self)._get_fields_for_order_line()
        fields.extend([
            'refund_sale_order_id',
            'refund_sale_order_line_id',
        ])
        return fields

    def _prepare_order_line(self, order_line):
        order_line = super()._prepare_order_line(order_line)
        if order_line.get('refund_sale_order_id'):
            order_line['refund_sale_order_id'] = {
                'id': order_line['refund_sale_order_id'][0],
                'name': order_line['refund_sale_order_id'][1],
            }
        if order_line.get('refund_sale_order_line_id'):
            order_line['refund_sale_order_line_id'] = {
                'id': order_line['refund_sale_order_line_id'][0],
            }
        return order_line

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    refund_sale_order_id = fields.Many2one('sale.order', string="Linked Sale Order")
    refund_sale_order_line_id = fields.Many2one('sale.order.line', string="Source Sale Order Line")
    refunded_sale_qty = fields.Float(string='Refunded Sale Quantity', default=0.0)

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        params += ['refund_sale_order_id', 'refund_sale_order_line_id', 'refunded_sale_qty']
        return params
