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




class Product(models.Model):
    _inherit = "product.product"

    def _get_description(self, picking_type_id):
        picking_type_id = self.env['stock.picking.type'].sudo().browse(
            picking_type_id.id)
        return super(Product, self)._get_description(
            picking_type_id=picking_type_id)




