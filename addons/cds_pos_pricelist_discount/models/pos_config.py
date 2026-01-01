# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)

# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies

# of the Software or modified copies of the Software.

# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    discount_pricelist_id = fields.Many2one('product.pricelist', string='Discount Pricelist')

    # @api.model
    # def _load_pos_data_fields(self, config):
    #     """Add discount_pricelist_id to the fields loaded for POS."""
    #     fields = super()._load_pos_data_fields(config)
    #     fields += ['discount_pricelist_id']
    #     return fields

    def _get_available_pricelists(self):
        """Include discount pricelist in available pricelists for POS loading."""
        pricelists = super()._get_available_pricelists()
        if self.discount_pricelist_id:
            pricelists |= self.discount_pricelist_id
        return pricelists


