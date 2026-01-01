# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

from odoo import fields, models, api, _


import logging

LOGGER = logging.getLogger(__name__)
class ProductSeason(models.Model):
    _name = 'product.season'
    _rec_name = 'name'
    _description = 'Product Season'

    name = fields.Char(string="Name", required=True, )
