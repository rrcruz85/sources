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
    _description = 'Missing Quantities per Lines'

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
        'line'                  : fields.char(string='Line', size = 128),
        'pedido_id'             : fields.many2one('pedido.cliente', 'Pedido'),
        'cliente_id'            : fields.related('pedido_id','partner_id', type ='many2one',relation = 'res.partner', string ='Cliente'),
        'product_variant_id'    : fields.many2one('request.product.variant', 'Variant'),
        'type'                  : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Order'),
        
        'product_id'            : fields.many2one('product.product', 'Product', required=True),
        'variant_id'            : fields.many2one('product.variant', 'Variety', required=True),
        
        'missing_qty_ids'       : fields.one2many('missing.qty.wzd','wzd_id','Missing quantities per line'),
         
        'subclient_id'          : fields.many2one('res.partner', 'SubClient')       
    }

    def get_client(self, cr, uid, context):
        if context and 'cliente_id' in context and context['cliente_id']:
            return context['cliente_id']
        return False

    _defaults = {
        'cliente_id'   :  get_client,
    }
        
purchase_line_wzd()


class missing_qty_wzd(osv.osv_memory):
    _name = 'missing.qty.wzd'
    _description = 'Missing Qty'
    
    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'qty':'Qty','bxs_qty':'BXS','full_boxes':0}
            bxs_qty = obj.box_qty if obj.is_box_qty else (round(float(obj.tale_qty)/(obj.bunch_type * obj.bunch_per_box), 2) if obj.bunch_type and obj.bunch_per_box else 0)
            res[obj.id]['bxs_qty'] =  str(bxs_qty) + ' ' + obj.uom
            res[obj.id]['qty'] =  (str(obj.box_qty) + ' Boxes' if obj.is_box_qty else str(obj.tale_qty) + ' Stems') 
            full_boxes = float(bxs_qty)/uom[obj.uom]
            res[obj.id]['full_boxes'] = full_boxes
        return res

    _columns = {
        'wzd_id'                : fields.many2one('purchase.line.wzd','Wizard'),
        'length'                : fields.char(string='Length', size = 128),
        'sale_price'            : fields.float(string='Sale Price'),
        
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'box_qty'               : fields.integer('Bxs', help = 'Boxes'),        
        'tale_qty'              : fields.integer('Stems'),
        'bunch_per_box'         : fields.integer(string= 'Bunches', help= 'Bunches per Box'),
        'bunch_type'            : fields.integer(string = 'UxB', help= 'Stems per Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], string = 'UOM', help='Unit of Measure'),
        
        'full_boxes'            : fields.function(_get_info, type='float', string='FB', help="Full Boxes", multi = '_data'),
        'bxs_qty'               : fields.function(_get_info, type='char', string='BXS', multi = '_data'),
        'qty'                   : fields.function(_get_info, type='char', string='Qty', help="Quantity", multi = '_data'),

    }
    
    def on_change_vals(self, cr, uid, ids, is_box_qty, box_qty, tale_qty, bunch_per_box, bunch_type, uom, context=None):
        res = {'value':{'bxs_qty': 'BXS', 'full_boxes':0}}
        uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
        bxs_qty = box_qty if is_box_qty else (round(float(tale_qty)/(bunch_type * bunch_per_box), 2) if bunch_type and bunch_per_box else 0)
        res['value']['bxs_qty'] =  str(bxs_qty) + ' ' + uom
        full_boxes = float(bxs_qty)/uom_dict[uom]
        res['value']['full_boxes'] = full_boxes
        return res

    _defaults = {
        'wzd_id'     :  lambda self, cr, uid, context : context['wzd_id'] if context and 'wzd_id' in context else None,
    }
    
    def purchase_line(self, cr, uid, ids, arg, context=None):
        obj = self.browse(cr, uid, ids[0])

missing_qty_wzd()

class purchase_line_length_wzd(osv.osv_memory):
    _name = 'purchase.line.length.wzd'
    _description = 'Purchase Line'

    _columns = {       
        'pedido_id'             : fields.many2one('pedido.cliente', 'Pedido'),
        'product_variant_id'    : fields.many2one('request.product.variant', 'Variant'),  
        'get_supplier_ids'      : fields.char(string='Suppliers', size = 256),
              
        'supplier_id'           : fields.many2one('res.partner', 'Farm',required=True),
        'product_id'            : fields.many2one('product.product', 'Product', required=True),
        'variant_id'            : fields.many2one('product.variant', 'Variety', required=True),
        'length'                : fields.char(string='Length', size = 128, required=True),
        
        
        'purchase_price'        : fields.float(string='Purchase Price'),
        'sale_price'            : fields.float(string='Sale Price'),        
         
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'qty'                   : fields.integer('Quantity'),        
        'bunch_per_box'         : fields.integer(string= 'Bunches', help= 'Bunch per Box'),
        'bunch_type'            : fields.integer(string= 'Stems per Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], string = 'UOM', help='Unit of Measure'),
        'subclient_id'          : fields.many2one('res.partner', 'SubCliente'),
	}
    
    _defaults = {
        'bunch_per_box' :  12,
        'bunch_type'    :  25,
        'uom'           :  'HB'
    }
    
    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25
    
    def _check_sale_price(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.sale_price > 0 
    
    def _check_purchase_price(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.purchase_price > 0
    
    def _check_stems_qty(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type * obj.bunch_per_box == obj.qty if not obj.is_box_qty else True
    
    def _check_length(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        exist = False
        for v in obj.product_id.variants_ids:
            if v.id == obj.variant_id.id and v.description == obj.length:
                exist = True
                break                
        return exist 

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
        (_check_sale_price, 'El valor del precio de venta debe ser mayor que 0', []),
        (_check_purchase_price, 'El valor del precio de compra debe ser mayor que 0', []),
        (_check_stems_qty, 'La cantidad de tallos debe coincidir con la cantidad de bunches por el numero de unidades por bunch', []),
        (_check_length, 'La longitud del producto esta incorrecta, el producto no tiene ninguna variedad con la longitud especificada', []),
    ]
    
    def on_change_supplier(self, cr, uid, ids, supplier_id, product_id, variant_id, length, context=None):
        res = {'value':{}}
        if supplier_id and product_id and variant_id and length:
            cr.execute("select prvl.purchase_price " +
                   "from purchase_request_template pr inner join purchase_request_product_variant prv on pr.id = prv.template_id " +
                   "inner join purchase_request_product_variant_length prvl on prv.id = prvl.variant_id " +
                   "where pr.partner_id = %s and prv.product_id = %s and prv.variant_id = %s " +
                   "and prvl.length = %s", (supplier_id, product_id, variant_id, length,))
            records = cr.fetchall()
            if records and records[0]:
                res['value']['purchase_price'] = records[0][0]
        return res

    def on_change_qty(self, cr, uid, ids, qty, bunch_type, context=None):
        res = {'value':{}}
        if qty and bunch_type:
            res['value']['bunch_per_box'] = qty/bunch_type
        return res
    
    def save(self, cr, uid, ids, arg, context=None):
        obj = self.browse(cr, uid, ids[0])
        
        detalle_dict = {
            'name'           : str(obj.product_variant_id.line),
            'pedido_id'      : obj.pedido_id.id if obj.pedido_id else None,
            'line_id'        : obj.product_variant_id.id if obj.product_variant_id else None,
            'type'           : 'open_market',
            'supplier_id'    : obj.supplier_id.id if obj.supplier_id else None,
            'product_id'     : obj.product_id.id,
            'variant_id'     : obj.variant_id.id,
            'length'         : obj.length,
            'qty'            : obj.qty,
            'is_box_qty'     : obj.is_box_qty,
            'bunch_type'     : obj.bunch_type,
            'bunch_per_box'  : obj.bunch_per_box,
            'uom'            : obj.uom,
            'purchase_price' : obj.purchase_price,
            'sale_price'     : obj.sale_price,
            'subclient_id'   : obj.subclient_id.id if obj.subclient_id else None,            
        }
        self.pool.get('detalle.lines').create(cr, uid, detalle_dict)

        return {
            'name'       : 'Pedidos de Clientes',
            'view_type'  : 'form',
            'view_mode'  : 'form',
            'res_model'  : 'pedido.cliente',
            'type'       : 'ir.actions.act_window',           
            'res_id'     : obj.pedido_id.id,
        }

purchase_line_length_wzd()
