# -*- coding: utf-8 -*-
{
    'name': "CDS POS Pricelist Discount",
    'summary': """
        Apply automatic discounts from a separate discount pricelist in POS.
    """,
    'description': """
        This module allows you to configure a discount pricelist on POS config.
        When products are added to the order, discounts from the discount pricelist
        are automatically applied based on the pricelist rules.
        
        Features:
        - Configure discount pricelist per POS config
        - Auto-apply percentage discounts from pricelist rules
        - Track total discount amount on orders
        - Bulk add products to pricelist with discount wizard
    """,
    'author': "CDS Solutions SRL",
    'website': "https://www.cdsegypt.com",
    'contributors': [
        'Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)',
        'Abdelrahman Menisy (<a.mansy@cdsegypt.com>)',
        'Ragab Deaf <ragabdeaf93@outlook.com>',
    ],
    'version': '19.0.1.0.0',
    'depends': ['point_of_sale'],
    "data": [
        "security/ir.model.access.csv",
        "wizard/product_pricelist_item_multi_product.xml",
        "views/pos_config_views.xml",
        "views/pos_order_views.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'cds_pos_pricelist_discount/static/src/**/*',
        ],
    },
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'auto_install': False,
}