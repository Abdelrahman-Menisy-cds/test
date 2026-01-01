# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CODOOS SRL. (http://codoos.com)
#    Maintainer: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date
from odoo.models import BaseModel


"""
inherit BaseModel to change the read_group method to use en_US context
"""

class Base(models.AbstractModel):
    _inherit = 'base'

    # @api.model
    # def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    #     return super(CDSBaseModel).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

    # @api.model
    # def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, count_limit=None):
    #     return super(Base, self).web_search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order, count_limit=count_limit)
    #
    #
    #
    #
    #
