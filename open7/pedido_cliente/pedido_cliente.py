# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010 Acysos S.L. (http://acysos.com) All Rights Reserved.
#                       Ignacio Ibeas <ignacio@acysos.com>
#    $Id$
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
import math
import re

class pedido_cliente(osv.osv):
    _name = 'pedido.cliente'
    _description = 'Pedido del cliente' 

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            boxes = 0
            stems = 0
            tipo_flete = obj.partner_id.tipo_flete if obj.partner_id.tipo_flete else 'n'
            '''
            for v in obj.variant_ids:
                if v.is_box_qty:
                    boxes += math.ceil(float(v.box_qty)/uom[v.uom])
                    stems += math.ceil(float(v.box_qty * int(v.bunch_type) * v.bunch_per_box))
                else:
                    stems += math.ceil(float(v.tale_qty))
                    boxes += math.ceil(float(v.tale_qty)/ (int(v.bunch_type) * v.bunch_per_box  * uom[v.uom]))
            '''
            res[obj.id] = {'boxes':boxes, 'stems':stems, 'tipo_flete' : tipo_flete}
        return res

    _columns = {
        'name'                  : fields.integer('Request Number',),
        'request_date'          : fields.date('Airport Date',),
        'partner_id'            : fields.many2one('res.partner', 'Client', domain=[('customer', '=', True)], required=True),
        'freight_agency_id'     : fields.many2one('freight.agency', 'Freight Agency'),
        'type'                  : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Order'),
        'state'                 : fields.selection([('draft', 'Nuevo'),
                                                    ('progress', 'En Compras'),
                                                    ('verified', 'Verificado'),
                                                    ('invoice', 'Facturar'),
                                                    ('cancel', 'Cancelado')], 'State', readonly=True),
        'variant_ids'           : fields.one2many('request.product.variant', 'pedido_id', 'Request Lines', ondelete='cascade'),
        'purchase_line_ids'     : fields.one2many('detalle.lines', 'pedido_id', 'Purchased Lines',ondelete='cascade'),
        
        'boxes'                 : fields.function(_get_info, type='integer', string='Full Boxes', multi = '_val'),
        'stems'                 : fields.function(_get_info, type='integer', string='Stems', multi = '_val'),
        'tipo_flete'            : fields.function(_get_info, type='char', string='Tipo Flete', multi = '_val'),
      
        'account_invoice_ids'   : fields.one2many('account.invoice', 'pedido_cliente_id', 'Invoices'),
        'airline_id'            : fields.many2one('pedido_cliente.airline', string='Airline'),
        'number'                : fields.char('Flight Number'),
        'precio_flete'          : fields.float('Precio Flete', digits = (0,2)),
        'sale_request_id'       : fields.many2one('sale.request', 'Sale Request'),       
    }

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        return super(pedido_cliente, self).name_search(cr, user, name, args, operator=operator, context=context, limit=limit)

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        reads = self.browse(cr, uid, ids, context=context)
        res = []
        types = {'standing_order' : 'Standing Order','open_market': 'Open Market'}
        for record in reads:
            if context and 'from_wizard_request' in context:
                res.append((record.id, str(record.name) + '/ '+ types[record.type] + '/ ' + record.partner_id.name + '/ ' + record.request_date))
            else:
                res.append((record.id, record.partner_id.name))
        return res

    def on_change_partner(self, cr, uid, ids, partner_id, context=None):
        val = 1
        if partner_id:
            cr.execute('select max(p.name) from pedido_cliente p where p.partner_id = %s',(partner_id,))
            val_tmp = cr.fetchone()[0] or 0.0
            val = val_tmp + 1
        return {'value': {'name': val}}

    _defaults = {
        'state'        : 'draft',
        'name'         : 1,
        'request_date' : time.strftime('%Y-%m-%d'),
        'type'         : 'open_market'        
    }
    
    _order = 'name'

    def _check_tipo_flete(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.partner_id and obj.partner_id.tipo_flete and obj.partner_id.tipo_flete == 'fob_f_p':
            return obj.precio_flete != 0
        else:
            return True

    _constraints = [
        (_check_tipo_flete, 'El precio del flete no puede ser cero.', []),
    ]

    _sql_constraints = [
        ('name_partner_uniq', 'unique(name, partner_id)', 'El nro. de pedido debe ser unico por cliente!'),
    ]

    def action_print_report(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        context['default_pedido_id'] = ids[0]
        proveedores = []
        for l in self.browse(cr, uid, ids[0]).purchase_line_ids:
            if not l.confirmada and l.supplier_id.name not in proveedores:
                proveedores.append(l.supplier_id.name)
        if proveedores:
            raise osv.except_osv('Error', "Los siguientes proveedores: "+ ','.join(proveedores) + " tienen lineas de compras sin confirmar.\nPara poder imprimir este pedido debe confirmar todas las lineas de compras de los proveedores.")

        return {
            'name'      : _('Print report'),
            'view_type' : 'form',
            "view_mode" : 'form',
            'res_model' : 'pedido_cliente.wizard_to_print_report',
            'type'      : 'ir.actions.act_window',
            'target'    : 'new',
            'view_id'   : '',
            'context'   : context
        }

pedido_cliente()

class AirLine(osv.osv):
    _name = 'pedido_cliente.airline'
    _description = 'pedido_cliente.airline'

    _columns = {
        'name': fields.char('Name', required=True),
        'avb_number': fields.char('#AVB', required=True),
    }

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        reads = self.browse(cr, uid, ids, context=context)
        res = []
        for record in reads:
            res.append((record.id, str(record.avb_number) + '/' + record.name))
        return res

AirLine()

class request_product_variant(osv.osv):
    _name = 'request.product.variant'
    _description = 'Variety'

    def _get_info(self, cr, uid, ids, field_name, arg, context = None):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'request_qty': '0','missing_qty':0}
            lengths = [(l.length, str(l.sale_price), l.full_boxes) for l in obj.length_ids] 
            res[obj.id]['lengths'] =  '-'.join([l[0] for l in lengths])
            res[obj.id]['sale_prices'] = '-'.join([l[1] for l in lengths])
            res[obj.id]['full_boxes'] = sum([l[2] for l in lengths]) 
            res[obj.id]['bxs_qty'] = str(sum([l[2] for l in lengths]) * 2) + ' HB'
            request_qty = sum([l.box_qty * l.bunch_type * l.bunch_per_box if l.is_box_qty else l.tale_qty for l in obj.length_ids])
            res[obj.id]['request_qty'] = str(request_qty) + ' Stems' 
            
            purchased_qty = 0
            if obj.subclient_id:
                purchased_ids = self.pool.get('detalle.lines').search(cr,uid, [('pedido_id', '=',obj.pedido_id.id),('line_id', '=',obj.id),('subclient_id', '=',obj.subclient_id.id)])
                if purchased_ids:
                    lines = self.pool.get('detalle.lines').browse(cr,uid, purchased_ids)                    
                    purchased_qty = sum([l.qty * l.bunch_type * l.bunch_per_box if l.is_box_qty else l.qty for l in lines]) 
                    
            missing_qty = request_qty - purchased_qty
            
            res[obj.id]['missing_qty'] = missing_qty
            res[obj.id]['missing_qty2'] = '-' + str(missing_qty) if missing_qty > 0 else '0' if missing_qty == 0 else '+' + str(missing_qty)
             
        return res

    def _get_ids(self, cr, uid, ids, context=None):
        res = []
        for length in self.pool.get('request.product.variant.length').browse(cr, uid, ids, context=context):
            if length.variant_id and length.variant_id.id not in res:
                res.append(length.variant_id.id)
        return res

    _columns = {
        'pedido_id'            : fields.many2one('pedido.cliente', string ='Pedido',ondelete='cascade'),
        'line'                 : fields.integer(string = '#', help= 'Line Number'),        
        'cliente_id'           : fields.related('pedido_id','partner_id', type ='many2one',relation = 'res.partner', string ='Cliente'),
        'type'                 : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'product_id'           : fields.many2one('product.product','Product'),
        'variant_id'           : fields.many2one('product.variant','Variety'),
        'length_ids'           : fields.one2many('request.product.variant.length','variant_id','Lengths'),
       
      	'subclient_id'         : fields.many2one('res.partner', 'SubCliente'),
        'purchased_line_ids'   : fields.one2many('detalle.lines','line_id','Purchased Lines'),
        'length_deleted'       : fields.boolean('Deleted'),
        'is_standing_order'    : fields.boolean('Is standing order'),
         
        'lengths'              : fields.function(_get_info, type='char', string='Lengths', multi = '_data',
                                        store = {
                                            'request.product.variant': (lambda self,cr,uid,ids,c=None: ids, ['length_ids','length_deleted'], 10),
                                            'request.product.variant.length': (_get_ids, ['length'], 10),}),
        'sale_prices'          : fields.function(_get_info, type='char', string='Sale Prices', multi = '_data'),
        'full_boxes'           : fields.function(_get_info, type='float', string='Full Boxes', multi = '_data'),
        'bxs_qty'              : fields.function(_get_info, type='char', string='BXS', multi = '_data'),
        'request_qty'          : fields.function(_get_info, type='char', string='Qty', multi = '_data'),
        'missing_qty'          : fields.function(_get_info, type='integer', string='Misssing Qty', multi = '_data'),
        'missing_qty2'         : fields.function(_get_info, type='char', string='Misssing Qty', multi = '_data'),
    }

    _order = "line"

    def get_default_line_number(self, cr, uid, context=None):
        if context and 'lines' in context:
            return len(context['lines']) + 1
        else:
            return 1

    _defaults = {         
        'type'             : 'open_market',        
        'product_id'       : lambda self, cr, uid, context : context['product_id'] if context and 'product_id' in context else None,
        'pedido_id'        : lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else None,
        'cliente_id'       : lambda self, cr, uid, context : context['cliente_id'] if context and 'cliente_id' in context else None,
        'line'             : get_default_line_number,
    }

request_product_variant()

class request_product_variant_length(osv.osv):
    _name = 'request.product.variant.length'
    _description = 'Variety Length'
    
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
            
            stems = obj.box_qty * obj.bunch_type * obj.bunch_per_box if obj.is_box_qty else obj.tale_qty
            
            purchased_lines = self.pool.get('detalle.lines').search(cr, uid, [('line_id', '=', obj.variant_id.id),('product_id','=',obj.variant_id.product_id.id),('variant_id','=',obj.variant_id.variant_id.id),('length','=',obj.length)])
            purchased_qty = sum([p.qty * p.bunch_type * p.bunch_per_box if p.is_box_qty else p.qty for p in self.pool.get('detalle.lines').browse(cr, uid, purchased_lines)])
            
            diff =stems - purchased_qty
            res[obj.id]['missing_qty'] =  diff if diff > 0 else 0
            res[obj.id]['missing_qty2'] = str(diff) + ' Stems' if diff > 0 else ''
            
        return res

    _columns = {
        'variant_id'            : fields.many2one('request.product.variant','Variety'),
        'length'                : fields.char(string='Length', size = 128),
        'sale_price'            : fields.float(string='Sale Price'),
        
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'box_qty'               : fields.integer('BXS'),        
        'tale_qty'              : fields.integer('Stems'),
        'bunch_per_box'         : fields.integer(string= 'Bunches', help= 'Bunch per Box'),
        'bunch_type'            : fields.integer(string= 'Stems per Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], string = 'UOM', help='Unit of Measure'),
        
        'full_boxes'            : fields.function(_get_info, type='float', string='FB', help="Full Boxes", multi = '_data'),
        'bxs_qty'               : fields.function(_get_info, type='char', string='BXS', multi = '_data'),
        'qty'                   : fields.function(_get_info, type='char', string='Qty', help="Quantity", multi = '_data'),
        'missing_qty'           : fields.function(_get_info, type='integer', string='Misssing Qty', multi = '_data'),
        'missing_qty2'          : fields.function(_get_info, type='char', string='Misssing Qty', multi = '_data'),
	}

    _defaults = {
        'variant_id'    :  lambda self, cr, uid, context : context['variant_id'] if context and 'variant_id' in context else None,
        'bunch_per_box' :  12,
        'bunch_type'    :  25,
        'uom'           :  'HB'
    }
    
    def _check_stems_qty(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type * obj.bunch_per_box == obj.tale_qty if not obj.is_box_qty else True
    
    def _check_sale_price(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.sale_price > 0  
    
    def _check_length(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        exist = False
        for v in obj.variant_id.product_id.variants_ids:
            if v.id == obj.variant_id.variant_id.id and v.description == obj.length:
                exist = True
                break                
        return exist 
    
    _constraints = [
        (_check_stems_qty, 'La cantidad de tallos debe coincidir con la cantidad de bunches por el numero de unidades por bunch', []),
        (_check_sale_price, 'El precio de venta debe ser mayor que cero', ['sale_price']), 
        #(_check_length, 'La longitud del producto esta incorrecta, el producto no tiene ninguna variedad con la longitud especificada', []),
    ]
    
    def on_change_vals(self, cr, uid, ids, is_box_qty, box_qty, tale_qty, bunch_per_box, bunch_type, uom, context=None):
        res = {'value':{'bxs_qty': 'BXS', 'full_boxes':0}}
        uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
        bxs_qty = box_qty if is_box_qty else (round(float(tale_qty)/(bunch_type * bunch_per_box), 2) if bunch_type and bunch_per_box else 0)
        res['value']['bxs_qty'] =  str(bxs_qty) + ' ' + uom
        full_boxes = float(bxs_qty)/uom_dict[uom]
        res['value']['full_boxes'] = full_boxes
        return res

    def unlink(self, cr, uid, ids, context=None):
        v_ids = []
        for l in self.browse(cr, uid, ids, context=context):
            if l.variant_id and l.variant_id.id not in v_ids:
                v_ids.append(l.variant_id.id)
        result = super(request_product_variant_length, self).unlink(cr, uid, ids, context=context)
        for v in self.pool.get('request.product.variant').browse(cr,uid,v_ids):
            self.pool.get('request.product.variant').write(cr,uid,[v.id], {'length_deleted' : not v.length_deleted})
        return result
    
    def purchase(self, cr, uid, ids, *args):
        obj = self.browse(cr, uid, ids[0])  
        
        missing_qty = obj.missing_qty
        cliente_id = obj.variant_id.pedido_id.partner_id.id
        subclient_id = obj.variant_id.subclient_id.id if obj.variant_id.subclient_id else 0
        
        cr.execute("select pr.partner_id, prvl.bunch_per_box, prvl.bunch_type," +
                   "coalesce(prvl.is_box_qty, false) as is_box_qty, coalesce(prvl.box_qty,0) as box_qty, coalesce(prvl.tale_qty, 0) as tale_qty,"
                   "prvl.uom, pr.sucursal_id from purchase_request_template pr inner join purchase_request_product_variant prv on pr.id = prv.template_id " +
                   "inner join purchase_request_product_variant_length prvl on prv.id = prvl.variant_id " +
                   "where pr.client_id = %s and prv.subclient_id = %s and prv.product_id = %s and prv.variant_id = %s " +
                   "and prvl.length = %s", (cliente_id, subclient_id, obj.variant_id.product_id.id, obj.variant_id.variant_id.id, obj.length,))
                    
        records = cr.fetchall()
        supplier_ids = map(lambda r: str(r[0]), filter(lambda r: (r[4] * r[1] * r[2] >= missing_qty if r[3] else r[5] >= missing_qty), records))
        
        context = {
            'default_pedido_id'          : obj.variant_id.pedido_id.id,
            'default_product_variant_id' : obj.variant_id.id,               
            'default_product_id'         : obj.variant_id.product_id.id,
            'default_variant_id'         : obj.variant_id.variant_id.id,
            'default_subclient_id'       : obj.variant_id.subclient_id.id,
            'default_length'             : obj.length,
            'default_get_supplier_ids'   : ','.join(supplier_ids),
            'default_is_box_qty'         : obj.is_box_qty,
            'default_qty'                : missing_qty,
            'default_bunch_per_box'      : missing_qty/obj.bunch_type if not obj.is_box_qty and obj.bunch_type else 0,
            'default_bunch_type'         : obj.bunch_type,
            'default_uom'                : obj.uom,
            'default_sale_price'         : obj.sale_price,           
            'default_uom'                : obj.uom,
        }
            
        return {
            'name': _("Purchase Line"),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.line.length.wzd',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }     
    
request_product_variant_length()

class detalle_line(osv.osv):
    _name = 'detalle.lines'
    _description = 'Detalle de compras'
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        res = []
        types = {'standing_order' : 'Standing Order','open_market': 'Open Market'}
        
        for obj in self.browse(cr, uid, ids, context=context):
            res.append((obj.id, types[obj.type] + '/' + obj.product_id.name_template + '/' + obj.variant_id.name + '/' + obj.length))
        return res

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context and 'lines' in context:
            lines = context['lines']
            ids = []
            for l in lines:
                if 'client_invoice' in context:
                    detalle_id = self.pool.get('invoice.client.line.wizard').read(cr,uid,l[1],['detalle_id'])
                    if detalle_id:
                        ids.append(detalle_id['detalle_id'][0])
                else:
                    detalle_id = self.pool.get('invoice.line.wizard').read(cr,uid,l[1],['detalle_id'])
                    if detalle_id and detalle_id['detalle_id'] and detalle_id['detalle_id'][0]:
                        ids.append(detalle_id['detalle_id'][0])
            return ids
        args.append(['active','=',True])
        return super(detalle_line, self).search(cr, uid, args, offset, limit, order, context, count)

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'bxs_qty':'BXS','full_boxes':0}
            bxs_qty = obj.qty if obj.is_box_qty else (round(float(obj.qty)/(obj.bunch_type * obj.bunch_per_box), 2) if obj.bunch_type and obj.bunch_per_box else 0)
            res[obj.id]['bxs_qty'] =  str(bxs_qty) + ' ' + obj.uom
            full_boxes = float(bxs_qty)/uom[obj.uom]
            res[obj.id]['full_boxes'] = full_boxes
            
            stems = obj.qty * obj.bunch_type * obj.bunch_per_box if obj.is_box_qty else obj.qty
            total_sale = stems * obj.sale_price
            total_purchase = stems * obj.purchase_price
            
            res[obj.id]['total_purchase'] = total_purchase
            res[obj.id]['total_sale'] = total_sale
            res[obj.id]['profit'] = total_sale - total_purchase
            
        return res
    
    _columns = {
        'name'                  : fields.char(size = 128, string= '#', help = 'Line Number'),
        'pedido_id'             : fields.many2one('pedido.cliente', 'Request',ondelete='cascade'),
        'line_id'               : fields.many2one('request.product.variant', 'Lines'),
       
        'type'                  : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'supplier_id'           : fields.many2one('res.partner', 'Farm', required=True, domain=[('supplier', '=', True)]),
        'product_id'            : fields.many2one('product.product', string='Product',required=True),
        'variant_id'            : fields.many2one('product.variant', 'Variety', required=True),
        'length'                : fields.char(size = 128, string= 'Length', required=True),        
        
        'qty'                   : fields.float('Qty'),
        'is_box_qty'            : fields.boolean('Box Packing?'),
		'bunch_per_box'         : fields.integer(string = 'Bunches', help = 'Bunches per Box'),
        'bunch_type'            : fields.integer(string = 'UxB', help = 'Units per Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], string = 'UOM', help= 'Unit of Measure'),
        
        'sale_price'            : fields.float(string='Sale Price'),
        'purchase_price'        : fields.float(string='Purchase Price'),
        
        'origin_id'             : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubCliente'),        
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        
        'confirmada'            : fields.boolean('Conf.', help="Linea confirmada"),
        'active'                : fields.boolean('Active'),
        
        'full_boxes'            : fields.function(_get_info, type='float', string='FB', help="Full Boxes", multi = '_data'),
        'bxs_qty'               : fields.function(_get_info, type='char', string='BXS', multi = '_data'),
        'total_sale'            : fields.function(_get_info, type='float', string='Total Sale', help = 'Qty x Sale Price',  multi = '_data'),
        'total_purchase'        : fields.function(_get_info, type='float', string='Total Purchase', help = 'Qty x Purchase Price', multi = '_data'),
        'profit'                : fields.function(_get_info, type='float', string='Profit', help = 'Total Sale - Total Purchase', multi = '_data'),

    }

    _defaults = {
        'bunch_type'    : 25,
        'uom'           : 'HB',
        'type'          : 'open_market',
        'bunch_per_box' : 12,
        'pedido_id'     : lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else None,
        'active'        : True
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
        #(_check_length, 'La longitud del producto esta incorrecta, el producto no tiene ninguna variedad con la longitud especificada', []),
    ]
    
    def on_change_vals(self, cr, uid, ids, is_box_qty, qty, bunch_per_box, bunch_type, uom, context=None):
        res = {'value':{'bxs_qty': 'BXS', 'full_boxes':0}}
        uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
        bxs_qty = qty if is_box_qty else (round(float(qty)/(bunch_type * bunch_per_box), 2) if bunch_type and bunch_per_box else 0)
        res['value']['bxs_qty'] =  str(bxs_qty) + ' ' + uom
        full_boxes = float(bxs_qty)/uom_dict[uom]
        res['value']['full_boxes'] = full_boxes
        return res
    
    def on_change_qty(self, cr, uid, ids, qty, bunch_type, context=None):
        res = {'value':{}}
        if qty and bunch_type:
            res['value']['bunch_per_box'] = qty/bunch_type
        return res
    
    def unlink(self, cr, uid, ids, context=None):
        for l in self.browse(cr, uid, ids, context=context):
            if l.confirmada:
                raise osv.except_osv("Error", "No se pueden eliminar las lineas de compras que estan confirmadas") 
        return super(detalle_line, self).unlink(cr, uid, ids, context)

detalle_line()

class detalle_line_origin(osv.osv):
    _name = 'detalle.lines.origin'
    _description = 'detalle.lines.origin'
    
    _columns = {
        'name'    : fields.char('Origen'),
    }

detalle_line_origin()

class freight_agency(osv.osv):
    _name = 'freight.agency'
    _description = 'freight.agency'
    _columns = {
        'name'    : fields.char('Nombre', size=128),
        'address'    : fields.char('Direccion', size=256),
        'mobil'    : fields.char('Mobil', size=64),
        'phone1'    : fields.char('Tel.1', size=64),
        'phone2'    : fields.char('Tel.2', size=64),
        'contact'    : fields.char('Contacto', size=128),
        'cuarto_frio'    : fields.char('Cuarto Frio', size=256),
        'email1'    : fields.char('Correo 1', size=128),
        'email2'    : fields.char('Correo 2', size=128),
    }

    def _check_email1(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.email1:
            return re.match("^[\w\.\-]+\@[\w\.]+\.[a-z]{2,3}$", obj.email1)
        return True

    def _check_email2(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.email2:
            return re.match("^[\w\.\-]+\@[\w\.]+\.[a-z]{2,3}$", obj.email2)
        return True

    def _check_mobile(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.mobil:
            return re.match("^(\+?[0-9]{1,3})*((-)*[0-9]{7,10})$", obj.mobil)
        return True

    def _check_phone1(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.phone1:
            return re.match("^(\+?[0-9]{1,3})*((-)*[0-9]{7,10})$", obj.phone1)
        return True

    def _check_phone2(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.phone2:
            return re.match("^(\+?[0-9]{1,3})*((-)*[0-9]{7,10})$", obj.phone2)
        return True

    _constraints = [
        (_check_email1, 'La direccion de correo 1 esta incorrecta', []),
        (_check_email2, 'La direccion de correo 2 esta incorrecta', []),
        (_check_mobile, 'El numero del mobil esta incorrecto', []),
        (_check_phone1, 'El numero de telefono 1 esta incorrecto', []),
        (_check_phone2, 'El numero de telefono 2 esta incorrecto', []),
    ]

freight_agency()

class confirm_invoice(osv.osv):
    _name = 'confirm.invoice'
    _description = 'Confirm Invoice'

    _columns = {
        'pedido_id'      : fields.many2one('pedido.cliente','Pedido'),
        'supplier_id'    : fields.many2one('res.partner','Supplier'),
        'line_ids': fields.one2many('confirm.invoice.line', 'invoice_id', 'Purchase Lines'),
        'invoice_number' : fields.char('Supplier Invoice Number', size=64),
        'date_invoice': fields.date('Invoice Date', help="Keep empty to use the current date"),
        'account_id': fields.many2one('account.account', 'Account To Pay Supplier', domain=[('type', '=', 'payable')]),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position'),
        'period_id': fields.many2one('account.period', 'Fiscal Period', domain=[('state', '<>', 'done')], ),
        'currency_id': fields.many2one('res.currency', 'Currency'),
        'journal_id': fields.many2one('account.journal', 'Journal', domain=[('type', '=', 'purchase')]),
        'company_id': fields.many2one('res.company', 'Company'),
        'user_id': fields.many2one('res.users', 'Salesperson'),
    }

confirm_invoice()

class confirm_invoice_line(osv.osv):
    _name = 'confirm.invoice.line'
    _description = 'Invoice Line'

    _columns = {
        'invoice_id'      : fields.many2one('confirm.invoice','Invoice',ondelete='cascade'),
        'pedido_id'      : fields.many2one('pedido.cliente','Pedido',ondelete='cascade'),
        'detalle_id'      : fields.many2one('detalle.lines','Detalle', ondelete='cascade'),
        'supplier_id'    : fields.many2one('res.partner','Supplier'),

        'line_number'   : fields.char(size=128, string ='#', help='Line Number'),
        'product_id'      : fields.many2one('product.product','Product'),
        'variant_id'      : fields.many2one('product.variant','Variety',),
        'length'              : fields.char(size=128, string ='Length'),
        'purchase_price'  : fields.float('Purchase Price'),
        'sale_price'  : fields.float('Sale Price'),
        'qty'             : fields.float('Qty', help = "Quantity"),
        'boxes'             : fields.float('Full Boxes'),
        'total_purchase'    : fields.float(string='Total'),
        'total_sale'    : fields.float(string='Total'),
        'bunch_per_box'   : fields.integer('Bunch per Box'),
        'bunch_type'            : fields.integer( 'Stems x Bunch'),
        'uom'              : fields.selection([('FB', 'FB'),
                                               ('HB', 'HB'),
                                               ('QB', 'QB'),
                                               ('OB', 'OB')], 'UOM'),
        'origin'                : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubClient'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'type'                     : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'confirmada'            : fields.boolean('Confirmada'),
    }

confirm_invoice_line()

class confirm_client_invoice(osv.osv):
    _name = 'confirm.client.invoice'
    _description = 'Confirm Invoice'

    _columns = {
        'pedido_id'      : fields.many2one('pedido.cliente','Pedido'),
        'line_ids': fields.one2many('confirm.client.invoice.line', 'invoice_id', 'Purchase Lines'),
        'date_invoice': fields.date('Invoice Date', help="Keep empty to use the current date"),
        'account_id': fields.many2one('account.account', 'Account To Pay Supplier', domain=[('type', '=', 'receivable')]),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position'),
        'period_id': fields.many2one('account.period', 'Fiscal Period', domain=[('state', '<>', 'done')], ),
        'currency_id': fields.many2one('res.currency', 'Currency'),
        'journal_id': fields.many2one('account.journal', 'Journal', domain=[('type', '=', 'purchase')]),
        'company_id': fields.many2one('res.company', 'Company'),
        'user_id': fields.many2one('res.users', 'Salesperson'),
   }

confirm_client_invoice()

class confirm_client_invoice_line(osv.osv):
    _name = 'confirm.client.invoice.line'
    _description = 'Invoice Line'

    _columns = {
        'invoice_id'      : fields.many2one('confirm.client.invoice','Invoice'),
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
        'bunch_type'            : fields.integer( 'Stems x Bunch'),
        'uom'              : fields.selection([('FB', 'FB'),
                                               ('HB', 'HB'),
                                               ('QB', 'QB'),
                                               ('OB', 'OB')], 'UOM'),
        'origin'                : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubClient'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'type'                     : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'confirmada'            : fields.boolean('Confirmada'),
    }

confirm_client_invoice_line()






