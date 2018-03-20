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

    def _get_purchase_lines(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for id in ids:
            lines = self.pool.get('purchase.lines.wzd').search(cr,uid,[('pedido_id','=',id)])
            if lines:
                self.pool.get('purchase.lines.wzd').unlink(cr,uid,lines)
            cr.execute( "SELECT "+
                        "pedido_cliente.id as pedido_id,"+
                        "detalle_lines.type,"+
                        "detalle_lines.supplier_id,"+
                        "detalle_lines.product_id,"+
                        "detalle_lines.variant_id,"+
                        "detalle_lines.lengths as lenght,"+
                        "detalle_lines.qty as purchased_qty,"+
                        "detalle_lines.purchase_price::varchar purchase_price,"+
                        "detalle_lines.sale_price::varchar sale_price,"+
                        "case when detalle_lines.is_box_qty then detalle_lines.qty * detalle_lines.bunch_type::int * detalle_lines.bunch_per_box * detalle_lines.purchase_price else detalle_lines.qty * detalle_lines.purchase_price end as farm_total,"+
                        "case when detalle_lines.is_box_qty then detalle_lines.qty * detalle_lines.bunch_type::int * detalle_lines.bunch_per_box * detalle_lines.sale_price else detalle_lines.qty * detalle_lines.sale_price end as total,"+
                        "case when detalle_lines.is_box_qty then (detalle_lines.qty * detalle_lines.bunch_type::int * detalle_lines.bunch_per_box) * (detalle_lines.sale_price - detalle_lines.purchase_price) else detalle_lines.qty * (detalle_lines.sale_price - detalle_lines.purchase_price) end as profit,"+
                        "detalle_lines.origin as origin_id,"+
                        "detalle_lines.sucursal_id as sucursal_id,"+
                        "detalle_lines.subclient_id as subclient_id,"+
                        "detalle_lines.id as detalle_id,"+
                        "detalle_lines.bunch_type as bunch_type,"+
                        "detalle_lines.bunch_per_box as bunch_per_box,"+
                        "detalle_lines.uom as uom,"+
                        "request_product_variant.line,"+
                        "detalle_lines.confirmada "+
                        "FROM "+
                        "public.detalle_lines,"+
                        "public.request_product_variant,"+
                        "public.pedido_cliente "+
                        "WHERE "+
                        "detalle_lines.pedido_id = pedido_cliente.id "+
                        "AND detalle_lines.line_id = request_product_variant.id "+
                        "AND pedido_cliente.id = %s " +
                        "order by " +
                        "request_product_variant.line ", (id,))

            result = cr.fetchall()
            list_ids = []
            for record in result:
                cr.execute("SELECT " +
                           "sum((case when is_box_qty then box_qty * bunch_type::int * bunch_per_box else tale_qty end))" +
                           "from PUBLIC.request_product_variant as v " +
                           "WHERE " +
                           "v.pedido_id = %s and " +
                           "v.product_id = %s and " +
                           "v.variant_id = %s " , (id, record[3], record[4],))
                result = cr.fetchone()
                request_qty = result[0]

                vals = {
                    'pedido_id'     : record[0],
                    'request_qty'   : request_qty,
                    'type'   : record[1],
                    'supplier_id'   : record[2],
                    'product_id'   : record[3],
                    'variant_id'    : record[4],
                    'lenght'        : record[5],
                    'purchased_qty' : record[6],
                    'purchase_price': record[7],
                    'farm_total'    : record[9],
                    'sale_price'    : record[8],
                    'total'         : record[10],
                    'profit'        : record[11],
                    'origin_id'     : record[12],
                    'sucursal_id'   : record[13],
                    'subclient_id'  : record[14],
                    'detalle_id'    : record[15],
                    'bunch_type'    : record[16],
                    'bunch_per_box' : record[17],
                    'uom': record[18],
                    'line': record[19],
                    'confirmada': record[20]
                }
                list_ids.append(self.pool.get('purchase.lines.wzd').create(cr,uid,vals))
            res[id] = list_ids
        return res

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            boxes = 0
            stems = 0
            tipo_flete = obj.partner_id.tipo_flete if obj.partner_id.tipo_flete else 'n'
            for v in obj.variant_ids:
                if v.is_box_qty:
                    boxes += math.ceil(float(v.box_qty)/uom[v.uom])
                    stems += math.ceil(float(v.box_qty * int(v.bunch_type) * v.bunch_per_box))
                else:
                    stems += math.ceil(float(v.tale_qty))
                    boxes += math.ceil(float(v.tale_qty)/ (int(v.bunch_type) * v.bunch_per_box  * uom[v.uom]))
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
        'boxes'         : fields.function(_get_info, type='integer', string='Full Boxes', multi = '_val'),
        'stems'        : fields.function(_get_info, type='integer', string='Stems', multi = '_val'),
        'tipo_flete'        : fields.function(_get_info, type='char', string='Tipo Flete', multi = '_val'),
        'line_ids'              : fields.function(_get_purchase_lines, type='one2many', relation="purchase.lines.wzd", string='Purchase Lines'),

        'account_invoice_ids': fields.one2many('account.invoice', 'pedido_cliente_id', 'Invoices'),
        'airline_id': fields.many2one('pedido_cliente.airline', string='Airline'),
        'number': fields.char('Flight Number'),
        'precio_flete'  : fields.float('Precio Flete', digits = (0,2)),
        'sale_request_id' : fields.many2one('sale.request', 'Sale Request'),
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
        'type'         : 'open_market',
    }

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
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            lines = []
            purchased_ids = []
            if obj.subclient_id:
                purchased_ids = self.pool.get('detalle.lines').search(cr,uid, [('line_id', '=',obj.id),('subclient_id', '=',obj.subclient_id.id) ])

            if purchased_ids:
                purchased_lines = self.pool.get('detalle.lines').browse(cr,uid, purchased_ids)
                lines = [p.qty * int(p.bunch_type) * p.bunch_per_box if p.is_box_qty else p.qty  for p in purchased_lines]

            purchased_qty = sum(lines) if lines else 0
            request_qty = obj.box_qty * obj.bunch_per_box * int(obj.bunch_type) if obj.is_box_qty else obj.tale_qty
            missing_qty = request_qty - purchased_qty

            res[obj.id] = {'stimated_stems':0, 'full_boxes': 0,'request_qty': '','missing_qty':0,'sale_price':0}
            if obj.is_box_qty:
                res[obj.id]['request_qty'] = str(obj.box_qty) + ' BXS'
                res[obj.id]['stimated_stems'] = obj.box_qty * int(obj.bunch_type) * obj.bunch_per_box
            else:
                res[obj.id]['request_qty'] = str(obj.tale_qty) + ' Stems'
                res[obj.id]['stimated_stems'] = obj.tale_qty

            bxs_qty = obj.box_qty if obj.is_box_qty else (1 if not (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)) else (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)))
            res[obj.id]['qty'] =  str(bxs_qty) + ' ' + obj.uom
            full_boxes = float(bxs_qty)/uom[obj.uom]
            res[obj.id]['full_boxes'] = full_boxes

            prices = [l.sale_price for l in obj.length_ids]
            lengths = [l.length for l in obj.length_ids]
            res[obj.id]['sale_price'] = sum(prices)/len(prices) if prices else 0
            res[obj.id]['lengths'] = '-'.join(lengths) if lengths else ''
            res[obj.id]['missing_qty'] = missing_qty
            res[obj.id]['missing_qty2'] = '-' + str(int(missing_qty)) if missing_qty > 0 else '0' if missing_qty ==0 else '+' + str(int(math.fabs(missing_qty)))

        return res

    def _get_ids(self, cr, uid, ids, context=None):
        res = []
        for length in self.pool.get('request.product.variant.length').browse(cr, uid, ids, context=context):
            if length.variant_id and length.variant_id.id not in res:
                res.append(length.variant_id.id)
        return res

    _columns = {
        'line'                      : fields.integer(string = '#', help= 'Line Number'),
        'pedido_id'             : fields.many2one('pedido.cliente', string ='Pedido',ondelete='cascade'),
        'cliente_id'           : fields.related('pedido_id','partner_id', type ='many2one',relation = 'res.partner', string ='Cliente'),
        'type'                     : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Type'),
        'product_id'           : fields.many2one('product.product','Product'),
        'variant_id'            : fields.many2one('product.variant','Variety'),
        'length_ids'            : fields.one2many('request.product.variant.length','variant_id','Lengths'),
        'length_deleted'     : fields.boolean('Deleted'),
      	'is_box_qty'           : fields.boolean('Box Packing?'),
        'is_standing_order' : fields.boolean('Is standing order'),
        'box_qty'               : fields.integer('BXS'),
		'tale_qty'               : fields.integer('Stems'),
		'bunch_per_box'     : fields.integer('Bunch per Box'),
        'bunch_type'            : fields.integer( 'Stems x Bunch'),
        'uom'                      : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], 'UOM'),
        'subclient_id'          : fields.many2one('res.partner', 'SubCliente'),
        'purchased_line_ids' : fields.one2many('detalle.lines','line_id','Purchased Lines'),

        'sale_price'              : fields.function(_get_info, type='float', string='Sale Price', multi = '_data'),
        'lengths'                  : fields.function(_get_info, type='char', string='Lengths', multi = '_data',
                                        store = {
                                            'request.product.variant': (lambda self,cr,uid,ids,c=None: ids, ['length_ids','length_deleted'], 10),
                                            'request.product.variant.length': (_get_ids, ['length'], 10),
                                        }),
        'qty'                        : fields.function(_get_info, type='char', string='BXS', multi = '_data'),
        'stimated_stems'     : fields.function(_get_info, type='integer', string='Stimated Stems', multi = '_data'),
        'full_boxes'              : fields.function(_get_info, type='float', string='Full Boxes', multi = '_data'),
        'request_qty'           : fields.function(_get_info, type='char', string='Qty', multi = '_data'),
        'missing_qty'           : fields.function(_get_info, type='integer', string='Misssing Qty', multi = '_data'),
        'missing_qty2'           : fields.function(_get_info, type='char', string='Misssing Qty', multi = '_data'),
    }

    _order = "line"

    def on_change_vals(self, cr, uid, ids, is_box_qty, box_qty, tale_qty, bunch_per_box, bunch_type, uom, context=None):
        res = {'value':{'stimated_stems':0,'qty':0, 'full_boxes': 0}}
        uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
       	if is_box_qty:
           res['value']['stimated_stems'] = box_qty * int(bunch_type)* bunch_per_box
        else:
           res['value']['stimated_stems'] = tale_qty
        bxs_qty = box_qty if is_box_qty else  (1  if not (tale_qty / (int(bunch_type) * bunch_per_box)) else (tale_qty / (int(bunch_type) * bunch_per_box)))
        res['value']['qty']  = str(bxs_qty) + ' ' + uom
        full_boxes = float(bxs_qty)/uom_dict[uom]
        res['value']['full_boxes'] = full_boxes
        return res

    def get_default_line_number(self, cr, uid, context=None):
        if context and 'lines' in context:
            return len(context['lines']) + 1
        else:
            return 1

    def get_client(self, cr, uid, context):
        if context and 'cliente_id' in context and context['cliente_id']:
            return context['cliente_id']
        return False

    _defaults = {
        'bunch_per_box'    :  10,
        'type'              : 'open_market',
        'bunch_type'   :  25,
		'uom'              :  'HB',
        'product_id'     :  lambda self, cr, uid, context : context['product_id'] if context and 'product_id' in context else None,
        'pedido_id'      :  lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else None,
        'line'               : get_default_line_number,
        'cliente_id'   :  get_client,
    }

    def on_change_variant(self, cr, uid, ids, variant_id, context=None):
        res = {'value':{}}
        if variant_id and 'cliente_id' in context and context['cliente_id']:
            cliente = self.pool.get('res.partner').browse(cr, uid, context['cliente_id'])
            res['value']['description'] = self.pool.get('product.variant').browse(cr, uid, variant_id).description
            for l in cliente.purchase_template_ids:
                for v in l.variant_ids:
                    if  v.variant_id.id == variant_id:
                        res['value']['purchase_price'] = v.purchase_price
                        res['value']['description'] =  v.length
        return res

    def search_providers(self, cr, uid, ids, *args):
        context = args[0]
        obj = self.browse(cr, uid, ids[0])
        context['default_request_id'] = obj.pedido_id.id
        context['default_product_variant_id'] = ids[0]
        pedido = self.pool.get('pedido.cliente').browse(cr, uid, obj.pedido_id.id)
        context['default_client_id'] = pedido.partner_id.id if pedido.partner_id else False

        variants = []
        product_variants = self.pool.get('purchase.request.product.variant').browse(cr, uid, self.pool.get('purchase.request.product.variant').search(cr, uid, [('product_id', '=', obj.product_id.id),('variant_id', '=', obj.variant_id.id)]))

        sale_prices = [v.sale_price for v in obj.length_ids]
        my_lengths = [v.length.upper() for v in obj.length_ids]
        sale_price = sum(sale_prices) / len(sale_prices) if sale_prices else 0

        funct_vals = self._get_info(cr,uid, ids, '', [])

        for pv in product_variants:
            if pv.template_id.client_id.id == pedido.partner_id.id:
                lengths = [p.length.upper() for p in pv.length_ids]

                if set(my_lengths) & set(lengths):
                    purchase_prices = [p.purchase_price for p in pv.length_ids]
                    purchase_price = sum(purchase_prices) / len(purchase_prices) if purchase_prices else 0
                    subclient_id = False
                    lengths = [(0,0,{'length': l.length, 'purchase_price': l.purchase_price})for l in pv.length_ids]

                    vals = {
                        'type' : 'open_market',
                        'request_id': obj.pedido_id.id,
                        'product_variant_id' : ids[0],
                        'res_partner_id': pv.template_id.partner_id.id,
                        'client_id': pedido.partner_id.id,
                        'product_id': obj.product_id.id,
                        'variant_id': obj.variant_id.id,
                        'length_ids':lengths,
                        'purchase_price': purchase_price,
                        'sale_price': sale_price,
                        'bunch_type': pv.bunch_type,
                        'bunch_per_box': pv.bunch_per_box,
                        'uom': pv.uom,
                        'qty': funct_vals[ids[0]]['missing_qty'],
                        'is_box_qty': pv.is_box_qty,
                        'origin': False,
                        'subclient_id': subclient_id,
                        'sucursal_id': pv.template_id.sucursal_id.id if pv.template_id.sucursal_id else False
                    }
                    variants.append((0, 0, vals))

        context['default_product_info_ids'] = variants

        return {
            'name': _("Product Suppliers"),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pedido_cliente.product_order_wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }

    def purchase(self, cr, uid, ids, *args):
        obj = self.browse(cr, uid, ids[0])
        sale_prices = [v.sale_price for v in obj.length_ids]
        sale_price = sum(sale_prices) / len(sale_prices) if sale_prices else 0
        qty_bxs = obj.box_qty if obj.is_box_qty else (1 if not (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)) else (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)))

        vals = self._get_info(cr,uid, ids, '', [])
        lengths = [(0,0,{'length': l.length, 'purchase_price': 0})for l in obj.length_ids]
        lengths_desc = [l.length for l in obj.length_ids]

        #Buscando Proveedores
        farm_ids = []
        l_ids = self.pool.get('purchase.request.template').search(cr,uid,[('client_id','=',obj.pedido_id.partner_id.id)])
        v_ids = self.pool.get('purchase.request.product.variant').search(cr,uid,[('template_id','in',l_ids), ('product_id','=',obj.product_id.id),('variant_id','=',obj.variant_id.id),('subclient_id','=',obj.subclient_id.id if obj.subclient_id else False)])
        if v_ids:
            for l in obj.length_ids:
                ll_ids = self.pool.get('purchase.request.product.variant.length').search(cr,uid,[('variant_id','in',v_ids),('length','=',l.length)])
                if ll_ids:
                    for ll in self.pool.get('purchase.request.product.variant.length').browse(cr,uid,ll_ids):
                        if ll.variant_id.template_id.partner_id.id not in farm_ids:
                            farm_ids.append(str(ll.variant_id.template_id.partner_id.id))
        context = {
            'default_pedido_id': obj.pedido_id.id,
            'default_product_variant_id': ids[0],
            'default_supplier_id': False,
            'default_product_id': obj.product_id.id,
            'default_variant_id': obj.variant_id.id,
            'default_is_box_qty': obj.is_box_qty,
            'default_box_qty': vals[ids[0]]['missing_qty']/(int(obj.bunch_type) * obj.bunch_per_box) if obj.is_box_qty else 0,
            'default_tale_qty': vals[ids[0]]['missing_qty'] if not obj.is_box_qty else 0,
            'default_bunch_type': obj.bunch_type,
            'default_bunch_per_box': obj.bunch_per_box,
            'default_uom': obj.uom,
            'default_qty_bxs': str(qty_bxs) + ' ' + obj.uom,
            'default_length_ids': lengths,
            'default_sale_price': sale_price,
            'default_origin': False,
            'default_subclient_id': obj.subclient_id.id if obj.subclient_id else False,
            'default_sucursal_id': False,
            #'default_supplier_ids': ','.join(farm_ids)
        }
        return {
            'name': _("Purchase Line"),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.line.wzd',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

request_product_variant()

class request_product_variant_length(osv.osv):
    _name = 'request.product.variant.length'
    _description = 'Variety Length'

    _columns = {
        'variant_id'            : fields.many2one('request.product.variant','Variety'),
        'length'           : fields.char(string='Length', size = 128),
        'sale_price'            : fields.float(string='Sale Price'),
	}

    _defaults = {
        'variant_id'     :  lambda self, cr, uid, context : context['variant_id'] if context and 'variant_id' in context else None,
    }

    def unlink(self, cr, uid, ids, context=None):
        v_ids = []
        for l in self.browse(cr, uid, ids, context=context):
            if l.variant_id and l.variant_id.id not in v_ids:
                v_ids.append(l.variant_id.id)
        result = super(request_product_variant_length, self).unlink(cr, uid, ids, context=context)
        for v in self.pool.get('request.product.variant').browse(cr,uid,v_ids):
            self.pool.get('request.product.variant').write(cr,uid,[v.id], {'length_deleted' : not v.length_deleted})
        return result

request_product_variant_length()

class detalle_line(osv.osv):
    _name = 'detalle.lines'
    _description = 'Detalle de compras'

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
        return super(detalle_line, self).search(cr, uid, args, offset, limit, order, context, count)

    def _get_info(self, cr, uid, ids, field_name, arg, context = None):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'purchase_price': 0, 'lengths' : ''}
            prices = [l.purchase_price for l in obj.length_ids]
            lengths = [l.length for l in obj.length_ids]
            res[obj.id]['purchase_price'] = sum(prices) / len(prices) if prices else 0
            res[obj.id]['lengths'] = '-'.join(lengths) if lengths else ''
        return res

    def _get_ids(self, cr, uid, ids, context=None):
        res = []
        for length in self.pool.get('detalle.lines.length').browse(cr, uid, ids, context=context):
            if length.detalle_id and length.detalle_id.id not in res:
                res.append(length.detalle_id.id)
        return res

    _columns = {
        'pedido_id'            : fields.many2one('pedido.cliente', 'Request',ondelete='cascade'),
        'line_id'                 : fields.many2one('request.product.variant', 'Lines'),
        'name'                  : fields.char(size = 128, string= 'Line Number'),
        'type'                    : fields.selection([('standing_order', 'Standing Order'), ('open_market','Open Market')], 'Order'),
        'supplier_id'           : fields.many2one('res.partner', 'Farm', required=True, domain=[('supplier', '=', True)]),
        'product_id'            : fields.many2one('product.product', string='Product',required=True),
        'variant_id'            : fields.many2one('product.variant', 'Variety', required=True),
        'length_ids'            : fields.one2many('detalle.lines.length','detalle_id','Lengths'),
        'qty'                      : fields.float('Qty'),
        'is_box_qty'            : fields.boolean('Box Packing?'),
		'bunch_per_box'         : fields.integer('Bunch per Box'),
        'bunch_type'            : fields.integer( 'Stems x Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], string = 'UOM', help= 'Unit of Measure'),
        'sale_price'            : fields.float(string='Sale Price'),
        'origin'                : fields.many2one('detalle.lines.origin', string='Origin'),
        'subclient_id'          : fields.many2one('res.partner', 'SubCliente'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'purchase_price'      : fields.function(_get_info, type='float', string='Purchase Price', multi = '_data',
                                        store={
                                            'detalle.lines': (lambda self, cr, uid, ids, c=None: ids, ['length_ids'], 10),
                                            'detalle.lines.length': (_get_ids, ['purchase_price'], 10),
                                        }),
        'lengths'                  : fields.function(_get_info, type='char', string='Lengths', multi = '_data',
                                        store={
                                            'detalle.lines': (lambda self, cr, uid, ids, c=None: ids, ['length_ids'], 10),
                                            'detalle.lines.length': (_get_ids, ['length'], 10),
                                        }),
        'confirmada'    : fields.boolean('Confirmada'),
    }

    _defaults = {
        'bunch_type': 25,
        'uom': 'HB',
        'type': 'open_market',
        'bunch_per_box' : 10,
        'pedido_id'    :lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else None,
    }

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

detalle_line()

class detalle_line_length(osv.osv):
    _name = 'detalle.lines.length'
    _description = 'Variety Length'

    _columns = {
        'detalle_id'            : fields.many2one('detalle.lines','Detalle', ondelete='cascade'),
        'length'           : fields.char(string='Length', size = 128),
        'purchase_price'            : fields.float(string='Purchase Price'),
	}

detalle_line_length()

class detalle_line_origin(osv.osv):
    _name = 'detalle.lines.origin'
    _description = 'detalle.lines.origin'
    
    _columns = {
        'name'                  : fields.char('Origen'),
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






