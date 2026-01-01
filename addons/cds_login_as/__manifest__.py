# -*- coding: utf-8 -*-
{
    'name': "CDS Login As Another User",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "https://www.cdsegypt.com",
    'contributors': [
        'Ramadan Khalil <rkhalil1990@gmail.com>',
    ],
    'version': '0.1',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/cds_login_as_wizard_view.xml'

    ],

    'assets': {
        'web.assets_backend': [
            'cds_login_as/static/src/js/user_menu_items.js',
            'cds_login_as/static/src/js/service.js'

        ],

    },
    "pre_init_hook": None,
    "post_init_hook": None,
    'license': 'OPL-1',
}
