# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class ProductTemplate(models.Model):
    _inherit = "product.template"
    # template_code = fields.Char('Import Code')

    @api.depends('product_variant_ids', 'product_variant_ids.default_code')
    def _compute_default_code(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.default_code = template.product_variant_ids.default_code
        # for template in (self - unique_variants):
        #     template.default_code = False
