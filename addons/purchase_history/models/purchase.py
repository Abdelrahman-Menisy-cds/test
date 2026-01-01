# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2023-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    last_price1 = fields.Float(
        'Last Purchase Price 1',
        help="Shows the last purchase price of the product for the selected supplier from the past two Purchase Orders",
        compute="_compute_last_prices",
        store=False,
    )

    last_price2 = fields.Float(
        'Last Purchase Price 2',
        help="Shows the second last purchase price of the product for the selected supplier from the past two Purchase Orders",
        compute="_compute_last_prices",
        store=False,
    )

    @api.depends('product_id')
    def _compute_last_prices(self):
        for record in self:
            record.last_price1 = 0.0
            record.last_price2 = 0.0

            if not record.product_id:
                continue

            # Fetch last 2 purchase lines ordered by ID (latest first)
            purchase_lines = self.env['purchase.order.line'].sudo().search(
                [
                    ('product_id', '=', record.product_id.id),
                    ('order_id.state', 'in', ('purchase', 'done')),('id','!=',record.id),
                ],
                order='id desc',
                limit=2,
            )

            if purchase_lines:
                record.last_price1 = purchase_lines[0].price_unit

            if len(purchase_lines) > 1:
                record.last_price2 = purchase_lines[1].price_unit
