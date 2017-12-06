# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import psycopg2

_logger = logging.getLogger(__name__)

class PosOrder(osv.osv):
    _inherit = 'pos.order'

    def _amount_all_new(self, cr, uid, ids, name, args, context=None):
        res = {}

        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_paid': 0.0,
                'amount_tax': 0.0,
                'amount_iva_compensation': 0.0,
                'paymentLines': []
            }

            cur = order.company_id.currency_id

            payment_lines = {}
            change = 0.0
            total = 0.0
            iva_comp_total = 0.0
            total_taxes = 0.0
            for payment in order.statement_ids:
                if payment.amount < 0:
                    change += abs(payment.amount)
                else:
                    total += payment.amount
                    if payment.journal_id.name not in payment_lines:
                        payment_lines[payment.journal_id.name] = payment.amount
                    else:
                        payment_lines[payment.journal_id.name] += payment.amount

                res[order.id]['amount_paid'] += payment.amount
                iva_comp_total += payment.iva_compensation

            payment_ids = [self.pool.get('account.bank.statement.line.tmp').create(cr,uid, {'order_id': order.id,'name': key,'amount' : payment_lines[key]})  for key in payment_lines if payment_lines[key] > 0]
            cur_obj = self.pool.get('res.currency')

            sql = 'select discount, price_unit, qty from pos_order_line where order_id = %s '
            cr.execute(sql, (order.id,))
            result = cr.fetchall()
            total_discount = 0.0
            amount_untaxed = 0.0

            for line in result:
                total_discount = total_discount + (line[2] * (line[0] * line[1] / 100))
                amount_untaxed = amount_untaxed + (line[2] * line[1])

            for line in order.lines:
                total_taxes += self._amount_line_tax(cr, uid, line, context=context)

            amount_untaxed = cur_obj.round(cr, uid, cur, amount_untaxed)
            total_discount = cur_obj.round(cr, uid, cur, total_discount)
            total = cur_obj.round(cr, uid, cur, total)
            total_taxes = cur_obj.round(cr, uid, cur, total_taxes)
            iva_comp_total = cur_obj.round(cr, uid, cur, iva_comp_total)
            res[order.id]['total_discount'] = total_discount
            res[order.id]['amount_untaxed'] = amount_untaxed
            res[order.id]['amount_tax'] = total_taxes
            res[order.id]['amount_iva_compensation'] = iva_comp_total
            res[order.id]['amount_iva_compensation_str'] = '- ' + str(iva_comp_total)
            res[order.id]['amount_total'] = amount_untaxed + (total_taxes - iva_comp_total)
            res[order.id]['amount_total_with_compensation'] = total - iva_comp_total
            res[order.id]['amount_paid'] = total - iva_comp_total
            res[order.id]['paymentLines'] = payment_ids
            res[order.id]['total_change'] = change
        return res

    _columns = {

        'amount_iva_compensation': fields.function(_amount_all_new, string='IVA Compensation', multi='all'),
        'amount_iva_compensation_str': fields.function(_amount_all_new, type = "char",string='IVA Compensation', multi='all'),

        'amount_untaxed': fields.function(
            _amount_all_new, string='Subtotal', digits_compute=dp.get_precision('Account'), multi='all'
        ),

        'total_discount': fields.function(
            _amount_all_new, string='Subtotal', digits_compute=dp.get_precision('Account'), multi='all'
        ),

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

        'paymentLines': fields.function(
            _amount_all_new, 'Returned', type="one2many", relation="account.bank.statement.line.tmp", multi='all'
        ),
        'total_change': fields.function(
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

    def create_from_ui(self, cr, uid, orders, context=None):
        # Keep only new orders
        submitted_references = [o['data']['name'] for o in orders]
        existing_order_ids = self.search(cr, uid, [('pos_reference', 'in', submitted_references)], context=context)
        existing_orders = self.read(cr, uid, existing_order_ids, ['pos_reference'], context=context)
        existing_references = set([o['pos_reference'] for o in existing_orders])
        orders_to_save = [o for o in orders if o['data']['name'] not in existing_references]

        order_ids = []

        for tmp_order in orders_to_save:
            to_invoice = tmp_order['to_invoice']
            order = tmp_order['data']
            order_id = self._process_order(cr, uid, order, context=context)
            order_ids.append(order_id)

            try:
                self.signal_workflow(cr, uid, [order_id], 'paid')
                result = self.read(cr, uid, [order_id], ['state'])
                if result[0]['state'] != 'paid':
                    self.action_paid(cr, uid, [order_id], context=context)

            except psycopg2.OperationalError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

            if to_invoice:
                self.action_invoice(cr, uid, [order_id], context)
                order_obj = self.browse(cr, uid, order_id, context)
                self.pool['account.invoice'].signal_workflow(cr, uid, [order_obj.invoice_id.id], 'invoice_open')

        return order_ids

    def action_paid(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'paid'}, context=context)
        self.create_picking(cr, uid, ids, context=context)
        return True

    def create_picking(self, cr, uid, ids, context=None):
        """Create a picking for each order and validate it."""
        picking_obj = self.pool.get('stock.picking')
        partner_obj = self.pool.get('res.partner')
        move_obj = self.pool.get('stock.move')

        for order in self.browse(cr, uid, ids, context=context):
            if all(t == 'service' for t in order.lines.mapped('product_id.type')):
                continue
            addr = order.partner_id and partner_obj.address_get(cr, uid, [order.partner_id.id], ['delivery']) or {}
            picking_type = order.picking_type_id
            picking_id = False
            if picking_type:
                picking_id = picking_obj.create(cr, uid, {
                    'origin': order.name,
                    'partner_id': addr.get('delivery', False),
                    'date_done': order.date_order,
                    'picking_type_id': picking_type.id,
                    'company_id': order.company_id.id,
                    'move_type': 'direct',
                    'note': order.note or "",
                    'invoice_state': 'none',
                }, context=context)
                self.write(cr, uid, [order.id], {'picking_id': picking_id}, context=context)
            location_id = order.location_id.id
            if order.partner_id:
                destination_id = order.partner_id.property_stock_customer.id
            elif picking_type:
                if not picking_type.default_location_dest_id:
                    raise osv.except_osv(_('Error!'), _(
                        'Missing source or destination location for picking type %s. Please configure those fields and try again.' % (
                        picking_type.name,)))
                destination_id = picking_type.default_location_dest_id.id
            else:
                destination_id = partner_obj.default_get(cr, uid, ['property_stock_customer'], context=context)[
                    'property_stock_customer']

            move_list = []
            for line in order.lines:
                if line.product_id and line.product_id.type == 'service':
                    continue

                move_list.append(move_obj.create(cr, uid, {
                    'name': line.name,
                    'product_uom': line.product_id.uom_id.id,
                    'product_uos': line.product_id.uom_id.id,
                    'picking_id': picking_id,
                    'picking_type_id': picking_type.id,
                    'product_id': line.product_id.id,
                    'product_uos_qty': abs(line.qty),
                    'product_uom_qty': abs(line.qty),
                    'state': 'draft',
                    'location_id': location_id if line.qty >= 0 else destination_id,
                    'location_dest_id': destination_id if line.qty >= 0 else location_id,
                    'restrict_lot_id' : line.lot_id.id if line.lot_id and line.product_id.track_all else False,
                }, context=context))

            if picking_id:
                picking_obj.action_confirm(cr, uid, [picking_id], context=context)
                picking_obj.force_assign(cr, uid, [picking_id], context=context)
                picking_obj.action_done(cr, uid, [picking_id], context=context)
            elif move_list:
                move_obj.action_confirm(cr, uid, move_list, context=context)
                move_obj.force_assign(cr, uid, move_list, context=context)
                move_obj.action_done(cr, uid, move_list, context=context)
        return True


class PosOrderLine(osv.osv):
    _inherit = "pos.order.line"

    _columns = {
        'lot_id': fields.many2one('stock.production.lot', 'Production lot', ondelete='set null'),
    }
