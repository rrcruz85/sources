from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import logging
import pdb
import time

import openerp
from openerp import netsvc, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product

_logger = logging.getLogger(__name__)

class account_journal(osv.osv):
    _name = "account.journal"
    _inherit = "account.journal"
    _description = "Journal"

    _columns = {
        'card_payment': fields.boolean('Credit Card Payment')
    }
account_journal()

class pos_credit_card(osv.osv):
    _name = 'pos.credit.card'
    _description = 'POS Credit Card'

    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Name', required=True),
        'active': fields.boolean('Active')
    }

    _defaults = {
        'active': True,
    }
pos_credit_card()

class pos_config(osv.osv):
    _inherit = 'pos.config'
    
    _columns = {
        'show_all_products'     : fields.boolean('Show all products?', help='If not checked, the product list in the point of sale will be limited...'),
        'iva_compensation'      : fields.float('IVA Compensation (%)', digits=(16, 2), help="It's the value of the IVA compensation that will be apply to the products..."),
        'order_seq_start_from'  : fields.integer('Order Number Start'),
    }
    
    _defaults = {  
        'show_all_products'     : True,
        'order_seq_start_from'  : 1,
    }
    
    def _check_order_seq_start_from(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context)
        return obj.order_seq_start_from > 0
    
    _constraints = [
        (_check_order_seq_start_from, 'Order Number Start must be be higher than zero', []),
    ]
    
pos_config()

class pos_order(osv.osv):
    _name = "pos.order"
    _inherit = "pos.order"
    _description = "Point of Sale"
    
    def create_from_ui(self, cr, uid, orders, context=None):
        order_ids = super(pos_order, self).create_from_ui(cr, uid, orders, context=context)
        orders_saved = self.read(cr, uid, order_ids, ['pos_reference'], context=context)
        
        for order_saved in orders_saved:
            for o in orders:
                order = {}
                if o['data']['name'] == order_saved['pos_reference']: 
                    order = o['data']
                vals = {
                    'card_type': order.get('card_type', False),
                    'partner_id': order.get('customer', False),
                    'iva_compensation': order.get('iva_compensation', 0.0),                    
                }
                
                super(pos_order, self).write(cr, uid, [order_saved['id']], vals, context=context)
        
        return order_ids
    
    def _get_type_journal(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        if not ids:
            return res
        for i in self.browse(cr,uid,ids):
            if i.statement_ids:
                for j in i.statement_ids:
                    if j.journal_id.card_payment:
                        res[i.id] = True
                    else:
                        res[i.id] = False
            else:
                res[i.id] = False
        return res
    
    def _amount_all_upd(self, cr, uid, ids, name, args, context=None):
        
        cur_obj = self.pool.get('res.currency')
        res = {}
        
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_paid'       : 0.0,
                'amount_return'     : 0.0,
                'amount_tax'        : 0.0,
                'amount_iva_comp'   : 0.0,
            }
            
            val1 = val2 = val3 = 0.0
            cur = order.pricelist_id.currency_id
            
            for payment in order.statement_ids:
                res[order.id]['amount_paid'] +=  payment.amount
                res[order.id]['amount_return'] += (payment.amount < 0 and payment.amount or 0)
            
            for line in order.lines:
                val1 += line.price_subtotal_incl
                val2 += line.price_subtotal
                val3 += line.iva_compensation
            
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val1-val2)
            res[order.id]['amount_iva_comp'] = cur_obj.round(cr, uid, cur, val3)
            res[order.id]['amount_total'] = cur_obj.round(cr, uid, cur, val1)
            
        return res
    
    _columns = {
        'card_payment'          : fields.function(_get_type_journal, method=True, type='boolean', string='Credit Card Payment', store=False),
        'acquirer'              : fields.many2one('res.bank', 'Acquirer'),
        'card_type'             : fields.many2one('pos.credit.card', 'Card Type'),
        'card_number'           : fields.char('Card Number', size=16),
        'approval_number'       : fields.char('Approbal Number', size=9),
        'lot_number'            : fields.char('Lot Number', size=6),
        'reference'             : fields.char('Reference', size=6),         
        
        # IVA Compensation for all products in the order...
        'iva_compensation'      : fields.float('IVA Compensation (%)', digits=(16, 2)),
        
        'amount_tax'            : fields.function(_amount_all_upd, string='Taxes', digits_compute=dp.get_precision('Point Of Sale'), multi='all'),
        'amount_total'          : fields.function(_amount_all_upd, string='Total', multi='all'),
        'amount_paid'           : fields.function(_amount_all_upd, string='Paid', states={'draft': [('readonly', False)]}, readonly=True, digits_compute=dp.get_precision('Point Of Sale'), multi='all'),
        'amount_return'         : fields.function(_amount_all_upd, 'Returned', digits_compute=dp.get_precision('Point Of Sale'), multi='all'),
        'amount_iva_comp'       : fields.function(_amount_all_upd, string='IVA Compensation', multi='all'),
       
    }
    
    def create(self, cr, uid, vals, context=None):        
        seq_number = 0
        config = self.pool.get('pos.session').browse(cr, uid, vals['session_id']).config_id
        if vals.get('pos_reference'):
            seq_number = int(vals['pos_reference'].split(' ')[-1].strip())
        else:            
            vals['pos_reference'] = 'Order ' + str(config.order_seq_start_from)
        order_id = super(pos_order, self).create(cr, uid, vals, context=context)
        self.pool.get('pos.config').write(cr, uid, [config.id],{'order_seq_start_from' : seq_number + 1})
        return order_id
    
    def action_invoice(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        inv_ref = self.pool.get('account.invoice')
        inv_line_ref = self.pool.get('account.invoice.line')
        product_obj = self.pool.get('product.product')
        inv_ids = []

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
                'currency_id': order.pricelist_id.currency_id.id, # considering partner's sale pricelist's currency
                'iva_compensation_persent': order.iva_compensation,
            }
            inv.update(inv_ref.onchange_partner_id(cr, uid, [], 'out_invoice', order.partner_id.id)['value'])
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
                    'iva_compensation': line.iva_compensation,
                }
                inv_name = product_obj.name_get(cr, uid, [line.product_id.id], context=context)[0][1]
                inv_line.update(inv_line_ref.product_id_change(cr, uid, [],
                                                               line.product_id.id,
                                                               line.product_id.uom_id.id,
                                                               line.qty, partner_id = order.partner_id.id,
                                                               fposition_id=order.partner_id.property_account_position.id)['value'])
                if line.product_id.description_sale:
                    inv_line['note'] = line.product_id.description_sale
                inv_line['price_unit'] = line.price_unit
                inv_line['discount'] = line.discount
                inv_line['name'] = inv_name
                inv_line['invoice_line_tax_id'] = [(6, 0, [x.id for x in line.product_id.taxes_id] )]
                inv_line_ref.create(cr, uid, inv_line, context=context)
            inv_ref.button_reset_taxes(cr, uid, [inv_id], context=context)
            wf_service.trg_validate(uid, 'pos.order', order.id, 'invoice', cr)

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
    
