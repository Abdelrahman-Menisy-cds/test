# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################
from odoo import models, fields


class PosConfig(models.Model):
    """Inherit pos configuration and add new fields."""
    _inherit = 'pos.config'

    refund_security = fields.Char(string='Refund Security')
    price_password = fields.Char(string=u"Price Password")
    discount_password = fields.Char(string="Discount Password")
    delete_password = fields.Char(string="Delete Password")
    fiscal_position_password = fields.Char(string="Fiscal Position Password")
    global_discount_password = fields.Char(string="Global Discount Password")
    delete_order_pwd = fields.Char(string="Delete Order Password")
    change_sign_pwd = fields.Char(string="Change Sign Password")
    view_orders_pwd = fields.Char(string=u"View Order Password")
    pricelist_pwd = fields.Char(string="Pricelist Password")
    change_cashier_pwd = fields.Char(string="Change Cashier Password")
