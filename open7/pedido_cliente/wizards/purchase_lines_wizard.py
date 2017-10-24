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
import math
from openerp.tools.translate import _

class puchase_lines_wzd(osv.osv_memory):
    _name = 'purchase.lines.wzd'
    _description = 'Purchase Lines'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'total_qty_purchased': 'BXS', 'stimated_qty': 'BXS','qty':''}
            if obj.detalle_id.is_box_qty:
                res[obj.id]['total_qty_purchased'] = str(obj.purchased_qty) + ' BXS'
            else:
                res[obj.id]['total_qty_purchased'] = str(obj.purchased_qty) + ' Stems'

            bxs_qty = obj.purchased_qty if obj.detalle_id.is_box_qty else (1 if not (obj.purchased_qty / (int(obj.bunch_type) * obj.bunch_per_box)) else (obj.purchased_qty / (int(obj.bunch_type) * obj.bunch_per_box)))
            res[obj.id]['qty'] = str(bxs_qty) + ' ' + obj.uom
            full_boxes = float(bxs_qty)/uom[obj.uom]
            res[obj.id]['stimated_qty'] = full_boxes
        return res

    _columns = {
        'line'                    : fields.integer(string='#', help = 'Request Line'),
        'pedido_id'             : fields.many2one('pedido.cliente', 'Pedido',),
        'detalle_id'            : fields.many2one('detalle.lines', 'Detalle'),
        'type'                    : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'supplier_id'           : fields.many2one('res.partner', 'Farm',),
        'product_id'            : fields.many2one('product.product', 'Product'),
        'variant_id'            : fields.many2one('product.variant', 'Variety'),
        'lenght'                : fields.char(size = 128, string= 'Length'),
        'bunch_type'            : fields.char(size = 128, string= 'Stems x Bunch'),
        'uom'                   : fields.char(size = 128, string= 'UOM'),
        'bunch_per_box'         : fields.integer(string='Bunch Per Box'),
        'request_qty'           : fields.integer(string='Request Qty'),
        'purchased_qty'         : fields.integer(string='Purchased Qty'),
        'purchase_price'        : fields.char(size = 128, string= 'Purchase price'),
        'farm_total'            : fields.float(string= 'Farm total'),
        'sale_price'            : fields.char(size = 128, string= 'Sale price'),
        'total'                 : fields.float(string= 'Total'),
        'profit'                : fields.float(string= 'Profit'),
        'is_purchase'        : fields.boolean(string= 'Purchase'),
        'origin_id'             : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubCliente'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'total_qty_purchased'   : fields.function(_get_info, type='char', string='Purchased Qty', multi="_vals"),
        'qty'                        : fields.function(_get_info, type='char', string='BXS', multi = '_vals'),
        'stimated_qty'          : fields.function(_get_info, type='float', string='Full Boxes', multi="_vals"),
        'confirmada'            : fields.boolean(string='Confirmada'),
    }

    _order = "line"

    def delete_lines(self, cr, uid, ids, *args):
        obj = self.browse(cr,uid,ids[0])
        if obj.detalle_id.confirmada:
            raise osv.except_osv('Error', "Esta linea de compra no puede ser borrada porque ya fue confirmada.")

        self.pool.get('detalle.lines').unlink(cr, uid, [obj.detalle_id.id])
        return {
                'name'      : 'Pedidos de Clientes',
                'view_type' : 'form',
                'view_mode' : 'form,tree',
                'res_model' : 'pedido.cliente',
                'type'      : 'ir.actions.act_window',
                'res_id'    : obj.pedido_id.id,
               }

    def edit_lines(self, cr, uid, ids, *args):
        obj = self.browse(cr,uid,ids[0])
        detalle = obj.detalle_id

        if detalle.confirmada:
            raise osv.except_osv('Error', "Esta linea de compra no puede ser modificada porque ya fue confirmada.")

        lengths = [(0,0,{'length': l.length, 'purchase_price': l.purchase_price}) for l in detalle.length_ids]

        #Buscando Proveedores
        farm_ids = []
        l_ids = self.pool.get('purchase.request.template').search(cr,uid,[('client_id','=',obj.pedido_id.partner_id.id)])
        v_ids = self.pool.get('purchase.request.product.variant').search(cr,uid,[('template_id','in',l_ids), ('product_id','=',obj.product_id.id),('variant_id','=',obj.variant_id.id),('subclient_id','=',obj.subclient_id.id if obj.subclient_id else False)])
        if v_ids:
            for l in obj.detalle_id.length_ids:
                ll_ids = self.pool.get('purchase.request.product.variant.length').search(cr,uid,[('variant_id','in',v_ids),('length','=',l.length)])
                if ll_ids:
                    for ll in self.pool.get('purchase.request.product.variant.length').browse(cr,uid,ll_ids):
                        if ll.variant_id.template_id.partner_id.id not in farm_ids:
                            farm_ids.append(str(ll.variant_id.template_id.partner_id.id))

        context = {
            'default_detalle_id': obj.detalle_id.id,
            'default_confirmada': obj.detalle_id.confirmada,
            'default_cliente_id': obj.detalle_id.pedido_id.partner_id.id,
            'default_supplier_id': detalle.supplier_id.id if detalle.supplier_id else None,
            'default_type': detalle.type,
            'default_product_id': detalle.product_id.id,
            'default_variant_id': detalle.variant_id.id,
            'default_length_ids': lengths,
            'default_is_box_qty': detalle.is_box_qty,
            'default_box_qty': detalle.qty if detalle.is_box_qty else 0,
            'default_tale_qty': detalle.qty if not detalle.is_box_qty else 0,

            'default_bunch_type': detalle.bunch_type,
            'default_bunch_per_box': detalle.bunch_per_box,
            'default_uom': detalle.uom,

            'default_purchase_price': detalle.purchase_price,
            'default_sale_price': detalle.sale_price,
            'default_origin': detalle.origin.id if detalle.origin else False,
            'default_subclient_id': detalle.subclient_id.id if detalle.subclient_id else False,
            'default_sucursal_id': detalle.sucursal_id.id if detalle.sucursal_id else False,
            'default_supplier_ids': ','.join(farm_ids)
        }
        return {
            'name': _("Purchase Line"),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'detalle.line.wzd',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }

