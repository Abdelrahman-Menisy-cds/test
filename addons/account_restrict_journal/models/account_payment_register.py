# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, models, Command


class AccountPaymentRegister(models.TransientModel):
    """ Adding allowed journal in functionality"""

    _inherit = 'account.payment.register'

    @api.depends('payment_type', 'company_id', 'can_edit_wizard')
    def _compute_available_journal_ids(self):
        """
        Check all available journals on register payment.
        Only includes journals allowed for the current user.
        """
        for wizard in self:
            available_journals = self.env['account.journal']
            for batch in wizard.batches:
                available_journals |= wizard._get_batch_available_journals(batch)
            # Filter to only allowed journals for current user (if configured)
            allowed_journal_ids = self.env.user.journal_ids.ids
            if allowed_journal_ids:
                available_journals = available_journals.filtered(
                    lambda j: j.id in allowed_journal_ids
                )
            wizard.available_journal_ids = [Command.set(available_journals.ids)]

    @api.model
    def _get_batch_available_journals(self, batch_result):
        """ Helper to compute the available journals based on the batch.

        :param batch_result:    A batch computed by '_compute_batches'.
        :return:                A recordset of account.journal.
        """
        payment_type = batch_result['payment_values']['payment_type']
        company = batch_result['lines'].company_id
        journals = self.env['account.journal'].search([
            *self.env['account.journal']._check_company_domain(company),
            ('type', 'in', ('bank', 'cash', 'credit')),
        ])
        # Filter to only allowed journals for current user (if configured)
        allowed_journal_ids = self.env.user.journal_ids.ids
        if allowed_journal_ids:
            journals = journals.filtered(
                lambda j: j.id in allowed_journal_ids
            )
        if payment_type == 'inbound':
            return journals.filtered('inbound_payment_method_line_ids')
        else:
            return journals.filtered('outbound_payment_method_line_ids')
