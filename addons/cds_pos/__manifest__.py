# -*- coding: utf-8 -*-
{
    'name': "CDS POS Updates",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "www.cdsegypt.com",
    'contributors': [
        'Ahmed Elmasry <ahmed.elmasry@cdsegypt.com>',
    ],
    'version': '0.1',
    'depends': ['pos_hr', 'pos_sale', 'pos_discount', 'pos_loyalty'],
    'data': [
        'security/groups.xml',
        'views/res_config_settings_views.xml',
        'views/cds_pos_config_dashboard_view.xml',
    ],    'assets': {
        'web.assets_backend': [
            'cds_pos/static/src/js/libs/jquery-barcode-last.min.js',
        ],
        'point_of_sale.base_app': [
            'cds_pos/static/src/js/libs/jquery-barcode-last.min.js',
        ],
        'point_of_sale._assets_pos': [
            ('remove', 'pos_hr/static/src/app/components/popups/closing_popup/closing_popup.xml'),
            'cds_pos/static/src//overrides/components/ticket_screen/*',
            'cds_pos/static/src/overrides/components/closing_popup/*',
            'cds_pos/static/src/overrides/components/payment_screen/*',
            'cds_pos/static/src/js/order_receipt.js',
            'cds_pos/static/src/xml/order_receipt.xml',
        ]
    },
    'license': 'OPL-1',
    "pre_init_hook": None,
    "post_init_hook": None,
}