puchase_lines_wzd()


class detalle_line_wzd(osv.osv_memory):
    _name = 'detalle.line.wzd'
    _description = 'Detalle de compras'

    def _get_quantity(self, cr, uid, ids, field_name, arg, context):
        result = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            qty_bxs = obj.box_qty if obj.is_box_qty else (1 if not (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)) else (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)))
            qty = obj.box_qty * obj.bunch_per_box *  int(obj.bunch_type) if obj.is_box_qty else obj.tale_qty
            full_boxes = float(qty_bxs) / uom[obj.uom]
            prices = []
            for l in obj.length_ids:
                prices.append(l.purchase_price)
            purchase_price = sum(prices) / len(prices) if prices else 0

            result[obj.id] = {
                'total_purchase': qty * purchase_price,
                'total_sale': qty * obj.sale_price,
                'profit': qty * (obj.sale_price - purchase_price),
                'qty_bxs': str(qty_bxs) + ' ' + obj.uom,
                'full_boxes': full_boxes,
                'stimated_stems' : qty
            }
        return result

    _columns = {
        'detalle_id'            : fields.many2one('detalle.lines', 'Details'),
        'cliente_id'           : fields.related('detalle_id','pedido_id','partner_id', type ='many2one',relation = 'res.partner', string ='Cliente'),
        'type'                     : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'supplier_id'           : fields.many2one('res.partner', 'Farm', required=True, domain=[('supplier', '=', True)]),
        'product_id'            : fields.many2one('product.product', 'Product', required=True),
        'variant_id'            : fields.many2one('product.variant', 'Variety', required=True),
        'length_ids'            : fields.one2many('detalle.line.length.wzd','detalle_id','Lengths'),
       	'is_box_qty'            : fields.boolean('Box Packing?'),
        'box_qty'               : fields.integer('BXS'),
		'tale_qty'              : fields.integer('Stems'),
		'bunch_per_box'         : fields.integer('Bunch per Box'),
        'bunch_type'            : fields.integer('Stems x Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], string = 'UOM', help = 'Unit of Measure'),
        'sale_price'            : fields.float(string='Sale Price'),
        'origin'                : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubCliente'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'supplier_ids'            : fields.char(string='Supplier Ids', size = 128),
        'confirmada'            : fields.boolean(string='Confirmada'),

        'total_purchase'        : fields.function(_get_quantity, type='float', string='Farm Total', multi='compute_data'),
        'total_sale'            : fields.function(_get_quantity, type='float', string='Total', multi='compute_data'),
        'profit'                : fields.function(_get_quantity, type='float', string='Profit', multi='compute_data'),
        'full_boxes'            : fields.function(_get_quantity, type='float', string='Full Boxes', multi = '_data'),
        'qty_bxs'            : fields.function(_get_quantity, type='char', string='BXS', multi = '_data'),
        'stimated_stems'     : fields.function(_get_quantity, type='integer', string='Stems', multi = '_data'),
    }

    def on_chance_vals(self, cr, uid, ids, is_box_qty,box_qty,tale_qty, bunch_type,bunch_per_box, uom, sale_price, length_ids, context=None):
        result = {}
        qty = box_qty if is_box_qty else tale_qty
        if uom and bunch_type and bunch_per_box:
            uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
            qty_bxs = box_qty if is_box_qty else  (1 if not (tale_qty / (int(bunch_type) * bunch_per_box)) else  (tale_qty / (int(bunch_type) * bunch_per_box)))
            full_boxes = float(qty_bxs) / uom_dict[uom]
            prices = []
            for l in length_ids:
                prices.append(l[2]['purchase_price'])
            purchase_price = sum(prices)/len(prices) if prices else 0

            result['value'] = {
                'total_purchase': qty * purchase_price if not is_box_qty else qty * bunch_per_box *  int(bunch_type) *  purchase_price,
                'total_sale'    : qty * sale_price if not is_box_qty else qty * bunch_per_box *  int(bunch_type) *  sale_price,
                'profit'        : qty * (sale_price - purchase_price) if not is_box_qty else qty * bunch_per_box *  int(bunch_type) *  (sale_price - purchase_price),
                'qty_bxs': str(qty_bxs) + ' ' + uom,
                'full_boxes' : full_boxes,
                'stimated_stems' : tale_qty if not is_box_qty else box_qty * bunch_per_box *  int(bunch_type),
            }
        return result

    def save(self, cr, uid, ids, arg, context=None):
        detalle = self.browse(cr,uid,ids[0])
        if detalle:
            if not detalle.length_ids:
                name = detalle.product_id.name_template + ' ' + detalle.variant_id.name
                raise osv.except_osv('Error', "Debe especificar las longitudes y los precios de compras de la variedad para el producto " + name)
            lengths = [l.length for l in detalle.length_ids]
            if detalle.box_qty <= 0 and detalle.tale_qty <= 0:
                name = detalle.product_id.name_template + ' ' + detalle.variant_id.name + '-'.join(lengths)
                raise osv.except_osv('Error', "La cantidad del producto " + name + " no puede ser 0")

            purchase_prices  = [l.purchase_price for l in detalle .length_ids]
            purchase_price = sum(purchase_prices)/len(purchase_prices) if purchase_prices else 0

            if purchase_price <= 0:
                name = detalle.product_id.name_template + ' ' + detalle.variant_id.name + '-'.join(lengths)
                raise osv.except_osv('Error', "El precio de compra del producto " + name + " no puede ser 0")
            if detalle.sale_price <= 0:
                name = detalle.product_id.name_template + ' ' + detalle.variant_id.name + '-'.join(lengths)
                raise osv.except_osv('Error', "El precio de venta del producto " + name + " no puede ser 0")

            l_ids = [l.id for l in detalle.detalle_id.length_ids]
            self.pool.get('detalle.lines.length').unlink(cr, uid, l_ids)

            lengths =  [(0,0,{'length': l.length,'purchase_price':l.purchase_price}) for l in detalle.length_ids]

            detalle_dict = {
                'supplier_id': detalle.supplier_id.id if detalle.supplier_id else None,
                'type': detalle.type,
                'product_id': detalle.product_id.id,
                'variant_id': detalle.variant_id.id,
                'length_ids': lengths,
                'qty': detalle.box_qty if detalle.is_box_qty else detalle.tale_qty,
                'is_box_qty': detalle.is_box_qty,
                'bunch_type': detalle.bunch_type,
                'bunch_per_box': detalle.bunch_per_box,
                'uom': detalle.uom,
                'origin': detalle.origin.id if detalle.origin else None,
                'subclient_id': detalle.subclient_id.id if detalle.subclient_id else None,
                'sucursal_id': detalle.sucursal_id.id if detalle.sucursal_id else None,
            }
            self.pool.get('detalle.lines').write(cr,uid,[detalle.detalle_id.id], detalle_dict)

            if not detalle.detalle_id.confirmada and detalle.confirmada:
                confirm_ids = self.pool.get('confirm.invoice').search(cr, uid, [('pedido_id', '=', detalle.detalle_id.pedido_id.id),('supplier_id', '=', detalle.supplier_id.id)])
                lines = []
                result = self._get_quantity(cr, uid, ids, 'field', arg, context)
                vals = {
                    'pedido_id': detalle.detalle_id.pedido_id.id,
                    'detalle_id': detalle.detalle_id.id,
                    'supplier_id': detalle.supplier_id.id,
                    'line_number': '1',
                    'product_id': detalle.product_id.id,
                    'variant_id': detalle.variant_id.id,
                    'length': '-'.join([l.length for l in detalle.length_ids]),
                    'purchase_price': l.purchase_price,
                    'sale_price': detalle.sale_price,
                    'qty': result[ids[0]]['stimated_stems'],
                    'boxes': result[ids[0]]['full_boxes'],
                    'total_purchase': result[ids[0]]['total_purchase'],
                    'total_sale': result[ids[0]]['total_sale'],
                    'bunch_per_box': detalle.bunch_per_box,
                    'bunch_type': detalle.bunch_type,
                    'uom': detalle.uom,
                    'origin': detalle.origin.id if detalle.origin else False,
                    'subclient_id': detalle.subclient_id.id if detalle.subclient_id else False,
                    'sucursal_id': detalle.sucursal_id.id if detalle.sucursal_id else False,
                    'type': detalle.detalle_id.type,
                    'is_box_qty': detalle.is_box_qty,
                    'confirmada': True
                }
                lines.append((0, 0, vals))

                if not confirm_ids:
                    self.pool.get('confirm.invoice').create(cr, uid, {
                        'pedido_id': detalle.detalle_id.pedido_id.id,
                        'supplier_id': detalle.supplier_id.id,
                        'user_id': uid,
                        'line_ids': lines
                    })
                else:
                    self.pool.get('confirm.invoice').write(cr, uid, confirm_ids, {'line_ids': lines})

                self.pool.get('detalle.lines').write(cr,uid,[detalle.detalle_id.id], {'confirmada':True})

            return {
                    'name'      : 'Pedidos de Clientes',
                    'view_type' : 'form',
                    'view_mode' : 'form',
                    'res_model' : 'pedido.cliente',
                    'type'      : 'ir.actions.act_window',
                    'context'   : context,
                    'res_id'    : detalle.detalle_id.pedido_id.id,
                   }

        return {
            'name': 'Pedidos de Clientes',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'pedido.cliente',
            'type': 'ir.actions.act_window',
            'context': context,
        }

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

detalle_line_wzd()


class detalle_line_length_wzd(osv.osv_memory):
    _name = 'detalle.line.length.wzd'
    _description = 'Lengths'

    _columns = {
        'detalle_id'   : fields.many2one('detalle.line.wzd', 'Details'),
        'length'           : fields.char(string='Length', size = 128, required=True),
        'purchase_price'            : fields.float(string='Purchase Price'),
     }

    _defaults = {
         'detalle_id'     :  lambda self, cr, uid, context : context['detalle_id'] if context and 'detalle_id' in context else None,
    }

detalle_line_length_wzd()