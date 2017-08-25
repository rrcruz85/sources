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

class product_order_wizard(osv.osv_memory):
    _name = 'pedido_cliente.product_order_wizard'
    _description = 'pedido_cliente.product_order_wizard'

    _columns = {
        'request_id'             : fields.integer('Id Pedido'),
        'product_variant_id' : fields.many2one('request.product.variant', 'Variant'),
        'client_id'            : fields.integer('Id Cliente'),
	    'product_info_ids'   : fields.one2many('pedido_cliente.product_order_wizard_info', 'wizard_id', 'Information'),
    }

    _defaults = {
        'client_id'              : lambda self, cr, uid, context : context['client_id'] if context and 'client_id' in context else 0,
        'request_id'              : lambda self, cr, uid, context : context['request_id'] if context and 'request_id' in context else 0,
    }

    def action_create(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if not obj.product_info_ids:
            raise osv.except_osv('Error', "Debe especificar al menos una linea de compra.")

        pedido = self.pool.get('pedido.cliente').browse(cr, uid, obj.request_id)
        for l in obj.product_info_ids:
            if not l.length_ids:
                name = l.product_id.name_template + ' ' + l.variant_id.name
                raise osv.except_osv('Error', "Debe especificar las longitudes y los precios de compra para el producto " + name)
            if l.qty == 0:
                name = l.product_id.name_template + ' ' + l.variant_id.name + l.lengths
                raise osv.except_osv('Error', "La cantidad del producto " + name + " no puede ser 0")
            if l.purchase_price == 0:
                name = l.product_id.name_template + ' ' + l.variant_id.name + l.lengths
                raise osv.except_osv('Error', "El precio de compra del producto " + name + " no puede ser 0")
            if l.sale_price == 0:
                name = l.product_id.name_template + ' ' + l.variant_id.name + l.lengths
                raise osv.except_osv('Error', "El precio de venta del producto " + name + " no puede ser 0")
            # if l.sale_price <= l.purchase_price:
            #     name = l.product_id.name_template + ' ' + l.variant_id.name + l.descripcion
            #     raise osv.except_osv('Error',
            #                          "El precio de venta del producto " + name + " no puede ser menor o igual al precio de compra")

            lengths = [(0,0,{'length': ll.length, 'purchase_price': ll.purchase_price}) for ll in l.length_ids]

            vals = {
                'pedido_id': pedido.id,
                'line_id': obj.product_variant_id.id,
                'type':  l.type,
                'supplier_id': l.res_partner_id.id,
                'product_id': l.product_id.id,
                'variant_id': l.variant_id.id,
                'length_ids': lengths,
                'qty': l.qty,
                'is_box_qty': l.is_box_qty,
                'bunch_type': l.bunch_type,
                'bunch_per_box': l.bunch_per_box,
                'uom': l.uom,
                'sale_price': l.sale_price,
                'origin': l.origin.id if l.origin else False,
                'subclient_id': l.subclient_id.id if l.subclient_id else False,
                'sucursal_id': l.sucursal_id.id if l.sucursal_id else False,
            }
            self.pool.get('detalle.lines').create(cr, uid, vals, context=context)

        return {
            'name': 'Pedidos de Clientes',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pedido.cliente',
            'type': 'ir.actions.act_window',
            'context': context,
            'res_id': pedido.id,
        }

product_order_wizard()

class product_order_wizard_info(osv.osv_memory):
    _name = 'pedido_cliente.product_order_wizard_info'
    _description = 'pedido_cliente.product_order_wizard_info'

    _columns = {
        'wizard_id'             : fields.many2one('pedido_cliente.product_order_wizard', 'Wizard'),
        'product_variant_id' : fields.many2one('request.product.variant', 'Variant'),
        'type'                  : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Order'),
        'request_id'             : fields.integer('Id Pedido'),
        'res_partner_id'        : fields.many2one('res.partner', 'Farm',),
        'client_id'            : fields.many2one('res.partner', 'Client'),
        'product_id'            : fields.many2one('product.product', 'Product'),
        'variant_id'            : fields.many2one('product.variant', 'Variety'),
        'length_ids'            : fields.one2many('product.order.wizard.info.length','wzd_id','Lengths'),
        'qty'                   : fields.integer('Quantity'),
        'is_box_qty'         : fields.boolean('Box Packing'),
        'bunch_per_box'         : fields.integer('Bunch per Box'),
        'bunch_type'            : fields.integer('Stems x Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                           ('HB', 'HB'),
                                                           ('QB', 'QB'),
                                                           ('OB', 'OB')], 'Unit of Measure'),
        'sale_price'            : fields.float('Sale Price', digits=(16, 2)),
        'origin'                : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubClient'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'purchased_boxes'         : fields.integer('Purchased Boxes'),
        'purchased_stems'         : fields.integer('Purchased Stems'),
    }

    def on_change_variety(self, cr, uid, ids, product_variant_id,supplier_id,product_id,variant_id,  context = None):
        res = {'value':{}}
        if product_variant_id and supplier_id and product_id and variant_id:
            #Sale Price
            product_variant = self.pool.get('request.product.variant').browse(cr,uid, product_variant_id)
            sale_prices =  [p.sale_price for p in product_variant.length_ids]
            res['value']['sale_price'] = sum(sale_prices)/len(sale_prices) if sale_prices else 0
            # Purchase Price
            suppliers = self.pool.get('purchase.request.template').search(cr, uid, [('partner_id', '=', supplier_id)])
            if suppliers:
                val_ids = self.pool.get('purchase.request.product.variant').search(cr, uid,[('template_id', '=', suppliers[0]),('product_id', '=', product_id),('variant_id', '=', variant_id)])
                if val_ids:
                    pv = self.pool.get('purchase.request.product.variant').browse(cr, uid, val_ids[0])
                    lengths = [(0,0,{'length': l.length, 'purchase_price': l.purchase_price})for l in pv.length_ids]
                    res['value']['length_ids'] = lengths
        return res

    _defaults = {
        'type': 'open_market',
        'bunch_type'       : 25,
        'bunch_per_box' : 10,
        'uom'                 : 'HB',
        'wizard_id'          : lambda self, cr, uid, context : context['wizard_id'] if context and 'wizard_id' in context else None,
        'client_id'        : lambda self, cr, uid, context : context['client_id'] if context and 'client_id' in context else 0,
        'request_id'              : lambda self, cr, uid, context : context['request_id'] if context and 'request_id' in context else 0,
        'product_variant_id'              : lambda self, cr, uid, context : context['product_variant_id'] if context and 'product_variant_id' in context else 0,
	}

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

product_order_wizard_info()

class product_order_wizard_info_length(osv.osv_memory):
    _name = 'product.order.wizard.info.length'
    _description = 'Variety Length'

    _columns = {
        'wzd_id'            : fields.many2one('pedido_cliente.product_order_wizard_info','Wizard'),
        'length'           : fields.char(string='Length', size = 128, required=True),
        'purchase_price'            : fields.float(string='Purchase Price'),
	}

    _defaults = {
        'wzd_id'     :  lambda self, cr, uid, context : context['wzd_id'] if context and 'wzd_id' in context else None,
    }

product_order_wizard_info_length()