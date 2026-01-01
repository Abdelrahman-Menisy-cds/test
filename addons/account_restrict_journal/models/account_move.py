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
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    """Inherited model for checking the journal type in account.move."""
    _inherit = 'account.move'

    check_journal = fields.Boolean(string="Check Journal",
                                   help="Compute field for check the current "
                                        "record's journal type ",
                                   compute="_compute_journal")

    def _compute_journal(self):
        """Compute field for showing validation error for non-allowed journal's
        records"""
        self.check_journal = True
        allowed_journal_ids = self.env.user.journal_ids.ids
        # If no allowed journals configured, allow all
        if not allowed_journal_ids:
            return
        for rec in self.line_ids:
            if rec.full_reconcile_id:
                payment = self.env['account.payment.register'].search(
                    [('id', '=', rec.full_reconcile_id.id)])
                if payment.journal_id.id and payment.journal_id.id not in allowed_journal_ids:
                    raise ValidationError(_('You are not allowed to access this journal.'))
        if self.journal_id.id and self.journal_id.id not in allowed_journal_ids:
            raise ValidationError(_('You are not allowed to access this journal.'))

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Function for hiding non-allowed journals from account.move."""
        super()._onchange_partner_id()
        allowed_journal_ids = self.env.user.journal_ids.ids
        # If allowed journals configured and current journal not in allowed list, clear it
        if allowed_journal_ids and self.journal_id.id and self.journal_id.id not in allowed_journal_ids:
            self.journal_id = False

    @api.model
    def am_cds_action_move_journal_line(self):
        """Override Journal Entries action to add allowed journals domain."""
        action = self.env['ir.actions.act_window']._for_xml_id('account.action_move_journal_line')
        allowed_journal_ids = self.env.user.journal_ids.ids
        if allowed_journal_ids:
            action['domain'] = [('journal_id', 'in', allowed_journal_ids)]
        return action
