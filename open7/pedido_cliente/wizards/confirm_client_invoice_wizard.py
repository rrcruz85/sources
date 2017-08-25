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

class confirm_client_invoice_wizard(osv.osv_memory):
    _name = 'confirm.client.invoice.wizard'
    _description = 'Confirm Invoice'

    _columns = {
        'pedido_id'      : fields.many2one('pedido.cliente','Pedido'),
        'client_id'    : fields.many2one('res.partner','Client'),
        'date_invoice': fields.date('Invoice Date', help="Keep empty to use the current date"),
        'account_id'     : fields.many2one('account.account', 'Account To Pay Supplier', domain=[('type','=','payable')]),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position'),
        'period_id'      : fields.many2one('account.period', 'Fiscal Period', domain=[('state','<>','done')],),
        'currency_id'    : fields.many2one('res.currency', 'Currency'),
        'journal_id'     : fields.many2one('account.journal', 'Journal', domain=[('type','=','purchase')]),
        'company_id'     : fields.many2one('res.company', 'Company'),
        'user_id'        : fields.many2one('res.users', 'Salesperson'),
        'line_ids'       : fields.one2many('confirm.client.invoice.line.wizard','invoice_id','Invoice Lines'),
        'next'    : fields.boolean('Next?'),
        'confirmada'    : fields.boolean('Confirmada'),
    }

    def _get_journal(self, cr, uid, context=None):
        if context is None:
            context = {}
        type_inv = context.get('type', 'in_invoice')
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        company_id = context.get('company_id', user.company_id.id)
        type2journal = {'out_invoice': 'sale', 'in_invoice': 'purchase', 'out_refund': 'sale_refund','in_refund': 'purchase_refund'}
        journal_obj = self.pool.get('account.journal')
        domain = [('company_id', '=', company_id)]
        if isinstance(type_inv, list):
            domain.append(('type', 'in', [type2journal.get(type) for type in type_inv if type2journal.get(type)]))
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

    def _default_account_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        if context.get('type') in ('out_invoice', 'out_refund'):
            prop = self.pool.get('ir.property').get(cr, uid, 'property_account_income_categ', 'product.category',context=context)
        else:
            prop = self.pool.get('ir.property').get(cr, uid, 'property_account_expense_categ', 'product.category',context=context)
        return prop and prop.id or False

    def _get_period(self, cr, uid, context=None):
        period = time.strftime('%m/%Y')
        period_ids = self.pool.get('account.period').search(cr, uid, [('name', '=', period)])
        if period_ids:
            return period_ids[0]
        return False

    _defaults = {
        'journal_id': _get_journal,
        'period_id': _get_period,
        'currency_id': _get_currency,
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid,'invoice.wizard',context=c),
        'user_id': lambda s, cr, u, c: u,
        'date_invoice': time.strftime('%Y-%m-%d'),
    }

    def _get_account_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        if context.get('type') in ('out_invoice', 'out_refund'):
            prop = self.pool.get('ir.property').get(cr, uid, 'property_account_income_categ', 'product.category',context=context)
        else:
            prop = self.pool.get('ir.property').get(cr, uid, 'property_account_expense_categ', 'product.category',context=context)
        return prop and prop.id or False

    def on_change_pedido(self, cr, uid, ids, pedido_id, context=None):
        res = {'value': {}}
        if pedido_id:
            list_vals = []
            pedido = self.pool.get('pedido.cliente').browse(cr, uid, pedido_id)
            res['value']['client_id'] = pedido.partner_id.id
            res['value']['account_id'] = pedido.partner_id.property_account_receivable.id if pedido.partner_id and pedido.partner_id.property_account_receivable else False
            res['value']['fiscal_position'] = pedido.partner_id.property_account_position.id if pedido.partner_id and pedido.partner_id.property_account_position else False
            res['value']['date_invoice'] = pedido.request_date

            p_ids = self.pool.get('confirm.client.invoice').search(cr,uid,[('pedido_id','=',pedido_id)])
            if p_ids:
                obj = self.pool.get('confirm.client.invoice').browse(cr, uid, p_ids[0])
                line = 1
                for v in obj.line_ids:
                    if v.detalle_id and not v.detalle_id.confirmada_cliente:
                        qty_bxs = float(v.qty) if v.is_box_qty else  float(v.qty) / (int(v.bunch_type) * v.bunch_per_box)
                        if qty_bxs < 1:
                            qty_bxs = 1
                        vals = {
                            'pedido_id': pedido_id,
                            'supplier_id': v.detalle_id.supplier_id.id,
                            'detalle_id': v.detalle_id.id,
                            'line_number': v.line_number if v.line_number else str(line),
                            'product_id': v.product_id.id,
                            'variant_id': v.variant_id.id,
                            'length': v.length,
                            'purchase_price': v.purchase_price,
                            'sale_price': v.sale_price,
                            'qty': v.qty,
                            'boxes': v.boxes,
                            'total_purchase': v.total_purchase,
                            'total_sale': v.total_sale,
                            'bunch_per_box': v.bunch_per_box,
                            'bunch_type': v.bunch_type,
                            'uom': v.uom,
                            'origin': v.origin.id if v.origin else False,
                            'subclient_id': v.subclient_id.id if v.subclient_id else False,
                            'sucursal_id': v.sucursal_id.id if v.sucursal_id else False,
                            'type': v.type if v.type else False,
                            'is_box_qty': v.is_box_qty,
                            'qty_bxs': str(qty_bxs) + ' ' + v.uom
                        }
                        list_vals.append((0, 0, vals))
                        line +=1

                if not list_vals:
                    warning = {
                        'title': 'Informacion',
                        'message': 'Para el pedido seleccionado ya todas las lineas han sido confirmadas.'
                    }
                    res['warning'] = warning

                res['value']['date_invoice'] = obj.date_invoice
                res['value']['account_id'] = obj.account_id.id
                res['value']['fiscal_position'] = obj.fiscal_position.id
                res['value']['period_id'] = obj.period_id.id
                res['value']['currency_id'] = obj.currency_id.id
                res['value']['journal_id'] = obj.journal_id.id
                res['value']['company_id'] = obj.company_id.id
                res['value']['user_id'] = obj.user_id.id
                res['value']['line_ids'] = list_vals
            else:
                product_accounts = []
                uom = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
                line = 1
                for v in pedido.purchase_line_ids:
                    account_id = v.product_id.property_account_expense.id if v.product_id.property_account_expense else False
                    if not account_id:
                        account_id = v.product_id.categ_id.property_account_expense_categ.id if v.product_id.categ_id and v.product_id.categ_id.property_account_expense_categ else False
                    qty_bxs = float(v.qty) if v.is_box_qty else  float(v.qty) / (int(v.bunch_type) * v.bunch_per_box)
                    if qty_bxs < 1:
                        qty_bxs = 1
                    boxes = qty_bxs / uom[v.uom]
                    vals = {
                        'pedido_id': pedido_id,
                        'supplier_id': v.supplier_id.id,
                        'detalle_id': v.id,
                        'line_number': str(line),
                        'product_id': v.product_id.id,
                        'variant_id': v.variant_id.id,
                        'length': v.lengths,
                        'purchase_price': v.purchase_price,
                        'sale_price': v.sale_price,
                        'qty': v.qty,
                        'boxes': boxes,
                        'total_purchase': v.qty * v.purchase_price if not v.is_box_qty else ((v.qty * v.bunch_per_box * int(v.bunch_type))) * v.purchase_price,
                        'total_sale': v.qty * v.sale_price if not v.is_box_qty else ((v.qty * v.bunch_per_box * int(v.bunch_type))) * v.sale_price,
                        'bunch_per_box': v.bunch_per_box,
                        'bunch_type': v.bunch_type,
                        'uom': v.uom,
                        'origin': v.origin.id if v.origin else False,
                        'subclient_id': v.subclient_id.id if v.subclient_id else False,
                        'sucursal_id': v.sucursal_id.id if v.sucursal_id else False,
                        'type': v.type if v.type else False,
                        'is_box_qty': v.is_box_qty,
                        'qty_bxs': str(qty_bxs) + ' ' + v.uom
                    }
                    line += 1
                    if not account_id and v.product_id.name_template not in product_accounts:
                        product_accounts.append(v.product_id.name_template)
                    list_vals.append((0, 0, vals))

                res['value']['line_ids'] = list_vals
                if not list_vals:
                    warning = {
                        'title': 'Informacion!',
                        'message': 'Para el pedido seleccionado ya todas las lineas han sido confirmadas.'
                    }
                    res['warning'] = warning

        # warning_msgs = ''
        # if not res['value']['account_id']:
        #     warning_msgs += 'El proveedor no tiene la cuenta de pagos configurada.\n'
        # if not res['value']['fiscal_position']:
        #     warning_msgs += 'El proveedor no tiene la posición fiscal configurada.\n'
        # if product_accounts:
        #     warning_msgs = 'Los siguientes productos ' + ','.join(list(product_accounts)) + ' no tienen una cuenta de gasto configurada.'
        # if warning_msgs:
        #     warning = {
        #            'title': _('Configuration Error!'),
        #            'message' : warning_msgs
        #     }
        #     res['warning'] = warning
        return res

    def confirm_invoice(self, cr, uid, ids, context=None):
        uom = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
        for o in self.browse(cr, uid, ids):
            if not o.line_ids:
                raise osv.except_osv('Error', "Debe especificar al menos una linea de confirmacion")

            lines = []
            p_ids = self.pool.get('confirm.client.invoice').search(cr,uid,[('pedido_id','=',o.pedido_id.id)])
            l_ids = []
            if p_ids:
                l_ids = self.pool.get('confirm.client.invoice.line').search(cr,uid,[('invoice_id','in',p_ids)])

            line = len(l_ids) + 1

            for l in o.line_ids:
                account_id = l.product_id.property_account_expense.id if l.product_id.property_account_expense else False
                if not account_id:
                    account_id = l.product_id.categ_id.property_account_expense_categ.id if l.product_id.categ_id and l.product_id.categ_id.property_account_expense_categ else False
                if not account_id:
                    raise osv.except_osv('Error',"El producto " + l.product_id.name_template + " no tiene una cuenta de gastos configurada.")
                boxes = l.qty if l.is_box_qty  else l.qty / (int(l.bunch_type) * l.bunch_per_box)
                if boxes < 1:
                    boxes = 1
                boxes = boxes/ uom[l.uom]
                vals = {
                    'pedido_id': l.invoice_id.pedido_id.id if l.invoice_id and l.invoice_id.pedido_id else False,
                    'detalle_id': l.detalle_id.id if l.detalle_id else False,
                    'supplier_id': l.supplier_id.id if l.supplier_id else False,
                    'line_number': l.line_number if l.line_number else str(line),
                    'product_id': l.product_id.id if l.product_id else False,
                    'variant_id': l.variant_id.id if l.variant_id else False,
                    'length': l.length,
                    'purchase_price': l.purchase_price,
                    'sale_price': l.sale_price,
                    'qty': l.qty,
                    'boxes':  boxes,
                    'total_purchase': l.qty * l.purchase_price if not l.is_box_qty else (l.qty * l.bunch_per_box * int(l.bunch_type)) * l.purchase_price,
                    'total_sale': l.qty * l.sale_price if not l.is_box_qty else (l.qty * l.bunch_per_box * int(l.bunch_type)) * l.sale_price,
                    'bunch_per_box': l.bunch_per_box,
                    'bunch_type': l.bunch_type,
                    'uom': l.uom,
                    'origin': l.origin.id if l.origin else False,
                    'subclient_id': l.subclient_id.id if l.subclient_id else False,
                    'sucursal_id': l.sucursal_id.id if l.sucursal_id else False,
                    'type': l.type if l.type else False,
                    'is_box_qty': l.is_box_qty,
                }
                lines.append((0, 0, vals))
                line += 1
                if l.detalle_id:
                    self.pool.get('detalle.lines').write(cr, uid, [l.detalle_id.id], {'confirmada_cliente': True})

            if p_ids and l_ids:
                self.pool.get('confirm.client.invoice').write(cr, uid, p_ids, {
                    'pedido_id': o.pedido_id.id if o.pedido_id else False,
                    'date_invoice': o.date_invoice,
                    'account_id': o.account_id.id if o.account_id else False,
                    'fiscal_position': o.fiscal_position.id if o.fiscal_position else False,
                    'period_id': o.period_id.id if o.pedido_id else False,
                    'currency_id': o.currency_id.id if o.currency_id else False,
                    'journal_id': o.journal_id.id if o.journal_id else False,
                    'company_id': o.company_id.id if o.company_id else False,
                    'user_id': o.user_id.id if o.user_id else False,
                    'charge_account_id': o.property_account_receivable.id if o.property_account_receivable else False,
                    'taxpayer_type': o.property_account_position if o.property_account_position else False,
                    'line_ids': lines,
                })
            else:
                p_ids.append(self.pool.get('confirm.client.invoice').create(cr, uid, {
                    'pedido_id': o.pedido_id.id if o.pedido_id else False,
                    'date_invoice': o.date_invoice,
                    'account_id': o.account_id.id if o.account_id else False,
                    'fiscal_position': o.fiscal_position.id if o.fiscal_position else False,
                    'period_id': o.period_id.id if o.period_id else False,
                    'currency_id': o.currency_id.id if o.currency_id else False,
                    'journal_id': o.journal_id.id if o.journal_id else False,
                    'company_id': o.company_id.id if o.company_id else False,
                    'user_id': o.user_id.id if o.user_id else False,
                    'charge_account_id': o.property_account_receivable.id if o.property_account_receivable else False,
                    'taxpayer_type': o.property_account_position if o.property_account_position else False,
                    'line_ids': lines
                }))

            self.write(cr, uid, ids, {'confirmada': True})

        return {
            'name': 'Generate Supplier Invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'confirm.client.invoice.wizard',
            'type': 'ir.actions.act_window',
            'res_id': ids[0],
            'target': 'new',
            'context': {'lines': lines},
        }

        # return {
        #     'name': 'Confirmar',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'confirm.windows.wizard',
        #     'type': 'ir.actions.act_window',
        #     'target' : 'new',
        #     'context': {'default_confirm_id': p_ids[0]},
        # }

    def generate_invoice(self, cr, uid, ids, context=None):
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for o in self.browse(cr, uid, ids):
            if not o.confirmada:
                raise osv.except_osv('Error', "Debe confirmar primero las lineas de facturas")

            if not o.line_ids:
                raise osv.except_osv('Error', "Debe especificar al menos una linea de factura")

            lines = []
            sequence = 1
            for l in o.line_ids:
                account_id = l.product_id.property_account_expense.id if l.product_id.property_account_expense else False
                if not account_id:
                    account_id = l.product_id.categ_id.property_account_expense_categ.id if l.product_id.categ_id and l.product_id.categ_id.property_account_expense_categ else False
                if not account_id:
                    raise osv.except_osv('Error',"El producto " + l.product_id.name_template + " no tiene una cuenta de gastos configurada.")

                name = l.variant_id.name if l.variant_id else ''
                if l.length:
                    name += ' - ' + l.length

                if l.detalle_id and l.detalle_id.type == 'standing_order':
                    name = 'SO ' + name
                if l.detalle_id and l.detalle_id.type != 'standing_order':
                    name = 'OM ' + name

                taxes = [(4, t.id) for t in l.product_id.supplier_taxes_id]

                qty_bxs = l.qty if l.is_box_qty else float(l.qty)/(int(l.bunch_type) * l.bunch_per_box)
                boxes = float(qty_bxs)/uom[l.uom]
                qty_bxs = str(qty_bxs) + l.uom

                vals = {
                    'sequence_box': sequence,
                    'box': boxes,
                    'qty_bxs' : qty_bxs,
                    'name': name,
                    'uos_id': l.product_id.uom_id.id if l.product_id.uom_id else False,
                    'product_id': l.product_id.id,
                    'account_id': account_id,
                    'price_unit': l.sale_price,
                    'quantity': l.qty * l.bunch_per_box * int(l.bunch_type) if l.is_box_qty else l.qty,
                    'sequence': 10,
                    'uom': l.uom,
                    'bunch_type': l.bunch_type,
                    'invoice_line_tax_id': taxes,
                    'is_box_qty': l.is_box_qty,
                    'bunch_per_box': l.bunch_per_box,
                    'mark_id': l.subclient_id.id if l.subclient_id else False
                }
                lines.append((0, 0, vals))
                sequence += 1

            inv_vals = {
                'name': 'Invoice for ' + o.client_id.name,
                'type': 'out_invoice',
                'origin': 'Pedido #' + str(o.pedido_id.name),
                'reference_type': 'none',
                'state': 'draft',
                'date_invoice': o.date_invoice,
                'partner_id': o.client_id.id,
                'account_id': o.account_id.id,
                'journal_id': o.journal_id.id if o.journal_id else None,
                'period_id': o.period_id.id if o.period_id else None,
                'fiscal_position': o.fiscal_position.id if o.fiscal_position else None,
                'currency_id': o.currency_id.id if o.currency_id else None,
                'company_id': o.company_id.id if o.company_id else None,
                'invoice_line': lines,
                'user_id': o.user_id.id if o.user_id else None,
                'pedido_cliente_id': o.pedido_id.id if o.pedido_id else None,
                'charge_account_id': o.property_account_receivable.id if o.property_account_receivable else False,
                'taxpayer_type': o.property_account_position if o.property_account_position else False,
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

confirm_client_invoice_wizard()

class confirm_client_invoice_line_wizard(osv.osv_memory):
    _name = 'confirm.client.invoice.line.wizard'
    _description = 'Invoice Line'
    _rec_name = 'line_number'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.is_box_qty:
               res[obj.id] = str(obj.qty) + ' ' + obj.detalle_id.uom
            else:
               qty = int(obj.qty / (int(obj.bunch_type) * obj.bunch_per_box))
               if qty < 1:
                   qty = 1
               res[obj.id] = str(qty) + ' ' + obj.uom
        return res

    _columns = {
        'invoice_id'      : fields.many2one('confirm.client.invoice.wizard','Invoice'),
        'pedido_id'      : fields.many2one('pedido.cliente','Pedido'),
        'detalle_id'      : fields.many2one('detalle.lines','Detalle'),
        'supplier_id'    : fields.many2one('res.partner','Supplier'),

        'line_number'   : fields.char(size=128, string ='#', help='Line Number'),
        'product_id'      : fields.many2one('product.product','Product'),
        'variant_id'      : fields.many2one('product.variant','Variety',),
        'length'              : fields.char(size=128, string ='Length'),
        'purchase_price'  : fields.float('Purchase Price'),
        'sale_price'  : fields.float('Sale Price'),
        'qty'             : fields.integer('Qty', help = "Quantity"),
        'boxes'             : fields.float('Full Boxes'),
        'total_purchase'    : fields.float(string='Total'),
        'total_sale'    : fields.float(string='Total'),
        'bunch_per_box'   : fields.integer('Bunch per Box'),
        'bunch_type'      : fields.integer('Stems x Bunch'),
        'uom'              : fields.selection([('FB', 'FB'),
                                               ('HB', 'HB'),
                                               ('QB', 'QB'),
                                               ('OB', 'OB')], 'UOM'),
        'origin'                : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubCliente'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'type'                     : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'qty_bxs'                 : fields.function(_get_info, type='char', string='BXS'),
        'selected'               : fields.boolean('Selected'),
    }

    def on_change_vals(self, cr, uid, ids, qty,purchase_price,sale_price, uom,is_box_qty,bunch_per_box,bunch_type, context=None):
        uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
        qty_bxs = qty if is_box_qty else int(qty / (int(bunch_type) * bunch_per_box))
        if qty_bxs < 1:
            qty_bxs = 1
        boxes = float(qty_bxs) / uom_dict[uom] if uom else 0

        res = {'value':
                         {'boxes': boxes,
                           'total_purchase': qty * purchase_price if not is_box_qty else  (qty * int(bunch_type) * bunch_per_box) * purchase_price if bunch_type and bunch_per_box else 0 ,
                           'total_sale': qty * sale_price if not is_box_qty else (qty * int(bunch_type) * bunch_per_box) * sale_price if bunch_type and bunch_per_box else 0,
                           'qty_bxs':  str(qty_bxs) + ' ' + uom
                          }
        }
        return res

    def on_change_variety(self, cr, uid, ids, pedido_id, supplier_id, product_id,variety_id, context=None):
        res = {'value': {}}
        if pedido_id and supplier_id and product_id and variety_id:
            #Sale Price
            client_id = self.pool.get('pedido.cliente').read(cr,uid,pedido_id)['partner_id'][0]
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
                val_ids = self.pool.get('purchase.request.product.variant').search(cr, uid,[('template_id', '=', suppliers[0]),('product_id', '=', product_id),('variant_id', '=', variety_id)])
                if val_ids:
                    pv = self.pool.get('purchase.request.product.variant').browse(cr, uid, val_ids[0])
                    purchase_prices = [p.purchase_price for p in pv.length_ids]
                    lenghts = [p.length for p in pv.length_ids]
                    res['value']['purchase_price'] = sum(purchase_prices)/len(purchase_prices) if purchase_prices else 0
                    res['value']['length'] = '-'.join(lenghts)
        return res

    def get_default_line_number(self,cr, uid, context = None):
        if context and 'lines' in context:
            return len(context['lines']) +1
        else:
            return 0

    _defaults = {
        'bunch_per_box': 10,
        'bunch_type'   : 25,
        'uom'          : 'HB',
        'type'  : 'open_market',
        'pedido_id'    :  lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else False,
        'product_id'    :  lambda self, cr, uid, context : context['product_id'] if context and 'product_id' in context else False,
        'invoice_id'    :  lambda self, cr, uid, context : context['invoice_id'] if context and 'invoice_id' in context else False,
        'supplier_id'    :  lambda self, cr, uid, context : context['supplier_id'] if context and 'supplier_id' in context else False,
        'line_number'  : get_default_line_number,
    }

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
           (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

confirm_client_invoice_line_wizard()




