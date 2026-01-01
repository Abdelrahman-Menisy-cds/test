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
from odoo import api, fields, models


class ResUsers(models.Model):
    """ Adding journal fields where we can select allowed journal """

    _inherit = 'res.users'

    check_user = fields.Boolean(string="Check", compute='_compute_check_user',
                                help="Check the field is true or false")
    journal_ids = fields.Many2many(
        'account.journal', 'account_restrict_journal_journal_ids_rel',
        string='Allowed Journals',
        help='Only the selected journals will be accessible'
             ' to this user. Leave empty to allow all journals.')

    @api.depends('group_ids')
    def _compute_check_user(self):
        """Function for viewing the page for restrict journal users."""
        group = self.env.ref('account_restrict_journal.user_allowed_journal', raise_if_not_found=False)
        for user in self:
            user.check_user = bool(group and group in user.group_ids)
