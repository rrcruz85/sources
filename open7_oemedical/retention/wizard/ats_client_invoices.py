# -*- coding: utf-8 -*-
##############################################################################
#
#    Author :  Cristian Salamea cristian.salamea@gnuthink.com
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

import time
import base64
import StringIO
from lxml import etree
from lxml.etree import DocumentInvalid
import os
import datetime
import pdb
import logging
import unicodedata
import re

from osv import osv
from osv import fields

tpIdProv = {
    'ruc' : '01',
    'cedula' : '02',
    'pasaporte' : '03',
}

tpIdCliente = {
    'ruc': '04',
    'cedula': '05',
    'pasaporte': '06'
    }


class ats_client_invoices(osv.osv_memory):

    _name = 'ats.client.invoices'
    _description = 'ATS con facturas de cientes en detalle para revision'
    __logger = logging.getLogger(_name)

    def _get_period(self, cr, uid, context):
        periods = self.pool.get('account.period').find(cr, uid)
        if periods:
            return periods[0]
        else:
            return False

    def _get_company(self, cr, uid, context):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        return user.company_id.id

    def process_lines(self, cr, uid, lines):
        data = {}
        for line in lines:
            if line.tax_group in ('ret_ir', 'no_ret_ir'):
                self.__logger.info('Factura: %s Codigo codRetAir: %s' % (line.invoice_id.number,line.base_code_id.code))
                data['codRetAir'] = line.base_code_id.code
                data['baseImpAir'] = abs(line.base_amount)
                data['porcentajeAir'] = float(line.percent)
                data['valRetAir'] = abs(line.tax_amount)
        return data

    def convertir_fecha(self, fecha):
        """
        fecha: '2012-12-15'
        return: '15/12/2012'
        """
        f = fecha.split('-')
        date = datetime.date(int(f[0]), int(f[1]), int(f[2]))
        return date.strftime('%d/%m/%Y')

    def elimina_tildes(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

    def act_valid_ats(self, cr, uid, ids, context):
        inv_obj = self.pool.get('account.invoice')
        wiz = self.browse(cr, uid, ids)[0]
        period_id = wiz.period_id.id
        ruc = wiz.company_id.partner_id.ced_ruc
        if not ruc:
            raise osv.except_osv('Datos incompletos', 'No ha ingresado RUC para la compañía')
        
        ats = etree.Element('iva')
        etree.SubElement(ats, 'TipoIDInformante').text = 'R'
        etree.SubElement(ats, 'IdInformante').text = str(ruc)
        razon = self.elimina_tildes(wiz.company_id.name)
        social = re.search('(.*?)(([a-zA-Z]\.){2,})(.*)', razon)
        if social:
            replacement=''.join(social.group(2).split('.'))
            razon=social.group(1)+replacement+social.group(4)
        etree.SubElement(ats, 'razonSocial').text = razon
        period = self.pool.get('account.period').browse(cr, uid, [period_id])[0]
        etree.SubElement(ats, 'Anio').text = time.strftime('%Y',time.strptime(period.date_start, '%Y-%m-%d'))
        etree.SubElement(ats, 'Mes'). text = time.strftime('%m',time.strptime(period.date_start, '%Y-%m-%d'))
        
        estabRuc = '001'
        #pos = self.pool.get('pos.config').browse(cr,uid,uid)
        #if pos:
        #    estabRuc = pos.local_id
        #    ptoemi = True
        #    if not (estabRuc and ptoemi):
        #        raise osv.except_osv(_('UserError'), _('No se ha definido el establecimiento'))
        #    elif estabRuc == '000':
        #        raise osv.except_osv(_('UserError'), _('Establecimiento no puede ser 000'))
        #else:
        #    raise osv.except_osv(_('UserError'), _('No se ha definido el establecimiento'))

        etree.SubElement(ats, 'numEstabRuc').text = estabRuc
        ventas_ids = inv_obj.search(cr, uid, [('state','in',['open','paid']),
                                           ('period_id','=',period_id),
                                           ('type','=','out_invoice'),
                                           ('company_id','=',wiz.company_id.id)])
        sub_ventas = 0.0
        for i in inv_obj.browse(cr,uid,ventas_ids):
            #sub_ventas += i.amount_untaxed
            sub_ventas += (i.amount_tax + i.amount_vat)
        
        # total de notas de credito
        sub_ndc = 0.0
        ndc_ids = inv_obj.search(cr, uid, [('state','in',['open','paid']),
                                           ('period_id','=',period_id),
                                           ('type','=','out_refund'),
                                           ('company_id','=',wiz.company_id.id)])
        for i in inv_obj.browse(cr,uid,ndc_ids):
            sub_ndc += (i.amount_tax + i.amount_vat)
        
        if sub_ventas > 0.00:
            sub_ventas = sub_ventas - sub_ndc
        
        total_ventas = '%.2f' %sub_ventas
        etree.SubElement(ats, 'totalVentas').text = total_ventas
        etree.SubElement(ats, 'codigoOperativo').text = 'IVA'
        compras = etree.Element('compras')
        '''Facturas de Compra con retenciones '''
        inv_ids = inv_obj.search(cr, uid, [('state','in',['open','paid']),
                                            ('period_id','=',period_id),
                                            ('type','in',['in_invoice','liq_purchase','in_refund']),
                                            ('company_id','=',wiz.company_id.id)])
        for inv in inv_obj.browse(cr, uid, inv_ids):
            if inv.auth_inv_id:
                #print inv.auth_inv_id.id
                detallecompras = etree.Element('detalleCompras')
                #if inv.sustento_id.code == '00':
                #    raise osv.except_osv(_('UserError'), _('Codigo de sustento no puede ser 00'))
                if inv.type == 'liq_purchase':
                    etree.SubElement(detallecompras, 'codSustento').text = '02'
                else:
                    etree.SubElement(detallecompras, 'codSustento').text = inv.sustento_id.code
                if not inv.partner_id.parent_id:
                    if not inv.partner_id.ced_ruc:
                        raise osv.except_osv('Datos incompletos', 'No ha ingresado Ced/RUC de %s' % inv.partner_id.name)
                    etree.SubElement(detallecompras, 'tpIdProv').text = tpIdProv[inv.partner_id.type_ced_ruc]
                    etree.SubElement(detallecompras, 'idProv').text = inv.partner_id.ced_ruc
                else:
                    etree.SubElement(detallecompras, 'tpIdProv').text = tpIdProv[inv.partner_id.parent_id.type_ced_ruc]
                    etree.SubElement(detallecompras, 'idProv').text = inv.partner_id.parent_id.ced_ruc
                if inv.auth_inv_id:
                    tcomp = inv.auth_inv_id.type_id.code
                else:
                    tcomp = '03'
                etree.SubElement(detallecompras, 'tipoComprobante').text = tcomp
                if inv.partner_id.parte_relacion:
                    etree.SubElement(detallecompras, 'parteRel').text = 'SI'
                else:
                    etree.SubElement(detallecompras, 'parteRel').text = 'NO'
                etree.SubElement(detallecompras, 'fechaRegistro').text = self.convertir_fecha(inv.date_invoice)
                if inv.type in ('in_invoice', 'in_refund'):
                    se = inv.auth_inv_id.serie_entidad
                    pe = inv.auth_inv_id.serie_emision
                    sec = '%09d' % int(inv.reference)
                    auth = inv.auth_inv_id.name
                elif inv.type == 'liq_purchase':
                    se = inv.journal_id.auth_id.serie_entidad
                    pe = inv.journal_id.auth_id.serie_emision
                    sec = inv.number[8:]
                    auth = inv.journal_id.auth_id.name
                etree.SubElement(detallecompras, 'establecimiento').text = se
                etree.SubElement(detallecompras, 'puntoEmision').text = pe
                etree.SubElement(detallecompras, 'secuencial').text = sec
                etree.SubElement(detallecompras, 'fechaEmision').text = self.convertir_fecha(inv.date_invoice)
                #aumentar en la autorizacion si es o no electronica.
                #Para VENTA (cliente) va la autorizacion del SRI o electronica
                #validar 10 para dada por el SRI o 37 si es electronica 
                etree.SubElement(detallecompras, 'autorizacion').text = auth
                etree.SubElement(detallecompras, 'baseNoGraIva').text = inv.amount_novat==0 and '0.00' or '%.2f' %inv.amount_novat
                etree.SubElement(detallecompras, 'baseImponible').text = '%.2f' %inv.amount_vat_cero
                #imp_vat = inv.amount_vat_cero + inv.amount_vat
                etree.SubElement(detallecompras, 'baseImpGrav').text = '%.2f' %inv.amount_vat
                #etree.SubElement(detallecompras, 'baseImpGrav').text = '%.2f' %imp_vat
                etree.SubElement(detallecompras, 'baseImpExe').text = '0.00'
                etree.SubElement(detallecompras, 'montoIce').text = '%.2f' %inv.amount_ice
                etree.SubElement(detallecompras, 'montoIva').text = '%.2f' %inv.amount_tax
                etree.SubElement(detallecompras, 'valRetBien10').text ='0.00'
                etree.SubElement(detallecompras, 'valRetServ20').text ='0.00'
                etree.SubElement(detallecompras, 'valorRetBienes').text = '%.2f' % abs(inv.taxed_ret_vatb)
                etree.SubElement(detallecompras, 'valorRetServicios').text = aux_ret_srv = inv.amount_tax==inv.taxed_ret_vatsrv and '%.2f' %abs(inv.taxed_ret_vatsrv) or '0.00' #'%.2f' % abs(inv.taxed_ret_vatsrv)
                etree.SubElement(detallecompras, 'valRetServ100').text = aux_ret_100 = inv.amount_tax==abs(inv.taxed_ret_vatsrv) and '%.2f' %abs(inv.taxed_ret_vatsrv) or '0.00'
                etree.SubElement(detallecompras, 'totbasesImpReemb').text = '0.00'
                pago_exterior = etree.Element('pagoExterior')
                etree.SubElement(pago_exterior, 'pagoLocExt').text = '01'
                etree.SubElement(pago_exterior, 'paisEfecPago').text = 'NA'
                etree.SubElement(pago_exterior, 'aplicConvDobTrib').text = 'NA'
                etree.SubElement(pago_exterior, 'pagExtSujRetNorLeg').text = 'NA'
                detallecompras.append(pago_exterior)
                if (inv.amount_novat + inv.amount_tax + inv.amount_vat_cero + inv.amount_vat) > 1000 and inv.type != 'in_refund':
                #if inv.amount_pay > 1000:
                    if inv.payment_ids:
                        #raise osv.except_osv('Datos incompletos', 'Las facturas con montos de bases imponibles e impuestos superiores a 1000 requieren la forma de pago')
                    #else:
                        #agregar campo CODIGO ATS en diario (efectivo, banco-cheques)
                        #validar que el diario sea efectivo, banco-cheques
                        #que el numero no sea 00
                        #valores catalogo tabla 16
                        #etree.SubElement(forma_pago, 'formaPago').text = formaPago[i.journal_id.name]
                        forma_pago = etree.Element('formasDePago')
                        for i in inv.payment_ids:
                            if not i.journal_id.payment_method:
                                raise osv.except_osv('Datos incompletos', 'No ha definido forma de pago del diario %s' % i.journal_id.name)
                            
                            etree.SubElement(forma_pago, 'formaPago').text = i.journal_id.payment_method
                        detallecompras.append(forma_pago)
                    else:
                        forma_pago = etree.Element('formasDePago')
                        etree.SubElement(forma_pago, 'formaPago').text = '02'
                        detallecompras.append(forma_pago)
                        
                air = etree.Element('air')
                if inv.retention_ir:
                    data_air = self.process_lines(cr, uid, inv.tax_line)
                    detalleAir = etree.Element('detalleAir')
                    etree.SubElement(detalleAir, 'codRetAir').text = data_air['codRetAir']
                    etree.SubElement(detalleAir, 'baseImpAir').text = '%.2f' % data_air['baseImpAir']
                    etree.SubElement(detalleAir, 'porcentajeAir').text = '%.2f' % data_air['porcentajeAir']
                    etree.SubElement(detalleAir, 'valRetAir').text = '%.2f' % data_air['valRetAir']
                    air.append(detalleAir)
                detallecompras.append(air)
                flag = False
                if inv.retention_ir or inv.retention_vat:
                    flag = True
                if inv.retention_id:
                    etree.SubElement(detallecompras, 'estabRetencion1').text = flag and inv.journal_id.auth_ret_id.serie_entidad or '000'
                    etree.SubElement(detallecompras, 'ptoEmiRetencion1').text = flag and inv.journal_id.auth_ret_id.serie_emision or '000'
                    etree.SubElement(detallecompras, 'secRetencion1').text = flag and inv.retention_id.number[6:] or '%09d'%0
                    etree.SubElement(detallecompras, 'autRetencion1').text = flag and inv.journal_id.auth_ret_id.name or '%010d'%0
                    etree.SubElement(detallecompras, 'fechaEmiRet1').text = flag and self.convertir_fecha(inv.retention_id.date) or '00/00/0000'
                    
                if inv.type == 'in_refund':
                    etree.SubElement(detallecompras, 'docModificado').text = '01'
                    etree.SubElement(detallecompras, 'estabModificado').text = inv.supplier_invoice_number[:3]
                    etree.SubElement(detallecompras, 'ptoEmiModificado').text = inv.supplier_invoice_number[4:7]
                    etree.SubElement(detallecompras, 'secModificado').text = inv.supplier_invoice_number[8:]
                    ndd_ids = inv_obj.search(cr, uid, [('state','in',['open','paid']),
                                            #('period_id','=',period_id),
                                            ('type','in',['in_invoice']),
                                            ('supplier_invoice_number', '=', inv.supplier_invoice_number),
                                            ('company_id','=', wiz.company_id.id)])
                    if ndd_ids:
                        for ndd in inv_obj.browse(cr, uid, ndd_ids):
                            etree.SubElement(detallecompras, 'autModificado').text = ndd.auth_inv_id.name
                    
                compras.append(detallecompras)

        ats.append(compras)
        """VENTAS DECLARADAS"""
        ventas = etree.Element('ventas')
        inv_ids = inv_obj.search(cr, uid, [('state','in',['open','paid']),
                                           ('period_id','=',period_id),
                                           ('type','in',['out_invoice','out_refund']),
                                           ('company_id','=',wiz.company_id.id)])
        pdata = {}
        base_imponible = 0.0
        for inv in inv_obj.browse(cr, uid, inv_ids):
            if not pdata or not pdata.get(inv.partner_id.id, False):
                if inv.partner_id.parte_relacion:
                    parte_rel = 'SI'
                else:
                    parte_rel = 'NO'
                if not inv.partner_id.parent_id:
                    tpIdCliente = inv.partner_id.type_ced_ruc
                    idCliente = inv.partner_id.ced_ruc
                    cliente = inv.partner_id.name
                else:
                    tpIdCliente = inv.partner_id.parent_id.type_ced_ruc
                    idCliente = inv.partner_id.parent_id.ced_ruc
                    cliente = inv.partner_id.parent_id.name
            if inv.type == 'out_refund':
                tipoComprobante = '04'
            else:
                tipoComprobante = '18'
            basenoGraIva = inv.amount_novat==0 and '0.00' or '%.2f' %inv.amount_novat
            baseImponible = inv.amount_vat_cero
            baseImpGrav = inv.amount_vat
            montoIva = inv.amount_tax
            if inv.retention_ir:
                data_air = self.process_lines(cr, uid, inv.tax_line)
                valorRetRenta = data_air['valRetAir']
            else:
                valorRetRenta = 0.00
            valorRetIva = abs(inv.taxed_ret_vatb) + abs(inv.taxed_ret_vatsrv)
            reference = inv.reference
            
            detalleVentas = etree.Element('detalleVentas')
            etree.SubElement(detalleVentas, 'tpIdCliente').text = tpIdCliente
            etree.SubElement(detalleVentas, 'idCliente').text = idCliente
            etree.SubElement(detalleVentas, 'NombreCliente').text = cliente
            etree.SubElement(detalleVentas, 'fechaFactura').text = self.convertir_fecha(inv.date_invoice)
            etree.SubElement(detalleVentas, 'parteRelVtas').text = parte_rel
            etree.SubElement(detalleVentas, 'tipoComprobante').text = tipoComprobante
            etree.SubElement(detalleVentas, 'Secuencial').text = inv.number[8:]
            etree.SubElement(detalleVentas, 'baseNoGraIva').text = basenoGraIva
            etree.SubElement(detalleVentas, 'baseImponible').text = '%.2f' % baseImponible
            etree.SubElement(detalleVentas, 'baseImpGrav').text = '%.2f' % baseImpGrav
            etree.SubElement(detalleVentas, 'montoIva').text = '%.2f' % montoIva
            if 'NO OBLIGAD' not in inv.partner_id.property_account_position.name:
                etree.SubElement(detalleVentas, 'valorRetIva').text = '%.2f' % (montoIva * 30.0/100)
                etree.SubElement(detalleVentas, 'valorRetRenta').text = '%.2f' % ((float(basenoGraIva) + baseImponible + baseImpGrav) * 1.0/100)
                etree.SubElement(detalleVentas, 'totalFacturaConRet').text = '%.2f' % (inv.amount_total - (montoIva * 30.0/100) - ((float(basenoGraIva) + baseImponible + baseImpGrav) * 1.0/100))
            else:
                etree.SubElement(detalleVentas, 'valorRetIva').text = '%.2f' % 0.00
                etree.SubElement(detalleVentas, 'valorRetRenta').text = '%.2f' % 0.00
                etree.SubElement(detalleVentas, 'totalFacturaConRet').text = '%.2f' % inv.amount_total
            etree.SubElement(detalleVentas, 'totalFactura').text = '%.2f' % inv.amount_total
            ventas.append(detalleVentas)
                    
        ats.append(ventas)
        ventas_establecimiento = etree.Element('ventasEstablecimiento')
        ventas_est = etree.Element('ventaEst')
        #Cambiar al campo de la configuracion de la CO.
        etree.SubElement(ventas_est, 'codEstab').text = estabRuc
        etree.SubElement(ventas_est, 'ventasEstab').text = total_ventas
        ventas_establecimiento.append(ventas_est)
        ats.append(ventas_establecimiento)
        """Documentos Anulados"""
        anulados = etree.Element('anulados')
        inv_ids = inv_obj.search(cr, uid, [('state','=','cancel'),
                                            ('period_id','=',period_id),
                                            ('type','=','out_invoice'),
                                            ('company_id','=',wiz.company_id.id)])
        for inv in inv_obj.browse(cr, uid, inv_ids):
            detalleAnulados = etree.Element('detalleAnulados')
            etree.SubElement(detalleAnulados, 'tipoComprobante').text = inv.journal_id.auth_id.type_id.code
            etree.SubElement(detalleAnulados, 'establecimiento').text = inv.journal_id.auth_id.serie_entidad
            etree.SubElement(detalleAnulados, 'puntoEmision').text = inv.journal_id.auth_id.serie_emision
            if inv.number:
                etree.SubElement(detalleAnulados, 'secuencialInicio').text = str(int(inv.number[8:]))
                etree.SubElement(detalleAnulados, 'secuencialFin').text = str(int(inv.number[8:]))
            else:
                etree.SubElement(detalleAnulados, 'secuencialInicio').text = ''
                etree.SubElement(detalleAnulados, 'secuencialFin').text = ''
            etree.SubElement(detalleAnulados, 'autorizacion').text = inv.journal_id.auth_id.name
            anulados.append(detalleAnulados)
        liq_ids = inv_obj.search(cr, uid, [('state','=','cancel'),
                                            ('period_id','=',period_id),
                                            ('type','=','liq_purchase'),
                                            ('company_id','=',wiz.company_id.id)])
        for inv in inv_obj.browse(cr, uid, liq_ids):
            detalleAnulados = etree.Element('detalleAnulados')
            etree.SubElement(detalleAnulados, 'tipoComprobante').text = inv.journal_id.auth_id.type_id.code
            etree.SubElement(detalleAnulados, 'establecimiento').text = inv.journal_id.auth_id.serie_entidad
            etree.SubElement(detalleAnulados, 'puntoEmision').text = inv.journal_id.auth_id.serie_emision
            etree.SubElement(detalleAnulados, 'secuencialInicio').text = str(int(inv.number[8:]))
            etree.SubElement(detalleAnulados, 'secuencialFin').text = str(int(inv.number[8:]))
            etree.SubElement(detalleAnulados, 'autorizacion').text = inv.journal_id.auth_id.name
            anulados.append(detalleAnulados)
        retention_obj = self.pool.get('account.retention')
        ret_ids = retention_obj.search(cr, uid, [('state','=','cancel'),
                                                 ('in_type','=','ret_out_invoice'),
                                                 ('date','>=',wiz.period_id.date_start),
                                                 ('date','<=',wiz.period_id.date_stop)])
        for ret in retention_obj.browse(cr, uid, ret_ids):
            detalleAnulados = etree.Element('detalleAnulados')
            etree.SubElement(detalleAnulados, 'tipoComprobante').text = ret.auth_id.type_id.code
            etree.SubElement(detalleAnulados, 'establecimiento').text = ret.auth_id.serie_entidad
            etree.SubElement(detalleAnulados, 'puntoEmision').text = ret.auth_id.serie_emision
            etree.SubElement(detalleAnulados, 'secuencialInicio').text = str(int(ret.number[8:]))
            etree.SubElement(detalleAnulados, 'secuencialFin').text = str(int(ret.number[8:]))
            etree.SubElement(detalleAnulados, 'autorizacion').text = ret.auth_id.name
            anulados.append(detalleAnulados)
        ats.append(anulados)
        #file_path = os.path.join(os.path.dirname(__file__), 'XSD/at.xsd')
        #schema_file = open(file_path)
        file_ats = etree.tostring(ats, pretty_print=True, encoding='iso-8859-1')
        #validata schema
        #xmlschema_doc = etree.parse(schema_file)
        #xmlschema = etree.XMLSchema(xmlschema_doc)
        #if not wiz.no_validate:
        #    try:
        #        xmlschema.assertValid(ats)
        #    except DocumentInvalid as e:
        #        raise osv.except_osv('Error de Datos', """El sistema generó el XML pero los datos no pasan la validación XSD del SRI.
        #        \nLos errores mas comunes son:\n* RUC,Cédula o Pasaporte contiene caracteres no válidos.\n* Números de documentos están duplicados.\n\nEl siguiente error contiene el identificador o número de documento en conflicto:\n\n %s""" % str(e))
        buf = StringIO.StringIO()
        buf.write(file_ats)
        out=base64.encodestring(buf.getvalue())
        buf.close()
        name = "%s%s%s.xml" % ("VAL", time.strftime('%m',time.strptime(period.date_start, '%Y-%m-%d')), time.strftime('%Y',time.strptime(period.date_start, '%Y-%m-%d')))
        self.write(cr, uid, ids, {'state': 'export', 'data': out, 'name': name})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ats.client.invoices',
            'target':'new',
            'res_id': ids[0],
            'type': 'ir.actions.act_window',
            'context':"{ 'active_model': 'ats.client.invoices', 'active_id': %s }" % (ids[0])
        }
        
    _columns = {
        'name' : fields.char('Nombre de Archivo', size=50, readonly=True),
        'period_id' : fields.many2one('account.period', 'Periodo'),
        'company_id': fields.many2one('res.company', 'Compania'),
        'data' : fields.binary('Archivo XML'),
        #'no_validate': fields.boolean('No Validar'),
        'state' : fields.selection((('choose', 'choose'),
                                    ('export', 'export'))),
        }

    _defaults = {
        'state' : 'choose',
        'period_id': _get_period,
        'company_id': _get_company
    }    

ats_client_invoices()
