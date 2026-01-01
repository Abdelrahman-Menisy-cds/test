# -*- coding: utf-8 -*-
{
    'name': "CDS POS Security",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "https://www.cdsegypt.com",
    'depends': ['point_of_sale', 'pos_discount'],
    'data': [
        'views/pos_config_views.xml',
        'views/res_config_settings_views.xml',
        # 'security/ir.model.access.csv',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'cds_pos_security/static/src/**/*',

        ],
    },
    'license': "AGPL-3",
    'installable': True,
    'application': False,
    'auto_install': False,
}
