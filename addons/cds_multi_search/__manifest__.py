# -*- coding: utf-8 -*-
{
    'name': "CDS MultiSearch",
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
    'depends': ['base_import'],
    'data': [
        # 'security/ir.model.access.csv',
    ],
     'assets': {
        'web.assets_backend': [
            'cds_multi_search/static/src/**/*',
        ],
    },
    'license': 'OPL-1',
    "pre_init_hook": None,
    "post_init_hook": None,
}