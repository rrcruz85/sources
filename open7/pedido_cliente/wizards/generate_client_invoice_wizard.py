# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from osv import osv
from osv import fields
import time

class invoice_client_wizard(osv.osv_memory):
    _name = 'invoice.client.wizard'
    _description = 'Generate Invoice'

    _columns = {
        'pedido_id'         : fields.many2one('pedido.cliente', 'Pedido'),
        'client_id'         : fields.many2one('res.partner', 'Client'),
        'account_id'        : fields.many2one('account.account', 'Account Receivable', domain=[('type', '=', 'receivable')]),
        'fiscal_position'   : fields.many2one('account.fiscal.position', 'Fiscal Position'),
        'period_id'         : fields.many2one('account.period', 'Fiscal Period', domain=[('state', '<>', 'done')], ),
        'currency_id'       : fields.many2one('res.currency', 'Currency'),
        'journal_id'        : fields.many2one('account.journal', 'Journal', domain=[('type', '=', 'purchase')]),
        'company_id'        : fields.many2one('res.company', 'Company'),
        'user_id'           : fields.many2one('res.users', 'Salesperson'),
        'line_ids'          : fields.one2many('invoice.client.line.wizard', 'invoice_id', 'Sale Lines'),         
        'date_invoice'      : fields.date('Invoice Date', help="Keep empty to use the current date"),
    }

    def _get_journal(self, cr, uid, context=None):
        if context is None:
            context = {}
        type_inv = context.get('type', 'in_invoice')
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        company_id = context.get('company_id', user.company_id.id)
        type2journal = {'out_invoice': 'sale', 'in_invoice': 'purchase', 'out_refund': 'sale_refund',
                        'in_refund': 'purchase_refund'}
        journal_obj = self.pool.get('account.journal')
        domain = [('company_id', '=', company_id)]
        if isinstance(type_inv, list):
            domain.append(('type', 'in', [type2journal.get(t) for t in type_inv if type2journal.get(t)]))
        else:
            domain.append(('type', '=', type2journal.get(type_inv, 'sale')))
        res = journal_obj.search(cr, uid, domain, limit=1)
        return res and res[0] or False

    def _get_currency(self, cr, uid, context=None):
        res = False
        journal_id = self._get_journal(cr, uid, context=context)
        if journal_id:
            journal = self.pool.get('account.journal').browse(cr, uid, journal_id, context=context)
            res = journal.currency and journal.currency.id or journal.company_id.currency_id.id
        return res

    def _default_account_id(self, cr, uid, client_id, context=None):
        if context is None:
            context = {}
        if context.get('type') in ('out_invoice', 'out_refund'):
            prop = self.pool.get('ir.property').get(cr, uid, 'property_account_income_categ', 'product.category',
                                                    context=context)
        else:
            prop = self.pool.get('ir.property').get(cr, uid, 'property_account_expense_categ', 'product.category',
                                                    context=context)
        return prop and prop.id or False

    def _get_period(self, cr, uid, context=None):
        period = time.strftime('%m/%Y')
        period_ids = self.pool.get('account.period').search(cr, uid, [('name', '=', period)])
        if period_ids:
            return period_ids[0]
        return False

    _defaults = {
        'journal_id'    : _get_journal,
        'period_id'     : _get_period,
        'currency_id'   : _get_currency,
        'company_id'    : lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid,'invoice.wizard',context=c),
        'user_id'       : lambda s, cr, u, c: u,
        'date_invoice'  : time.strftime('%Y-%m-%d'),
    }

    def on_change_pedido(self, cr, uid, ids, pedido_id, context=None):
        res = {'value': {}}
        if pedido_id:
            lines_confirmed = self.pool.get('detalle.lines').search(cr, uid, [('pedido_id', '=', pedido_id)], order = 'name')
            if lines_confirmed:
                uom = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
                list_vals = []
                lines = self.pool.get('detalle.lines').browse(cr, uid, lines_confirmed)
                for l in lines:                
                    if l.agrupada:
                        cr.execute("select sum(dl.bunch_per_box) from detalle_lines dl where dl.group_id =" + str(l.group_id) + " and dl.active = true and dl.agrupada = true and dl.pedido_id = " + str(pedido_id) + 
                                    " and dl.supplier_id = " + str(l.supplier_id.id) + " and dl.product_id = " + str(l.product_id.id) +
                                    " group by dl.group_id, dl.pedido_id, dl.supplier_id, dl.product_id")            
                        record = cr.fetchone()
                        totals = record[0] if record else 0                        
                        qty_bxs = round(float(l.bunch_per_box)/totals, 2) if totals else 0
                    else:
                        qty_bxs = l.qty if l.is_box_qty else (1 if not (l.qty /(int(l.bunch_type) * l.bunch_per_box)) else (l.qty / (int(l.bunch_type) * l.bunch_per_box)))
                    
                    vals = {
                        'pedido_id'     : pedido_id,
                        'supplier_id'   : l.supplier_id.id,
                        'detalle_id'    : l.id,
                        'line_number'   : l.name,
                        'product_id'    : l.product_id.id if l.product_id else False,
                        'variant_id'    : l.variant_id.id if l.variant_id else False,
                        'length'        : l.lengths,
                        'purchase_price': l.purchase_price,
                        'sale_price'    : l.sale_price,
                        'qty'           : l.qty,
                        'boxes'         : qty_bxs/uom[l.uom],
                        'total_purchase': l.qty * l.purchase_price if not l.is_box_qty else ((l.qty * l.bunch_per_box * int(l.bunch_type))) * l.purchase_price,
                        'total_sale'    : l.qty * l.sale_price if not l.is_box_qty else ((l.qty * l.bunch_per_box * int(l.bunch_type))) * l.sale_price,
                        'bunch_per_box' : l.bunch_per_box,
                        'bunch_type'    : l.bunch_type,
                        'uom'           : l.uom,
                        'origin'        : l.origin.id if l.origin else False,
                        'subclient_id'  : l.subclient_id.id if l.subclient_id else False,
                        'sucursal_id'   : l.sucursal_id.id if l.sucursal_id else False,
                        'type'          : l.type if l.type else False,
                        'is_box_qty'    : l.is_box_qty,
                        'qty_bxs'       : str(qty_bxs) + ' ' + l.uom,
                        'box_id'        : l.box_id.id if l.box_id else False,
                        'box'           : l.box_id.box if l.box_id else False,
                    }
                    list_vals.append((0, 0, vals))
                res['value']['line_ids'] = list_vals
            res['value']['client_id'] =  self.pool.get('pedido.cliente').read(cr, uid, pedido_id,['partner_id'])['partner_id'][0]     
        return res
    
    def generate_invoice(self, cr, uid, ids, context=None):
        uom = {'FB':1, 'HB':2, 'QB':4, 'OB':8}
        obj = self.browse(cr, uid, ids[0])        
        lines_not_confirmed = self.pool.get('detalle.lines').search(cr, uid, [('pedido_id', '=', obj.pedido_id.id),('box_id', '=', False)])
        if lines_not_confirmed:
            records = self.pool.get('detalle.lines').read(cr, uid, lines_not_confirmed, ['name'])
            lineas = ','.join(map(lambda r: r['name'], records))
            raise osv.except_osv('Error',"Las siguientes lineas:[" + lineas + "] no tienen un id de caja asignado")
       
        lines = []
        sequence = 1            
        for l in obj.line_ids:                     
                
                account_id = l.product_id.property_account_expense.id if l.product_id.property_account_expense else False
                if not account_id:
                    account_id = l.product_id.categ_id.property_account_expense_categ.id if l.product_id.categ_id and l.product_id.categ_id.property_account_expense_categ else False
                if not account_id:
                    raise osv.except_osv('Error', "El producto " + l.product_id.name_template + " no tiene una cuenta de gastos configurada.")
                
                name = l.variant_id.name if l.variant_id else ''
                if l.length:
                    name += ' - ' + l.length
                    
                if l.detalle_id and l.detalle_id.type == 'standing_order':
                    name = 'Standing Order ' + name
                if l.detalle_id and l.detalle_id.type != 'standing_order':
                    name = 'Open Market ' + name

                taxes = [(4, t.id) for t in l.product_id.supplier_taxes_id]
                        
                if l.detalle_id.agrupada:
                    cr.execute("select sum(dl.bunch_per_box) from detalle_lines dl where dl.group_id =" + str(l.detalle_id.group_id) + " and dl.active = true and dl.agrupada = true and dl.pedido_id = " + str(l.pedido_id.id) + 
                                " and dl.supplier_id = " + str(l.supplier_id.id) + " and dl.product_id = " + str(l.product_id.id) + 
                                " group by dl.group_id, dl.pedido_id, dl.supplier_id, dl.product_id")            
                    record = cr.fetchone()
                    totals = record[0] if record else 0                        
                    qty_bxs = round(float(l.bunch_per_box) / totals, 2) if totals else 0
                else:
                    qty_bxs = l.qty if l.is_box_qty else (1 if not (l.qty / (int(l.bunch_type) * l.bunch_per_box)) else (l.qty / (int(l.bunch_type) * l.bunch_per_box)))
                    
                boxes = float(qty_bxs) / uom[l.uom]                        
                stems = l.qty if not l.is_box_qty else l.qty * int(l.bunch_type) * l.bunch_per_box

                hb_qty = 0
                qb_qty = 0
                if l.uom == 'FB':
                    hb_qty = boxes * 2
                if l.uom == 'OB':
                    hb_qty = boxes * 8
                if l.uom == 'HB':
                    hb_qty = l.qty if l.is_box_qty else qty_bxs
                if l.uom == 'QB':
                    qb_qty = l.qty if l.is_box_qty else qty_bxs 

                vals = {
                    'sequence_box'          : l.box_id.box if l.box_id else sequence,
                    'stems'                 : stems,
                    'box'                   : boxes,
                    'hb'                    : hb_qty,
                    'qb'                    : qb_qty,
                    'qty_bxs'               : str(qty_bxs) + ' ' + l.uom,
                    'name'                  : name,
                    'uos_id'                : l.product_id.uom_id.id if l.product_id.uom_id else False,
                    'product_id'            : l.product_id.id,
                    'account_id'            : account_id,
                    'price_unit'            : l.purchase_price,
                    'quantity'              : l.qty * l.bunch_per_box * int(l.bunch_type) if l.is_box_qty else l.qty,
                    'sequence'              : 10,
                    'uom'                   : l.uom,
                    'bunch_type'            : l.bunch_type,
                    'invoice_line_tax_id'   : taxes,
                    'is_box_qty'            : l.is_box_qty,
                    'bunch_per_box'         : l.bunch_per_box,
                    'mark_id'               : l.subclient_id.id if l.subclient_id else False
                }
                
                lines.append((0, 0, vals))
                sequence += 1
        client = self.pool.get('pedido.cliente').read(cr, uid, obj.pedido_id.id, ['partner_id'])['partner_id']
        inv_vals = {
            'name'              : 'Invoice for ' + client[1],
            'type'              : 'out_invoice',
            'origin'            : 'Pedido #' + str(obj.pedido_id.name),
            'reference_type'    : 'none',
            'state'             : 'draft',
            'date_invoice'      : obj.date_invoice,
            'partner_id'        : client[0],
            'account_id'        : obj.account_id.id,
            'journal_id'        : obj.journal_id.id if obj.journal_id else None,
            'period_id'         : obj.period_id.id if obj.period_id else None,
            'fiscal_position'   : obj.fiscal_position.id if obj.fiscal_position else None,
            'currency_id'       : obj.currency_id.id if obj.currency_id else None,
            'company_id'        : obj.company_id.id if obj.company_id else None,
            'invoice_line'      : lines,
            'user_id'           : obj.user_id.id if obj.user_id else None,
            'pedido_cliente_id' : obj.pedido_id.id if obj.pedido_id else None,
        }
        self.pool.get('account.invoice').create(cr, uid, inv_vals, context)

        return {
            'name': 'Customer Invoices',
            'view_type': 'form',
            'view_mode': 'tree,form,calendar,graph',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'domain': [('type', '=', 'out_invoice')],
            'context': {'default_type': 'out_invoice', 'type': 'out_invoice', 'journal_type': 'sale'},
        }    


