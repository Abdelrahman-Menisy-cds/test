# -*- coding: utf-8 -*-
{
    "name": "CDS POS Split Loyalty",
    "summary": """
    """,
    "description": """
    """,
    "author": "CDS Solutions SRL",
    "website": "http://www.cdsegypt.com",
    "contributors": [
        "Ramadan Khalil <rkhalil1990@gmail.com>",
    ],
    "version": "0.1",
    "depends": ["pos_loyalty","cds_pos_pricelist_discount"],
    "data": [
        # 'security/ir.model.access.csv',
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "cds_pos_split_loyalty/static/src/**/*",
        ],
    },
    "license": "OPL-1",
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
}
