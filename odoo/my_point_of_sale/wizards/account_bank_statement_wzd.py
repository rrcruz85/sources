# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class AccountBankStatementLineTmp(osv.osv_memory):
    _name = "account.bank.statement.line.tmp"
    _columns = {
        'order_id': fields.many2one('pos.order', 'Order'),
        'name': fields.char('name', size=32),
        'amount': fields.float('amount', digits=(16, 2)),
    }
