# -*- coding: utf-8 -*-


from odoo import api, fields, models, _


class ProductYear(models.Model):
    _name = "product.year"
    _description = "Product Year"

    name = fields.Char('Year', required=True)

