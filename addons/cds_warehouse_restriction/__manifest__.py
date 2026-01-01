# -*- coding: utf-8 -*-
{
    'name': "CDS Warehouse Restriction",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "https://www.cdsegypt.com",
    'contributors': [
        'Ramadan Khalil <rkhalil1990@gmail.com>',
    ],
    'version': '0.1',
    'depends': ['stock', 'point_of_sale','stock_barcode','purchase_stock'],
    'data': [
        'security/groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
        'views/stock_picking_type_view.xml',
        'views/stock_picking_view.xml',
        'views/stock_warehouse_orderpoint_view.xml',
        'views/purchase_order_view.xml'

    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'cds_warehouse_restriction/static/src/**/*.js',
    #     ],

    # },
    "pre_init_hook": None,
    "post_init_hook": None,
    "license": "LGPL-3",
}
