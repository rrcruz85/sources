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

class purchase_line_wzd(osv.osv_memory):
    _name = 'purchase.line.wzd'
    _description = 'Detalle de compras'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = 0
            if obj.is_box_qty:
                res[obj.id] = obj.box_qty * int(obj.bunch_type) * obj.bunch_per_box
            else:
                res[obj.id] = obj.tale_qty
        return res

    def _get_quantity(self, cr, uid, ids, field_name, arg, context):
        result = {}
        uom = {'FB': 1, 'HB': 2, 'QB': 4, 'OB': 8}
        for obj in self.browse(cr, uid, ids, context=context):
            bxs_qty = obj.box_qty if obj.is_box_qty else (1 if not (float(obj.tale_qty) / (int(obj.bunch_type) * obj.bunch_per_box)) else (float(obj.tale_qty) / (int(obj.bunch_type) * obj.bunch_per_box)))
            full_boxes = float(bxs_qty)/uom[obj.uom]
            result[obj.id] = full_boxes
        return result

    _columns = {
        'pedido_id'            : fields.many2one('pedido.cliente', 'Pedido'),
        'cliente_id'           : fields.related('pedido_id','partner_id', type ='many2one',relation = 'res.partner', string ='Cliente'),
        'product_variant_id'            : fields.many2one('request.product.variant', 'Variant'),
        'type'                  : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Order'),
        'supplier_id'           : fields.many2one('res.partner', 'Farm', required=True, domain=[('supplier', '=', True)]),
        'product_id'            : fields.many2one('product.product', 'Product', required=True),
        'variant_id'            : fields.many2one('product.variant', 'Variety', required=True),
        'length_ids'            : fields.one2many('purchase.line.length.wzd','wzd_id','Lengths'),
       	'is_box_qty'            : fields.boolean('Box Packing?'),
        'box_qty'               : fields.integer('Boxes'),
		'tale_qty'              : fields.integer('Stems'),
		'bunch_per_box'         : fields.integer('Bunch per Box'),
        'bunch_type'            : fields.integer('Stems x Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], 'Unit of Measure'),
        'sale_price'            : fields.float(string='Sale Price'),
        'origin'                : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubClient'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),

        #'total_purchase'        : fields.function(_get_quantity, type='float', string='Farm Total', multi='compute_data'),
        #'total_sale'            : fields.function(_get_quantity, type='float', string='Total', multi='compute_data'),
        #'profit'                : fields.function(_get_quantity, type='float', string='Profit', multi='compute_data'),
        'full_boxes'            : fields.function(_get_quantity, type='float', string='Full Boxes'),
        'stimated_stems'     : fields.function(_get_info, type='integer', string='Stems'),
        'qty_bxs'                 : fields.char(string='BXS', size = 10),
        'supplier_ids'                 : fields.char(string='Suppliers', size = 250),
    }

    def get_client(self, cr, uid, context):
        if context and 'cliente_id' in context and context['cliente_id']:
            return context['cliente_id']
        return False

    _defaults = {
        'type': 'open_market',
        'cliente_id'   :  get_client,
    }

    def on_chance_vals(self, cr, uid, ids, is_box_qty,box_qty,tale_qty, bunch_type,bunch_per_box, uom, sale_price, context=None):
        result = {}
        if uom and bunch_type and bunch_per_box:
            uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
            qty_bxs = box_qty if is_box_qty else  (1 if not (tale_qty / (int(bunch_type) * bunch_per_box)) else (tale_qty / (int(bunch_type) * bunch_per_box)))
            boxes = float(qty_bxs) / uom_dict[uom]
            result['value'] = {
                'full_boxes' : boxes,
                'qty_bxs' : str(qty_bxs) + ' ' + uom,
                'stimated_stems' :  box_qty * int(bunch_type) * bunch_per_box if is_box_qty else tale_qty
            }
        return result

    def on_chance_supplier(self, cr, uid, ids, supplier_id, product_id, variant_id, context=None):
        result = {}
        if supplier_id and product_id and variant_id:
            suppliers = self.pool.get('purchase.request.template').search(cr,uid,[('partner_id','=',supplier_id)])
            if suppliers:
                val_ids = self.pool.get('purchase.request.product.variant').search(cr, uid, [('template_id', '=', suppliers[0]),('product_id', '=', product_id),('variant_id', '=', variant_id)])
                if val_ids:
                    product_variant = self.pool.get('purchase.request.product.variant').browse(cr, uid, val_ids[0])
                    vals =[(0,0,{'length': p.length,'purchase_price':p.purchase_price}) for p in product_variant.length_ids]
                    result['value'] = {'length_ids':vals}
        return result

    def save(self, cr, uid, ids, arg, context=None):
        obj = self.browse(cr, uid, ids[0])
        if not obj.length_ids:
            name = obj.product_id.name_template + ' ' + obj.variant_id.name
            raise osv.except_osv('Error', "Debe especificar las longitudes y los precios de compra para el producto " + name)

        lengths = [(0,0,{'length': l.length, 'purchase_price': l.purchase_price})for l in obj.length_ids]
        detalle_dict = {
            'pedido_id': obj.pedido_id.id if obj.pedido_id else None,
            'line_id': obj.product_variant_id.id if obj.product_variant_id else None,
            'type': obj.type if obj.type else None,
            'supplier_id': obj.supplier_id.id if obj.supplier_id else None,
            'product_id': obj.product_id.id,
            'variant_id': obj.variant_id.id,
            'qty': obj.box_qty if obj.is_box_qty else obj.tale_qty,
            'is_box_qty': obj.is_box_qty,
            'bunch_type': obj.bunch_type,
            'bunch_per_box': obj.bunch_per_box,
            'uom': obj.uom,
            'sale_price': obj.sale_price,
            'origin': obj.origin.id if obj.origin else None,
            'subclient_id': obj.subclient_id.id if obj.subclient_id else None,
            'sucursal_id': obj.sucursal_id.id if obj.sucursal_id else None,
            'length_ids': lengths
        }
        self.pool.get('detalle.lines').create(cr, uid, detalle_dict)

        return {
            'name': 'Pedidos de Clientes',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pedido.cliente',
            'type': 'ir.actions.act_window',
            'context': context,
            'res_id': obj.pedido_id.id,
        }

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

purchase_line_wzd()


class purchase_line_length_wzd(osv.osv_memory):
    _name = 'purchase.line.length.wzd'
    _description = 'Variety Length'

    _columns = {
        'wzd_id'            : fields.many2one('purchase.line.wzd','Wizard'),
        'length'           : fields.char(string='Length', size = 128, required=True),
        'purchase_price'            : fields.float(string='Purchase Price'),
	}

    _defaults = {
        'wzd_id'     :  lambda self, cr, uid, context : context['wzd_id'] if context and 'wzd_id' in context else None,
    }

purchase_line_length_wzd()
