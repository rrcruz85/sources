# -*- coding: utf-8 -*-

from lxml import etree
from openerp.osv import fields, osv


class AccountBankStatement(osv.osv):
    _inherit = "account.bank.statement"

    def _get_journal_type(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = obj.journal_id.type
        return res

    _columns = {
        'journal_type': fields.function(_get_journal_type, type='char', string='Payment Type')
    }


class AccountBankStatementLine(osv.osv):
    _inherit = "account.bank.statement.line"

    _columns = {
        'card_number': fields.char('Card Number', size=16),
        'check_number': fields.char('Check Number', size=16),
        'check_date': fields.char('Check Date', size=25),
        'card_type_id': fields.many2one('pos.credit_card', 'Card Type'),
        'bank_id': fields.many2one('res.bank', 'Acquirer'),
        'approval_number': fields.char('Approval Number', size=9),
        'lot_number': fields.char('Lot Number', size=6),
        'reference': fields.char('Reference', size=6),
        'iva_compensation': fields.float('IVA Compensation', digits=(16, 2)),
        'card_comition': fields.float('Card Comition', digits=(16, 2)),
        'taxes': fields.float('Taxes', digits=(16, 2)),
    }

class AccountBankStatementLineTax(osv.osv):
    _name = 'account.bank.statement.line.tax'

    _columns = {
        'line_id': fields.many2one('account.bank.statement.line', 'Payment Line'),
        'tax_id': fields.many2one('account.tax', 'Tax'),
        'product_id': fields.many2one('product.product', 'Product'),
        'tax': fields.float('Tax Amount'),
        'card_comition': fields.float('Card Comition'),
    }