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

                                <blockSpan start="0,0" stop="0,0"/>
                                <blockSpan start="2,0" stop="3,0"/>
                                <blockSpan start="4,0" stop="4,0"/>
                                <blockSpan start="5,0" stop="5,0"/>
                                <blockSpan start="6,0" stop="6,0"/>
                                <blockSpan start="7,0" stop="7,0"/>
                                <blockSpan start="8,0" stop="8,0"/>
                                <blockSpan start="9,0" stop="9,0"/>
                                <blockSpan start="10,0" stop="10,0"/>
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
                            <paraStyle name="P6_BOLD_JUSTIFY_TITLE" fontName="Helvetica-Bold" fontSize="4.0" leading="4" alignment="JUSTIFY"/>

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
            if pedido.partner_id and len(pedido.partner_id.child_ids) and pedido.partner_id.child_ids[0].name:
                contact = pedido.partner_id.child_ids[0].name

            request_date = ''
            if pedido.request_date:
                request_date = pedido.request_date
                str_date = request_date.split('-')
                xdate = datetime.date(int(str_date[0]), int(str_date[1]), int(str_date[2]))
                request_date = xdate.strftime("%B %d, %Y")

            freight_agency = ''
            if pedido.freight_agency_id and pedido.freight_agency_id.name:
                freight_agency = pedido.freight_agency_id.name

            rml += """  <blockTable colWidths="60.0,100.0,40.0,100.0,30.0,70.0,100.0" rowHeights="10.0,10.0,10.0,12.0" style="TwoTables">
                            <tr>
                                <td><para style="P6_LEFT">NAME:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(pedido.partner_id.name if pedido.partner_id and pedido.partner_id.name else '') + """</para></td>
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

            rml += """<blockTable colWidths="500.0" rowHeights="12.0" style="LEFT_RIGHT">
                            <tr><td><para style="P8_BOLD_LEFT">COUNTRY OF ORIGIN """ + ustr('(País de Origen): ') + """ ECUADOR</para></td></tr>
                        </blockTable>"""

            rml += """<blockTable colWidths="85.0,55.0,20.0,20.0,40.0,30.0,30.0,85.0,75.0,30.0,30.0" rowHeights="12.0,12.0" style="TableHeader">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE">VARIETY</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">LENGTH</para></td>
                                <td><para style="P6_BOLD_JUSTIFY_TITLE">PIECES/PACKING</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">UNITS</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">STEMS</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">BUNCH</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">DESCRIPTION</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">CLIENT</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">UNIT</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">TOTAL</para></td>
                            </tr>
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">CM</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">HB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">QB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">x HB</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">TOTAL</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">TOTAL</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">REMARKS</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">PRICE</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">PRICE</para></td>
                            </tr>
                        </blockTable>"""

            cr.execute("""select *,
                                coalesce((select sum(case when t."type" = 'percent' then t.amount * lines.stems else t.amount end)
                                from product_taxes_rel ptt
                                inner JOIN account_tax t on ptt.tax_id = t.id
                                where ptt.prod_id = lines.product_id), 0) as taxes
                                from (
                                SELECT
                                v."name" as variety,
                                "length",
                                sum(case
                                when cl.uom = 'HB' then (case when cl.is_box_qty = TRUE then cl.qty else cl.qty/(cl.bunch_type::INT * cl.bunch_per_box) end)
                                when cl.uom = 'FB' then (case when cl.is_box_qty = TRUE then cl.qty * 2 else (cl.qty/(cl.bunch_type::INT * cl.bunch_per_box)) * 2 end)
                                when cl.uom = 'OB' then (case when cl.is_box_qty = TRUE then cl.qty / 4 else (cl.qty/(cl.bunch_type::INT * cl.bunch_per_box * 4)) end)
                                else 0 end) as hb,
                                sum(case when cl.uom = 'QB' then (case when cl.is_box_qty = TRUE then cl.qty else cl.qty/(cl.bunch_type::INT * cl.bunch_per_box) end)
                                when cl.uom = 'FB' then (case when cl.is_box_qty = TRUE then cl.qty * 4 else (cl.qty/(cl.bunch_type::INT * cl.bunch_per_box)) * 4 end)
                                when cl.uom = 'OB' then (case when cl.is_box_qty = TRUE then cl.qty / 2 else (cl.qty/(cl.bunch_type::INT * cl.bunch_per_box * 2)) end)
                                else 0 end) as qb,
                                (select sum(dl.bunch_per_box * dl.bunch_type::int) from detalle_lines dl where pedido_id = %s) as units_per_hb,
                                sum(case when cl.is_box_qty = TRUE then cl.qty * cl.bunch_per_box * cl.bunch_type::int else cl.qty end) as stems,
                                sum(case when cl.is_box_qty = TRUE then cl.qty * cl.bunch_per_box  else cl.qty/cl.bunch_type::FLOAT end) as bunch,
                                min(case when p."type" = 'standing_order' then 'Standing Order' else 'Open Market' end) as Descripcion,
                                pp."name" as subclient,
                                sum(case when cl.is_box_qty = TRUE then (cl.qty * cl.bunch_per_box * cl.bunch_type::int * cl.sale_price)::FLOAT else (cl.qty * cl.sale_price)::FLOAT end)/
                                sum(case when cl.is_box_qty = TRUE then cl.qty * cl.bunch_per_box * cl.bunch_type::int else cl.qty end) as unit_price,
                                sum(case when cl.is_box_qty = TRUE then (cl.qty * cl.bunch_per_box * cl.bunch_type::int * cl.sale_price)::FLOAT else (cl.qty * cl.sale_price)::FLOAT end) as total,
                                min(cl.product_id) as product_id,
                                dl.group_id
                                from
                                confirm_invoice_line cl
                                inner join detalle_lines dl on cl.detalle_id = dl."id"
                                inner join product_variant v on v."id" = cl.variant_id
                                inner join pedido_cliente p on p.id = cl.pedido_id
                                LEFT JOIN res_partner pp on cl.subclient_id = pp."id"
                                where cl.pedido_id = %s
                                GROUP BY v."name", cl."length",pp."name",dl.group_id
                                order by pp."name",v."name") lines""", (pedido.id, pedido.id,))

            lines = cr.fetchall()

            total_hb = 0
            total_qb = 0
            total_stems = 0
            total_bunch = 0
            total_price = 0
            total_taxes = 0
            
            for line in lines:                
                total_bunches = sum(map(lambda r: r[6], filter(lambda r: r[12] == line[12], lines))) if line[12] else 0               
                variety = line[0]
                length = line[1]
                qb_cont = line[3]
                unit_per_hb = line[4]
                stems = line[5]
                bunch = line[6]
                description = line[7]
                subclient = line[8]
                sale_price = line[9]
                total = line[10]                
                total_qb += line[3]
                total_stems += line[5]
                total_price += line[10]
                total_taxes += line[13]
                line_hb =  line[6]/total_bunches if total_bunches else line[2]
                total_hb += line_hb
                total_bunch += bunch
                
                rml += """
                        <blockTable colWidths="85.0,55.0,20.0,20.0,40.0,30.0,30.0,85.0,75.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(variety[0:25] if variety else '')) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (ustr(length[0:15])) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(line_hb,2)) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(qb_cont,2)) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(int(unit_per_hb)) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(stems,2)) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(bunch,2)) + """</para></td>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(description[0:20] if description else '')) + """</para></td>
                                <td><para style="P5_COURIER_JUSTIFY">""" + ustr(subclient or '') + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(sale_price,2)) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(total,2)) + """</para></td>
                            </tr>
                        </blockTable>"""

            rml += """
                        <blockTable colWidths="85.0,55.0,20.0,20.0,40.0,30.0,30.0,85.0,75.0,30.0,30.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P5_COURIER_BOLD_JUSTIFY">""" + _('Total farm') + """</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(round(total_hb,2)) + """</para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(round(total_qb,2)) + """</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(round(total_stems,0)) + """</para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(round(total_bunch,2)) + """</para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(round(float(total_hb)/2 + float(total_qb)/4, 2)) + """ Full Boxes</para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_CENTER"></para></td>
                                <td><para style="P5_COURIER_BOLD_CENTER">""" + str(round(total_price,2)) + """</para></td>
                            </tr>
                        </blockTable>"""

            res_tipo_neg = pedido.partner_id.tipo_neg_id.name if pedido.partner_id.tipo_neg_id and pedido.partner_id.tipo_neg_id.name else ''
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
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(total_price + total_taxes,2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">I.V.A</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(total_taxes,2)) + """</para></td>
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
                                            <td><para style="P6_LEFT">""" + _('Freight') + ' ' + (ustr(pedido.freight_agency_id.name) if pedido.freight_agency_id and pedido.freight_agency_id.name else '') + """</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(flete_value,2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">TOTAL</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(total_price + total_taxes + flete_value,2)) + """</para></td>
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
                                       <tr><td><para style="P6_CENTER">""" + (company.street +', ' if company.street  else '')  + (company.street2 + ', ' if company.street2 else '') + (company.city + ', ' if company.city else '')  + (company.state_id.name + ', ' if company.state_id and company.state_id.name else '')  + (company.country_id.name if  company.country_id and company.country_id.name else '') + """</para></td></tr>
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

            cr.execute(""" SELECT
                                pp.name as farm,                                
                                sum(case
                                when cl.uom = 'HB' then (case when cl.is_box_qty = TRUE then cl.qty else cl.qty/(cl.bunch_type::INT * cl.bunch_per_box) end)
                                when cl.uom = 'FB' then (case when cl.is_box_qty = TRUE then cl.qty * 2 else (cl.qty/(cl.bunch_type::INT * cl.bunch_per_box)) * 2 end)
                                when cl.uom = 'OB' then (case when cl.is_box_qty = TRUE then cl.qty / 4 else (cl.qty/(cl.bunch_type::INT * cl.bunch_per_box * 4)) end)
                                else 0 end) as hb,
                                sum(case when cl.uom = 'QB' then (case when cl.is_box_qty = TRUE then cl.qty else cl.qty/(cl.bunch_type::INT * cl.bunch_per_box) end)
                                when cl.uom = 'FB' then (case when cl.is_box_qty = TRUE then cl.qty * 4 else (cl.qty/(cl.bunch_type::INT * cl.bunch_per_box)) * 4 end)
                                when cl.uom = 'OB' then (case when cl.is_box_qty = TRUE then cl.qty / 2 else (cl.qty/(cl.bunch_type::INT * cl.bunch_per_box * 2)) end)
                                else 0 end) as qb,   
                                dl.group_id 
                                from
                                confirm_invoice_line cl
                                inner join detalle_lines dl on cl.detalle_id = dl."id"                                
                                inner join pedido_cliente p on p.id = cl.pedido_id
                                LEFT JOIN res_partner pp on cl.supplier_id = pp."id"
                                where cl.pedido_id = %s
                                GROUP BY pp."name", dl.group_id 
                                order by pp."name" """, (pedido.id,))
            lines = cr.fetchall()
            total_hb = 0
            total_qb = 0
            total_fb = 0
            for line in lines:
                hb = line[1]/2 if line[3] else line[1]
                qb = line[2]/4 if line[3] else line[2]
                total = line[1]/4 + line[2]/8 if line[3] else line[1]/2 + line[2]/4
                total_hb += hb
                total_qb += qb
                total_fb += total
                
                rml += """<tr>"""
                rml += """<td><para style="P6_CENTER">""" + ustr(line[0] or '') + """</para></td>"""
                rml += """<td><para style="P6_CENTER">""" + (str(round(hb, 2))) + """</para></td>"""
                rml += """<td><para style="P6_CENTER">""" + (str(round(qb, 2))) + """</para></td>"""
                rml += """<td><para style="P6_CENTER">""" + (str(round(total, 2))) + """</para></td>"""
                rml += """<td></td></tr>"""

            rml += """<tr>
                                <td><para style="P6_CENTER">TOTAL</para></td>
                                <td><para style="P6_CENTER">""" + str(round(total_hb,2)) + """</para></td>
                                <td><para style="P6_CENTER">""" + str(round(total_qb,2)) + """</para></td>
                                <td><para style="P6_CENTER">""" + str(round(total_fb ,2)) + """</para></td>
                                <td></td>
                            </tr>"""

            rml += """</blockTable>"""

            rml += """  </story>
                    </document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        return pdf, report_type

AccountInvoiceVarietyReport('report.account_invoice_variety_report', 'pedido.cliente', '', '')
