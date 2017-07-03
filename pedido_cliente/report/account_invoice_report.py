# -*- coding: utf-8 -*-

import datetime
from openerp import pooler
from openerp.tools.translate import _
from openerp.report.interface import report_rml
from openerp.tools import ustr


class AccountInvoiceReport(report_rml):
    def create(self, cr, uid, ids, datas, context):
        obj = pooler.get_pool(cr.dbname).get('pedido.cliente')

        for pedido in obj.browse(cr, uid, [datas.get('request_id', False)], context):
            rml = """
                    <document filename="test.pdf">
                        <template pageSize="(595.0,842.0)" title=" """ + _("Account Invoice") + """ " author="" allowSplitting="20">
                            <pageTemplate id="page1">
                                <frame id="first" x1="47.0" y1="50.0" width="500" height="780"/>
                            </pageTemplate>
                        </template>"""

            rml += """  <stylesheet>
                            <blockTableStyle id="MainTable">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>

                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,0" thickness="0.1"/>
                            </blockTableStyle>

                            <blockTableStyle id="LEFT_RIGHT">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>

                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                            </blockTableStyle>

                            <blockTableStyle id="TwoTables">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>

                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>

                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="3,0" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="3,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="3,0" stop="3,-1" thickness="0.1"/>

                                <lineStyle kind="LINEABOVE" colorName="#000000" start="5,0" stop="-1,0" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="5,-1" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="5,0" stop="5,-1" thickness="0.1"/>

                                <blockSpan start="1,0" stop="3,0"/>
                                <blockSpan start="1,1" stop="3,1"/>
                            </blockTableStyle>

                            <blockTableStyle id="CentralTable">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>

                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>

                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>

                                <blockSpan start="5,0" stop="6,0"/>
                            </blockTableStyle>

                            <blockTableStyle id="AllBorders">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>

                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>

                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                            </blockTableStyle>

                            <blockTableStyle id="TableX">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>

                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>

                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>

                                <blockSpan start="0,0" stop="1,0"/>
                                <blockSpan start="0,1" stop="1,1"/>
                                <blockSpan start="0,2" stop="1,2"/>
                                <blockSpan start="2,0" stop="2,-1"/>
                            </blockTableStyle>

                            <blockTableStyle id="TableY">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>

                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,0" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            </blockTableStyle>

                            <blockTableStyle id="TableZ">
                                <ALIGNMENT value="LEFT"/>
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="LEFT"/>

                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="3,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="3,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="3,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="4,-1" thickness="0.1"/>

                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="3,-1" thickness="0.1"/>
                            </blockTableStyle>

                            <initialize>
                                <paraStyle name="all" alignment="justify"/>
                            </initialize>

                            <paraStyle name="P14_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="14.0" alignment="CENTER"/>

                            <paraStyle name="P10_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="10.0" alignment="CENTER"/>
                            <paraStyle name="P10_CENTER" fontName="Helvetica" fontSize="10.0" alignment="CENTER"/>

                            <paraStyle name="P8_BOLD_LEFT" fontName="Helvetica-Bold" fontSize="8.0" alignment="LEFT"/>
                            <paraStyle name="P8_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="8.0" alignment="CENTER"/>

                            <paraStyle name="P6_BOLD_CENTER_TITLE" fontName="Helvetica-Bold" fontSize="4.0" leading="4" alignment="CENTER"/>
                            <paraStyle name="P6_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="5.0" alignment="CENTER"/>
                            <paraStyle name="P6_BOLD_LEFT" fontName="Helvetica-Bold" fontSize="6.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P6_CENTER" fontName="Helvetica" fontSize="6.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P6_LEFT" fontName="Helvetica" fontSize="6.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P6_LEFT_1" fontName="Helvetica" fontSize="4.0" leading="4" alignment="RIGHT"/>

                            <paraStyle name="P5_RIGHT" fontName="Helvetica" fontSize="5.0" leading="5" alignment="RIGHT"/>
                            <paraStyle name="P5_COURIER_CENTER" fontName="Courier" fontSize="5.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P5_COURIER_JUSTIFY" fontName="Courier" fontSize="5.0" leading="5" alignment="JUSTIFY"/>
                        </stylesheet>"""

            rml += """  <story>"""

            rml += """  <spacer length="2.cm"/>"""

            rml += """  <blockTable colWidths="500.0" rowHeights="60.0" style="MainTable">
                            <tr><td><para style="P14_BOLD_CENTER">INVOICE PACKING</para></td></tr>
                        </blockTable>"""

            invoice_obj = pooler.get_pool(cr.dbname).get('confirm.invoice')
            invoices = invoice_obj.search(cr, uid, [('pedido_id', '=', pedido.id)])
            invoice_number = invoice_obj.browse(cr, uid, invoices[0]).invoice_number

            invoice_line_obj = pooler.get_pool(cr.dbname).get('confirm.invoice.line')
            invoices_ids = invoice_line_obj.search(cr, uid, [('invoice_id', 'in', invoices)])

            rml += """  <blockTable colWidths="300.0,30.0,170.0" rowHeights="12.0,12.0,12.0" style="LEFT_RIGHT">
                            <tr>
                                <td></td>
                                <td></td>
                                <td><para style="P10_CENTER">INVOICE</para></td>
                            </tr>
                            <tr>
                                <td></td>
                                <td></td>
                                <td><para style="P10_CENTER">FACTURA No. """ + invoice_number + """</para></td>
                            </tr>
                            <tr>
                                <td><para style="P8_BOLD_LEFT">CONSIGNEE (Consignatario)</para></td>
                                <td></td>
                                <td></td>
                            </tr>
                        </blockTable>"""

            contact = ''
            if pedido.partner_id and len(pedido.partner_id.child_ids):
                contact = pedido.partner_id.child_ids[0].name

            request_date = ''
            if pedido.request_date:
                request_date = pedido.request_date
                str_date = request_date.split('-')
                xdate = datetime.date(int(str_date[0]), int(str_date[1]), int(str_date[2]))
                request_date = xdate.strftime("%B %d, %Y")

            freight_agency = ''
            if pedido.freight_agency_id:
                freight_agency = pedido.freight_agency_id.name

            rml += """ <blockTable colWidths="60.0,100.0,40.0,100.0,30.0,70.0,100.0" rowHeights="10.0,10.0,10.0,12.0" style="TwoTables">
                            <tr>
                                <td><para style="P6_LEFT">NAME:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(pedido.partner_id.name) + """</para></td>
                                <td><para style="P10_CENTER"></para></td>
                                <td><para style="P10_CENTER"></para></td>
                                <td><para style="P10_CENTER"></para></td>
                                <td><para style="P6_LEFT">Flight Date:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + request_date + """</para></td>
                            </tr>
                            <tr>
                                <td><para style="P10_CENTER"></para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(pedido.partner_id.street or '') + """</para></td>
                                <td><para style="P10_CENTER"></para></td>
                                <td><para style="P10_CENTER"></para></td>
                                <td><para style="P10_CENTER"></para></td>
                                <td><para style="P6_LEFT">""" + ustr('Avb#:') + """</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + (str(pedido.airline_id.avb_number) if pedido.airline_id and pedido.airline_id.avb_number else '') + ' ' + (pedido.number if pedido.number else '') + """</para></td>
                            </tr>
                            <tr>
                                <td><para style="P6_LEFT">PHONE:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(pedido.partner_id.phone or '') + """</para></td>
                                <td><para style="P6_LEFT">FAX:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(pedido.partner_id.fax or '') + """</para></td>
                                <td><para style="P6_BOLD_LEFT"></para></td>
                                <td><para style="P6_LEFT">Airline:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + (str(pedido.airline_id.name) if pedido.airline_id and pedido.airline_id.name else '') + """</para></td>
                            </tr>
                            <tr>
                                <td><para style="P6_LEFT">CITY-COUNTRY:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(pedido.partner_id.city or '') + ustr(pedido.partner_id.country_id.name or '') + """</para></td>
                                <td><para style="P6_LEFT">Contact:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(contact) + """</para></td>
                                <td><para style="P6_BOLD_LEFT"></para></td>
                                <td><para style="P6_LEFT">Cargo Agency:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + freight_agency + """</para></td>
                            </tr>
                        </blockTable>"""

            rml += """  <blockTable colWidths="500.0" rowHeights="12.0" style="LEFT_RIGHT">
                            <tr><td><para style="P8_BOLD_LEFT">COUNTRY OF ORIGIN """ + ustr('(País de Origen): ') + """ ECUADOR</para></td></tr>
                        </blockTable>"""

            rml += """<blockTable colWidths="70.0,70.0,55.0,30.0,30.0,20.0,20.0,75.0,70.0,30.0,30.0" rowHeights="20.0" style="CentralTable">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE">FARMS</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">VARIETY</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">LENGTH</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">STEMS</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">BUNCH</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">PIECES / PACKING</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">DESCRIPTION</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">CLIENT</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">UNIT PRICE</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">TOTAL PRICE</para></td>
                            </tr>
                        </blockTable>"""

            rml += """<blockTable colWidths="70.0,70.0,55.0,30.0,30.0,20.0,20.0,75.0,70.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">CM</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">HB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">QB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                            </tr>
                        </blockTable>"""

            first = True
            total_farm_stems = 0
            total_stems = 0

            total_farm_bunch = 0.0
            total_bunch = 0.0

            total_fb, total_hb, total_qb, total_price = 0.0, 0.0, 0.0, 0.0
            last_supplier_name = ''
            summary = {}

            total_tax = 0.0

            for line in invoice_line_obj.browse(cr, uid, invoices_ids):
                stems_cant = line.qty * line.bunch_per_box * int(line.bunch_type) if line.is_box_qty else line.qty
                bunch_cant = float(stems_cant) / int(line.bunch_type)
                cant = float(stems_cant) / (int(line.bunch_type) * line.bunch_per_box)
                #if cant < 1:
                #    cant = 1
                qb_cont, hb_cont = 0.0, 0.0
                if not line.is_box_qty:
                    if line.uom == 'QB':
                        qb_cont = cant
                    elif line.uom == 'HB':
                        hb_cont = cant
                    elif line.uom == 'FB':
                        hb_cont = cant * 2
                    else:
                        hb_cont = cant * 4
                else:
                    if line.uom == 'HB':
                        hb_cont = line.qty
                    elif line.uom == 'QB':
                        qb_cont = line.qty
                    elif line.uom == 'FB':
                        hb_cont = line.qty * 2
                    else:
                        hb_cont = line.qty / 4

                total_farm_bunch += line.qty if line.is_box_qty else float(line.qty) / int(line.bunch_type)
                total_tmp = line.qty * int(line.bunch_type) * line.bunch_per_box * line.sale_price if line.is_box_qty else line.qty * line.sale_price

                total_bunch += bunch_cant
                total_price += total_tmp
                total_farm_stems += stems_cant
                total_stems += stems_cant

                total_hb += hb_cont
                total_qb += qb_cont

                if last_supplier_name != line.supplier_id.name and not summary.get(line.supplier_id.id, False):
                    summary[line.supplier_id.id] = [0.0, 0.0, 0.0]
                    first = True

                summary[line.supplier_id.id][0] += hb_cont
                summary[line.supplier_id.id][1] += qb_cont
                summary[line.supplier_id.id][2] += float(hb_cont)/2 if hb_cont else float(qb_cont)/4

                for tax in line.product_id.taxes_id:
                    if tax.type == 'percent':
                        total_tax += tax.amount * total_tmp
                    elif tax.type == 'fixed':
                        total_tax += tax.amount

                rml += """
                        <blockTable colWidths="70.0,70.0,55.0,30.0,30.0,20.0,20.0,75.0,70.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(line.supplier_id.name[0:18] if first else '')) + """</para></td>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(line.variant_id.name[0:18])) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (ustr(line.length)[0:15]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (str(round(stems_cant,2))) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (str(round(bunch_cant,2))) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(hb_cont,2)) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(qb_cont,2)) + """</para></td>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(line.product_id.name[0:20] if line.product_id else '')) + """</para></td>
								<td><para style="P5_COURIER_JUSTIFY">""" + ustr(pedido.partner_id.name) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (str(round(line.sale_price,2)) if line.sale_price else '') + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(total_tmp,2)) + """</para></td>
                            </tr>
                        </blockTable>"""

                first = False
                last_supplier_name = line.supplier_id.name

            total_fb += float(total_hb)/2 + float(total_qb)/4

            rml += """  <blockTable colWidths="70.0,70.0,55.0,30.0,30.0,20.0,20.0,75.0,70.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE">Total Farm</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_farm_stems,2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_farm_bunch,2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_hb,2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_qb,2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_price,2)) + """</para></td>
                            </tr>
                        </blockTable>"""

            rml += """  <blockTable colWidths="70.0,70.0,55.0,30.0,30.0,20.0,20.0,75.0,70.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE">TOTAL</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_stems,2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_bunch,2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_hb,2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_qb,2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_fb,2)) + """ Full Box</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                            </tr>
                        </blockTable>"""

            res_tipo_neg = pedido.partner_id.tipo_neg_id.name if pedido.partner_id.tipo_neg_id else ''
            tipo_flete = pedido.partner_id.tipo_flete
            flete_value = pedido.precio_flete if tipo_flete == 'fob_f_p' else 0.0

            rml += """  <blockTable colWidths="182.5,182.5,135.0" rowHeights="" style="TableX">
                            <tr>
                                <td>
                                    <blockTable colWidths="225.0,50.0,225.0" rowHeights="8.0,8.0" style="">
                                        <tr>
                                            <td><para style="P5_RIGHT">Gross Weight</para></td>
                                            <td><para style="P5_RIGHT">""" + (datas['gross_weight'] or '') + """</para></td>
                                            <td></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P5_RIGHT">(Peso Bruto)</para></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                                <td>
                                    <blockTable colWidths="70.0,30.0,40.0" rowHeights="" style="">
                                        <tr>
                                            <td><para style="P6_LEFT">""" + ustr('TOTAL INVOICE') + """</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round((total_price + total_tax), 2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">I.V.A</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(total_tax,2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">SUBTOTAL</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(total_price,2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td></td><td></td><td></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">""" + _('Freight') + ' ' + (ustr(pedido.freight_agency_id.name) if pedido.freight_agency_id else '') + """</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(flete_value,2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">TOTAL</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round((total_price + total_tax + flete_value),2)) + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                            </tr>
                            <tr>
                                <td><para style="P6_CENTER">ALL STEMS AND PACKING FROM ECUADOR</para></td>
                                <td></td>
                                <td></td>
                            </tr>
                            <tr>
                                <td><para style="P6_CENTER">""" + ustr(res_tipo_neg).replace('&', '&amp;') + """</para></td>
                                <td></td>
                                <td></td>
                            </tr>
                            <tr>
                                <td><para style="P6_CENTER">Elaborado por: """ + (datas['make_by'] or '') + """</para></td>
                                <td><para style="P6_CENTER">Despachado por: """ + (datas['served_by'] or '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""

            company_obj = pooler.get_pool(cr.dbname).get('res.company')
            companies_ids = company_obj.search(cr, uid, [])
            company = company_obj.browse(cr, uid, companies_ids[0], context)

            rml += """  <blockTable colWidths="500.0" rowHeights="" style="TableY">
                            <tr><td><para style="P10_CENTER">Think in flowers????, think about us "INFLOWERS"</para></td></tr>
                            <tr><td><para style="P6_CENTER">""" + (company.street +', ' if company.street  else '')  + (company.street2 + ', ' if company.street2 else '') + (company.city + ', ' if company.city else '')  + (company.state_id.name + ', ' if company.state_id else '')  + (company.country_id.name if  company.country_id else '') + """</para></td></tr>
                            <tr><td><para style="P6_CENTER">Phone: """ + (company.phone + ',' if company.phone else '')+ """ Mobile: 59399 821-2383</para></td></tr>
                            <tr><td><para style="P6_CENTER">Email/MSN: """ + (company.email if company.email else '') + """ Skype: Inflowers</para></td></tr>
                        </blockTable>"""

            rml += """  <spacer length="0.5cm"/>"""

            rml += """<blockTable colWidths="110.0,30.0,35.0,30.0,300.0" rowHeights="12.0" style="TableZ">
                            <tr>
                                <td><para style="P6_CENTER">FINCA</para></td>
                                <td><para style="P6_CENTER">HALF</para></td>
                                <td><para style="P6_CENTER">QUART</para></td>
                                <td><para style="P6_CENTER">FULL</para></td>
                                <td></td>
                            </tr>"""

            partner_obj = pooler.get_pool(cr.dbname).get('res.partner')
            partner_ids = partner_obj.search(cr, uid, [])
            partners = partner_obj.browse(cr, uid, partner_ids, context)

            for partner in partners:
                if summary.get(partner.id, False):
                    res = summary[partner.id]
                    rml += """<tr>"""
                    rml += """<td><para style="P6_CENTER">""" + ustr(partner.name) + """</para></td>"""
                    for x in res:
                        rml += """<td><para style="P6_CENTER">""" + (str(round(x,2)) if x else '') + """</para></td>"""
                    rml += """<td></td></tr>"""

            rml += """      <tr>
                                        <td><para style="P6_CENTER">TOTAL</para></td>
                                        <td><para style="P6_CENTER">""" + str(round(total_hb,2)) + """</para></td>
                                        <td><para style="P6_CENTER">""" + str(round(total_qb,2)) + """</para></td>
                                        <td><para style="P6_CENTER">""" + str(round(float(total_fb),2)) + """</para></td>
                                        <td></td>
                                    </tr>"""

            rml += """  </blockTable>"""

            rml += """  </story>
                    </document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        return pdf, report_type


AccountInvoiceReport('report.account_invoice_report', 'pedido.cliente', '', '')
