# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    refund_period = fields.Integer(string='Refund Period', default=14)
    enable_load_pos_orders_days = fields.Boolean("Enable Load Orders of Last Days", default=False)
    load_pos_orders_days = fields.Integer("Load Orders of Last Days", default=0)
    show_invoice_button = fields.Boolean(
        string='Show Invoice Button',
        default=True,
        help="If enabled, the Invoice button will be visible on the payment screen."
    )



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_refund_period = fields.Integer(string='Refund Period', related='pos_config_id.refund_period', readonly=False)
    enable_load_pos_orders_days = fields.Boolean(related='pos_config_id.enable_load_pos_orders_days',readonly=False)
    load_pos_orders_days = fields.Integer(related='pos_config_id.load_pos_orders_days',readonly=False)
    pos_show_invoice_button = fields.Boolean(
        string='Show Invoice Button',
        related='pos_config_id.show_invoice_button',
        readonly=False,
        help="If enabled, the Invoice button will be visible on the payment screen."
    )