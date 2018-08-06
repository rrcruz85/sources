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
from openerp.tools.translate import _

class puchase_lines_wzd(osv.osv_memory):
    _name = 'purchase.lines.wzd'
    _description = 'Purchase Lines'
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None,context=None, count=False):
        if context is None:
            context = {}
        ids = super(puchase_lines_wzd, self).search(cr, uid, args,offset,limit,order, context,count)
        if 'lines_selected' in context and context['lines_selected']:
            selected_lines = context['lines_selected'].split(',')
            lines = self.read(cr, uid, ids, ['line_number'])
            ids = [l['id'] for l in lines if str(l['line_number']) not in selected_lines]        
        return ids
    
    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'total_qty_purchased': 'BXS', 'stimated_qty': 'BXS','qty':'','box':0}
            if obj.detalle_id.is_box_qty:
                res[obj.id]['total_qty_purchased'] = str(obj.purchased_qty) + ' BXS'
            else:
                res[obj.id]['total_qty_purchased'] = str(obj.purchased_qty) + ' Stems'

            if obj.detalle_id.agrupada:
                cr.execute("select  sum(dl.bunch_per_box) from detalle_lines dl where dl.group_id =" + str(obj.detalle_id.group_id) + " and dl.active = true and dl.agrupada = true and dl.pedido_id = " + str(obj.pedido_id.id) + 
                           " and dl.supplier_id = " + str(obj.supplier_id.id) + " and dl.product_id = " + str(obj.product_id.id) +
                           " group by dl.group_id, dl.pedido_id, dl.supplier_id, dl.product_id")
                record = cr.fetchone()
                totals = record[0] if record else 0
                qty = (float(obj.bunch_per_box)/totals) * obj.detalle_id.qty if obj.detalle_id.is_box_qty else (float(obj.bunch_per_box)/totals)  
                res[obj.id]['qty'] = str(round(qty, 2) if totals else 0) + ' ' + obj.uom
                full_boxes = (round(qty, 2) if totals else 0)/uom[obj.uom]
                res[obj.id]['stimated_qty'] = full_boxes
            else:
                bxs_qty = obj.purchased_qty if obj.detalle_id.is_box_qty else (1 if not (obj.purchased_qty /(int(obj.bunch_type) * obj.bunch_per_box)) else (obj.purchased_qty / (int(obj.bunch_type) * obj.bunch_per_box)))
                res[obj.id]['qty'] = str(round(float(bxs_qty), 2)) + ' ' + obj.uom
                full_boxes = round(float(bxs_qty)/uom[obj.uom], 2)
                res[obj.id]['stimated_qty'] = full_boxes
                
            res[obj.id]['box'] = obj.detalle_id.box_id.box if obj.detalle_id.box_id else False
        return res

    _columns = {
        'line_number'           : fields.integer(string='#', help = 'Line Number'),
        'line'                  : fields.integer(string='RL', help = 'Request Line'),
        'box_id'                : fields.many2one('detalle.lines.box', 'Box Id',),
        'pedido_id'             : fields.many2one('pedido.cliente', 'Pedido',),
        'detalle_id'            : fields.many2one('detalle.lines', 'Detalle'),
        'type'                  : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'supplier_id'           : fields.many2one('res.partner', 'Farm',),
        'product_id'            : fields.many2one('product.product', 'Product'),
        'variant_id'            : fields.many2one('product.variant', 'Variety'),
        'lenght'                : fields.char(size = 128, string= 'Length'),
        'bunch_type'            : fields.char(size = 128, string= 'Stems x Bunch'),
        'uom'                   : fields.char(size = 128, string= 'UOM'),
        'bunch_per_box'         : fields.integer(string='Bunch Per Box'),
        'request_qty'           : fields.integer(string='Request Qty'),
        'purchased_qty'         : fields.integer(string='Purchased Qty'),
        'stems'                 : fields.integer(string='Stems'),
        'purchase_price'        : fields.char(size = 128, string= 'Purchase price'),
        'farm_total'            : fields.float(string= 'Farm total'),
        'sale_price'            : fields.char(size = 128, string= 'Sale price'),
        'total'                 : fields.float(string= 'Total'),
        'profit'                : fields.float(string= 'Profit'),
        'is_purchase'           : fields.boolean(string= 'Purchase'),
        'origin_id'             : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubCliente'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'total_qty_purchased'   : fields.function(_get_info, type='char', string='Purchased Qty', multi="_vals"),
        'qty'                   : fields.function(_get_info, type='char', string='BXS', multi = '_vals'),
        'stimated_qty'          : fields.function(_get_info, type='float', string='Full Boxes', multi="_vals"),
        'box'                   : fields.function(_get_info, type='integer', string='Box Id', help="Box Group Id", multi="_vals"),              
    }

    _order = "line_number"
    
    def split_purchase_line(self, cr, uid, ids, *args):
        
        obj = self.browse(cr,uid,ids[0])
        detalle = obj.detalle_id
        
        lengths = [l.length for l in detalle.length_ids]
        bxs_qty = detalle.qty if detalle.is_box_qty else (1 if not int(detalle.qty / (detalle.bunch_type * detalle.bunch_per_box)) else int(detalle.qty / (detalle.bunch_type * detalle.bunch_per_box)))
           
        vals = [(0,0,{
            'supplier_id'     : detalle.supplier_id.id if detalle.supplier_id else None,
            'type'            : detalle.type,
            'product_id'      : detalle.product_id.id,
            'variant_id'      : detalle.variant_id.id,            
            'length'          : ','.join(lengths),   
            'qty'             : detalle.qty,         
            'bunch_per_box'   : detalle.bunch_per_box,
            'bunch_type'      : detalle.bunch_type,             
            'qty_uom'         : str(bxs_qty) + ' ' + detalle.uom,
            'stems'           : detalle.qty * detalle.bunch_per_box * detalle.bunch_type if detalle.is_box_qty else detalle.qty
        })]
        
        context = {
            'default_detalle_id'      : detalle.id,  
            'default_parent_line_ids' : vals   
        }   
    
        return {
            'name': _("Detail Bunches"),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'split.purchase.line.wzd',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }        

    def delete_lines(self, cr, uid, ids, *args):
        obj = self.browse(cr,uid,ids[0])
       
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
        'cliente_id'            : fields.related('detalle_id','pedido_id','partner_id', type ='many2one',relation = 'res.partner', string ='Cliente'),
        'type'                  : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
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
        'supplier_ids'          : fields.char(string='Supplier Ids', size = 128),
       
        'total_purchase'        : fields.function(_get_quantity, type='float', string='Farm Total', multi='compute_data'),
        'total_sale'            : fields.function(_get_quantity, type='float', string='Total', multi='compute_data'),
        'profit'                : fields.function(_get_quantity, type='float', string='Profit', multi='compute_data'),
        'full_boxes'            : fields.function(_get_quantity, type='float', string='Full Boxes', multi = '_data'),
        'qty_bxs'               : fields.function(_get_quantity, type='char', string='BXS', multi = '_data'),
        'stimated_stems'        : fields.function(_get_quantity, type='integer', string='Stems', multi = '_data'),
    }

    def on_chance_vals(self, cr, uid, ids, is_box_qty,box_qty,tale_qty, bunch_type, bunch_per_box, uom, sale_price, length_ids, context=None):
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
                'total_purchase'    : qty * purchase_price if not is_box_qty else qty * bunch_per_box *  int(bunch_type) *  purchase_price,
                'total_sale'        : qty * sale_price if not is_box_qty else qty * bunch_per_box *  int(bunch_type) *  sale_price,
                'profit'            : qty * (sale_price - purchase_price) if not is_box_qty else qty * bunch_per_box *  int(bunch_type) *  (sale_price - purchase_price),
                'qty_bxs'           : str(qty_bxs) + ' ' + uom,
                'full_boxes'        : full_boxes,
                'stimated_stems'    : tale_qty if not is_box_qty else box_qty * bunch_per_box *  int(bunch_type),                
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
                'sale_price': detalle.sale_price,
                'origin': detalle.origin.id if detalle.origin else None,
                'subclient_id': detalle.subclient_id.id if detalle.subclient_id else None,
                'sucursal_id': detalle.sucursal_id.id if detalle.sucursal_id else None,                
            }
            self.pool.get('detalle.lines').write(cr,uid,[detalle.detalle_id.id], detalle_dict)
        
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
        'detalle_id'       : fields.many2one('detalle.line.wzd', 'Details'),
        'length'           : fields.char(string='Length', size = 128, required=True),
        'purchase_price'   : fields.float(string='Purchase Price'),
     }

    _defaults = {
         'detalle_id'     :  lambda self, cr, uid, context : context['detalle_id'] if context and 'detalle_id' in context else None,
    }

