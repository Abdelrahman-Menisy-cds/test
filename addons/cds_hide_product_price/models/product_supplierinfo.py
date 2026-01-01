
from odoo import api, fields, models, _


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"
    def _default_user_take_group(self):
        if self.env.user.has_groups('cds_hide_product_price.group_show_product_product_price'):
            return True
        else:
            return False    
    
    is_take_group = fields.Boolean(compute='_compute_user_take_group' , default=_default_user_take_group)
    def _compute_user_take_group(self):
        if self.env.user.has_groups('cds_hide_product_price.group_show_product_product_price'):
            self.is_take_group = True
        else:
            self.is_take_group = False


    