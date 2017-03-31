# -*- coding: utf-8 -*-

import datetime

from openerp import pooler
from openerp.tools.translate import _
from openerp.report.interface import report_rml
from openerp.tools import ustr


class AccountInvoiceVarietyReport(report_rml):
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

                            <blockTableStyle id="TableHeader">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>

                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>

                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>

                                <blockSpan start="0,0" stop="0,1"/>
                                <blockSpan start="2,0" stop="3,0"/>
                                <blockSpan start="4,0" stop="4,1"/>
                                <blockSpan start="5,0" stop="5,1"/>
                                <blockSpan start="6,0" stop="6,1"/>
                                <blockSpan start="7,0" stop="7,1"/>
                                <blockSpan start="8,0" stop="8,1"/>
                                <blockSpan start="9,0" stop="9,1"/>
                                <blockSpan start="10,0" stop="10,1"/>
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
                            <paraStyle name="P5_COURIER_BOLD_CENTER" fontName="Courier-Bold" fontSize="5.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P5_COURIER_BOLD_JUSTIFY" fontName="Courier-Bold" fontSize="5.0" leading="5" alignment="JUSTIFY"/>
                        </stylesheet>"""

            rml += """  <story>"""

            rml += """  <spacer length="2.cm"/>"""

            rml += """  <blockTable colWidths="500.0" rowHeights="60.0" style="MainTable">
                            <tr><td><para style="P14_BOLD_CENTER">INVOICE PACKING</para></td></tr>
                        </blockTable>"""

            rml += """  <blockTable colWidths="300.0,30.0,170.0" rowHeights="12.0,12.0,12.0" style="LEFT_RIGHT">
                            <tr>
                                <td></td>
                                <td></td>
                                <td><para style="P10_CENTER">INVOICE</para></td>
                            </tr>
                            <tr>
                                <td></td>
                                <td></td>
                                <td><para style="P10_CENTER">FACTURA No. """ + (pedido.account_invoice_ids[0].supplier_invoice_number if len(pedido.account_invoice_ids) and pedido.account_invoice_ids[0].supplier_invoice_number else '') + """</para></td>
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

            rml += """  <blockTable colWidths="60.0,100.0,40.0,100.0,30.0,70.0,100.0" rowHeights="10.0,10.0,10.0,12.0" style="TwoTables">
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

            rml += """  <blockTable colWidths="85.0,55.0,20.0,20.0,40.0,30.0,30.0,85.0,75.0,30.0,30.0" rowHeights="12.0,12.0" style="TableHeader">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE">VARIETY</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">LENGTH</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">UNITS X HB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">STEMS TOTAL</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">BUNCH TOTAL</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">DESCRIPTION</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">CLIENT REMARKS</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">UNIT PRICE</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">TOTAL PRICE</para></td>
                            </tr>
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">CM</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">HB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">QB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">HB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                            </tr>
                        </blockTable>"""

            total_farm_stems = 0
            total_stems = 0

            total_farm_bunch = 0
            total_bunch = 0

            total_fb, total_hb, total_qb, total_price = 0.0, 0, 0, 0.0
            summary = {}
            total_tax = 0.0
            last_supplier_name = ''

            subtotal_hb, subtotal_qb = 0, 0
            subtotal_stems, subtotal_bunchcant = 0, 0
            subtotal_amount = 0.0

            invoice_obj = pooler.get_pool(cr.dbname).get('confirm.invoice')
            invoices = invoice_obj.search(cr, uid, [('pedido_id', '=', pedido.id)])
            invoice_line_obj = pooler.get_pool(cr.dbname).get('confirm.invoice.line')
            invoices_ids = invoice_line_obj.search(cr, uid, [('invoice_id', 'in', invoices)])

            data_to_print = []
            uom = {'FB':1,'HB':2,'QB':4,'OB':8}
            for line in invoice_line_obj.browse(cr, uid, invoices_ids):
                stems_cant = line.qty * line.bunch_per_box * int(line.bunch_type) if line.is_box_qty else line.qty
                bunch_cant = int(stems_cant) / int(line.bunch_type)
                cant = int(stems_cant) / (int(line.bunch_type) * line.bunch_per_box)
                if cant < 1:
                    cant = 1
                qb_cont, hb_cont = 0, 0

                bxs_qty = line.qty if line.is_box_qty else (1 if not (line.qty / (int(line.bunch_type) * line.bunch_per_box)) else (line.qty / (int(line.bunch_type) * line.bunch_per_box)))
                full_boxes = float(bxs_qty)/uom[line.uom]

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

                total_farm_bunch += line.qty if line.is_box_qty else line.qty / int(line.bunch_type)
                total_tmp = line.qty * int(line.bunch_type) * line.bunch_per_box * line.purchase_price if line.is_box_qty else line.qty * line.purchase_price

                total_bunch += bunch_cant
                total_price += total_tmp
                total_farm_stems += stems_cant
                total_stems += stems_cant

                total_hb += hb_cont
                total_qb += qb_cont

                units_x_hb = stems_cant / hb_cont if hb_cont != 0 else 0

                for tax in line.product_id.taxes_id:
                    if tax.type == 'percent':
                        total_tax += tax.amount * total_tmp
                    elif tax.type == 'fixed':
                        total_tax += tax.amount

                if not len(data_to_print):
                    data_to_print.append([
                        line.supplier_id,
                        line.variant_id,
                        line.length,
                        hb_cont,
                        units_x_hb,
                        stems_cant,
                        bunch_cant,
                        pedido.partner_id,
                        line.purchase_price,
                        total_tmp,
                        full_boxes,
                        qb_cont,
                    ])
                else:
                    exist = False
                    for _data in data_to_print:
                        y = _data[1].id == line.variant_id.id
                        z = _data[2] == line.length

                        if y and z:
                            _data[3] += hb_cont
                            _data[4] += units_x_hb
                            _data[5] += stems_cant
                            _data[6] += bunch_cant
                            _data[9] += total_tmp
                            _data[10] += full_boxes
                            _data[11] += qb_cont
                            exist = True
                            break

                    if not exist:
                        data_to_print.append([
                            line.supplier_id,
                            line.variant_id,
                            line.length,
                            hb_cont,
                            units_x_hb,
                            stems_cant,
                            bunch_cant,
                            pedido.partner_id,
                            line.purchase_price,
                            total_tmp,
                            full_boxes,
                            qb_cont
                        ])

            last_variant = ''
            subtotal_hb, subtotal_qb, subtotal_bunchcant, subtotal_amount = 0, 0, 0, 0.0

            for data in data_to_print:
                if last_variant == '':
                    last_variant = data[1].name
                elif last_variant != '' and last_variant != data[1].name:
                    last_variant = data[1].name
                    rml += """
                        <blockTable colWidths="85.0,55.0,20.0,20.0,40.0,30.0,30.0,85.0,75.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P5_COURIER_BOLD_JUSTIFY">""" + ustr('Total farm') + """</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_hb) + """</para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_qb) + """</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_stems) + """</para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_bunchcant) + """</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_amount) + """</para></td>
                            </tr>
                        </blockTable>"""

                    subtotal_hb = 0
                    subtotal_qb = 0
                    subtotal_stems = 0
                    subtotal_bunchcant = 0
                    subtotal_amount = 0.0

                subtotal_hb += data[3]
                subtotal_qb += data[11]
                subtotal_stems += int(data[5])
                subtotal_bunchcant += int(data[6])
                subtotal_amount += float(data[9]) if isinstance(data[9], float) else 0.0

                rml += """
                        <blockTable colWidths="85.0,55.0,20.0,20.0,40.0,30.0,30.0,85.0,75.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(data[1].name)[0:25]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (ustr(data[2])[0:15]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(data[3]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(data[11]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(data[4]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(data[5]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(data[6]) + """</para></td>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(data[1].product_id.name)[0:20] if data[1].product_id else '') + """</para></td>
                                <td><para style="P5_COURIER_JUSTIFY">""" + ustr(data[7].name) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(data[8]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(data[9]) + """</para></td>
                            </tr>
                        </blockTable>"""

            rml += """
                        <blockTable colWidths="85.0,55.0,20.0,20.0,40.0,30.0,30.0,85.0,75.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P5_COURIER_BOLD_JUSTIFY">""" + _('Total farm') + """</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_hb) + """</para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_qb) + """</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_stems) + """</para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_bunchcant) + """</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(subtotal_amount) + """</para></td>
                            </tr>
                        </blockTable>"""

            total_fb += float(total_hb)/2 + float(total_qb)/4

            rml += """  <blockTable colWidths="85.0,55.0,20.0,20.0,40.0,30.0,30.0,85.0,75.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE">TOTAL</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(total_hb) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(total_qb) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(total_farm_stems) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(total_farm_bunch) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(total_fb) + """ Full Box</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(total_price) + """</para></td>
                            </tr>
                        </blockTable>"""

            res_tipo_neg = pedido.partner_id.tipo_neg_id.name if pedido.partner_id.tipo_neg_id else ''
            tipo_flete = pedido.partner_id.tipo_flete if pedido.partner_id.tipo_flete else ''
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
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(total_price + total_tax) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">I.V.A</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(total_tax) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">SUBTOTAL</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(total_price) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td></td><td></td><td></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">""" + _('Freight') + ' ' + (ustr(pedido.freight_agency_id.name) if pedido.freight_agency_id else '') + """</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(flete_value) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">TOTAL</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(total_price + total_tax + flete_value) + """</para></td>
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

            rml += """  <blockTable colWidths="110.0,30.0,35.0,30.0,300.0" rowHeights="12.0" style="TableZ">
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

            summary = {}
            last_supplier_name = ''

            for line in pedido.line_ids:
                qb_cont, hb_cont = 0, 0
                if not line.detalle_id.is_box_qty:
                    stems = int(str(line.total_qty_purchased).split(' ')[0])
                    cant = stems / (int(line.bunch_type) * line.bunch_per_box)
                    if cant < 1:
                        cant = 1
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
                        hb_cont = line.detalle_id.qty
                    elif line.uom == 'QB':
                        qb_cont = line.detalle_id.qty
                    else:
                        hb_cont = int(str(line.stimated_qty).split(' ')[0]) * 2

                if last_supplier_name != line.supplier_id.name and not summary.get(line.supplier_id.id, False):
                    summary[line.supplier_id.id] = [0, 0, 0.0]

                summary[line.supplier_id.id][0] += hb_cont
                summary[line.supplier_id.id][1] += qb_cont
                summary[line.supplier_id.id][2] += float(hb_cont)/2 if hb_cont else float(qb_cont)/4

            for partner in partners:
                if summary.get(partner.id, False):
                    res = summary[partner.id]
                    rml += """<tr>"""
                    rml += """<td><para style="P6_CENTER">""" + ustr(partner.name) + """</para></td>"""
                    for x in res:
                        rml += """<td><para style="P6_CENTER">""" + (str(x) if x else '') + """</para></td>"""
                    rml += """<td></td></tr>"""

            rml += """      <tr>
                                <td><para style="P6_CENTER">TOTAL</para></td>
                                <td><para style="P6_CENTER">""" + str(total_hb) + """</para></td>
                                <td><para style="P6_CENTER">""" + str(total_qb) + """</para></td>
                                <td><para style="P6_CENTER">""" + str(float(total_fb)) + """</para></td>
                                <td></td>
                            </tr>"""

            rml += """  </blockTable>"""

            rml += """  </story>
                    </document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        return pdf, report_type

AccountInvoiceVarietyReport('report.account_invoice_variety_report', 'pedido.cliente', '', '')
