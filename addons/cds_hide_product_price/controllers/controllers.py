# -*- coding: utf-8 -*-

##############################################################################
#
#
#    Copyright (C) 2019-TODAY .
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################


from odoo.addons.web.controllers.export import CSVExport, ExportFormat,ExcelExport, http

import json
from odoo.exceptions import ValidationError


class CdsPriceExcelExport(ExcelExport):

    @http.route('/web/export/xlsx', type='http', auth="user")
    def web_export_xlsx(self, data):
        params = json.loads(data)
        request = http.request
        if params.get('model') and params.get('model') in ['product.product',
                                                           'product.template']:
            fields = params.get('fields')
            field_names = [f['name'] for f in fields]
            if 'list_price' in field_names or 'lst_price' in field_names or 'price' in field_names:
                if not request.env.user.has_group(
                        'cds_hide_product_price.group_show_product_product_price'):
                    raise ValidationError(
                        'You are not allowed to export product prices')

        return super(CdsPriceExcelExport, self).web_export_xlsx(data=data)


class CdsPriceCSVExport(CSVExport):

    @http.route('/web/export/csv', type='http', auth="user")
    def web_export_csv(self, data):
        params = json.loads(data)
        request = http.request
        if params.get('model') and params.get('model') in ['product.product',
                                                           'product.template']:
            fields = params.get('fields')
            field_names = [f['name'] for f in fields]
            if 'list_price' in field_names or 'lst_price' in field_names or 'price' in field_names:
                if not request.env.user.has_group(
                        'cds_hide_product_price.group_show_product_product_price'):
                    raise ValidationError(
                        'You are not allowed to export product prices')

        return super(CdsPriceCSVExport, self).web_export_csv(data=data)
