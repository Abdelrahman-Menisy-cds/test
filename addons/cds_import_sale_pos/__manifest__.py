# -*- coding: utf-8 -*-
{
    'name': "Import Sale Order POS",
    'summary': """
    Import Sale Order POS
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "www.cdsegypt.com",
    'contributors': [
        'Abdelrhman Gouda <a.goda@cdsegypt.com>',
    ],
    'version': '19.0.1.0.0',
    'depends': ['sale', 'pos_sale'],
    'data': [
        'views/res_config_settings.xml',
        'views/pos_order_views.xml',
        'views/sale_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'cds_import_sale_pos/static/src/**/*',
        ],
    },
    'license': 'OPL-1',
    "pre_init_hook": None,
    "post_init_hook": None,
}
