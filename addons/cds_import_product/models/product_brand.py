# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class ProductBrand(models.Model):
    _name = 'product.brand'
    _rec_name = 'name'
    _description = 'Product Brand'
    _order = 'name asc, id desc'

    name = fields.Char(string="Name",
                       required=True, )
