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
        'views/test_module_view.xml',
        'views/test_module_menuitem.xml',
    ],

    'qweb': [
        'static/src/xml/test.xml',
    ],

    'css': [
         'static/src/css/styles.css',
    ],

    'js': [
        'static/src/css/widgets.js',
    ],

    'demo':[],

    'installable': True,
    'application': False,
    'auto_install': False,
}
