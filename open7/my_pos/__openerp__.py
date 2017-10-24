# -*- coding: utf-8 -*-
{
    'name': 'MY POS',
    'version': '1.0.0',
    'category': 'Point Of Sale',
    'sequence': 1,
    'author': '',
    'summary': 'POS modifications',
    'description': """
    """,
    'depends': ["base", "account", "point_of_sale", ],
    'data': [
        'data/account_journal_data.xml',
        'data/pos_credit_card_data.xml',
        'views/res_partner_view.xml',
        'views/product_view.xml',
        'views/pos_view.xml',
        'views/account_invoice_view.xml',
        
        'reports/reports_menu.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'js': [
        'static/src/js/pos.js',
        'static/src/js/widgets.js',
    ],
    'css':[
        'static/src/css/pos.css',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}