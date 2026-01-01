# -*- coding: utf-8 -*-
{
    'name': "CDS Sale Agent",
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
    'depends': ['sale_management', 'hr','account'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/account_payment_view.xml',
        'views/account_invoice_report_view.xml'
    ],
    "pre_init_hook": None,
    "post_init_hook": None,
}