pos_order()

class pos_order_line(osv.osv):
    _inherit = "pos.order.line"
    
    def create(self, cr, uid, vals, context={}):
        vals['iva_compensation'] = vals['iva_compensation'] * vals['qty']
        res_id = super(pos_order_line, self).create(cr, uid, vals, context)
        return res_id
    
    def _amount_line_all_updated(self, cr, uid, ids, field_names, arg, context=None):
        res = dict([(i, {}) for i in ids])
        account_tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        
        for line in self.browse(cr, uid, ids, context=context):
            taxes_ids = [ tax for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id ]
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) - line.iva_compensation / line.qty
            taxes = account_tax_obj.compute_all(cr, uid, taxes_ids, price, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)

            cur = line.order_id.pricelist_id.currency_id
            res[line.id]['price_subtotal'] = cur_obj.round(cr, uid, cur, taxes['total'])
            res[line.id]['price_subtotal_incl'] = cur_obj.round(cr, uid, cur, taxes['total_included'])
        return res
    
    _columns = {
        'iva_compensation'      : fields.float('IVA Compensation', digits=(16, 2)),
        'price_subtotal'        : fields.function(_amount_line_all_updated, multi='pos_order_line_amount', string='Subtotal w/o Tax', store=True),
        'price_subtotal_incl'   : fields.function(_amount_line_all_updated, multi='pos_order_line_amount', string='Subtotal', store=True),
    }
pos_order_line()