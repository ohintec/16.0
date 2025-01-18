# -*- coding: utf-8 -*-
{
    'name': "N2d Logo Full Header",

    'summary': """
        N2d Logo Full Header""",

    'description': """
        N2d Logo Full Header
    """,

    'author': "Hintegration",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/report_layout_inherit.xml',
        'static/src/templates.html',
    ],
   'assets': {
        'web.assets_backend': [
            '/n2d_logo_full_header/static/src/img/invoice.png',
            '/n2d_logo_full_header/static/src/bannar.jpeg',
            '/n2d_logo_full_header/static/src/Hintegration.png',
        ],
       },

    'price': '5.00',

    'currency': 'USD',

    'support': 'info@ohint.net',

    'license': 'AGPL-3',

     'live_test_url': 'demo.net2do.com',
}
