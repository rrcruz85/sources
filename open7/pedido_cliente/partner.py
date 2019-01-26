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

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def search(self, cr, uid, args, offset=0, limit=None, order=None,context=None, count=False):
        if context is None:
            context = {}
        customers_ids = super(res_partner, self).search(cr, uid, args,offset,limit,order, context,count)
        if context and 'cliente_id' in context and context['cliente_id'] and context['cliente_id'] in customers_ids:
            customers_ids.remove(context['cliente_id'])
        if context and 'subcliente_de' in context and context['subcliente_de']:
            customers_ids =[s.id for s in self.browse(cr, uid, context['subcliente_de']).sub_client_ids]
        return customers_ids

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):

        if context and 'cliente_id' in context and context['cliente_id']:
            customers_ids = self.pool.get('res.partner').search(cr, user, [('customer','=',True)])
            if context['cliente_id'] in customers_ids:
                customers_ids.remove(context['cliente_id'])
            return self.name_get(cr, user, customers_ids, context)

        if context and 'get_supplier_ids' in context and context['get_supplier_ids']:
            customers_ids = context['get_supplier_ids'].split(',')
            customers_ids = list(map(lambda x: int(x), customers_ids))
            return self.name_get(cr, user, customers_ids, context)

        if context and 'subcliente_de' in context and context['subcliente_de']:
            subclient_ids =[s.id for s in self.browse(cr, user, context['subcliente_de']).sub_client_ids]
            return self.name_get(cr, user, subclient_ids, context)

        if context.get('from_wizard_rqt', False):
            suppliers = []
            pedido = self.pool.get('pedido.cliente').browse(cr,user, context['from_wizard_rqt'])
            for v in pedido.purchase_line_ids:
                if v.supplier_id and v.supplier_id.id not in suppliers:
                    suppliers.append(v.supplier_id.id)
            return self.name_get(cr, user, suppliers, context)

        if context.get('search_just_suppliers', False):
            variant = self.pool.get('request.product.variant').browse(cr, user, context['search_just_suppliers'])
            product_variants = self.pool.get('purchase.request.product.variant').browse(cr, user, self.pool.get('purchase.request.product.variant').search(cr, user, [('product_id', '=', variant.product_id.id),('variant_id', '=', variant.variant_id.id)]))
            suppliers = [p.template_id.partner_id.id for p in product_variants if variant.pedido_id.partner_id.id == p.template_id.client_id.id]
            return self.name_get(cr, user, suppliers, context)

        elif context.get('from_wizard', False) and context.get('from_subclient', False):
            partner_ids = []
            if ('default_client_id' in context and context['default_client_id']):
                partner_id = context['default_client_id'] if 'default_client_id' in context and context['default_client_id'] else None
                if partner_id:
                    partner_ids = [partner_id]
            else:
                partner_ids = self.pool.get('res.partner').search(cr, user, [], context=context)
            partners = self.pool.get('res.partner').browse(cr, user, partner_ids, context=context)

            subclient_ids_list = []
            for partner in partners:
                for subclient in partner.sub_client_ids:
                    if subclient.id not in subclient_ids_list:
                        subclient_ids_list.append(subclient.id)
            return self.name_get(cr, user, subclient_ids_list, context)

        return super(res_partner, self).name_search(cr, user, name, args, operator=operator, context=context, limit=limit)

    _columns = {
            'sale_request_ids'      : fields.one2many('sale.request', 'partner_id', 'Ordenes de Ventas'),
            'purchase_template_ids' : fields.one2many('purchase.request.template', 'partner_id', 'Plantillas de Compras'),
            'sub_client_ids'        : fields.many2many('res.partner', 'subclient_relation', 'supplier_id', 'client_id', 'Subclientes'),
            'tipo_neg_id'           : fields.many2one('res.partner.tipo.negociacion','Tipo Negociacion'),
            'tipo_flete'            : fields.selection([('cf_f_0', 'C&F Flete Cero'),('fob_f_0', 'FOB Flete Cero'),('fob_f_p', 'FOB Flete Pagado')], string = 'Flete'),
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if 'from_subclient' in context and context['from_subclient']:
            vals['supplier'] = False
            vals['customer'] = True
        return super(res_partner, self).create(cr, uid, vals, context)

res_partner()

class sale_request(osv.osv):
    _name = 'sale.request'
    _description = 'sale.request'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {}
            dias = []
            products = []
            if obj.lunes:
                dias.append('Lun')
            if obj.martes:
                dias.append('Mar')
            if obj.miercoles:
                dias.append('Mie')
            if obj.jueves:
                dias.append('Jue')
            if obj.viernes:
                dias.append('Vie')
            if obj.sabado:
                dias.append('Sab')
            if obj.domingo:
                dias.append('Dom')
            for p in obj.variant_ids:
                if p.product_id.name_template not in products:
                    products.append(p.product_id.name_template)
            res[obj.id]['periodicidad'] = '-'.join(dias)
            res[obj.id]['products'] = '-'.join(products)


        return res

    _columns = {
        'partner_id'            : fields.many2one('res.partner', string ='Client', required = True),
        'variant_ids'           : fields.one2many('sale.request.product.variant', 'template_id',string ='Products'),

        'freight_agency_id'     : fields.many2one('freight.agency', 'Freight Agency'),
        'days'                  : fields.integer('Dias Anticipacion', help="Dias de Anticipo a la fecha de arribo al aeropuerto"),

        'lunes'                 : fields.boolean('Lunes'),
        'martes'                : fields.boolean('Martes'),
        'miercoles'             : fields.boolean('Miercoles'),
        'jueves'                : fields.boolean('Jueves'),
        'viernes'               : fields.boolean('Viernes'),
        'sabado'                : fields.boolean('Sabado'),
        'domingo'               : fields.boolean('Domingo'),

        'periodicidad'         : fields.function(_get_info, type='char', string='Periodicidad', multi = "vals"),
        'products'         : fields.function(_get_info, type='char', string='Producto', multi = "vals"),
    }

    _defaults = {
        'days'          :  2,
        'partner_id'    :  lambda self, cr, uid, context : context['partner_id'] if context and 'partner_id' in context else None,
    }

sale_request()

class sale_request_product_variant(osv.osv):
    _name = 'sale.request.product.variant'
    _description = 'Variety'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'stimated_boxs':0, 'stimated_stems':0,'stimated_qty':'BXS','qty':'BXS','full_boxes':0,'sale_price':0, 'lenghts':'','str_sale_price':''}
            if obj.is_box_qty:
                res[obj.id]['stimated_stems'] = (obj.box_qty * int(obj.bunch_type) * obj.bunch_per_box)
                res[obj.id]['stimated_qty'] = str(res[obj.id]['stimated_stems']) + ' Stems'
                res[obj.id]['qty'] = str(obj.box_qty) + ' BXS'
            else:
                res[obj.id]['stimated_boxs'] =  float(obj.tale_qty) / (int(obj.bunch_type) * obj.bunch_per_box * uom[obj.uom]) if obj.bunch_type and obj.bunch_per_box and obj.uom else 0
                res[obj.id]['stimated_qty'] = str(res[obj.id]['stimated_boxs']) + ' BXS'
                res[obj.id]['qty'] = str(obj.tale_qty) + ' Stems'

            bxs_qty = obj.box_qty if obj.is_box_qty else  (1 if obj.bunch_type and obj.bunch_per_box and not (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)) else (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)) if obj.bunch_type and obj.bunch_per_box else 0)
            prices = [l.sale_price for l in obj.length_ids]
            res[obj.id]['sale_price'] = sum(prices)/len(prices) if prices else 0
            res[obj.id]['str_sale_price'] = '-'.join([str(l.sale_price) for l in obj.length_ids])
            res[obj.id]['lenghts'] =  '-'.join([l.length for l in obj.length_ids])
            res[obj.id]['bxs_qty'] =  str(bxs_qty) + ' ' + obj.uom
            full_boxes = float(bxs_qty)/uom[obj.uom]
            res[obj.id]['full_boxes'] = full_boxes
        return res

    _columns = {
        'template_id'           : fields.many2one('sale.request', string ='Plantilla', required = True),
        'cliente_id'           : fields.related('template_id','partner_id', type ='many2one',relation = 'res.partner', string ='Cliente'),
        'product_id'            : fields.many2one('product.product','Product'),
        'variant_id'            : fields.many2one('product.variant','Variety'),        
        'length_ids'            : fields.one2many('sale.request.product.variant.length','variant_id','Length'),
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'box_qty'               : fields.integer('BXS'),
     	'tale_qty'              : fields.integer('Stems'),
		'bunch_per_box'         : fields.integer('Bunch per Box'),
        'bunch_type'            : fields.integer( 'Stems x Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')], string = 'UOM', help='Unit of Measure'),
        'subclient_id'          : fields.many2one('res.partner', string ='SubClient'),
        'sale_price'            : fields.function(_get_info, type='float', string='Sale Price', multi = '_data'),
        'str_sale_price'        : fields.function(_get_info, type='char', string='Sale Prices', multi = '_data'),
        'lenghts'               : fields.function(_get_info, type='char', string='Length', multi = '_data'),
        'stimated_boxs'         : fields.function(_get_info, type='integer', string='Stimated Boxs', multi = '_val'),
        'stimated_stems'        : fields.function(_get_info, type='integer', string='Stimated Stems', multi = '_val'),
        'stimated_qty'          : fields.function(_get_info, type='char', string='Stimated Qty', multi = '_val'),
        'qty'                   : fields.function(_get_info, type='char', string='Qty', multi = '_val'),
        'full_boxes'            : fields.function(_get_info, type='float', string='Full Boxes', multi = '_data'),
        'bxs_qty'               : fields.function(_get_info, type='char', string='BXS', multi = '_data'),
    }
	
    def on_change_vals(self, cr, uid, ids, is_box_qty, box_qty, tale_qty, bunch_per_box, bunch_type, uom, context=None):
        res = {'value':{'stimated_stems':0,'stimated_boxs':0, 'full_boxes':0}}
        uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
        if is_box_qty:
            res['value']['stimated_stems'] = box_qty * int(bunch_type)* bunch_per_box
        else:
            res['value']['stimated_boxs'] = float(tale_qty) / (int(bunch_type) * bunch_per_box)  if bunch_type and bunch_per_box else 0

        bxs_qty = box_qty if is_box_qty else  (1  if not (tale_qty / (int(bunch_type) * bunch_per_box)) else (tale_qty / (int(bunch_type) * bunch_per_box)))
        res['value']['bxs_qty']  = str(bxs_qty) + ' ' + uom
        full_boxes = float(bxs_qty)/uom_dict[uom]
        res['value']['full_boxes'] = full_boxes
        return res

    def get_client(self,cr, uid, context):
        if context and 'cliente_id' in context and context['cliente_id']:
            return context['cliente_id']
        return  False

    _defaults = {
        'bunch_per_box'    :  10,
        'bunch_type'    :  25,
		'uom'           :  'HB',
        'product_id'     :  lambda self, cr, uid, context : context['product_id'] if context and 'product_id' in context else None,
        'template_id'   :  lambda self, cr, uid, context : context['template_id'] if context and 'template_id' in context else None,
        'cliente_id'   :  get_client,
    }

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
            (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

sale_request_product_variant()

class sale_request_product_variant_length(osv.osv):
    _name = 'sale.request.product.variant.length'
    _description = 'Variety Length'

    _columns = {
        'variant_id'            : fields.many2one('sale.request.product.variant','Variety'),
        'length'           : fields.char(string='Length', size = 128),
        'sale_price'            : fields.float(string='Sale Price'),
	}

    _defaults = {
        'variant_id'     :  lambda self, cr, uid, context : context['variant_id'] if context and 'variant_id' in context else None,
    }

sale_request_product_variant_length()

class purchase_request_template(osv.osv):
    _name = 'purchase.request.template'
    _description = 'Plantilla de Compra'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {}
            dias = []
            products = []
            if obj.lunes:
                dias.append('Lun')
            if obj.martes:
                dias.append('Mar')
            if obj.miercoles:
                dias.append('Mie')
            if obj.jueves:
                dias.append('Jue')
            if obj.viernes:
                dias.append('Vie')
            if obj.sabado:
                dias.append('Sab')
            if obj.domingo:
                dias.append('Dom')
            for p in obj.variant_ids:
                if p.product_id.name_template not in products:
                    products.append(p.product_id.name_template)
            res[obj.id]['periodicidad'] = '-'.join(dias)
            res[obj.id]['products'] = '-'.join(products)

        return res

    _columns = {
        'partner_id'            : fields.many2one('res.partner', string ='Supplier', required = True),
        'client_id'             : fields.many2one('res.partner', string ='Cliente', required = True),
        'sub_client_ids'        : fields.many2many('res.partner', 'supplier_subclient_relation', 'supplier_id', 'client_id', 'Subclientes'),
        'variant_ids'           : fields.one2many('purchase.request.product.variant','template_id', 'Products'),
        'sucursal_id'           : fields.many2one('res.partner.subclient.sucursal', 'Sucursal'),
        'lunes'                 : fields.boolean('Lunes'),
        'martes'                : fields.boolean('Martes'),
        'miercoles'             : fields.boolean('Miercoles'),
        'jueves'                : fields.boolean('Jueves'),
        'viernes'               : fields.boolean('Viernes'),
        'sabado'                : fields.boolean('Sabado'),
        'domingo'               : fields.boolean('Domingo'),

        'periodicidad'          : fields.function(_get_info, type='char', string='Periodicidad', multi = "vals"),
        'products'              : fields.function(_get_info, type='char', string='Productos', multi = "vals"),
    }
	
    _defaults = {
        'partner_id'    :  lambda self, cr, uid, context : context['partner_id'] if context and 'partner_id' in context else None,
    }

purchase_request_template()

class purchase_request_product_variant(osv.osv):
    _name = 'purchase.request.product.variant'
    _description = 'Variety'

    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {'stimated_boxs':0,'stimated_stems':0, 'stimated_qty': '','request_qty': '','full_boxes':0, 'purchase_price':0, 'lenghts':'','str_purchase_price':''}
            if obj.is_box_qty:
                res[obj.id]['stimated_stems'] = obj.box_qty * int(obj.bunch_type) * obj.bunch_per_box
                res[obj.id]['stimated_qty'] = str(res[obj.id]['stimated_stems']) + ' Stems'
                res[obj.id]['request_qty'] = str(obj.box_qty) + ' BXS'
            else:
                res[obj.id]['stimated_boxs'] =  float(obj.tale_qty) / (int(obj.bunch_type) * obj.bunch_per_box * uom[obj.uom]) if obj.bunch_type and obj.bunch_per_box and obj.uom else 0
                res[obj.id]['stimated_qty'] = str(res[obj.id]['stimated_boxs']) + ' BXS'
                res[obj.id]['request_qty'] = str(obj.tale_qty) + ' Stems'

            bxs_qty = obj.box_qty if obj.is_box_qty else  (1 if obj.bunch_type and obj.bunch_per_box and not (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)) else (obj.tale_qty / (int(obj.bunch_type) * obj.bunch_per_box)) if obj.bunch_type and  obj.bunch_per_box else 0)
            prices = [l.purchase_price for l in obj.length_ids]
            res[obj.id]['purchase_price'] = sum(prices)/len(prices) if prices else 0
            res[obj.id]['lenghts'] =  '-'.join([l.length for l in obj.length_ids])
            res[obj.id]['str_purchase_price'] =  '-'.join([str(l.purchase_price) for l in obj.length_ids])
            res[obj.id]['bxs_qty'] =  str(bxs_qty) + ' ' + obj.uom
            full_boxes = float(bxs_qty)/uom[obj.uom]
            res[obj.id]['full_boxes'] = full_boxes

        return res

    _columns = {
        'template_id'           : fields.many2one('purchase.request.template', string ='Plantilla', required = True),
        'product_id'            : fields.many2one('product.product','Product'),
        'variant_id'            : fields.many2one('product.variant','Variety'),
        'cliente_id'            : fields.related('template_id','client_id', type ='many2one',relation = 'res.partner', string ='Cliente'),
        'subclient_id'          : fields.many2one('res.partner', string ='SubCliente'),

        'length_ids'            : fields.one2many('purchase.request.product.variant.length','variant_id','Length'),
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'box_qty'               : fields.integer('BXS'),
		'tale_qty'              : fields.integer('Stems'),
		'bunch_per_box'         : fields.integer('Bunch per Box'),
        'bunch_type'            : fields.integer( 'Stems x Bunch'),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                    ('HB', 'HB'),
                                                    ('QB', 'QB'),
                                                    ('OB', 'OB')],string="UOM", help = 'Unit of Measure'),
        'purchase_price'        : fields.function(_get_info, type='float', string='Purchase Price', multi = '_data'),
        'str_purchase_price'    : fields.function(_get_info, type='char', string='Purchase Prices', multi = '_data'),
        'lenghts'               : fields.function(_get_info, type='char', string='Length', multi = '_data'),
        'stimated_boxs'         : fields.function(_get_info, type='integer', string='Stimated Boxs', multi = '_data'),
        'stimated_stems'        : fields.function(_get_info, type='integer', string='Stimated Stems', multi = '_data'),
        'request_qty'           : fields.function(_get_info, type='char', string='Qty', multi = '_data'),
        'stimated_qty'          : fields.function(_get_info, type='char', string='Stimated Qty', multi = '_data'),
        'full_boxes'            : fields.function(_get_info, type='float', string='Full Boxes', multi = '_data'),
        'bxs_qty'               : fields.function(_get_info, type='char', string='BXS', multi = '_data'),
    }
	
    def on_change_vals(self, cr, uid, ids, is_box_qty, box_qty, tale_qty, bunch_per_box, bunch_type, uom, context=None):
        res = {'value':{'stimated_stems':0,'stimated_boxs':0,'full_boxes':0}}
        uom_dict = {'FB':1,'HB':2,'QB':4,'OB':8}
        if is_box_qty:
            res['value']['stimated_stems'] = box_qty * int(bunch_type)* bunch_per_box
        else:
            res['value']['stimated_boxs'] = float(tale_qty) / (int(bunch_type) * bunch_per_box)  if bunch_type and bunch_per_box else 0

        bxs_qty = box_qty if is_box_qty else  (1 if not (tale_qty / (int(bunch_type) * bunch_per_box)) else (tale_qty / (int(bunch_type) * bunch_per_box)))
        res['value']['bxs_qty']  = str(bxs_qty) + ' ' + uom
        full_boxes = float(bxs_qty)/uom_dict[uom]
        res['value']['full_boxes'] = full_boxes
        return res

    def get_client(self,cr, uid, context):
        if context and 'cliente_id' in context and context['cliente_id']:
            return context['cliente_id']
        return  False

    _defaults = {
        'bunch_per_box'    :  10,
        'bunch_type'    :  25,
		'uom'           :  'HB',
        'product_id'     :  lambda self, cr, uid, context : context['product_id'] if context and 'product_id' in context else None,
        'template_id'   :  lambda self, cr, uid, context : context['template_id'] if context and 'template_id' in context else None,
        'cliente_id'   :  get_client,
    }

    def _check_bunch_type(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.bunch_type > 0 and obj.bunch_type <= 25

    _constraints = [
        (_check_bunch_type, 'El valor del campo Stems x Bunch debe ser mayor que 0 y menor o igual que 25.', []),
    ]

purchase_request_product_variant()

class purchase_request_product_variant_length(osv.osv):
    _name = 'purchase.request.product.variant.length'
    _description = 'Variety Length'
    _rec_name = 'length'
    
    _columns = {
        'variant_id'            : fields.many2one('purchase.request.product.variant','Variety'),
        'length'                : fields.char(string='Length', size = 128),
        'purchase_price'        : fields.float(string='Purchase Price'),
	}
    
    _defaults = {
        'variant_id'     :  lambda self, cr, uid, context : context['variant_id'] if context and 'variant_id' in context else None,
    }

purchase_request_product_variant_length()

class res_partner_subclient_sucursal(osv.osv):
    _name = 'res.partner.subclient.sucursal'
    _description = 'res.partner.subclient.sucursal'
    _columns = {
        'name'      : fields.char(size = 128, string='Nombre'),
    }

res_partner_subclient_sucursal()

class res_partner_tipo_negociacion(osv.osv):
    _name = 'res.partner.tipo.negociacion'
    _description = 'Tipo de Negociacion'
    _columns = {
        'codigo'      : fields.char(size = 10, string='Codigo', required = True),
        'name'      : fields.char(size = 128, string='Nombre',required = True),
    }

res_partner_tipo_negociacion()
