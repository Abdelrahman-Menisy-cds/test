# -*- coding: utf-8 -*-
{
    'name': "CDS POS Analytic Account",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "https://www.cdsegypt.com",
    'version': '0.1',
    'depends': ['point_of_sale', 'account', 'analytic'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_config.xml',
        'views/pos_order.xml',
        'views/pos_session.xml',
    ],
    'license': 'OPL-1',
    "pre_init_hook": None,
    "post_init_hook": None,
}
