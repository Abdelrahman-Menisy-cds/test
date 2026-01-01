# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'
    product_season_id = fields.Many2one(comodel_name="product.season", string="Product Season", required=False )
    product_year_id = fields.Many2one(comodel_name="product.year", string="Product Year", required=False, help="The year associated with this product.")

