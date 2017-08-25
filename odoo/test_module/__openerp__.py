# -*- coding: utf-8 -*-

{
    'name': 'test_module',
    'version': '1.0',
    'category': 'Test Module',
    'author': 'Odoo',

    'summary': 'Test',
    'description': """
    """,

    'depends': ['base'],

    'data': [


        # Templates...
        'static/src/xml/assets_backend.xml',


    ],

    'qweb': [
        'static/src/xml/pos.xml',
    ],

    'demo':[],

    'installable': True,
    'application': False,
    'auto_install': False,
}
