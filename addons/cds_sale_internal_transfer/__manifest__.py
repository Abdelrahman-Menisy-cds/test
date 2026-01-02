# -*- coding: utf-8 -*-
# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

{
    'name': 'CDS Sale Internal Transfer Link',
    'version': '1.0',
    'category': 'Sales/Sales',
    'summary': 'Link Sales Orders with Internal Transfers',
    'description': """
        This module allows linking Sales Orders with Internal Transfers.
        Features:
        - Add Internal Transfer field in Quotations
        - Select Internal Transfers with Done status
        - Auto-populate products from selected Internal Transfer
        - Prevent selecting the same Internal Transfer in multiple Sales Orders
        - Ensure quantities and products match exactly
    """,
    'author': "CDS Solutions SRL",
    'website': "https://www.cdsegypt.com",
    'contributors': [
        'Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)',
        'Abdelrahman Menisy (<a.mansy@cdsegypt.com>)',
    ],
    'depends': [
        'sale',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
