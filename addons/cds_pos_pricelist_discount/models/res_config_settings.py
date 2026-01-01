# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)

# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies

# of the Software or modified copies of the Software.

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_discount_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        related='pos_config_id.discount_pricelist_id',
        readonly=False,
    )