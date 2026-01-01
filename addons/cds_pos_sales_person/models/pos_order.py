# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (https://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################
# from _typeshed import Self
from odoo import fields, models, api, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # sale_person_code = fields.Char()
    sale_person_id = fields.Many2one(comodel_name="hr.employee")
    # user_id = fields.Many2one(comodel_name="res.users", string="Cashier")

    # @api.model
    # def _complete_values_from_session(self, session, values):
    #     """Override to add sale_person_id from the order data"""
    #     values = super()._complete_values_from_session(session, values)
    #     if 'sale_person_id' in values:
    #         values['sale_person_id'] = values.get('sale_person_id', False)
    #     return values

    # def _prepare_invoice_vals(self):
    #     """Override to add sale_person_id to invoice"""
    #     vals = super()._prepare_invoice_vals()
    #     if self.sale_person_id:
    #         vals['sale_person_id'] = self.sale_person_id.id
    #     return vals

    # @api.model
    # def _load_pos_data(self, data):
    #     return super()._load_pos_data(data)

    # @api.model
    # def _load_pos_data_fields(self, config_id):
    #     fields = super()._load_pos_data_fields(config_id)
    #     return fields + ['sale_person_id']

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    sale_person_id = fields.Many2one(comodel_name="hr.employee", string="Sales Person")

    @api.model
    def _load_pos_data_fields(self, config_id):
        return super()._load_pos_data_fields(config_id) + ['sale_person_id']