detalle_line_length_wzd()

class split_purchase_line_wzd(osv.osv_memory):
    _name = 'split.purchase.line.wzd'
    _description = 'Split'

    _columns = {
        'detalle_id'         : fields.many2one('detalle.lines', 'Details'),
        'parent_line_ids'    : fields.one2many('split.purchase.line.parent.wzd', 'parent_line_id', 'Parent Line'),
        'line_ids'           : fields.one2many('split.purchase.line.detail.wzd', 'detail_line_id', 'Detail Lines'),
    }
    
    def save(self, cr, uid, ids, arg, context=None):
        
        obj = self.browse(cr,uid,ids[0])
        detalle = obj.detalle_id
        
        total = 0
        stems = 0
        lines = []
        for line in obj.line_ids:
            
            if line.purchase_price <= 0.0:
                raise osv.except_osv('Error', "El precio de compra no puede ser menor o igual a cero.")
            
            total += line.bunches
            stems += line.box_qty * line.bunches * line.stems_per_bunch if detalle.is_box_qty else line.bunches * line.stems_per_bunch
            
            lines.append((0,0,{                
                'line_id'       : detalle.line_id.id if detalle.line_id else None,
                'box_id'        : detalle.box_id.id if detalle.box_id else None,
                'name'          : detalle.name,
                'type'          : detalle.type,
                'supplier_id'   : detalle.supplier_id.id,
                'product_id'    : detalle.product_id.id,
                'variant_id'    : line.variant_id.id if line.variant_id else None,
                'length_ids'    : [(0,0,{'length': line.length_id.length, 'purchase_price': line.length_id.purchase_price})],
                'qty'           : line.box_qty if detalle.is_box_qty else line.bunches * line.stems_per_bunch,
                'is_box_qty'    : detalle.is_box_qty,
                'bunch_per_box' : line.bunches,
                'bunch_type'    : line.stems_per_bunch,
                'uom'           : detalle.uom,
                'sale_price'    : detalle.sale_price,                 
                'origin'        : detalle.origin.id if detalle.origin else None,
                'subclient_id'  : detalle.subclient_id.id if detalle.subclient_id else None,
                'sucursal_id'   : detalle.sucursal_id.id if detalle.sucursal_id else None,
                'agrupada'      : True, 
                'group_id'      : detalle.id
            }))
        
        if total != detalle.bunch_per_box:
            raise osv.except_osv('Error', "La cantidad de bunches especificados por lineas debe ser igual a " + str(detalle.bunch_per_box))
        
        total_stems = detalle.qty * detalle.bunch_per_box * detalle.bunch_type if detalle.is_box_qty else detalle.qty
        if stems != total_stems:
            raise osv.except_osv('Error', "La cantidad total de tallos especificados por lineas debe ser igual a " + str(total_stems))
        
        pedido_id = detalle.pedido_id.id  
        detalle_id = detalle.id     
        self.pool.get('pedido.cliente').write(cr, uid, [pedido_id], {'purchase_line_ids': lines})
        self.pool.get('detalle.lines').write(cr, uid, [detalle_id], {'active': False})
        cr.execute("delete from summary_by_farm_wizard where pedido_id = %s", (pedido_id,)) 
        
        return {
            'name'      : _('Pedidos de Clientes'),
            'view_type' : 'form',
            'view_mode' : 'form',
            'res_model' : 'pedido.cliente',
            'type'      : 'ir.actions.act_window',
            'res_id'    : pedido_id,
        }  

