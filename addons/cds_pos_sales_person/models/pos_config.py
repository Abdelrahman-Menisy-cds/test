# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (https://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################
from odoo import fields, models, api, _
from odoo.fields import Domain


class PosConfig(models.Model):
    _inherit = 'pos.config'

    sale_persons_ids = fields.Many2many(
        'hr.employee',
        'check_sale_persons_rel',
        'check_sale_persons_id',
        'sale_persons_id')

    def _employee_domain(self, user_id):
        """Override to include sales persons in the loaded employees."""
        domain = super()._employee_domain(user_id)
        if self.sale_persons_ids:
            domain = Domain.OR([
                domain,
                [('id', 'in', self.sale_persons_ids.ids)]
            ])
        return domain
    
# class PosConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'

#     sale_persons_ids = fields.Many2many(
#         related='pos_config_id.sale_persons_ids',
#         readonly=False)

