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
            list_details = []
            dia_semana = int(fecha_pedido.strftime('%w'))
            filtro = {1:('lunes','=',True),2:('martes','=',True),3:('miercoles','=',True),4:('jueves','=',True),5:('viernes','=',True),6:('sabado','=',True),7:('domingo','=',True)}
            dia =  dia_semana - p.days
            if dia <= 0:
                dia = 7 + dia

            uom = {'FB':1,'HB':2,'QB':4,'OB':8}
            request_lines = []
            tmp_dict = {}
            line = 1
            for v in p.variant_ids:
                lengths =  [(0,0,{'length': l.length,'sale_price':l.sale_price}) for l in v.length_ids]
                sale_lengths =  [l.length.upper() for l in v.length_ids]
                sale_prices =  [l.sale_price for l in v.length_ids]
                key = str(v.product_id.id) + ',' + str(v.variant_id.id) + ',' + '-'.join(sale_lengths)
                tmp_dict[key] = []
                request = {
                    'line': line,
                    'product_id': v.product_id.id,
                    'variant_id': v.variant_id.id,
                    'is_box_qty': v.is_box_qty,
                    'length_ids' : lengths,
                    'box_qty': v.box_qty if v.is_box_qty else 0,
                    'tale_qty': v.tale_qty if not v.is_box_qty else 0,
                    'bunch_type': v.bunch_type if v.bunch_type else 25,
                    'bunch_per_box': v.bunch_per_box,
                    'uom': v.uom,
                    'type':'standing_order',
                    'is_standing_order':True,
                }
                line += 1
                request_lines.append((0,0,request))
                request_qty = v.tale_qty if not v.is_box_qty else v.box_qty * int(v.bunch_type) * v.bunch_per_box

                puchase_ids = self.pool.get('purchase.request.template').search(cr,uid,[('client_id','=',p.partner_id.id),filtro[dia]])
                v_ids = self.pool.get('purchase.request.product.variant').search(cr,uid,[('template_id', 'in', puchase_ids),('variant_id','=', v.variant_id.id)])
                for s in self.pool.get('purchase.request.product.variant').browse(cr, uid, v_ids):
                    purchase_lengths = [ss.length.upper() for ss in s.length_ids]
                    if set(sale_lengths) & set(purchase_lengths) and request_qty > 0:
                        stems_qty = s.tale_qty if not s.is_box_qty else s.box_qty * int(s.bunch_type) * s.bunch_per_box
                        qty = 0
                        if request_qty > stems_qty:
                            qty = stems_qty
                        else:
                            qty = request_qty

                        request_qty -= qty

                        if s.is_box_qty and s.bunch_type:
                            qty = qty/(int(s.bunch_type) * s.bunch_per_box)

                        lengths =  [(0,0,{'length': l.length,'purchase_price':l.purchase_price}) for l in s .length_ids]

                        subclient_id = False
                        if s.subclient_id and v.subclient_id and s.subclient_id.id == v.subclient_id.id:
                            subclient_id =  v.subclient_id.id
                            detalle_dict = {
                                'supplier_id': s.template_id.partner_id.id,
                                'type': 'standing_order',
                                'product_id': v.product_id.id,
                                'variant_id': v.variant_id.id,
                                'length_ids': lengths,
                                'qty': qty,
                                'is_box_qty': s.is_box_qty,
                                'bunch_type': s.bunch_type if s.bunch_type else 25,
                                'bunch_per_box': s.bunch_per_box,
                                'uom': s.uom,
                                'sale_price': sum(sale_prices) / len(sale_prices) if sale_prices else 0,
                                'subclient_id': subclient_id,
                                'sucursal_id': s.template_id.sucursal_id.id if s.template_id.sucursal_id else None,
                            }
                            list_details.append((0, 0, detalle_dict))
                            l_key = str(s.template_id.partner_id.id) + ',' + str(v.product_id.id) + ',' + str(v.variant_id.id) + ',' + '-'.join(purchase_lengths)
                            tmp_dict[key].append(l_key)

            cr.execute('select max(p.name) from pedido_cliente p where p.partner_id = %s', (p.partner_id.id,))
            result = cr.fetchone()
            name = result[0] + 1 if result[0] else 1
            fecha_pedido = fecha_pedido - timedelta(days=p.days)

            if fecha_pedido >= datetime.datetime.now().date():

                tipo_flete = self.pool.get('res.partner').browse(cr, uid, cliente_id).tipo_flete
                precio_flete = 0
                if tipo_flete and tipo_flete == 'fob_f_p':
                    precio_flete = 0.01

                pedido_dict = {
                    'name': name,
                    'partner_id': cliente_id if cliente_id else p.partner_id.id,
                    'request_date': fecha_pedido,
                    'state': 'draft',
                    'type': 'standing_order',
                    'freight_agency_id': p.freight_agency_id.id if p.freight_agency_id else None,
                    'variant_ids': request_lines,
                    'purchase_line_ids': list_details,
                    'precio_flete': precio_flete,
                    'sale_request_id': p.id,
                }
                pedido_id = self.pool.get('pedido.cliente').create(cr, uid, pedido_dict)

                # Actulizando las lineas de compras
                for key in tmp_dict.keys():
                    request = key.split(',')
                    request_ids = self.pool.get('request.product.variant').search(cr, uid, [('pedido_id', '=', pedido_id), ('product_id', '=', int(request[0])), ('variant_id', '=', int(request[1])),('lengths', '=', request[2])])
                    if request_ids:
                        for line in tmp_dict[key]:
                            line_vals = line.split(',')
                            purchased_ids = self.pool.get('detalle.lines').search(cr, uid, [('pedido_id', '=', pedido_id), ('supplier_id', '=', int(line_vals[0])), ('product_id', '=', int(line_vals[1])), ('variant_id', '=',int(line_vals[2])), ('lengths', '=',line_vals[3])])
                            if purchased_ids:
                                self.pool.get('detalle.lines').write(cr, uid, purchased_ids, {'line_id': request_ids[0]})

            return 0

        hoy = int(datetime.datetime.now().strftime('%w'))
        if hoy == 0:
            hoy = 7

        obj = self.browse(cr,uid,ids[0])
        cliente_id = obj.client_id.id if obj.client_id else False
        sale_template_ids = []
        if obj.client_id:
            sale_template_ids = self.pool.get('sale.request').search(cr,uid,[('partner_id','=',obj.client_id.id)])
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
                #if days[day] >= hoy:
                #if days[day] <> hoy:
                fecha = proximo_dia(day, p.days)
                fechaTmp = fecha - timedelta(days= p.days)
                existe = self.pool.get('pedido.cliente').search(cr,uid,[('sale_request_id','=', p.id), ('request_date','=',fechaTmp),('partner_id','=',p.partner_id.id),('type','=','standing_order'),('state','=','draft')], count=True)
                if not existe:
                    generar_pedido(fecha, p, cliente_id)
        return {
            'name': 'Pedidos de Clientes',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'pedido.cliente',
            'type': 'ir.actions.act_window',
            'context': context,
        }
    
generate_request_wizard()
