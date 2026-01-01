# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (https://cdsegypt.com)
#    Maintainer: Ragab Deaf (<ragabdeaf93@outlook.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import models, fields, api, _
from odoo.tools import float_is_zero, float_compare, convert


class POSConfig(models.Model):
    _inherit = 'pos.config'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    analytic_account_id = fields.Many2one(related='pos_config_id.analytic_account_id', string='Analytic Account',
                                          readonly=False, store=True)


class POSSession(models.Model):
    _inherit = 'pos.session'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          related='config_id.analytic_account_id', store=True)

    # def _prepare_line(self, order_line):
    #     res = super(POSSession, self)._prepare_line(order_line)
    #     if self.analytic_account_id:
    #         res['analytic_distribution'] = {self.analytic_account_id.id: 100}
    #     return res

    def _get_sale_vals(self, key, sale_vals):
        res = super(POSSession, self)._get_sale_vals(key, sale_vals)
        if self.analytic_account_id:
            res['analytic_distribution'] = {self.analytic_account_id.id: 100}
        return res

    def _get_tax_vals(self, key, amount, amount_converted, base_amount_converted):
        res = super(POSSession, self)._get_tax_vals(key, amount, amount_converted, base_amount_converted)
        if self.analytic_account_id:
            res['analytic_distribution'] = {self.analytic_account_id.id: 100}
        return res

    def _get_related_account_moves(self):
        res = super(POSSession, self)._get_related_account_moves()
        if self.analytic_account_id:
            for move in res:
                for line in move.line_ids:
                    line.analytic_distribution = {
                        self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}
        return res

    def _validate_session(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        valid = super(POSSession, self)._validate_session(balancing_account, amount_to_balance, bank_payment_method_diffs)
        if valid and self.analytic_account_id:
            for move_line in self.move_id.line_ids:
                move_line.analytic_distribution = {
                    self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}
        return valid

    def _get_stock_expense_vals(self, exp_account, amount, amount_converted):
        res = super(POSSession, self)._get_stock_expense_vals(exp_account, amount, amount_converted)
        if self.analytic_account_id:
            res['analytic_distribution'] = {self.analytic_account_id.id: 100}
        return res

    def _get_stock_output_vals(self, out_account, amount, amount_converted):
        res = super(POSSession, self)._get_stock_output_vals(out_account, amount, amount_converted)
        if self.analytic_account_id:
            res['analytic_distribution'] = {self.analytic_account_id.id: 100}
        return res

    def _create_account_move(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        res = super(POSSession, self)._create_account_move(balancing_account, amount_to_balance, bank_payment_method_diffs)
        if self.analytic_account_id:

            if res["split_cash_statement_lines"] and len(res["split_cash_statement_lines"]):
                for line in res["split_cash_statement_lines"]:
                    line.analytic_distribution = {
                        self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}

            if res["combine_cash_statement_lines"] and len(res["combine_cash_statement_lines"]):
                for line in res["combine_cash_statement_lines"]:
                    line.analytic_distribution = {
                        self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}

            if res["split_cash_receivable_lines"] and len(res["split_cash_receivable_lines"]):
                for line in res["split_cash_receivable_lines"]:
                    line.analytic_distribution = {
                        self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}

            if res["combine_cash_receivable_lines"] and len(res["combine_cash_receivable_lines"]):
                for line in res["combine_cash_receivable_lines"]:
                    line.analytic_distribution = {
                        self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}

            if res["combine_invoice_receivable_lines"] and len(res["combine_invoice_receivable_lines"]):
                for payment_method, line in res["combine_invoice_receivable_lines"].items():
                    if line.analytic_distribution:
                        line.analytic_distribution = {
                            self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}
        return res

    def _get_invoice_receivable_vals(self, amount, amount_converted):
        res = super(POSSession, self)._get_invoice_receivable_vals(amount, amount_converted)
        if self.analytic_account_id:
            res['analytic_distribution'] = {self.analytic_account_id.id: 100}
        return res

    def _get_split_receivable_vals(self, payment, amount, amount_converted):
        res = super(POSSession, self)._get_split_receivable_vals(payment, amount, amount_converted)
        if self.analytic_account_id:
            res['analytic_distribution'] = {self.analytic_account_id.id: 100}
        return res

    def _get_combine_receivable_vals(self, payment_method, amount, amount_converted):
        res = super(POSSession, self)._get_combine_receivable_vals(payment_method, amount, amount_converted)
        if self.analytic_account_id:
            res['analytic_distribution'] = {self.analytic_account_id.id: 100}
        return res

    def _create_split_account_payment(self, payment, amounts):
        payment_method = payment.payment_method_id
        if not payment_method.journal_id:
            return self.env['account.move.line']
        outstanding_account = payment_method.outstanding_account_id
        accounting_partner = self.env["res.partner"]._find_accounting_partner(payment.partner_id)
        destination_account = accounting_partner.property_account_receivable_id

        if float_compare(amounts['amount'], 0, precision_rounding=self.currency_id.rounding) < 0:
            # revert the accounts because account.payment doesn't accept negative amount.
            outstanding_account, destination_account = destination_account, outstanding_account

        account_payment = self.env['account.payment'].create({
            'amount': abs(amounts['amount']),
            'partner_id': payment.partner_id.id,
            'journal_id': payment_method.journal_id.id,
            'force_outstanding_account_id': outstanding_account.id,
            'destination_account_id': destination_account.id,
            'memo': _('%s POS payment of %s in %s', payment_method.name, payment.partner_id.display_name, self.name),
            'pos_payment_method_id': payment_method.id,
            'pos_session_id': self.id,
        })
        account_payment.action_post()
        for line in account_payment.move_id.line_ids:
            if self.analytic_account_id:
                line.analytic_distribution = {self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}
        return account_payment.move_id.line_ids.filtered(lambda line: line.account_id == account_payment.destination_account_id)

    def _create_combine_account_payment(self, payment_method, amounts, diff_amount):
        outstanding_account = payment_method.outstanding_account_id
        destination_account = self._get_receivable_account(payment_method)

        account_payment = self.env['account.payment'].create({
            'amount': abs(amounts['amount']),
            'journal_id': payment_method.journal_id.id,
            'force_outstanding_account_id': outstanding_account.id,
            'destination_account_id': destination_account.id,
            'memo': _('Combine %(payment_method)s POS payments from %(session)s', payment_method=payment_method.name, session=self.name),
            'pos_payment_method_id': payment_method.id,
            'pos_session_id': self.id,
            'company_id': self.company_id.id,
        })

        if float_compare(amounts['amount'], 0, precision_rounding=self.currency_id.rounding) < 0:
            # revert the accounts because account.payment doesn't accept negative amount.
            account_payment.outstanding_account_id = account_payment.destination_account_id
            account_payment.destination_account_id = account_payment.outstanding_account_id

        account_payment.action_post()

        diff_amount_compare_to_zero = self.currency_id.compare_amounts(diff_amount, 0)
        if diff_amount_compare_to_zero != 0:
            self._apply_diff_on_account_payment_move(account_payment, payment_method, diff_amount)

        for line in account_payment.move_id.line_ids:
            if self.analytic_account_id:
                line.analytic_distribution = {self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}
        return account_payment.move_id.line_ids.filtered(lambda line: line.account_id == self._get_receivable_account(payment_method))


class POSOrder(models.Model):
    _inherit = 'pos.order'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          related='session_id.config_id.analytic_account_id', store=True)

    def _prepare_invoice_lines(self):
        res = super(POSOrder, self)._prepare_invoice_lines()
        if self.analytic_account_id:
            for line in res:
                line[2]['analytic_distribution'] = {
                    self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}
        return res

    def _process_saved_order(self, draft):
        res = super(POSOrder, self)._process_saved_order(draft)
        if self.picking_ids and len(self.picking_ids) > 0:
            if self.analytic_account_id:
                for line in self.picking_ids.move_ids.account_move_id.line_ids:
                    line.analytic_distribution = {
                        self.analytic_account_id.id: 100.0} if self.analytic_account_id else {}
        return res

    def _create_payment_moves(self, is_reverse=False):
        result = self.env['account.move']
        credit_line_ids = []
        change_payment = self.filtered(lambda p: p.is_change and p.payment_method_id.type == 'cash')
        payment_to_change = self.filtered(lambda p: not p.is_change and p.payment_method_id.type == 'cash')[:1]
        for payment in self - change_payment:
            order = payment.pos_order_id
            payment_method = payment.payment_method_id
            if payment_method.type == 'pay_later' or float_is_zero(payment.amount,
                                                                   precision_rounding=order.currency_id.rounding):
                continue
            accounting_partner = self.env["res.partner"]._find_accounting_partner(payment.partner_id)
            pos_session = order.session_id
            journal = pos_session.config_id.journal_id
            if change_payment and payment == payment_to_change:
                pos_payment_ids = payment.ids + change_payment.ids
                payment_amount = payment.amount + change_payment.amount
            else:
                pos_payment_ids = payment.ids
                payment_amount = payment.amount
            payment_move = self.env['account.move'].with_context(default_journal_id=journal.id).create({
                'journal_id': journal.id,
                'date': fields.Date.context_today(order, order.date_order),
                'ref': _('Invoice payment for %(order)s (%(account_move)s) using %(payment_method)s', order=order.name,
                         account_move=order.account_move.name, payment_method=payment_method.name),
                'pos_payment_ids': pos_payment_ids,
            })
            result |= payment_move
            payment.write({'account_move_id': payment_move.id})
            amounts = pos_session._update_amounts({'amount': 0, 'amount_converted': 0}, {'amount': payment_amount},
                                                  payment.payment_date)
            credit_line_vals = pos_session._credit_amounts({
                'account_id': accounting_partner.with_company(order.company_id).property_account_receivable_id.id,
                # The field being company dependant, we need to make sure the right value is received.
                'partner_id': accounting_partner.id,
                'move_id': payment_move.id,
            }, amounts['amount'], amounts['amount_converted'])
            is_split_transaction = payment.payment_method_id.split_transactions
            if is_split_transaction and is_reverse:
                reversed_move_receivable_account_id = accounting_partner.with_company(
                    order.company_id).property_account_receivable_id.id
            elif is_reverse:
                reversed_move_receivable_account_id = payment.payment_method_id.receivable_account_id.id or self.company_id.account_default_pos_receivable_account_id.id
            else:
                reversed_move_receivable_account_id = self.company_id.account_default_pos_receivable_account_id.id
            debit_line_vals = pos_session._debit_amounts({
                'account_id': reversed_move_receivable_account_id,
                'move_id': payment_move.id,
                'partner_id': accounting_partner.id if is_split_transaction and is_reverse else False,
            }, amounts['amount'], amounts['amount_converted'])
            lines = self.env['account.move.line'].create([credit_line_vals, debit_line_vals])
            if amounts['amount_converted'] < 0:
                credit_line_ids += lines.filtered(lambda l: l.debit).ids
            else:
                credit_line_ids += lines.filtered(lambda l: l.credit).ids
            payment_move._post()
            for line in payment_move.line_ids:
                if pos_session.analytic_account_id:
                    line.analytic_distribution = {
                        pos_session.analytic_account_id.id: 100.0} if pos_session.analytic_account_id else {}
        return result.with_context(credit_line_ids=credit_line_ids)


class POSOrderLine(models.Model):
    _inherit = 'pos.order.line'

    analytic_precision = fields.Integer(
        store=False,
        default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),
    )

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          related='order_id.analytic_account_id', store=True)
    analytic_distribution = fields.Json(string='Analytic Distribution', compute='_compute_analytic_distribution',
                                        store=True)

    @api.depends('analytic_account_id')
    def _compute_analytic_distribution(self):
        for line in self:
            line.analytic_distribution = {line.analytic_account_id.id: 100.0} if line.analytic_account_id.id else {}
