# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CODOOS SRL. (http://codoos.com)
#    Maintainer: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class SaleOrder(models.Model):
    _inherit = "sale.order"
    is_take_group = fields.Boolean(compute='_compute_user_take_group')
    def _compute_user_take_group(self):
        if self.env.user.has_groups('cds_hide_product_price.group_show_product_product_price'):
            self.is_take_group = True
        else:
            self.is_take_group = False

