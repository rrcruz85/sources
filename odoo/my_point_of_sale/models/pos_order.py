# -*- coding: utf-8 -*-

import logging

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)


class PosOrder(osv.osv):
    _inherit = 'pos.order'

    def _get_card_payment(self, cr, uid, ids, field_names, args, context=None):
        if not ids:
            return {}

        res = dict.fromkeys(ids, False)
        for i in self.browse(cr, uid, ids, context):
            if i.statement_ids:
                for j in i.statement_ids:
                    if j.journal_id.type == 'card':
                        res[i.id] = True
        return res

    def _get_check_payment(self, cr, uid, ids, field_names, args, context=None):
        if not ids:
            return {}

        res = dict.fromkeys(ids, False)
        for i in self.browse(cr, uid, ids, context):
            if i.statement_ids:
                for j in i.statement_ids:
                    if j.journal_id.type == 'check':
                        res[i.id] = True
        return res

    def _get_bank_payment(self, cr, uid, ids, field_names, args, context=None):
        if not ids:
            return {}

        res = dict.fromkeys(ids, False)
        for i in self.browse(cr, uid, ids, context):
            if i.statement_ids:
                for j in i.statement_ids:
                    if j.journal_id.type == 'bank':
                        res[i.id] = True
        return res

    def _order_fields(self, cr, uid, ui_order, context=None):
        values = super(PosOrder, self)._order_fields(cr, uid, ui_order, context)

        if ui_order.get('card_payment', False):
            values.update({
                'card_number': ui_order['card_number'],
                'card_type': ui_order['card_type'],
                'acquirer': ui_order['acquirer'],
                'approval_number': ui_order['approval_number'],
                'lot_number': ui_order['lot_number'],
                'reference': ui_order['reference'],
            })

        if ui_order.get('check_payment', False):
            values.update({
                'check_number': ui_order['check_number'],
                'acquirer': ui_order['acquirer'],
            })

        if ui_order.get('bank_payment', False):
            values.update({
                'approval_number': ui_order['approval_number'],
                'reference': ui_order['reference'],
                'acquirer': ui_order['acquirer'],
            })

        values.update({'iva_compensation': ui_order['iva_compensation']})
        return values

    def _amount_all_new(self, cr, uid, ids, name, args, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}

        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_paid': 0.0,
                'amount_return': 0.0,
                'amount_tax': 0.0,
                'amount_iva_compensation': 0.0
            }

            val1 = val2 = val3 = 0.0
            cur = order.pricelist_id.currency_id

            for payment in order.statement_ids:
                res[order.id]['amount_paid'] += payment.amount
                res[order.id]['amount_return'] += (payment.amount < 0 and payment.amount or 0)

            for line in order.lines:
                val1 += self._amount_line_tax(cr, uid, line, context=context)
                val2 += line.price_subtotal
                val3 += line.iva_compensation

            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val1)
            amount_untaxed = cur_obj.round(cr, uid, cur, val2)
            res[order.id]['amount_iva_compensation'] = cur_obj.round(cr, uid, cur, val3)
            res[order.id]['amount_total'] = res[order.id]['amount_tax'] + amount_untaxed
            res[order.id]['amount_total_with_compensation'] = res[order.id]['amount_total'] - res[order.id]['amount_iva_compensation']

        return res

    _columns = {
        'card_payment': fields.function(_get_card_payment, method=True, type='boolean', string='Credit Card Payment'),
        'bank_payment': fields.function(_get_bank_payment, method=True, type='boolean', string='Bank Payment'),
        'check_payment': fields.function(_get_check_payment, method=True, type='boolean', string='Check Payment'),

        'card_number': fields.char('Card Number', size=16),
        'check_number': fields.char('Check Number', size=16),
        'card_type': fields.many2one('pos.credit_card', 'Card Type'),

        'acquirer': fields.many2one('res.bank', 'Acquirer'),
        'approval_number': fields.char('Approval Number', size=9),
        'lot_number': fields.char('Lot Number', size=6),
        'reference': fields.char('Reference', size=6),

        # IVA Compensation for all products in the order...
        'iva_compensation': fields.float('IVA Compensation (%)', digits=(16, 2)),
        'amount_iva_compensation': fields.function(_amount_all_new, string='IVA Compensation', multi='all'),

        'amount_tax': fields.function(
            _amount_all_new, string='Taxes', digits_compute=dp.get_precision('Account'), multi='all'
        ),

        'amount_total': fields.function(
            _amount_all_new, string='Total', digits_compute=dp.get_precision('Account'),  multi='all'
        ),

        'amount_total_with_compensation': fields.function(
            _amount_all_new, string='Total', digits_compute=dp.get_precision('Account'),  multi='all'
        ),

        'amount_paid': fields.function(
            _amount_all_new, string='Paid', states={'draft': [('readonly', False)]}, readonly=True,
            digits_compute=dp.get_precision('Account'), multi='all'
        ),

        'amount_return': fields.function(
            _amount_all_new, 'Returned', digits_compute=dp.get_precision('Account'), multi='all'
        ),
    }


class PosOrderLine(osv.osv):
    _inherit = "pos.order.line"

    def _amount_line_all_new(self, cr, uid, ids, field_names, arg, context=None):
        res = dict([(i, {}) for i in ids])
        account_tax_obj = self.pool.get('account.tax')

        for line in self.browse(cr, uid, ids, context=context):
            taxes_ids = [ tax for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id ]
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = account_tax_obj.compute_all(cr, uid, taxes_ids, price, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)

            res[line.id]['price_subtotal'] = taxes['total']
            res[line.id]['price_subtotal_incl'] = taxes['total_included'] - line.iva_compensation

        return res

    _columns = {
        'iva_compensation': fields.float('IVA Compensation', digits=(16, 2), readonly=True),

        'price_subtotal': fields.function(
            _amount_line_all_new, multi='pos_order_line_amount', digits_compute=dp.get_precision('Product Price'),
            string='Subtotal w/o Tax', store=True
        ),

        'price_subtotal_incl': fields.function(
            _amount_line_all_new, multi='pos_order_line_amount', digits_compute=dp.get_precision('Account'),
            string='Subtotal', store=True
        ),
    }
