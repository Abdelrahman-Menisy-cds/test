# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CODOOS SRL. (http://codoos.com)
#    Maintainer: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from io import BytesIO
from odoo.exceptions import ValidationError, UserError
from openpyxl import load_workbook

from datetime import datetime, date
from xlrd import open_workbook, xldate_as_tuple
import base64
import ast

import logging

_logger = logging.getLogger('CDS IMPORT PRODUCTS >>>')
from pprint import pformat


def stringfy_value(value):
    value_str = value
    if isinstance(value, float):
        value_str = str(int(value)).strip()
    elif isinstance(value, int):
        value_str = str(value).strip()
    elif isinstance(value, str):
        value_str = value.strip()
    return value_str

def get_cell(sheet, row, col):
    return sheet.cell(row=row, column=col).value

class ActionProductImport(models.TransientModel):
    _name = 'action.product.import'
    _description = 'Import product'

    file = fields.Binary('Import File', required=True)
    file_name = fields.Char('File Name')
    update_exist = fields.Boolean('Update Existed Products')
    create_purchase = fields.Boolean('Create Purchase')
    partner_id = fields.Many2one('res.partner', 'Vendor')

    # import_type =fields.Selection([('new','Only Create New products'),
    #                                ('update','Create New Products And Update Existed'),
    #                                ('purchase_new','Only Create New Products')])

    def action_import_purchase(self):
        # Decode the base64 file content and load the workbook using openpyxl
        file_content = base64.b64decode(self.file)
        wb = load_workbook(filename=BytesIO(file_content))
        sheet = wb.active  # Get the first sheet

        product_ids = self.env['product.product']
        purchase_lines = []
        missing_products = []

        for row in range(2, sheet.max_row + 1):  # Start from row 2 to skip the header
            sku = str(get_cell(sheet, row, 4)).strip()  # SKU is in column 4 (D)

            if not sku:
                continue

            product_id = self.env['product.product'].search(
                [('default_code', '=', sku)], limit=1
            )

            if sku and product_id:
                qty = float(get_cell(sheet, row, 13) or 0)  # Quantity in column 13 (M)
                # po_price = float(sheet.cell(row=row, column=15).value)
                # po_price =  float(get_cell(sheet, row, 15) or 0) if sheet.max_column >= 15 else False

                purchase_lines.append((0, 0, {
                    'name': product_id.name,
                    'product_id': product_id.id,
                    'product_qty': qty,
                    'product_uom': product_id.uom_po_id.id,
                    'price_unit': product_id.standard_price,
                    'date_planned': fields.Datetime.now(),
                    # 'po_price': po_price,
                }))

                _logger.info('Existed barcodes is : %s' % product_id.mapped('display_name'))
            else:
                missing_products.append((row, sku))  # Append missing product details with row number

        # Raise validation error for missing products
        if missing_products:
            products_str = ['Row:{}     SKU: {}'.format(l[0], l[1]) for l in missing_products]
            raise ValidationError(_(
                'Please Check the following Rows for missing products: \n{}'.format('\n'.join(products_str))
            ))

        # Create purchase order if there are purchase lines
        if purchase_lines:
            purchase_order = self.env['purchase.order'].create({
                'partner_id': self.partner_id.id,
                'order_line': purchase_lines
            })

            action = self.env["ir.actions.actions"]._for_xml_id(
                'purchase.purchase_rfq'
            )
            action['views'] = [
                (self.env.ref('purchase.purchase_order_form').id, 'form')
            ]
            action['res_id'] = purchase_order.id
            return action

    def action_import(self):
        file_content = base64.b64decode(self.file)
        wb = load_workbook(filename=BytesIO(file_content), data_only=True)
        sheet = wb.active  # First sheet

        attr_obj = self.env['product.attribute']
        value_obj = self.env['product.attribute.value']
        categ_obj = self.env['product.category']
        pos_categ_obj = self.env['pos.category']

        color_attr = attr_obj.search([('name', 'in', ['color', 'Color'])], limit=1)
        if not color_attr:
            color_attr = attr_obj.create({'name': 'color'})

        size_attr = attr_obj.search([('name', 'in', ['size', 'Size'])], limit=1)
        if not size_attr:
            size_attr = attr_obj.create({'name': 'size'})

        product_temps = {}
        product_template_obj = self.env['product.template']
        purchase_products = []

        def get_cell(sheet, row, col):
            return sheet.cell(row=row, column=col).value

        def stringfy_value(val):
            return str(val).strip() if val not in (None, "") else ""

        for row in range(2, sheet.max_row + 1):  # Skip header row
            templ_code = get_cell(sheet, row, 1)
            templ_name = stringfy_value(get_cell(sheet, row, 2))
            category_code = stringfy_value(get_cell(sheet, row, 9))

            if not templ_code:
                raise ValidationError(_('Please set template code on row : %s' % row))
            if not templ_name:
                raise ValidationError(_('Please set template name on row : %s' % row))
            if not category_code:
                raise ValidationError(_('Please set product category code on row : %s' % row))

            pr_templ = str(int(templ_code)).strip() if isinstance(templ_code, float) else str(templ_code).strip()

            categ_id = categ_obj.search([('code', '=', category_code), ('code', '!=', False)], limit=1) or categ_obj.search(
                [('name', '=', category_code)], limit=1)
            if not categ_id:
                raise ValidationError(_('product category code: %s in row %s does not exist' % (category_code, row)))

            color_code = stringfy_value(get_cell(sheet, row, 5))
            c_val_id = False
            if color_code:
                c_val_id = value_obj.search([('code', '=', color_code), ('attribute_id', '=', color_attr.id)], limit=1)
                if not c_val_id:
                    raise ValidationError(_('Color Code:%s in row %s does not exist' % (color_code, row)))

            size_code = stringfy_value(get_cell(sheet, row, 6))
            s_val_id = False
            if size_code:
                s_val_id = value_obj.search([('code', '=', size_code), ('attribute_id', '=', size_attr.id)], limit=1)
                if not s_val_id:
                    raise ValidationError(_('Size Code:%s in row %s does not exist' % (size_code, row)))

            pos_category = []
            pos_categ = stringfy_value(get_cell(sheet, row, 12))
            if pos_categ:
                pos_categ_id = pos_categ_obj.search([('name', '=', pos_categ)], limit=1) or pos_categ_obj.search(
                    [('code', '=', pos_categ), ('code', '!=', False)], limit=1)
                if pos_categ_id:
                    pos_category = pos_categ_id.ids

            qty = float(get_cell(sheet, row, 13) or 0)
            barcode = stringfy_value(get_cell(sheet, row, 3))
            exist_barcode_products = self.env['product.product'].search([('barcode', '=', barcode)])
            if exist_barcode_products:
                _logger.info('Existed barcodes: %s' % exist_barcode_products.mapped('display_name'))

            price = float(get_cell(sheet, row, 7) or 0)
            cost = float(get_cell(sheet, row, 8) or 0)
            po_price = float(get_cell(sheet, row, 14) or 0) if sheet.max_column >= 14 else False
            # Get seller_ids data from column 15 if available
            seller_data = stringfy_value(get_cell(sheet, row, 15)) if sheet.max_column >= 15 else False
            
            #saerch for the seller data
            seller_id = None
            if seller_data:
                seller_id = self.env['res.partner'].search([('name', '=', seller_data)],limit=1)
                if seller_id:
                    seller_id = seller_id.id

            variant_data = {
                'row': row,
                'name': templ_name,
                'barcode': barcode,
                'code': stringfy_value(get_cell(sheet, row, 4)),
                'color': c_val_id.id if c_val_id else False,
                'size': s_val_id.id if s_val_id else False,
                'price': price,
                'cost': cost,
                'cat': categ_id.id,
                'available_in_pos': bool(get_cell(sheet, row, 11)),
                'pos_cat': pos_category,
                'qty': qty,
                'po_price': po_price,
                'seller_id': seller_id,
            }

            if sheet.max_column > 15:
                extra_variant_data = self.update_extra_fields(sheet, row)
                variant_data.update({'extra_data': extra_variant_data})

            product_temps.setdefault(pr_templ, []).append(variant_data)

        for prt, variants in product_temps.items():
            color_vals = list({v['color'] for v in variants if v['color']})
            size_vals = list({v['size'] for v in variants if v['size']})

            product_template_id = product_template_obj.search([('default_code', '=', prt)], limit=1)

            if product_template_id:
                if not self.update_exist:
                    continue

                color_att_line = product_template_id.attribute_line_ids.filtered(lambda l: l.attribute_id == color_attr)
                size_att_line = product_template_id.attribute_line_ids.filtered(lambda l: l.attribute_id == size_attr)

                if color_att_line and color_vals:
                    color_att_line.write({'value_ids': [(6, 0, list(set(color_att_line.value_ids.ids + color_vals)))]})
                if size_att_line and size_vals:
                    size_att_line.write({'value_ids': [(6, 0, list(set(size_att_line.value_ids.ids + size_vals)))]})

                product_template_id.default_code = prt
            else:
                attr_ids = []
                if color_vals:
                    attr_ids.append((0, 0, {'attribute_id': color_attr.id, 'value_ids': [(6, 0, color_vals)]}))
                if size_vals:
                    attr_ids.append((0, 0, {'attribute_id': size_attr.id, 'value_ids': [(6, 0, size_vals)]}))

                prt_vals = {
                    'name': variants[0]['name'],
                    'default_code': prt,
                    'attribute_line_ids': attr_ids,
                    'categ_id': variants[0]['cat'],
                    'list_price': variants[0]['price'],
                    # 'type': 'product',
                }

                _logger.info(pformat(prt_vals))
                product_template_id = product_template_obj.create(prt_vals)

            product_template_id._create_variant_ids()

            matched_products = []
            has_variant_codes = any(v.get('code') for v in variants)
            for pvv in variants:
                tmpl_has_color = bool(product_template_id.attribute_line_ids.filtered(lambda l: l.attribute_id == color_attr))
                tmpl_has_size = bool(product_template_id.attribute_line_ids.filtered(lambda l: l.attribute_id == size_attr))

                if tmpl_has_color and not pvv['color']:
                    raise ValidationError(_(
                        'No matching variant found for template code %s (row %s). Please set Color Code.'
                    ) % (prt, pvv.get('row')))
                if tmpl_has_size and not pvv['size']:
                    raise ValidationError(_(
                        'No matching variant found for template code %s (row %s). Please set Size Code.'
                    ) % (prt, pvv.get('row')))

                combination = self.env['product.template.attribute.value']
                if pvv['color']:
                    color_ptav = self.env['product.template.attribute.value'].search([
                        ('product_tmpl_id', '=', product_template_id.id),
                        ('product_attribute_value_id', '=', pvv['color']),
                    ], limit=1)
                    if not color_ptav:
                        raise ValidationError(_(
                            'Color value is not available on template code %s (row %s).'
                        ) % (prt, pvv.get('row')))
                    combination |= color_ptav
                if pvv['size']:
                    size_ptav = self.env['product.template.attribute.value'].search([
                        ('product_tmpl_id', '=', product_template_id.id),
                        ('product_attribute_value_id', '=', pvv['size']),
                    ], limit=1)
                    if not size_ptav:
                        raise ValidationError(_(
                            'Size value is not available on template code %s (row %s).'
                        ) % (prt, pvv.get('row')))
                    combination |= size_ptav

                product_variant_id = product_template_id._get_variant_for_combination(combination) if combination else product_template_id.product_variant_ids[:1]
                if not product_variant_id and combination and product_template_id.has_dynamic_attributes():
                    product_variant_id = product_template_id._create_product_variant(combination, log_warning=True)

                if not product_variant_id:
                    raise ValidationError(_(
                        'No matching variant found for template code %s (row %s).'
                    ) % (prt, pvv.get('row')))

                matched_products.append(
                    {'product': product_variant_id, 'qty': pvv['qty'], 'po_price': pvv['po_price']})
                write_vals = {
                    'lst_price': pvv['price'],
                    'standard_price': pvv['cost'],
                    'available_in_pos': pvv['available_in_pos'],
                }

                if pvv.get('code'):
                    write_vals['default_code'] = pvv['code']

                pos_cat_ids = pvv.get('pos_cat') or []
                if isinstance(pos_cat_ids, int):
                    pos_cat_ids = [pos_cat_ids]
                elif isinstance(pos_cat_ids, (set, tuple)):
                    pos_cat_ids = list(pos_cat_ids)

                if pos_cat_ids:
                    write_vals['pos_categ_ids'] = [(6, 0, pos_cat_ids)]

                # Add seller_ids if available
                if pvv.get('seller_id'):
                    write_vals['seller_ids'] = [(0, 0, {
                        'partner_id': pvv['seller_id'],  # First ID in the list
                        'price': pvv['po_price'] or pvv['cost'],  # Use po_price if available, otherwise cost
                        # 'delay': 1,  # Default delay
                    })]

                product_variant_id.write(write_vals)

                if pvv['barcode']:
                    product_name = product_variant_id.display_name
                    existing = self.env['product.product'].search(
                        [('barcode', '=', pvv['barcode']), ('id', '!=', product_variant_id.id)])
                    if existing:
                        raise ValidationError(
                            _('Barcode : {} already exists on product {}'.format(pvv['barcode'],
                                                                                 existing.display_name)))
                    product_variant_id.write({'barcode': pvv['barcode']})

                if pvv.get('extra_data'):
                    product_variant_id.write(pvv['extra_data'])

            if product_template_id.product_variant_ids and matched_products:
                purchase_products += matched_products

            product_template_id.write({'default_code': prt})
            #archive any varian with no default code
            if has_variant_codes:
                for variant in product_template_id.product_variant_ids:
                    if not variant.default_code:
                        variant.write({"active": False})

        if self.create_purchase and purchase_products:
            purchase_lines = [
                (0, 0, {
                    'name': line['product'].name,
                    'product_id': line['product'].id,
                    'product_qty': line['qty'],
                    'product_uom': line['product'].uom_po_id.id,
                    'price_unit': line['product'].standard_price,
                    'date_planned': fields.Datetime.now(),
                    # 'po_price': line['po_price'],
                }) for line in purchase_products
            ]

            purchase_order = self.env['purchase.order'].create({
                'partner_id': self.partner_id.id,
                'order_line': purchase_lines
            })

            action = self.env["ir.actions.actions"]._for_xml_id('purchase.purchase_rfq')
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchase_order.id
            return action

    def update_extra_fields(self, sheet, row):
        print(row)
        extra_data = {}
        product_obj = self.env['product.product']
        product_fields = {key: value for key, value in
                          product_obj._fields.items() if
                          value.type in ['char', 'selection', 'text',
                                         'boolean', 'many2one']}
        for col in range(16, sheet.max_column + 1):
            print(col)
            field_name = sheet.cell(row=1, column=col).value
            if field_name in product_fields.keys():
                field = product_fields[field_name]
                field_value = str(sheet.cell(row=row, column=col).value)
                if field.type == 'boolean':

                    try:
                        field_value = ast.literal_eval(field_value)
                    except:
                        pass

                    extra_data.update({field_name: field_value})
                elif field.type == 'selection':
                    selection_items = dict(
                        product_obj.fields_get()[field_name]['selection'])
                    for k, v in selection_items.items():
                        if v == field_value:
                            extra_data.update({field_name: k})
                            break
                elif field.type == 'many2one':
                    field_obj = self.env[field.comodel_name]
                    if hasattr(field_obj,
                               'name') and field_obj.check_access_rights('read',
                                                                         raise_exception=False):
                        field_record = field_obj.search(
                            [('name', '=', field_value)], limit=1)
                        if field_record:
                            extra_data.update({field_name: field_record.id})

                else:
                    extra_data.update({field_name: field_value})

        return extra_data
