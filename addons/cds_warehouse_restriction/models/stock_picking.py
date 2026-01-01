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


class StockPicking(models.Model):
    _inherit = "stock.picking"

    view_picking_type_id = fields.Many2one(related='picking_type_id')
    view_location_dest_id = fields.Many2one(related='location_dest_id')
    view_location_id = fields.Many2one(related='location_id')
    can_edit_src = fields.Boolean(compute='_compute_can_edit_src_dst', store=False, default=lambda self: self.get_default_edit_src())
    can_edit_dst = fields.Boolean(compute='_compute_can_edit_src_dst', store=False, default=lambda self: self.get_default_edit_dst())
    # location_id = fields.Many2one(
    #     'stock.location', domain=lambda self: [('id', 'in', self.env.user.allowed_location_ids.ids)]
    # )
    # location_dest_id = fields.Many2one(
    #     'stock.location', domain=lambda self: [('id', 'in', self.env.user.allowed_location_ids.ids)]
    # )
    def get_default_edit_src(self):
        return self.env.user.has_group(
            'cds_warehouse_restriction.group_change_picking_src_location') or self.env.user.has_group(
            'stock.group_stock_manager')
            
    def get_default_edit_dst(self):
        return self.env.user.has_group(
            'cds_warehouse_restriction.group_change_picking_dest_location') or self.env.user.has_group(
            'stock.group_stock_manager')
    def _compute_can_edit_src_dst(self):
        for rec in self:
            # Check source location edit permission
            if self.env.user.has_group(
                    'cds_warehouse_restriction.group_change_picking_src_location') or self.env.user.has_group(
                    'stock.group_stock_manager'):
                rec.can_edit_src = True
            else:
                rec.can_edit_src = False
                
            # Check destination location edit permission
            if self.env.user.has_group(
                    'cds_warehouse_restriction.group_change_picking_dest_location') or self.env.user.has_group(
                    'stock.group_stock_manager'):
                rec.can_edit_dst = True
            else:
                rec.can_edit_dst = False

    @api.model
    def action_view_picking_type(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            'cds_warehouse_restriction.cds_stock_picking_type_action')
        domain = []
        if self.env.user.has_group(
                'cds_warehouse_restriction.group_restrict_view_stock_operations'):
            domain = [('id', 'in',
                       self.env.user.allow_picking_type_ids.ids)]
            action['domain'] = domain
        action = {
            'name': _('Inventory Overview'),
            'view_mode': 'kanban,form',
            'res_model': 'stock.picking.type',
            'views': [(self.env.ref(
                "stock.stock_picking_type_kanban").id, "kanban"), (self.env.ref(
                "stock.view_picking_type_form").id, "form")],
            'type': 'ir.actions.act_window',
            'domain': domain,
        }
        return action

    def picking_type_barcode_action(self):
        domain = [('code', 'in', ('incoming', 'outgoing', 'internal'))]
        action = self.env["ir.actions.actions"]._for_xml_id('stock_barcode.stock_picking_type_action_kanban')
        if self.env.user.has_group(
                'cds_warehouse_restriction.group_restrict_view_stock_operations'):
            domain += [('id', 'in',
                        self.env.user.allow_picking_type_ids.ids)]
        action['domain'] = domain

        # action = {
        #     'name': _('Operations'),
        #     'view_mode': 'kanban,form',
        #     'res_model': 'stock.picking.type',
        #     'views': [(self.env.ref(
        #         "stock.stock_picking_type_kanban").id, "kanban"), (self.env.ref(
        #         "stock.view_picking_type_form").id, "form")],
        #     'type': 'ir.actions.act_window',
        #     'context': {
        #         'form_view_initial_mode': 'edit',
        #         'force_detailed_view': True,
        #     },
        #     'domain': domain,
        # }
        return action

    def button_validate(self):
        for picking in self:

            if picking.picking_type_code == 'internal' and self.env.user.id == picking.create_uid.id:
                if self.env.user.has_group('stock.group_stock_user') and not self.env.user.has_group('cds_warehouse_restriction.group_allow_validate_own_transfers') \
                    and not picking.picking_type_id.can_validate_own_transfers:
                    raise UserError(_(f"You can not Validate your own transfers"))

            if self.env.user.has_group('cds_warehouse_restriction.group_restrict_stock_locations'):
                if picking.location_id not in self.env.user.allowed_location_ids:
                    raise UserError(
                        _(f"You are not allowed to Validate Picking With Source Location : {picking.location_id.complete_name}"))
                if picking.location_dest_id not in self.env.user.allowed_location_ids:
                    raise UserError(
                        _(f"You are not allowed to Validate Picking With Destination Location : {picking.location_dest_id.complete_name}"))
            if self.env.user.has_group(
                    'cds_warehouse_restriction.group_restrict_view_stock_operations') and picking.picking_type_id.id not in self.env.user.allow_picking_type_ids.ids:
                raise UserError(
                    _(f"You are not allowed to Validate Picking With Operation Type  : {picking.picking_type_id.display_name}"))

        return super(StockPicking, self).button_validate()




    @api.model
    def action_view_user_transfers(self):
        domain = []
        if self.env.user.has_group(
                'cds_warehouse_restriction.group_restrict_view_stock_operations'):
            domain = [('picking_type_id', 'in',
                       self.env.user.allow_picking_type_ids.ids)]
        action = {
            'name': _('Transfers'),
            'view_mode': 'list,kanban,form,calendar',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'context': {'contact_display': 'partner_address',
                        'default_company_id': self.env.user.company_id.id},
            'domain': domain,
            'search_view_id': self.env.ref('stock.view_picking_internal_search').id
        }

        return action
