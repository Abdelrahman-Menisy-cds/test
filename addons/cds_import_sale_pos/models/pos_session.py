# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        data = super()._load_pos_data_models(config_id)
        if not ('sale.order' in data):
            data += ['sale.order']
        if not ('sale.order.line' in data):
            data += ['sale.order.line']
        return data
