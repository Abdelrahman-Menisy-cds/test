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


class ResUsers(models.Model):
    _inherit = "res.users"
    allow_picking_type_ids = fields.Many2many(comodel_name='stock.picking.type',
                                              string='Allow Stock Operations')
    view_picking_type_ids = fields.Many2many(comodel_name="stock.picking.type",
                                             relation="rel_stock_picking_type_rel",
                                             column1="stock_picking",
                                             column2="user_id",
                                             string="View Stock Operations", )
    allowed_warehouse_ids = fields.Many2many("stock.warehouse", string="Allowed Warehouses")
    allowed_location_ids = fields.Many2many("stock.location", string="Allowed Locations")

    allowed_route_ids = fields.Many2many(comodel_name='stock.route',
                                              string='Allow Replenishment Routes')

