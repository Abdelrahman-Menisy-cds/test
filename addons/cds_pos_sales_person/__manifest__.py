# -*- coding: utf-8 -*-
{
    'name': "CDS Pos Sales Person",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "www.cdsegypt.com",
    'contributors': [
        'Ramadan Khalil <rkhalil1990@gmail.com>',
        'Abdelrhman Gouda <abdelrhman.gouda@cdsegypt.com>',
    ],
    'category': 'point of sale',
    'version': '18.0',

    # any module necessary for this one to work correctly
    'depends': [
        'pos_hr',
        'bi_pos_order_line_view',
    ],

    # always loaded
    'data': [
        # 'views/templates.xml',
        'views/pos_order.xml',
        'views/pos_config.xml',
        'views/pos_order_line.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'cds_pos_sales_person/static/src/**/*',
        ],
    },
    'license': 'OPL-1',


}