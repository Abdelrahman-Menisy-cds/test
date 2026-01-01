# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """Adding a new field to res_config_settings model."""
    _inherit = 'res.config.settings'

    refund_security = fields.Char(string='Global Refund Security', related='pos_config_id.refund_security', readonly=False)
    price_password = fields.Char(string="Price Password",related='pos_config_id.price_password', readonly=False)
    discount_password = fields.Char(string="Discount Password", related='pos_config_id.discount_password', readonly=False)
    delete_password = fields.Char(string="Delete Password", related='pos_config_id.delete_password', readonly=False)
    delete_order_pwd = fields.Char(string="Delete Order Password", related='pos_config_id.delete_order_pwd', readonly=False)
    global_discount_password = fields.Char(string="Global Discount Password", related='pos_config_id.global_discount_password', readonly=False)
    change_sign_pwd = fields.Char(string="Change Sign Password", related='pos_config_id.change_sign_pwd', readonly=False)
    pricelist_pwd = fields.Char(string="Pricelist Password", related='pos_config_id.pricelist_pwd', readonly=False)
    view_orders_pwd = fields.Char(string="View Order Password", related='pos_config_id.view_orders_pwd', readonly=False)
    fiscal_position_password = fields.Char(string="Fiscal Position Password", related='pos_config_id.fiscal_position_password', readonly=False)
    change_cashier_pwd = fields.Char(string="Change Cashier Password", related='pos_config_id.change_cashier_pwd', readonly=False)

# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'

#     hr_expense_alias_domain_id = fields.Many2one('hr.expense.alias.domain', default=lambda self: self._create_default_expense_alias())
#
#     @api.model
#     def _create_default_expense_alias(self):
#         record = self.env['hr.expense.alias.domain'].search([], limit=1)
#         if not record:
#             record = self.env['hr.expense.alias.domain'].create({'name': 'Default Alias'})
#
#         return record.id
#
#     @api.depends('hr_expense_use_mailgateway')
#     def _compute_hr_expense_alias_domain_id(self):
#         hr_expense_alias_domain_id = False
#         for record in self:
#             if not record.hr_expense_use_mailgateway:
#                 hr_expense_alias_domain_id = record.hr_expense_alias_domain_id
#             record.hr_expense_alias_domain_id = hr_expense_alias_domain_id
#         # self.filtered(lambda w: not w.hr_expense_use_mailgateway).hr_expense_alias_domain_id = False
#
# class HrExpenseAliasDomain(models.Model):
#     _name = 'hr.expense.alias.domain'
#     _description = 'Expense Alias Domain'
#
#     name = fields.Char('Name')
