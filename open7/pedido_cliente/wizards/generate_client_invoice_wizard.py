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
        'pedido_id': fields.many2one('pedido.cliente', 'Pedido'),
        'client_id': fields.many2one('res.partner', 'Client'),
        'account_id': fields.many2one('account.account', 'Account Receivable', domain=[('type', '=', 'receivable')]),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position'),
        'period_id': fields.many2one('account.period', 'Fiscal Period', domain=[('state', '<>', 'done')], ),
        'currency_id': fields.many2one('res.currency', 'Currency'),
        'journal_id': fields.many2one('account.journal', 'Journal', domain=[('type', '=', 'purchase')]),
        'company_id': fields.many2one('res.company', 'Company'),
        'user_id': fields.many2one('res.users', 'Salesperson'),
        'line_ids': fields.one2many('invoice.client.line.wizard', 'invoice_id', 'Sale Lines'),
        'box_line_ids': fields.one2many('line.client.box.wizard', 'invoice_id', 'Invoice Lines per Box'),
        'next': fields.boolean('Next?'),
        'date_invoice': fields.date('Invoice Date', help="Keep empty to use the current date"),
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
        'journal_id': _get_journal,
        'period_id': _get_period,
        'currency_id': _get_currency,
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid,'invoice.wizard',context=c),
        'user_id': lambda s, cr, u, c: u,
        'date_invoice': time.strftime('%Y-%m-%d'),
    }

    def on_change_pedido(self, cr, uid, ids, pedido_id, context=None):
        res = {'value': {}}
        if pedido_id:
            pedido = self.pool.get('pedido.cliente').browse(cr, uid, pedido_id)
            p_ids = self.pool.get('confirm.invoice').search(cr, uid, [('pedido_id', '=', pedido_id)])
            if p_ids:
                confirmed_supplier_ids = [l.supplier_id.id for l in self.pool.get('confirm.invoice').browse(cr, uid, p_ids)]
                lines = self.pool.get('detalle.lines').search(cr, uid, [('pedido_id', '=', pedido_id)])
                line_ids = list(set([l.supplier_id.id for l in self.pool.get('detalle.lines').browse(cr, uid, lines)]))
                warning = {}
                not_confirmed_ids = list(set(line_ids) - set(confirmed_supplier_ids))
                if not_confirmed_ids:
                    names = [r['name'] for r in self.pool.get('res.partner').read(cr, uid, not_confirmed_ids, ['name'])]
                    warning = {
                        'title': " Error",
                        'message': "Para el pedido seleccionado no se han confirmado las lineas de factura de todos los proveedor. \nLos siguientes proveedores no han sido confirmados: " + ','.join(
                            names)
                    }
                list_vals = []
                if not warning:
                    uom = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
                    line = 1
                    for obj in self.pool.get('confirm.invoice').browse(cr, uid, p_ids):
                        for v in obj.line_ids:
                            qty_bxs = float(v.qty) if v.is_box_qty else  float(v.qty) / (
                                int(v.bunch_type) * v.bunch_per_box)
                            boxes = qty_bxs / uom[v.uom]
                            vals = {
                                'pedido_id': pedido_id,
                                'supplier_id': v.supplier_id.id if v.supplier_id else False,
                                'detalle_id': v.detalle_id.id if v.detalle_id else False,
                                'mark_id': v.detalle_id.subclient_id.id if v.detalle_id and v.detalle_id.subclient_id else False,
                                'line_number': str(line),
                                'product_id': v.product_id.id if v.product_id else False,
                                'variant_id': v.variant_id.id if v.variant_id else False,
                                'length': v.length,
                                'purchase_price': v.purchase_price,
                                'sale_price': v.sale_price,
                                'qty': v.qty,
                                'boxes': boxes,
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
                            line += 1
                            res['value']['account_id'] = pedido.partner_id.property_account_receivable.id if pedido.partner_id.property_account_receivable else None
                            res['value']['fiscal_position'] = pedido.partner_id.property_account_position.id if pedido.partner_id.property_account_position else None
                            # res['value']['date_invoice'] = obj.date_invoice
                            # res['value']['account_id'] = obj.account_id.id
                            # res['value']['fiscal_position'] = obj.fiscal_position.id
                            # res['value']['period_id'] = obj.period_id.id
                            # res['value']['currency_id'] = obj.currency_id.id
                            # res['value']['journal_id'] = obj.journal_id.id
                            # res['value']['company_id'] = obj.company_id.id
                            # res['value']['user_id'] = obj.user_id.id
                pedido = self.pool.get('pedido.cliente').browse(cr, uid, pedido_id)
                res['value']['client_id'] = pedido.partner_id.id
                res['value']['line_ids'] = list_vals
                res['value']['box_line_ids'] = []
                if warning:
                    res['warning'] = warning
            else:
                raise osv.except_osv('Error',"Para el pedido seleccionado no se ha confirmado ninguna factura para los proveedores.")
        return res

    def go_next(self, cr, uid, ids, context=None):

        obj = self.browse(cr, uid, ids[0])
        p_ids = self.pool.get('confirm.invoice').search(cr, uid, [('pedido_id', '=', obj.pedido_id.id)])
        if not p_ids:
            raise osv.except_osv('Error',
                                 "Para el pedido seleccionado no se ha confirmado ninguna factura para los proveedores.")
        else:
            confirmed_supplier_ids = [l.supplier_id.id for l in self.pool.get('confirm.invoice').browse(cr, uid, p_ids)]
            lines = self.pool.get('detalle.lines').search(cr, uid, [('pedido_id', '=', obj.pedido_id.id)])
            line_ids = list(set([l.supplier_id.id for l in self.pool.get('detalle.lines').browse(cr, uid, lines)]))
            not_confirmed_ids = list(set(line_ids) - set(confirmed_supplier_ids))
            if not_confirmed_ids:
                names = [r['name'] for r in self.pool.get('res.partner').read(cr, uid, not_confirmed_ids, ['name'])]
                raise osv.except_osv('Error',
                                     "Para el pedido seleccionado no se han confirmado las lineas de factura de todos los proveedor. \nLos siguientes proveedores no han sido confirmados: " + ','.join(
                                         names))

        if not context:
            context = {}
        context['default_next'] = True
        uom = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
        for o in self.browse(cr, uid, ids):
            i = 1
            for v in o.line_ids:
                qty_bxs = float(v.qty) if v.is_box_qty else float(v.qty) / (int(v.bunch_type) * v.bunch_per_box)
                boxes = qty_bxs / uom[v.uom]
                dict_vals = {
                    'line_number': str(i),
                    'boxes': boxes,
                    'total_purchase': v.qty * v.purchase_price if not v.is_box_qty else ((v.qty * v.bunch_per_box * int(
                        v.bunch_type)) / uom[v.uom]) * v.purchase_price,
                    'total_sale': v.qty * v.sale_price if not v.is_box_qty else ((v.qty * v.bunch_per_box * int(
                        v.bunch_type)) / uom[v.uom]) * v.sale_price,
                    'qty_bxs': str(qty_bxs) + ' ' + v.uom
                }
                self.pool.get('invoice.client.line.wizard').write(cr, uid, [v.id], dict_vals)
                i += 1

        self.write(cr, uid, ids,
                   {'next': True, 'client_id': obj.pedido_id.partner_id.id, 'pedido_id': obj.pedido_id.id})

        return {
            'name': 'Generate Client Invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'invoice.client.wizard',
            'type': 'ir.actions.act_window',
            'res_id': ids[0],
            'target': 'new',
            'context': context
        }

    def go_previous(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'next': False, 'box_line_ids': []})
        if not context:
            context = {}
        context['default_next'] = False
        context['default_box_line_ids'] = []
        return {
            'name': 'Generate Client Invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'invoice.wizard',
            'type': 'ir.actions.act_window',
            'res_id': ids[0],
            'target': 'new',
            'context': context
        }

    def generate_invoice(self, cr, uid, ids, context=None):
        uom = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
        for o in self.browse(cr, uid, ids):
            p_ids = self.pool.get('confirm.invoice').search(cr, uid, [('pedido_id', '=', o.pedido_id.id)])
            confirmed_supplier_ids = [l.supplier_id.id for l in self.pool.get('confirm.invoice').browse(cr, uid, p_ids)]
            lines = self.pool.get('detalle.lines').search(cr, uid, [('pedido_id', '=', o.pedido_id.id)])
            line_ids = list(set([l.supplier_id.id for l in self.pool.get('detalle.lines').browse(cr, uid, lines)]))
            not_confirmed_ids = list(set(line_ids) - set(confirmed_supplier_ids))
            if not_confirmed_ids:
                names = [r['name'] for r in self.pool.get('res.partner').read(cr, uid, not_confirmed_ids, ['name'])]
                raise osv.except_osv('Error',"Para el pedido seleccionado no se han confirmado las factura de todos los proveedor. \nLos siguientes proveedores no han sido confirmados: " + ','.join(names))

            lines = []
            sequence = 1
            if not o.box_line_ids:
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
                        name = 'Standing Order ' + name
                    if l.detalle_id and l.detalle_id.type != 'standing_order':
                        name = 'Open Market ' + name

                    taxes = [(4, t.id) for t in l.product_id.supplier_taxes_id]
                    qty_bxs = l.qty if l.is_box_qty else float(l.qty) / (int(l.bunch_type) * l.bunch_per_box)
                    boxes = float(qty_bxs) / uom[l.uom]
                    qty_bxs = str(qty_bxs) + l.uom

                    hb_qty = 0
                    qb_qty = 0
                    if l.uom == 'FB':
                        hb_qty = boxes * 2
                    if l.uom == 'OB':
                        hb_qty = boxes * 8
                    if l.uom == 'HB':
                        hb_qty = l.qty if l.is_box_qty else float(l.qty) / (int(l.bunch_type) * l.bunch_per_box)
                    if l.uom == 'QB':
                        qb_qty = l.qty if l.is_box_qty else float(l.qty) / (int(l.bunch_type) * l.bunch_per_box)

                    vals = {
                        'sequence_box': sequence,
                        'box': boxes,
                        'hb': hb_qty,
                        'qb': qb_qty,
                        'qty_bxs': qty_bxs,
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
                        'mark_id':  l.mark_id.id if l.mark_id else False
                    }
                    lines.append((0, 0, vals))
                    sequence += 1
            else:
                for v in o.box_line_ids:
                    for l in v.line_wzd_ids:

                        account_id = l.product_id.property_account_expense.id if l.product_id.property_account_expense else False
                        if not account_id:
                            account_id = l.product_id.categ_id.property_account_expense_categ.id if l.product_id.categ_id and l.product_id.categ_id.property_account_expense_categ else False
                        if not account_id:
                            raise osv.except_osv('Error',"El producto " + l.product_id.name_template + " no tiene una cuenta de gastos configurada.")

                        name = l.variant_id.name if l.variant_id else ''
                        if l.length:
                            name += ' - ' + l.length

                        if l.detalle_id and l.detalle_id.type == 'standing_order':
                            name = 'Standing Order ' + name
                        if l.detalle_id and l.detalle_id.type != 'standing_order':
                            name = 'Open Market ' + name

                        taxes = [(4, t.id) for t in l.product_id.supplier_taxes_id]

                        qty_bxs = l.qty if l.is_box_qty else float(l.qty) / (int(l.bunch_type) * l.bunch_per_box)
                        boxes = float(qty_bxs) / uom[l.uom]
                        qty_bxs = str(qty_bxs) + l.uom

                        hb_qty = 0
                        qb_qty = 0
                        if l.uom == 'FB':
                            hb_qty = boxes * 2
                        if l.uom == 'OB':
                            hb_qty = boxes * 8
                        if l.uom == 'HB':
                            hb_qty = l.qty if l.is_box_qty else float(l.qty) / (int(l.bunch_type) * l.bunch_per_box)
                        if l.uom == 'QB':
                            qb_qty = l.qty if l.is_box_qty else float(l.qty) / (int(l.bunch_type) * l.bunch_per_box)

                        vals = {
                            'sequence_box': sequence,
                            'box': boxes,
                            'hb': hb_qty,
                            'qb': qb_qty,
                            'qty_bxs': qty_bxs,
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
                            'mark_id':  l.mark_id.id if l.mark_id else False
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

    def on_change_box_line_ids(self, cr, uid, ids, box_line_ids, context=None):
        res = {'value': {}}
        selected = []
        if box_line_ids:
            for record in box_line_ids:
                if record[0] == 0:
                    for l in record[2]['line_wzd_ids']:
                        if l[0] == 6 and l[2]:
                            selected += l[2]
                            self.pool.get('invoice.client.line.wizard').write(cr, uid, l[2], {'selected': True})
        if ids:
            not_selected_ids = self.pool.get('invoice.client.line.wizard').search(cr, uid, [('invoice_id', '=', ids[0]),('id', 'not in', selected)])
            if not_selected_ids:
                self.pool.get('invoice.client.line.wizard').write(cr, uid, not_selected_ids, {'selected': False})
        return res

invoice_client_wizard()


class invoice_client_line_wizard(osv.osv_memory):
    _name = 'invoice.client.line.wizard'
    _description = 'Invoice Client Line'
    _rec_name = 'line_number'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.is_box_qty:
                res[obj.id] = str(obj.qty) + ' ' + obj.uom
            else:
                qty = float(obj.qty) / (int(obj.bunch_type) * obj.bunch_per_box)
                res[obj.id] = str(qty) + ' ' + obj.uom
        return res

    _columns = {
        'invoice_id': fields.many2one('invoice.client.wizard', 'Invoice'),
        'pedido_id': fields.many2one('pedido.cliente', 'Pedido'),
        'box_id': fields.many2one('line.client.box.wizard', 'Box'),
        'detalle_id': fields.many2one('detalle.lines', 'Detalle'),
        'supplier_id': fields.many2one('res.partner', 'Supplier', domain=[('supplier', '=', True)]),

        'line_number': fields.char(size=128, string='#', help='Line Number'),
        'product_id': fields.many2one('product.product', 'Product'),
        'variant_id': fields.many2one('product.variant', 'Variety', ),
        'length': fields.char(size=128, string='Length'),
        'purchase_price': fields.float('Purchase Price'),
        'sale_price': fields.float('Sale Price'),
        'qty': fields.float('Qty', help="Quantity"),
        'boxes': fields.float('Full Boxes'),
        'total_purchase': fields.float(string='Total'),
        'total_sale': fields.float(string='Total'),
        'bunch_per_box': fields.integer('Bunch per Box'),
        'bunch_type': fields.integer('Stems x Bunch'),
        'uom': fields.selection([('FB', 'FB'),
                                 ('HB', 'HB'),
                                 ('QB', 'QB'),
                                 ('OB', 'OB')], 'UOM'),
        'origin': fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id': fields.many2one('res.partner', 'SubCliente'),
        'sucursal_id': fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'type': fields.selection([('standing_order', 'Standing Order'), ('open_market', 'Open Market')], 'Order'),
        'is_box_qty': fields.boolean('Box Packing?'),
        'qty_bxs': fields.function(_get_info, type='char', string='BXS'),
        'selected': fields.boolean('Selected'),
        'mark_id': fields.many2one('res.partner', 'Marcacion'),
    }

    def on_change_vals(self, cr, uid, ids, qty, purchase_price, sale_price, uom, is_box_qty, bunch_per_box, bunch_type,context=None):
        uom_dict = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
        qty_bxs = qty if is_box_qty else int(qty / (int(bunch_type) * bunch_per_box))
        if qty_bxs < 1:
            qty_bxs = 1
        boxes = float(qty_bxs) / uom_dict[uom] if uom else 0
        res = {'value':
                   {'boxes': boxes,
                    'total_purchase': qty * purchase_price if not is_box_qty else  (qty * int(
                        bunch_type) * bunch_per_box) * purchase_price if uom and bunch_type and bunch_per_box else 0,
                    'total_sale': qty * sale_price if not is_box_qty else (qty * int(
                        bunch_type) * bunch_per_box) * sale_price if uom and bunch_type and bunch_per_box else 0,
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
                    res['value']['purchase_price'] = sum(purchase_prices) / len(
                        purchase_prices) if purchase_prices else 0
                    res['value']['length'] = '-'.join(lenghts)
        return res

    def get_default_line_number(self, cr, uid, context=None):
        if context and 'lines' in context:
            return len(context['lines']) + 1
        else:
            return 0

    _defaults = {
        'bunch_per_box': 10,
        'bunch_type': 25,
        'uom': 'HB',
        'type': 'open_market',
        'pedido_id': lambda self, cr, uid, context: context[
            'pedido_id'] if context and 'pedido_id' in context else False,
        'product_id': lambda self, cr, uid, context: context[
            'product_id'] if context and 'product_id' in context else False,
        'invoice_id': lambda self, cr, uid, context: context[
            'invoice_id'] if context and 'invoice_id' in context else False,
        'supplier_id': lambda self, cr, uid, context: context[
            'supplier_id'] if context and 'supplier_id' in context else False,
        'line_number': get_default_line_number,
    }

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context and context.get('invoice_id', False):
            ids = self.search(cr, uid, [('invoice_id', '=', context['invoice_id']), ('selected', '=', False)])
            return ids
        return super(invoice_client_line_wizard, self).search(cr, uid, args, offset, limit, order, context, count)

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

invoice_client_line_wizard()


class line_client_box_wizard(osv.osv_memory):
    _name = 'line.client.box.wizard'
    _description = 'Invoice Box Line'

    _columns = {
        'invoice_id': fields.many2one('invoice.client.wizard', 'Invoice'),
        'boxes': fields.integer('Boxes'),
        'line_wzd_ids': fields.many2many('invoice.client.line.wizard', 'box_line_client_relation', 'box_id', 'line_id','Invoice Lines'),
    }

    _defaults = {
        'boxes': 1,
        'invoice_id': lambda self, cr, uid, context: context['invoice_id'] if context and 'invoice_id' in context else False,
    }

line_client_box_wizard()

