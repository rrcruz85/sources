##############################################################################
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    OeMedical, HMS Opensource Solution
##############################################################################
#    Collaborators of this module:
#    Special Credit and Thanks to Thymbra Latinoamericana S.A.
#    Coded by: Parthiv Patel <parthiv@techreceptives.com>
#    Coded by: Ruchir Shukla <ruchir@techreceptives.com>
#    Planifyied by: Parthiv Patel <parthiv@techreceptives.com>
#    Planifyied by: Nhomar Hernandéz <nhomar@vauxoo.com>
#
##############################################################################
#    This project is mantained by OeMEdical Team:
#    https://launchpad.net/oemedical
#
##############################################################################
#    It is a collaborative effort between several companies that want to join
#    efforts in have a proposal solid and strong in the Health Care environment
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{

    'name': 'Pedido Cliente',
    'version': '1.0',
    'author': "CoreCloud Team",
    'category': 'Generic Modules/Others',
    'depends': ['base', 'sale', 'purchase', 'account', 'product'],
    'application': True,
    'description': """

Pedido Cliente
---------------
Gestion de pedidos de mercaderia 

""",
    "website": "http://www.corecloud.ec",
    "licence": "AGPL v3",
    "data": [
        'views/product_view.xml',
        'views/partner_view.xml',
        'views/account_account_view.xml',
        'views/pedido_cliente_view.xml',
        'wizards/purchase_line_wzd_view.xml',
        'wizards/purchase_lines_wizard_view.xml',
        'wizards/product_order_wizard_view.xml',
        'wizards/generate_request_wizard_view.xml',
        'wizards/generate_invoice_wizard_view.xml',
        'wizards/generate_invoice_client_wizard_view.xml',
        'wizards/wizard_to_print_invoice_packing_view.xml',
        'wizards/group_lines_wizard_view.xml',
		'report/reports_menu.xml',
        'data/partner_data.xml',
    ],
    "demo": [

    ],
    'test':[
    ],
    'css': [

    ],
    'js': [

    ],
    'qweb': [

    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
