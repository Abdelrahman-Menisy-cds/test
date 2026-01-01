# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (C) 2020.
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#    website': https://www.linkedin.com/in/ramadan-khalil-a7088164
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

# from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # @api.model
    # def _default_picking_type(self):
    #     return self._get_picking_type(
    #         self.env.context.get('company_id') or self.env.company.id)
    #
    # def _get_picking_type_domain(self):
    #     domain = [('code','=','incoming'),'|', ('warehouse_id', '=', False),
    #               ('warehouse_id.company_id', '=', self.env.company.id)]
    #     # if self.env.user.has_group(
    #     #         'cds_warehouse_restriction.group_restrict_view_stock_operations'):
    #     #     domain = [('id', 'in', self.env.user.allow_picking_type_ids.ids),('code','=','incoming'), '|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', self.env.company.id)]
    #     return domain
    #
    create_user = fields.Many2one(comodel_name="res.users", string="Responsible",
                                 required=False, default=lambda self: self._uid)

    def _default_allowed_picking_type(self):
        allowed_picking_type_ids = self.env.user.allow_picking_type_ids.filtered(lambda x: x.code == 'incoming' and x.warehouse_id.company_id.id in self.env.companies.ids)
        if len(allowed_picking_type_ids) <= 0:
                allowed_picking_type_ids = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('warehouse_id.company_id', 'in', self.env.companies.ids)])
        return allowed_picking_type_ids


    allowed_picking_type_ids = fields.Many2many('stock.picking.type', 'purchase_order_picking_type_rel',
                                                compute='_compute_allowed_picking_type_ids', default=_default_allowed_picking_type,compute_sudo=True)


    def _compute_allowed_picking_type_ids(self):
        for rec in self.sudo():
            rec.allowed_picking_type_ids = self.env.user.allow_picking_type_ids
            if len(rec.allowed_picking_type_ids) <= 0:
                rec.allowed_picking_type_ids = self.env['stock.picking.type'].search([])

    @api.model
    def _get_picking_type(self, company_id):
        allowed_picking_type_ids = self.env.user.allow_picking_type_ids
        if len(allowed_picking_type_ids) <= 0:
                allowed_picking_type_ids = self.env['stock.picking.type'].search([])
        picking_type = self.env['stock.picking.type'].search([('id', 'in', allowed_picking_type_ids.ids), ('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([('id', 'in', allowed_picking_type_ids.ids), ('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return picking_type[:1]
    #
    #
    #
    # picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To',
    #                                   states=Purchase.READONLY_STATES,
    #                                   required=True,
    #                                   default=_default_picking_type,
    #                                   domain=_get_picking_type_domain,
    #                                   help="This will determine operation type of incoming shipment")

    # @api.onchange('create_user')
    # def onchange_create_uid(self):
    #     if self.env.user.has_group(
    #             'cds_warehouse_restriction.group_restrict_view_stock_operations'):
    #         domain = [('code','=','incoming'),('id', 'in', self.env.user.allow_picking_type_ids.ids),
    #                   '|', ('warehouse_id', '=', False),
    #                   ('warehouse_id.company_id', '=', self.env.company.id)]
    #         self.picking_type_id = False
    #         return {
    #             'domain': {
    #                 'picking_type_id': domain,
    #
    #             }
    #         }