split_purchase_line_wzd()

class split_purchase_line_parent_wzd(osv.osv_memory):
    _name = 'split.purchase.line.parent.wzd'
    _description = 'Parent Line'

    _columns = {
        'parent_line_id' : fields.many2one('split.purchase.line.wzd', 'Parent Line'),        
        'type'           : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'supplier_id'    : fields.many2one('res.partner', 'Farm'),
        'product_id'     : fields.many2one('product.product', 'Product'),
        'variant_id'     : fields.many2one('product.variant', 'Variety'),
        'length'         : fields.char('Lengths', size=256),
        'qty'            : fields.integer('Qty'),
        'bunch_per_box'  : fields.integer('Bunches'),
        'bunch_type'     : fields.integer('Stems x Bunch'),
        'stems'          : fields.integer('Stems'),
        'qty_uom'        : fields.char('Boxes',size=256)                 
    }     

split_purchase_line_parent_wzd()

class split_purchase_line_detail_wzd(osv.osv_memory):
    _name = 'split.purchase.line.detail.wzd'
    _description = 'Detail Line'
    
    _columns = {
        'detail_line_id' : fields.many2one('split.purchase.line.wzd', 'Purchase Line'),        
        'detalle_id'     : fields.many2one('detalle.lines', 'Details'),
        'type'           : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'supplier_id'    : fields.many2one('res.partner', 'Farm'),
        'product_id'     : fields.many2one('product.product', 'Product'),
        'variant_id'     : fields.many2one('product.variant', 'Variety', domain="[('product_id','=',product_id)]"),
        'length_id'      : fields.many2one('purchase.request.product.variant.length', 'Length'),            
        'bunches'        : fields.integer('Bunches'),
        'purchase_price' : fields.float(string='Price', help="Purchase Price"),  
        'stems_per_bunch': fields.integer('Stems per Bunch'),
        'box_qty'        : fields.integer('Boxes'),
        'stems'          : fields.integer('Stems'),       
    }
    
    def onchange_bunches(self, cr, uid, ids, stems_per_bunch, box_qty, bunches, context=None):
        res = {'value': {}}
        if not context:
            context = {}
        if stems_per_bunch and box_qty and bunches:           
            res['value']['stems'] = stems_per_bunch * box_qty * bunches                            
        return res 
    
    def onchange_variant_id(self, cr, uid, ids, detalle_id, supplier_id, product_id, variant_id, context=None):
        res = {'value': {}}
        if not context:
            context = {}
        if detalle_id and supplier_id and product_id and variant_id:           
            detalle = self.pool.get('detalle.lines').browse(cr, uid, detalle_id)   
            request_ids = self.pool.get('purchase.request.template').search(cr, uid, [('partner_id','=', supplier_id),('client_id', '=', detalle.pedido_id.partner_id.id)])
            request_variant_ids = self.pool.get('purchase.request.product.variant').search(cr, uid, [('template_id','in', request_ids),('product_id','=', product_id),('variant_id', '=', variant_id)])
            request_variant_length_ids = self.pool.get('purchase.request.product.variant.length').search(cr, uid, [('variant_id','in', request_variant_ids)])
            if request_variant_length_ids:
                res['domain']  =   {'length_id': [('id','in',request_variant_length_ids)]}
                res['value']['length_id'] = request_variant_length_ids[0]                          
        return res            
    
    def onchange_length_id(self, cr, uid, ids, length_id, context=None):
        res = {'value': {}} 
        if length_id:
            length = self.pool.get('purchase.request.product.variant.length').browse(cr, uid, length_id)       
            res['value']['purchase_price'] = length.purchase_price
        return res
    
    def get_default_type(self, cr, uid, context = None):         
        detalle_id = context['detalle_id'] if context and 'detalle_id' in context else None
        if detalle_id:
            detalle = self.pool.get('detalle.lines').browse(cr, uid, detalle_id)
            return detalle.type                     
        return 'standing_order'
    
    def get_default_supplier_id(self, cr, uid, context = None):
         
        detalle_id = context['detalle_id'] if context and 'detalle_id' in context else None
        if detalle_id:
            detalle = self.pool.get('detalle.lines').browse(cr, uid, detalle_id)             
            return detalle.supplier_id.id                        
        return None
    
    def get_default_product_id(self, cr, uid, context = None):
         
        detalle_id = context['detalle_id'] if context and 'detalle_id' in context else None
        if detalle_id:
            detalle = self.pool.get('detalle.lines').browse(cr, uid, detalle_id)             
            return detalle.product_id.id                        
        return None
    
    def get_default_variant_id(self, cr, uid, context = None):
         
        detalle_id = context['detalle_id'] if context and 'detalle_id' in context else None
        if detalle_id:
            detalle = self.pool.get('detalle.lines').browse(cr, uid, detalle_id)             
            return detalle.variant_id.id                        
        return None   
    
    def get_default_stems_per_bunch(self, cr, uid, context = None):
         
        detalle_id = context['detalle_id'] if context and 'detalle_id' in context else None
        if detalle_id:
            detalle = self.pool.get('detalle.lines').browse(cr, uid, detalle_id)             
            return detalle.bunch_type                        
        return None
    
    def get_default_box_qty(self, cr, uid, context = None):
         
        detalle_id = context['detalle_id'] if context and 'detalle_id' in context else None
        if detalle_id:
            detalle = self.pool.get('detalle.lines').browse(cr, uid, detalle_id)             
            return detalle.qty if detalle.is_box_qty else 1                        
        return None
     
    
    _defaults = {
        'detalle_id'     :  lambda self, cr, uid, context : context['detalle_id'] if context and 'detalle_id' in context else None,
        'type'           :  get_default_type,
        'supplier_id'    :  get_default_supplier_id,
        'product_id'     :  get_default_product_id,
        'variant_id'     :  get_default_variant_id,
        'stems_per_bunch':  get_default_stems_per_bunch,
        'box_qty'        :  get_default_box_qty                 
    }     

split_purchase_line_detail_wzd()