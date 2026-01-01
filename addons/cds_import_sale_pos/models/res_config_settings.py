# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_sale_domain = fields.Char(related='pos_config_id.sale_domain', readonly=False)