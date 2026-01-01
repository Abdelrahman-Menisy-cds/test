# -*- coding: utf-8 -*-
{
    'name': "CDS Hide Product Price",
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
    'depends': ['stock', 'web', 'sale'],
    'data': [
        'security/groups.xml',
        'views/sale_order.xml',
        'views/product_view.xml',
        'views/product_supplierinfo.xml',
        # 'security/ir.model.access.csv',
    ],
    "pre_init_hook": None,
    "post_init_hook": None,
    "license": "LGPL-3",
}
