
import time
import openerp
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def create(self, cr, user, vals, context=None):
        res_id = super(account_invoice, self).create(cr, user, vals, context)
        return res_id
    
    def _amount_all_upd(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = {
                'amount_iva_comp': 0.0,
                'amount_vat': 0.0,
                'amount_untaxed': 0.0, 
                'amount_tax': 0.0,
                'amount_tax_retention': 0.0,
                'amount_tax_ret_ir': 0.0,
                'taxed_ret_ir': 0.0, 
                'amount_tax_ret_vatb': 0.0,
                'amount_tax_ret_vatsrv': 0.00,
                'taxed_ret_vatb': 0.0,
                'taxed_ret_vatsrv': 0.00,
                'amount_vat_cero': 0.0,
                'amount_novat': 0.0, 
                'amount_noret_ir': 0.0,
                'amount_total': 0.0,
                'amount_pay': 0.0,
                'invoice_discount': 0,
                'amount_discounted': 0.0,
                'amount_ice': 0.0,
                'amount_compensa': 0.0,
                'payment_form': 0.0,
            }
            
            #Total General
            not_discounted = 0
            for line in invoice.invoice_line:
                res[invoice.id]['amount_untaxed'] += line.price_subtotal
                res[invoice.id]['amount_iva_comp'] += line.iva_compensation
                if res[invoice.id]['amount_untaxed'] == 0:
                    res[invoice.id]['invoice_discount'] = 0
                if (line.quantity * line.price_unit) - line.price_subtotal > 0.00:
                    res[invoice.id]['amount_discounted'] += (line.quantity * line.price_unit) - line.price_subtotal
                    
            for line in invoice.tax_line:
                if line.tax_group == 'vat':
                    #res[invoice.id]['amount_tax'] += line.amount
                    res[invoice.id]['amount_tax'] += line.base * float(invoice.iva_percent) / 100
                    res[invoice.id]['amount_vat'] += line.base
                elif line.tax_group == 'vat0':
                    res[invoice.id]['amount_vat_cero'] += line.base
                elif line.tax_group == 'novat':
                    res[invoice.id]['amount_novat'] += line.base
                elif line.tax_group == 'no_ret_ir':
                    res[invoice.id]['amount_noret_ir'] += line.base
                elif line.tax_group in ['ret_vat_b', 'ret_vat_srv', 'ret_ir']:
                    res[invoice.id]['amount_tax_retention'] += line.amount
                    if line.tax_group == 'ret_vat_b':#in ['ret_vat_b', 'ret_vat_srv']:
                        res[invoice.id]['amount_tax_ret_vatb'] += line.base
                        res[invoice.id]['taxed_ret_vatb'] += line.amount
                    elif line.tax_group == 'ret_vat_srv':
                        res[invoice.id]['amount_tax_ret_vatsrv'] += line.base
                        res[invoice.id]['taxed_ret_vatsrv'] += line.amount                        
                    elif line.tax_group == 'ret_ir':
                        if line.tax_code_id.code == '604':
                            res[invoice.id]['amount_compensa'] += abs(line.amount)
                        res[invoice.id]['amount_tax_ret_ir'] += line.base
                        res[invoice.id]['taxed_ret_ir'] += line.amount
                elif line.tax_group == 'ice':
                    res[invoice.id]['amount_ice'] += line.amount
            #if res[invoice.id]['amount_vat'] == 0 and res[invoice.id]['amount_vat_cero'] == 0:
            #    res[invoice.id]['amount_vat'] = res[invoice.id]['amount_untaxed']

            res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed'] \
                                            + res[invoice.id]['amount_tax_retention'] + res[invoice.id]['amount_ice']
            res[invoice.id]['amount_pay']  = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']

        return res
    
    def _get_invoice_tax(self, cr, uid, ids, context=None):
        result = {}
        for tax in self.pool.get('account.invoice.tax').browse(cr, uid, ids, context=context):
            result[tax.invoice_id.id] = True
        return result.keys()
    
    def _get_invoice_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids, context=context):
            result[line.invoice_id.id] = True
        return result.keys()
    
    _columns = {
        'amount_iva_comp'       : fields.function(_amount_all_upd, string='IVA Compensation', multi='all'),
        'amount_untaxed'        : fields.function(_amount_all_upd, digits_compute=dp.get_precision('Account'), string='Subtotal', track_visibility='always',
                                    store={
                                        'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                                        'account.invoice.tax': (_get_invoice_tax, None, 20),
                                        'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
                                    }, multi='all'),
        'amount_tax'            : fields.function(_amount_all_upd, digits_compute=dp.get_precision('Account'), string='Tax',
                                    store={
                                        'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                                        'account.invoice.tax': (_get_invoice_tax, None, 20),
                                        'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
                                    }, multi='all'),
        'amount_total'          : fields.function(_amount_all_upd, digits_compute=dp.get_precision('Account'), string='Total',
                                    store={
                                        'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                                        'account.invoice.tax': (_get_invoice_tax, None, 20),
                                        'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
                                    }, multi='all'),
    }
