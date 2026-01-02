# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

{
    'name': 'CDS Sales Internal Transfer',
    'version': '1.0',
    'category': 'Sales/Sales',
    'summary': 'Link Sales Orders with Internal Transfers',
    'description': """
Link Sales Orders with Internal Transfers
==========================================

This module allows you to link Sales Orders with Internal Transfers by:
- Adding an Internal Transfer field in Quotations
- Selecting Internal Transfers in Done status
- Automatically adding products from the Internal Transfer to the Sales Order
- Preventing duplicate selection of the same Internal Transfer
- Ensuring quantities and products match exactly
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
    'license': 'LGPL-3',
}
