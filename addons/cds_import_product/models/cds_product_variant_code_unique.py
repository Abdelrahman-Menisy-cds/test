# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)

# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies

# of the Software or modified copies of the Software.


from odoo import api, models, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('default_code', 'company_id', 'active')
    def _check_unique_variant_code(self):
        for product in self.with_context(active_test=False).filtered(lambda p: p.default_code):
            company_id = product.company_id.id
            domain = [
                ('id', '!=', product.id),
                ('default_code', '=', product.default_code),
            ]
            if company_id:
                domain.append(('company_id', 'in', (False, company_id)))
            else:
                domain.append(('company_id', '=', False))

            duplicate = self.sudo().search(domain, limit=1)
            if duplicate:
                raise ValidationError(_(
                    'Variant Code "%s" is already assigned to product "%s".'
                ) % (product.default_code, duplicate.display_name))
