# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class PosOrder(osv.osv):
    _inherit = 'pos.order'

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
                val3 += payment.iva_compensation

            for line in order.lines:
                val1 += self._amount_line_tax(cr, uid, line, context=context)
                val2 += line.price_subtotal

            amount_untaxed = cur_obj.round(cr, uid, cur, val2)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_iva_compensation'] = cur_obj.round(cr, uid, cur, val3)
            res[order.id]['amount_iva_compensation_str'] = '- ' + str(res[order.id]['amount_iva_compensation']) if val3 else '- 0.0'
            res[order.id]['amount_total'] = res[order.id]['amount_tax'] + amount_untaxed - res[order.id]['amount_iva_compensation']
            res[order.id]['amount_total_with_compensation'] = res[order.id]['amount_total'] - res[order.id]['amount_iva_compensation']
            res[order.id]['amount_paid'] = res[order.id]['amount_total_with_compensation']
        return res

    _columns = {

        'amount_iva_compensation': fields.function(_amount_all_new, string='IVA Compensation', multi='all'),
        'amount_iva_compensation_str': fields.function(_amount_all_new, type = "char",string='IVA Compensation', multi='all'),

        'amount_tax': fields.function(
            _amount_all_new, string='Taxes', digits_compute=dp.get_precision('Account'), multi='all'
        ),

        'amount_total': fields.function(
            _amount_all_new, string='Total', digits_compute=dp.get_precision('Account'), multi='all'
        ),

        'amount_total_with_compensation': fields.function(
            _amount_all_new, string='Total', digits_compute=dp.get_precision('Account'), multi='all'
        ),

        'amount_paid': fields.function(
            _amount_all_new, string='Paid', states={'draft': [('readonly', False)]}, readonly=True,
            digits_compute=dp.get_precision('Account'), multi='all'
        ),

        'amount_return': fields.function(
            _amount_all_new, 'Returned', digits_compute=dp.get_precision('Account'), multi='all'
        ),
    }

    def _payment_fields(self, cr, uid, ui_paymentline, context=None):
        return {
            'amount': ui_paymentline['amount'] or 0.0,
            'payment_date': ui_paymentline['name'],
            'statement_id': ui_paymentline['statement_id'],
            'payment_name': ui_paymentline.get('note', False),
            'journal': ui_paymentline['journal_id'],
            # New Fields
            'card_number': ui_paymentline.get('card_number', False),
            'check_number': ui_paymentline.get('check_number', False),
            'check_date': ui_paymentline.get('check_date', False),
            'card_type_id': ui_paymentline.get('card_type_id', False),
            'bank_id': ui_paymentline.get('bank_id', False),
            'approval_number': ui_paymentline.get('approval_number', False),
            'lot_number': ui_paymentline.get('lot_number', False),
            'reference': ui_paymentline.get('reference', False),
            'iva_compensation': ui_paymentline.get('iva_compensation', False),
        }

    def add_payment(self, cr, uid, order_id, data, context=None):
        """Create a new payment for the order"""
        context = dict(context or {})
        statement_line_obj = self.pool.get('account.bank.statement.line')
        property_obj = self.pool.get('ir.property')
        order = self.browse(cr, uid, order_id, context=context)
        date = data.get('payment_date', time.strftime('%Y-%m-%d'))
        if len(date) > 10:
            timestamp = datetime.strptime(date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
            ts = fields.datetime.context_timestamp(cr, uid, timestamp, context)
            date = ts.strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
        args = {
            'amount': data['amount'],
            'date': date,
            'name': order.name + ': ' + (data.get('payment_name', '') or ''),
            'partner_id': order.partner_id and self.pool.get("res.partner")._find_accounting_partner(
                order.partner_id).id or False,
        }

        journal_id = data.get('journal', False)
        statement_id = data.get('statement_id', False)
        assert journal_id or statement_id, "No statement_id or journal_id passed to the method!"

        journal = self.pool['account.journal'].browse(cr, uid, journal_id, context=context)
        # use the company of the journal and not of the current user
        company_cxt = dict(context, force_company=journal.company_id.id)
        account_def = property_obj.get(cr, uid, 'property_account_receivable', 'res.partner', context=company_cxt)
        args['account_id'] = (order.partner_id and order.partner_id.property_account_receivable \
                              and order.partner_id.property_account_receivable.id) or (
                             account_def and account_def.id) or False

        if not args['account_id']:
            if not args['partner_id']:
                msg = _('There is no receivable account defined to make payment.')
            else:
                msg = _('There is no receivable account defined to make payment for the partner: "%s" (id:%d).') % (
                order.partner_id.name, order.partner_id.id,)
            raise osv.except_osv(_('Configuration Error!'), msg)

        context.pop('pos_session_id', False)

        for statement in order.session_id.statement_ids:
            if statement.id == statement_id:
                journal_id = statement.journal_id.id
                break
            elif statement.journal_id.id == journal_id:
                statement_id = statement.id
                break

        if not statement_id:
            raise osv.except_osv(_('Error!'), _('You have to open at least one cashbox.'))

        args.update({
            'statement_id': statement_id,
            'pos_statement_id': order_id,
            'journal_id': journal_id,
            'ref': order.session_id.name,
            'card_number': data.get('card_number', False),
            'check_number': data.get('check_number', False),
            'check_date': data.get('check_date', False),
            'card_type_id': data.get('card_type_id', False),
            'bank_id': data.get('bank_id', False),
            'approval_number': data.get('approval_number', False),
            'lot_number': data.get('lot_number', False),
            'reference': data.get('reference', False),
            'iva_compensation': data.get('iva_compensation', False),
        })

        statement_line_obj.create(cr, uid, args, context=context)

        return statement_id


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
            res[line.id]['price_subtotal_incl'] = taxes['total_included'] #- line.iva_compensation

        return res

    _columns = {
        'price_subtotal': fields.function(
            _amount_line_all_new, multi='pos_order_line_amount', digits_compute=dp.get_precision('Product Price'),
            string='Subtotal w/o Tax', store=True
        ),
        'price_subtotal_incl': fields.function(
            _amount_line_all_new, multi='pos_order_line_amount', digits_compute=dp.get_precision('Account'),
            string='Subtotal', store=True
        ),
        'lot_id': fields.many2one('stock.production.lot', 'Production lot', ondelete='set null'),
    }
