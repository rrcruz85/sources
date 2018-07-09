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
from datetime import timedelta
import datetime

class generate_request_wizard(osv.osv_memory):
    _name = 'generate.request.wizard'
    _description = 'generate request'

    _columns = {
           'client_id'            : fields.many2one('res.partner', 'Cliente'),
    }

    def generate_requests(self, cr, uid, ids, arg, context=None):

        def proximo_dia(dia, dias_ant):
            dias = {'Mon':1,'Tue':2,'Wed':3,'Thu':4,'Fri':5,'Sat':6,'Sun':7}
            hoy = int(datetime.datetime.now().strftime('%w'))
            if hoy == 0:
                hoy = 7
            fecha_tmp = datetime.datetime.now()
            if hoy >= dias[dia]:
                delta = 7 - hoy + dias[dia]
                return (fecha_tmp + timedelta(days=delta)).date()
            if dias[dia] - hoy <= dias_ant:
                return (fecha_tmp + timedelta(days=7 + dias[dia] - hoy)).date()
            while hoy < dias[dia]:
                hoy = hoy + 1
                fecha_tmp = fecha_tmp + timedelta(days=1)
            return (fecha_tmp).date()

        def generar_pedido(fecha_pedido, p, cliente_id):
            request_lines = []
            list_details = []
            pedidos = []            
            dia_semana = int(fecha_pedido.strftime('%w'))
            dia =  dia_semana - p.days
            if dia <= 0:
                dia = 7 + dia
                
            dias = []
            if dia == 1:
                dias.append('pr.lunes = true ')
            if dia == 2:
                dias.append('pr.martes = true ')
            if dia == 3:
                dias.append('pr.miercoles = true ')
            if dia == 4:
                dias.append('pr.jueves = true ')
            if dia == 5:
                dias.append('pr.viernes = true ')
            if dia == 6:
                dias.append('pr.sabado = true ')
            if dia == 7:
                dias.append('pr.domingo = true ')

            line = 1
            for v in p.variant_ids:
                line_dict = {
                    'line'              : line,
                    'type'              : 'standing_order',
                    'product_id'        : v.product_id.id,
                    'variant_id'        : v.variant_id.id,
                    'is_standing_order' : True,                    
                    'subclient_id'      : v.subclient_id.id if v.subclient_id else False,
                    'length_ids'        : [(0, 0, {'length'        : l.length, 
                                                   'sale_price'    : l.sale_price,
                                                   'is_box_qty'    : l.is_box_qty,
                                                   'box_qty'       : l.box_qty,
                                                   'tale_qty'      : l.tale_qty,
                                                   'bunch_type'    : l.bunch_type,
                                                   'bunch_per_box' : l.bunch_per_box,
                                                   'uom'           : l.uom}) for l in v.length_ids]
                }
                
                request_lines.append((0,0, line_dict))   
                
                for l in v.length_ids:
                    cr.execute("select pr.partner_id, prv.product_id, prv.variant_id, prvl.length, prvl.purchase_price, prvl.bunch_per_box, prvl.bunch_type," +
                               "coalesce(prvl.is_box_qty, false) as is_box_qty, coalesce(prvl.box_qty,0) as box_qty, coalesce(prvl.tale_qty, 0) as tale_qty,"
                               "prvl.uom, pr.sucursal_id from purchase_request_template pr inner join purchase_request_product_variant prv on pr.id = prv.template_id " +
                               "inner join purchase_request_product_variant_length prvl on prv.id = prvl.variant_id " +
                               "where pr.client_id = %s and prv.subclient_id = %s and " + " and ".join(dias) + " and prv.product_id = %s and prv.variant_id = %s " +
                               "and prvl.length = %s", (cliente_id, v.subclient_id.id, v.product_id.id, v.variant_id.id, l.length,))
                    
                    stems_qty = l.tale_qty if not l.is_box_qty else l.box_qty * l.bunch_type * l.bunch_per_box
                    records = cr.fetchall()
                     
                    for r in records:
                        supplier_id = r[0]
                        product_id = r[1]
                        variant_id = r[2]
                        length = r[3]
                        purchase_price = r[4]
                        bunch_per_box = r[5]
                        bunch_type = r[6]
                        is_box_qty = r[7]
                        box_qty = r[8]
                        tale_qty = r[9]
                        uom = r[10]
                        sucursal_id = r[11]
                        
                        if stems_qty > 0:
                            supplier_qty = tale_qty if not is_box_qty else box_qty * bunch_per_box * bunch_type
                            qty = 0
                            if supplier_qty >= stems_qty:
                                qty = stems_qty
                                stems_qty = 0
                            else:
                                qty = supplier_qty
                                stems_qty -= supplier_qty  
                            
                            detalle_dict = {
                                'name'          : str(line),
                                'supplier_id'   : supplier_id,
                                'type'          : 'standing_order',
                                'product_id'    : product_id,
                                'variant_id'    : variant_id,
                                'length'        : length,
                                'is_box_qty'    : is_box_qty,
                                'qty'           : qty if not is_box_qty else round(float(qty)/(bunch_type * bunch_per_box), 2),
                                'bunch_type'    : bunch_type,
                                'bunch_per_box' : bunch_per_box,
                                'uom'           : uom,
                                'purchase_price': purchase_price,
                                'sale_price'    : l.sale_price,
                                'subclient_id'  : v.subclient_id.id if v.subclient_id else False,
                                'sucursal_id'   : sucursal_id or False,
                            }
                            list_details.append((0, 0, detalle_dict))                   
                
                line += 1   
            
            fecha_pedido = fecha_pedido - timedelta(days=p.days)

            if fecha_pedido >= datetime.datetime.now().date():

                tipo_flete = self.pool.get('res.partner').browse(cr, uid, cliente_id).tipo_flete
                precio_flete = 0
                if tipo_flete and tipo_flete == 'fob_f_p':
                    precio_flete = 0.01
                    
                cliente_id = cliente_id if cliente_id else p.partner_id.id
                
                cr.execute("select count(*) from pedido_cliente where partner_id = %s", (cliente_id,))
                cant = cr.fetchall()[0][0] + 100                

                pedido_dict = {     
                    'name'              : cant,                  
                    'partner_id'        : cliente_id,
                    'request_date'      : fecha_pedido,
                    'state'             : 'draft',
                    'type'              : 'standing_order',
                    'freight_agency_id' : p.freight_agency_id.id if p.freight_agency_id else None,
                    'variant_ids'       : request_lines,
                    'purchase_line_ids' : list_details,
                    'precio_flete'      : precio_flete,
                    'sale_request_id'   : p.id,
                }
                
                pedido_id = self.pool.get('pedido.cliente').create(cr, uid, pedido_dict)                
                pedidos.append(pedido_id)
                v_ids = self.pool.get('request.product.variant').search(cr, uid, [('pedido_id', '=', pedido_id)])
                v_objs = self.pool.get('request.product.variant').browse(cr, uid, v_ids)
                for v in v_objs:
                    line_ids = self.pool.get('detalle.lines').search(cr, uid, [('pedido_id', '=', pedido_id),('name', '=', str(v.line))])
                    self.pool.get('detalle.lines').write(cr, uid, line_ids, {'line_id': v.id})
                            
            return pedidos

        hoy = int(datetime.datetime.now().strftime('%w'))
        if hoy == 0:
            hoy = 7
            
        obj = self.browse(cr,uid, ids[0])
        cliente_id = obj.client_id.id if obj.client_id else False
        sale_template_ids = []
        pedidos = []
        
        if obj.client_id:
            sale_template_ids = self.pool.get('sale.request').search(cr,uid,[('partner_id','=', obj.client_id.id)])
        else:
            sale_template_ids = self.pool.get('sale.request').search(cr,uid,[])
        
        for p in self.pool.get('sale.request').browse(cr,uid, sale_template_ids):
            days = {}
            if p.lunes:
                days['Mon'] = 1
            if p.martes:
                days['Tue'] = 2
            if p.miercoles:
                days['Wed'] = 3
            if p.jueves:
                days['Thu'] = 4
            if p.viernes:
                days['Fri'] = 5
            if p.sabado:
                days['Sat'] = 6
            if p.domingo:
                days['Sun'] = 7

            for day in days.keys():
                fecha = proximo_dia(day, p.days)
                fechaTmp = fecha - timedelta(days= p.days)
                existe = self.pool.get('pedido.cliente').search(cr,uid,[('sale_request_id','=', p.id), ('request_date','=',fechaTmp),('partner_id','=',p.partner_id.id),('type','=','standing_order'),('state','=','draft')], count=True)
                if not existe:
                    pedidos += generar_pedido(fecha, p, cliente_id)
        
        if pedidos:
            cr.execute("select id from pedido_cliente where id in (%s) order by request_date" % ','.join(map(str, pedidos)))
            records = cr.fetchall()
            line = 1
            for r in records:
                self.pool.get('pedido.cliente').write(cr, uid, r[0], {'name': line})
                line += 1  
        
        return {
            'name'       : 'Pedidos de Clientes',
            'view_type'  : 'form',
            'view_mode'  : 'tree,form',
            'res_model'  : 'pedido.cliente',
            'type'       : 'ir.actions.act_window',
            'context'    : context,
        }
    
generate_request_wizard()
