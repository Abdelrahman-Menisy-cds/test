# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)

# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies

# of the Software or modified copies of the Software.

{
    'name': 'CDS Sale Internal Transfer',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Link Sales Orders with Internal Transfers',
    'description': """
        This module allows linking Sales Orders with Internal Transfers.
        
        Features:
        - Add Internal Transfer field in Quotations
        - Select Internal Transfers with Done status
        - Auto-add products from Internal Transfer to Sales Order
        - Prevent using the same Internal Transfer in multiple Sales Orders
        - Ensure quantities and products match exactly
    """,
    'author': "CDS Solutions SRL",
    'website': "https://www.cdsegypt.com",
    'contributors': [
        'Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)',
        'Abdelrahman Menisy (<a.mansy@cdsegypt.com>)',
    ],
    'depends': ['sale', 'stock'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
