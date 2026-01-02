# -*- coding: utf-8 -*-
# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

{
    'name': 'CDS Sale Internal Transfer',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Link Sales Orders with Internal Transfers',
    'description': """
CDS Sale Internal Transfer Module
==================================

This module allows linking Sales Orders with Internal Transfers by:
- Adding a field in Quotations to select an Internal Transfer (Done status only)
- Automatically adding products from the selected Internal Transfer to the Sales Order
- Preventing selection of the same Internal Transfer in multiple Sales Orders
- Ensuring quantities and products match exactly those in the Internal Transfer
""",
    'author': "CDS Solutions SRL",
    'website': "https://www.cdsegypt.com",
    'contributors': [
        'Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)',
        'Abdelrahman Menisy (<a.mansy@cdsegypt.com>)',
    ],
    'depends': [
        'sale_management',
        'stock',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
