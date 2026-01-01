# -*- coding: utf-8 -*-
{
    'name': "CDS Import Products ",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "www.cdsegypt.com",
    'contributors': [
        'Ramadan Khalil <rkhalil1990@gmail.com>',
    ],
    'version': '0.1',
    'depends': ['stock', 'point_of_sale', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_product_wizard.xml',
        'views/product_attribute_view.xml',
        # 'views/product_brand.xml',
        'views/product_category_view.xml',
        'views/pos_category_view.xml',
        'views/product_season_views.xml',
        'views/product_product_views.xml',
        'views/product_year_view.xml',
    ],
}