account_invoice()

class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'
    
    def create(self, cr, user, vals, context=None):
        res_id = super(account_invoice_line, self).create(cr, user, vals, context)
        return res_id
    
    def _amount_line(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        
        for line in self.browse(cr, uid, ids):
            price = line.price_unit * (1-(line.discount or 0.0)/100.0)
            taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, line.quantity, product=line.product_id, partner=line.invoice_id.partner_id)
            res[line.id] = taxes['total'] - line.iva_compensation
            
            if line.invoice_id:
                cur = line.invoice_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
        
        return res
    
    _columns = {
        'iva_compensation'      : fields.float('IVA Compensation', digits=(16, 2)),
        'price_subtotal'        : fields.function(_amount_line, string='Amount', type="float", digits_compute= dp.get_precision('Account'), store=False),
    }
account_invoice_line()

"""
class account_invoice_tax(osv.osv):
    _inherit = "account.invoice.tax"
    
    def create(self, cr, user, vals, context=None):
        res_id = super(account_invoice_tax, self).create(cr, user, vals, context)
        return res_id
    
    def compute(self, cr, uid, invoice_id, context=None):
        tax_grouped = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        inv = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=context)
        
        cur = inv.currency_id
        company_currency = self.pool['res.company'].browse(cr, uid, inv.company_id.id).currency_id.id
        
        for line in inv.invoice_line:
            for tax in tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, (line.price_unit* (1-(line.discount or 0.0)/100.0)) - line.iva_compensation, line.quantity, line.product_id, inv.partner_id)['taxes']:
                val={}
                val['invoice_id'] = inv.id
                val['name'] = tax['name']
                val['amount'] = tax['amount']
                val['manual'] = False
                val['sequence'] = tax['sequence']
                val['base'] = cur_obj.round(cr, uid, cur, tax['price_unit'] * line['quantity'])

                if inv.type in ('out_invoice','in_invoice'):
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['base'] * tax['base_sign'], context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    val['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['amount'] * tax['tax_sign'], context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    val['account_id'] = tax['account_collected_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_collected_id']
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['base'] * tax['ref_base_sign'], context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    val['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['amount'] * tax['ref_tax_sign'], context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    val['account_id'] = tax['account_paid_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_paid_id']

                key = (val['tax_code_id'], val['base_code_id'], val['account_id'], val['account_analytic_id'])
                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for t in tax_grouped.values():
            t['base'] = cur_obj.round(cr, uid, cur, t['base'])
            t['amount'] = cur_obj.round(cr, uid, cur, t['amount'])
            t['base_amount'] = cur_obj.round(cr, uid, cur, t['base_amount'])
            t['tax_amount'] = cur_obj.round(cr, uid, cur, t['tax_amount'])
        
        return tax_grouped

account_invoice_tax()
"""