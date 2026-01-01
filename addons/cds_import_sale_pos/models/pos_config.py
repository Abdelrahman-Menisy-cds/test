# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
# from odoo.osv.expression import OR


class PosConfig(models.Model):
    _inherit = 'pos.config'

    sale_domain = fields.Char(string='Domain', default='[]')