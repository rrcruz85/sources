# -*- coding: utf-8 -*-

{
    'name': 'my_point_of_sale',
    'version': '1.0.0',
    'category': 'Point Of Sale',
    'author': 'Odoo',

    'summary': 'Point Of Sale New Release',
    'description': """
    """,

    'depends': ['base', 'account', 'point_of_sale', 'product','stock'],

    'data': [
        # Datas to load...
        'data/credit_card_data.xml',
        'data/account_journal_data.xml',

        # Views...
        'views/product_template_views.xml',
        'views/pos_config_views.xml',
        'views/pos_order_views.xml',
        'views/credit_card_views.xml',
        'views/account_journal_views.xml',
        'views/res_partner_views.xml',
        'views/account_views.xml',
        'views/res_company_views.xml',
        'views/account_invoice_view.xml',
        'wizards/pos_most_sold_product_wzd.xml',

        # Templates...
        'static/src/xml/assets_backend.xml',

        # Reports...
        'reports/report_receipt.xml',
        'reports/report_saleslines.xml',
        'reports/report_invoice.xml',
        'reports/report_detailsofsales.xml',
        'reports/report_pos_ticket.xml',
        # Template...
        'reports/post_most_sold_product_report.xml',
        'views/pos_order_template.xml',
    ],

    'qweb': [
        'static/src/xml/pos.xml',
    ],

    'css':[
        'static/src/css/styles.css',
    ],

    'demo':['demo/account_journal_demo.xml'],

    'installable': True,
    'application': False,
    'auto_install': False,
}
