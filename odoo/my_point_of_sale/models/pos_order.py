# -*- coding: utf-8 -*-

import logging
import time
import datetime
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
                'amount_card_comition': 0.0,
                'paymentLines': []
            }

            cur = order.company_id.currency_id

            payment_lines = {}
            change = 0.0
            total = 0.0
            iva_comp_total = 0.0
            total_taxes = 0.0
            total_card_comition = 0.0
            total_taxes_payment = 0.0
            for payment in order.statement_ids:
                total_card_comition += payment.card_comition
                total_taxes_payment += payment.taxes
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

            #payment_ids = [self.pool.get('account.bank.statement.line.tmp').create(cr,uid, {'order_id': order.id,'name': key,'amount' : payment_lines[key]})  for key in payment_lines if payment_lines[key] > 0]
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
            total_taxes_payment = cur_obj.round(cr, uid, cur, total_taxes_payment)
            if total_taxes_payment > total_taxes:
                total_taxes = total_taxes_payment

            if total_card_comition == 0 and not order.apply_taxes:
                total_taxes = 0
                iva_comp_total = 0

            iva_comp_total = cur_obj.round(cr, uid, cur, iva_comp_total)
            res[order.id]['total_discount'] = total_discount
            res[order.id]['amount_untaxed'] = amount_untaxed
            res[order.id]['amount_tax'] = total_taxes
            res[order.id]['amount_iva_compensation'] = iva_comp_total
            res[order.id]['amount_iva_compensation_str'] = '- ' + str(iva_comp_total)
            res[order.id]['amount_total'] = amount_untaxed + total_card_comition + (total_taxes - iva_comp_total)
            res[order.id]['amount_total_with_compensation'] = total - iva_comp_total
            res[order.id]['amount_paid'] = total - iva_comp_total
            res[order.id]['amount_card_comition'] = total_card_comition
            #res[order.id]['paymentLines'] = payment_ids
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

        'amount_card_comition': fields.function(
            _amount_all_new, string='Card Comition', digits_compute=dp.get_precision('Account'), multi='all'
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
        'apply_taxes': fields.boolean('Apply Taxes'),
    }

    def _order_fields(self, cr, uid, ui_order, context=None):
        return {
            'name':         ui_order['name'],
            'user_id':      ui_order['user_id'] or False,
            'session_id':   ui_order['pos_session_id'],
            'lines':        ui_order['lines'],
            'pos_reference':ui_order['name'],
            'partner_id':   ui_order['partner_id'] or False,
            'apply_taxes':  ui_order['apply_taxes'],
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
            'card_comition': ui_paymentline.get('card_comition', False),
            'taxes': ui_paymentline.get('taxes', False),
            'line_tax_ids': ui_paymentline.get('line_tax_ids', False),
        }

    def add_payment(self, cr, uid, order_id, data, context=None):
        """Create a new payment for the order"""
        context = dict(context or {})
        statement_line_obj = self.pool.get('account.bank.statement.line')
        property_obj = self.pool.get('ir.property')
        order = self.browse(cr, uid, order_id, context=context)
        date = data.get('payment_date', time.strftime('%Y-%m-%d'))
        if len(date) > 10:
            timestamp = datetime.datetime.strptime(date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
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
            'card_comition': data.get('card_comition', False),
            'taxes': data.get('taxes', False),
            'line_tax_ids': data.get('line_tax_ids', False)
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

    def action_invoice(self, cr, uid, ids, context=None):
        inv_ref = self.pool.get('account.invoice')
        account_period = self.pool.get('account.period')
        inv_line_ref = self.pool.get('account.invoice.line')
        product_obj = self.pool.get('product.product')
        inv_ids = []

        account_period_ids = account_period.search(cr,uid,[('state','=','draft')])
        account_period_id = account_period_ids and account_period_ids[-1] or False
        period = False
        if account_period_id:
            period = account_period.browse(cr,uid, account_period_id)

        for order in self.pool.get('pos.order').browse(cr, uid, ids, context=context):
            if order.invoice_id:
                inv_ids.append(order.invoice_id.id)
                continue

            if not order.partner_id:
                raise osv.except_osv(_('Error!'), _('Please provide a partner for the sale.'))

            acc = order.partner_id.property_account_receivable.id

            inv = {
                'name': order.name,
                'origin': order.name,
                'account_id': acc,
                'journal_id': order.sale_journal.id or None,
                'type': 'out_invoice',
                'reference': order.name,
                'partner_id': order.partner_id.id,
                'comment': order.note or '',
                'currency_id': order.pricelist_id.currency_id.id,
                'date_invoice': datetime.datetime.now().strftime('%Y-%m-%d'),
                'date_due': datetime.datetime.now().strftime('%Y-%m-%d'),
                'period_id': account_period_id
            }

            inv.update(inv_ref.onchange_partner_id(cr, uid, [], 'out_invoice', order.partner_id.id)['value'])
            # FORWARDPORT TO SAAS-6 ONLY!
            inv.update({'fiscal_position': order.partner_id.property_account_position and order.partner_id.property_account_position.id or False})

            if not inv.get('account_id', None):
                inv['account_id'] = acc
            inv_id = inv_ref.create(cr, uid, inv, context=context)

            self.write(cr, uid, [order.id], {'invoice_id': inv_id, 'state': 'invoiced'}, context=context)
            inv_ids.append(inv_id)
            for line in order.lines:
                inv_line = {
                    'invoice_id': inv_id,
                    'product_id': line.product_id.id,
                    'quantity': line.qty,
                }
                inv_name = product_obj.name_get(cr, uid, [line.product_id.id], context=context)[0][1]
                inv_line.update(inv_line_ref.product_id_change(cr, uid, [],
                                                               line.product_id.id,
                                                               line.product_id.uom_id.id,
                                                               line.qty, partner_id = order.partner_id.id)['value'])
                if not inv_line.get('account_analytic_id', False):
                    inv_line['account_analytic_id'] = \
                        self._prepare_analytic_account(cr, uid, line,
                                                       context=context)
                inv_line['price_unit'] = line.price_unit
                inv_line['discount'] = line.discount
                inv_line['name'] = inv_name
                if order.apply_taxes or order.amount_card_comition:
                    taxes_lines = inv_line['invoice_line_tax_id']
                    if order.amount_card_comition:
                        inv_line['price_unit'] = inv_line['price_unit'] + order.amount_card_comition
                    inv_line['invoice_line_tax_id'] = [(6, 0, taxes_lines)]
                else:
                    inv_line['invoice_line_tax_id'] = []
                inv_line_ref.create(cr, uid, inv_line, context=context)

            inv_ref.button_reset_taxes(cr, uid, [inv_id], context=context)
            self.signal_workflow(cr, uid, [order.id], 'invoice')
            #inv_ref.signal_workflow(cr, uid, [inv_id], 'validate')
            inv_ref.action_date_assign(cr, uid, [inv_id], context=context)
            inv_ref.action_move_create(cr, uid, [inv_id], context=context)
            inv_ref.action_number(cr, uid, [inv_id], context=context)
            inv_ref.invoice_validate(cr, uid, [inv_id], context=context)

            #creating payment lines
            self.create_payment_lines(cr, uid, order, period, inv_id, context = context)

        if not inv_ids: return {}

        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
        res_id = res and res[1] or False
        return {
            'name': _('Customer Invoice'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': 'account.invoice',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': inv_ids and inv_ids[0] or False,
        }

    def create_payment_lines(self, cr, uid, order, period, invoice_id,context = None):
        # Create payment lines
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        seq_obj = self.pool.get('ir.sequence')

        if order.sale_journal.sequence_id:
            if not order.sale_journal.sequence_id.active:
                raise osv.except_osv(_('Configuration Error !'), _('Please activate the sequence of selected journal !'))
            c = dict(context)
            c.update({'fiscalyear_id': period and period.fiscalyear_id.id or False})
            name = seq_obj.next_by_id(cr, uid, order.sale_journal.sequence_id.id, context=c)
        else:
            raise osv.except_osv(_('Error!'),_('Please define a sequence on the journal.'))

        ref = order.name.replace('/', '')

        #Creating Move
        move = {
            'name': name,
            'journal_id': order.sale_journal.id,
            'narration': '',
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'ref': ref,
            'period_id': period and period.id or False,
        }
        move_id = move_pool.create(cr, uid, move, context=context)

        move_line_ids = []
        #Creating Move Lines
        for line in order.statement_ids:
            account_id = line.partner_id.property_account_payable.id
            debit = credit = 0.0
            if order.sale_journal.type in ('purchase', 'payment'):
                credit = line.amount
            elif order.sale_journal.type in ('sale', 'receipt'):
                debit = line.amount
            if debit < 0: credit = -debit; debit = 0.0
            if credit < 0: debit = -credit; credit = 0.0

            #sign = debit - credit < 0 and -1 or 1
            move_line = {
                'name': name or '/',
                'debit': debit,
                'credit': credit,
                'account_id': account_id,
                'move_id': move_id,
                'journal_id': line.journal_id.id,
                'period_id': period and period.id or False,
                'partner_id': line.partner_id and line.partner_id.id or False,
                'currency_id':  False,#order.sale_journal.company_id.currency_id.id,
                'amount_currency': 0.0, #sign * abs(line.amount),
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'date_maturity': datetime.datetime.now().strftime('%Y-%m-%d'),
                'statement_id': line.statement_id.id
            }
            move_line_id = move_line_pool.create(cr, uid, move_line, context)
            move_line_ids.append(move_line_id)

            move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
            line_total = move_line_brw.debit - move_line_brw.credit

            move_line2 = {
                'journal_id': line.journal_id.id,
                'period_id': period and period.id or False,
                'name': line.name or '/',
                'account_id': account_id,
                'move_id': move_id,
                'partner_id': line.partner_id and line.partner_id.id or False,
                'currency_id': False,
                'analytic_account_id': False,
                'quantity': 1,
                'credit': line_total,
                'debit': 0.0,
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'statement_id': line.statement_id.id
            }
            move_line_id = move_line_pool.create(cr, uid, move_line2, context)
            move_line_ids.append(move_line_id)

            if move_line_ids:
                self.pool.get('account.move.line').reconcile_partial(cr, uid, move_line_ids,
                                                                             writeoff_acc_id=order.partner_id.property_account_receivable.id,
                                                                             writeoff_period_id=period.id,
                                                                             writeoff_journal_id=order.sale_journal.id)

        return self.pool.get('account.invoice').write(cr, uid, [invoice_id], {'move_id': move_id, 'state': 'paid', 'reconcile': True})

class PosOrderLine(osv.osv):
    _inherit = "pos.order.line"

    def _amount_line_all(self, cr, uid, ids, field_names, arg, context=None):
        res = dict([(i, {}) for i in ids])
        account_tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            taxes_ids = [tax for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id ]
            tax_ids = [tax.id for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id]

            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = account_tax_obj.compute_all(cr, uid, taxes_ids, price, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)

            new_taxes = 0.0
            card_comition = 0.0
            for pay in line.order_id.statement_ids:
                for ltaxes in pay.line_tax_ids:
                    if line.product_id.id == ltaxes.product_id.id and ltaxes.tax_id.id in tax_ids:
                        new_taxes = ltaxes.tax
                        card_comition = ltaxes.card_comition
                        break

            subtotal = taxes['total_included']
            if not line.order_id.apply_taxes:
                subtotal = taxes['total']
            if card_comition != 0:
                subtotal = taxes['total'] + card_comition + new_taxes

            res[line.id]['price_subtotal'] = taxes['total']
            res[line.id]['price_subtotal_incl'] = subtotal
        return res

    _columns = {
        'lot_id': fields.many2one('stock.production.lot', 'Production lot', ondelete='set null'),
        'price_subtotal': fields.function(_amount_line_all, multi='pos_order_line_amount',
                                          digits_compute=dp.get_precision('Product Price'), string='Subtotal w/o Tax',
                                          store=True),
        'price_subtotal_incl': fields.function(_amount_line_all, multi='pos_order_line_amount',
                                               digits_compute=dp.get_precision('Account'), string='Subtotal'),

    }

