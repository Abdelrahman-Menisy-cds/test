# -*- coding: utf-8 -*-
# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cds_internal_transfer_id = fields.Many2one(
        'stock.picking', 
        string='Internal Transfer',
        domain="[('picking_type_code', '=', 'internal'), ('state', '=', 'done')]",
        help='Select an Internal Transfer in Done status to automatically add its products to this Sales Order'
    )

    @api.onchange('cds_internal_transfer_id')
    def _onchange_internal_transfer(self):
        """When internal transfer changes, add its products to order lines"""
        if self.cds_internal_transfer_id:
            # Check if this internal transfer is already linked to another sale order
            existing_order = self.search([
                ('cds_internal_transfer_id', '=', self.cds_internal_transfer_id.id),
                ('id', '!=', self.id) if self.id else ('id', '!=', 0)
            ])
            if existing_order:
                raise ValidationError(_('This Internal Transfer is already linked to Sales Order %s') % existing_order.name)
            
            # Clear existing order lines
            self.order_line = [(5, 0, 0)]
            
            # Add products from internal transfer
            for move in self.cds_internal_transfer_id.move_ids:
                if move.product_id and move.product_qty > 0:
                    self.order_line = [(0, 0, {
                        'product_id': move.product_id.id,
                        'product_uom_qty': move.product_qty,
                        'product_uom': move.product_uom.id,
                        'name': move.product_id.name,
                        'price_unit': move.product_id.list_price or 0.0,
                    })]

    @api.constrains('cds_internal_transfer_id')
    def _check_internal_transfer_uniqueness(self):
        """Ensure internal transfer is not linked to multiple sale orders"""
        for order in self:
            if order.cds_internal_transfer_id:
                existing_order = self.search([
                    ('cds_internal_transfer_id', '=', order.cds_internal_transfer_id.id),
                    ('id', '!=', order.id)
                ])
                if existing_order:
                    raise ValidationError(_('This Internal Transfer is already linked to Sales Order %s') % existing_order.name)

    def write(self, vals):
        """Override write to handle internal transfer changes"""
        if 'cds_internal_transfer_id' in vals:
            for order in self:
                if vals.get('cds_internal_transfer_id'):
                    # Check if the new internal transfer is already used
                    existing_order = self.search([
                        ('cds_internal_transfer_id', '=', vals['cds_internal_transfer_id']),
                        ('id', '!=', order.id)
                    ])
                    if existing_order:
                        raise ValidationError(_('This Internal Transfer is already linked to Sales Order %s') % existing_order.name)
        return super(SaleOrder, self).write(vals)