invoice_client_wizard()


class invoice_client_line_wizard(osv.osv_memory):
    _name = 'invoice.client.line.wizard'
    _description = 'Invoice Client Line'
    _rec_name = 'line_number'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'qty_bxs':'','box': 0}
            if obj.is_box_qty:
                res[obj.id]['qty_bxs'] = str(obj.qty) + ' ' + obj.uom
            else:
                qty = obj.boxes * uom_dict[obj.uom] if obj.boxes else float(obj.qty)/ (int(obj.bunch_type) * obj.bunch_per_box)
                res[obj.id]['qty_bxs'] = str(qty) + ' ' + obj.uom
            res[obj.id]['box'] = obj.box_id.box if obj.box_id else False
        return res

    _columns = {
        'invoice_id'        : fields.many2one('invoice.client.wizard', 'Invoice'),
        'pedido_id'         : fields.many2one('pedido.cliente', 'Pedido'),        
        'detalle_id'        : fields.many2one('detalle.lines', 'Detalle'),
        'supplier_id'       : fields.many2one('res.partner', 'Supplier', domain=[('supplier', '=', True)]),

        'line_number'       : fields.char(size=128, string='#', help='Line Number'),
        'product_id'        : fields.many2one('product.product', 'Product'),
        'variant_id'        : fields.many2one('product.variant', 'Variety', ),
        'length'            : fields.char(size=128, string='Length'),
        'purchase_price'    : fields.float('Purchase Price'),
        'sale_price'        : fields.float('Sale Price'),
        'qty'               : fields.float('Qty', help="Quantity"),
        'boxes'             : fields.float('Full Boxes'),
        'total_purchase'    : fields.float(string='Total'),
        'total_sale'        : fields.float(string='Total'),
        'bunch_per_box'     : fields.integer('Bunch per Box'),
        'bunch_type'        : fields.integer('Stems x Bunch'),
        'uom'               : fields.selection([('FB', 'FB'),
                                 ('HB', 'HB'),
                                 ('QB', 'QB'),
                                 ('OB', 'OB')], 'UOM'),
        'origin'            : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'      : fields.many2one('res.partner', 'SubCliente'),
        'sucursal_id'       : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'type'              : fields.selection([('standing_order', 'Standing Order'), ('open_market', 'Open Market')], 'Order'),
        'is_box_qty'        : fields.boolean('Box Packing?'),
        'qty_bxs'           : fields.function(_get_info, type='char', string='BXS', multi='_vals'), 
        'box'               : fields.function(_get_info, type='integer', string='Box Id',multi='_vals'),        
        'mark_id'           : fields.many2one('res.partner', 'Marcacion'),
        'box_id'            : fields.many2one('detalle.lines.box', 'Box'), 
    }

    def on_change_vals(self, cr, uid, ids, qty, purchase_price, sale_price, uom, is_box_qty, bunch_per_box, bunch_type,context=None):
        uom_dict = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
        qty_bxs = qty if is_box_qty else int(qty / (int(bunch_type) * bunch_per_box))
        if qty_bxs < 1:
            qty_bxs = 1
        boxes = float(qty_bxs) / uom_dict[uom] if uom else 0
        res = {'value':
                   {'boxes': boxes,
                    'total_purchase': qty * purchase_price if not is_box_qty else  (qty * int(bunch_type) * bunch_per_box) * purchase_price if uom and bunch_type and bunch_per_box else 0,
                    'total_sale': qty * sale_price if not is_box_qty else (qty * int(bunch_type) * bunch_per_box) * sale_price if uom and bunch_type and bunch_per_box else 0,
                    'qty_bxs': str(qty_bxs) + ' ' + uom
                    }
               }
        return res

    def on_change_variety(self, cr, uid, ids, pedido_id, supplier_id, product_id, variety_id, context=None):
        res = {'value': {}}
        if pedido_id and supplier_id and product_id and variety_id:
            # Sale Price
            client_id = self.pool.get('pedido.cliente').read(cr, uid, pedido_id)['partner_id'][0]
            s_ids = self.pool.get('sale.request').search(cr, uid, [('partner_id', '=', client_id)])
            for s_id in s_ids:
                s_obj = self.pool.get('sale.request').browse(cr, uid, s_id)
                for s in s_obj.variant_ids:
                    if s.product_id.id == product_id and s.variant_id.id == variety_id:
                        sale_prices = [l.sale_price for l in s.length_ids]
                        res['value']['sale_price'] = sum(sale_prices) / len(sale_prices) if sale_prices else 0
                        break
                break

            # Purchase Price
            suppliers = self.pool.get('purchase.request.template').search(cr, uid, [('partner_id', '=', supplier_id)])
            if suppliers:
                val_ids = self.pool.get('purchase.request.product.variant').search(cr, uid,
                                                                                   [('template_id', '=', suppliers[0]),
                                                                                    ('product_id', '=', product_id),
                                                                                    ('variant_id', '=', variety_id)])
                if val_ids:
                    pv = self.pool.get('purchase.request.product.variant').browse(cr, uid, val_ids[0])
                    purchase_prices = [p.purchase_price for p in pv.length_ids]
                    lenghts = [p.length for p in pv.length_ids]
                    res['value']['purchase_price'] = sum(purchase_prices) / len(purchase_prices) if purchase_prices else 0
                    res['value']['length'] = '-'.join(lenghts)
        return res

    def get_default_line_number(self, cr, uid, context=None):
        if context and 'lines' in context:
            return len(context['lines']) + 1
        else:
            return 0

    _defaults = {
        'bunch_per_box': 12,
        'bunch_type': 25,
        'uom': 'HB',
        'type': 'open_market',
        'pedido_id': lambda self, cr, uid, context: context['pedido_id'] if context and 'pedido_id' in context else False,
        'product_id': lambda self, cr, uid, context: context['product_id'] if context and 'product_id' in context else False,
        'invoice_id': lambda self, cr, uid, context: context['invoice_id'] if context and 'invoice_id' in context else False,
        'supplier_id': lambda self, cr, uid, context: context['supplier_id'] if context and 'supplier_id' in context else False,
        'line_number': get_default_line_number,
    }

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context and context.get('invoice_id', False):
            ids = self.search(cr, uid, [('invoice_id', '=', context['invoice_id'])])
            return ids
        return super(invoice_client_line_wizard, self).search(cr, uid, args, offset, limit, order, context, count)

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

invoice_client_line_wizard()

