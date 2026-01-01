# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)

# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies

# of the Software or modified copies of the Software.

from odoo import api, models


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.model
    def _load_pos_data_fields(self, config):
        """Add applied_on field to the fields loaded for POS."""
        fields = super()._load_pos_data_fields(config)
        if 'applied_on' not in fields:
            fields.append('applied_on')
        return fields
