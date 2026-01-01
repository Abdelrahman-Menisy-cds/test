# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductPricelistItemMultiProduct(models.TransientModel):
    _name = 'product.pricelist.item.multi.product'
    _description = _('ProductPricelistItemMultiProduct')

    product_ids = fields.Many2many('product.product', string='Products')
    discount = fields.Float(string='Discount (%)', required=True)
    date_start = fields.Datetime('Start Date', help="Starting datetime for the pricelist item validation\n"
                                                "The displayed value depends on the timezone set in your preferences.")
    date_end = fields.Datetime('End Date', help="Ending datetime for the pricelist item validation\n"
                                                "The displayed value depends on the timezone set in your preferences.")

    def add(self):
        # add lines to product.pricelist.item
        active_id = self._context.get('active_id')
        pricelist_item = self.env['product.pricelist'].browse(active_id)

        if not self.product_ids:
            raise UserError(_('No products selected'))
        if self.discount <= 0:
            raise UserError(_('Discount must be greater than 0'))
        for product in self.product_ids:
            pricelist_item.write({
                'item_ids': [(0, 0, {
                    'applied_on': '0_product_variant',
                    'product_id': product.id,
                    'compute_price': 'fixed',
                    'compute_price': 'percentage',
                    'percent_price': self.discount,
                    'date_start': self.date_start,
                    'date_end': self.date_end,
                })]
            })
        print('add')