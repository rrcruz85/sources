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
                        <template pageSize="(595.0,842.0)" title=" """ + _("Account Invoice") + """ " allowSplitting="20">
                            <pageTemplate id="page1">
                                <frame id="first" x1="20.0" y1="30.0" width="560" height="835"/>
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

            rml += """  <spacer length="1.0 cm"/>"""

            rml += """  <blockTable colWidths="560.0" rowHeights="30.0" style="MainTable">
                            <tr><td><para style="P14_BOLD_CENTER">INVOICE PACKING</para></td></tr>
                        </blockTable>"""

            cr.execute("select supplier_invoice_number from account_invoice where pedido_cliente_id = %s", (pedido.id,))
            record = cr.fetchone()
            invoice_number = record[0] if record else ''

            rml += """  <blockTable colWidths="360.0,30.0,170.0" rowHeights="12.0,12.0,12.0" style="LEFT_RIGHT">
                            <tr>
                                <td></td>
                                <td></td>
                                <td><para style="P10_CENTER">INVOICE</para></td>
                            </tr>
                            <tr>
                                <td></td>
                                <td></td>
                                <td><para style="P10_CENTER">FACTURA No. """ + (invoice_number if invoice_number else 'n/d') + """</para></td>
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

            rml += """ <blockTable colWidths="120.0,100.0,40.0,100.0,30.0,70.0,100.0" rowHeights="10.0,10.0,10.0,12.0" style="TwoTables">
                            <tr>
                                <td><para style="P6_LEFT">NAME:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(pedido.partner_id.name or '') + """</para></td>
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
                                <td><para style="P6_BOLD_LEFT">""" + ustr(pedido.partner_id.city or '') + ustr(pedido.partner_id.country_id.name or '' if pedido.partner_id.country_id else '') + """</para></td>
                                <td><para style="P6_LEFT">Contact:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + ustr(contact) + """</para></td>
                                <td><para style="P6_BOLD_LEFT"></para></td>
                                <td><para style="P6_LEFT">Cargo Agency:</para></td>
                                <td><para style="P6_BOLD_LEFT">""" + freight_agency + """</para></td>
                            </tr>
                        </blockTable>"""

            rml += """  <blockTable colWidths="560.0" rowHeights="15.0" style="LEFT_RIGHT">
                            <tr><td><para style="P8_BOLD_LEFT">COUNTRY OF ORIGIN """ + ustr('(País de Origen): ') + """ ECUADOR</para></td></tr>
                        </blockTable>"""

            rml += """<blockTable colWidths="120.0,50.0,45.0,40.0,40.0,25.0,25.0,75.0,70.0,30.0,40.0" rowHeights="20.0" style="CentralTable">
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

            rml += """<blockTable colWidths="120.0,50.0,45.0,40.0,40.0,25.0,25.0,75.0,70.0,30.0,40.0" rowHeights="10.0" style="AllBorders">
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

            cr.execute("""select *,
                                coalesce(
                                (select
                                sum(case when t."type" = 'percent' then t.amount * lines.stems else t.amount end)
                                from product_taxes_rel ptt
                                inner JOIN account_tax t on ptt.tax_id = t.id
                                where ptt.prod_id = lines.product_id), 0) as taxes
                                from (                                
                                SELECT p.name as farm, 
                                v."name" as varianty, 
                                dl.lengths as "length",
                                sum(case when dl.is_box_qty = TRUE and dl.qty >= 1.00 then dl.qty * dl.bunch_per_box * dl.bunch_type::int 
                                when dl.is_box_qty = TRUE and dl.qty < 1.00 then dl.bunch_per_box * dl.bunch_type::int else dl.qty end) as stems,
                                sum(dl.bunch_per_box) as bunches,
                                pt."name" as product,
                                avg(dl.sale_price) as unit_price,
                                sum(case when dl.is_box_qty = TRUE and dl.qty >= 1.00 then (dl.qty * dl.bunch_per_box * dl.bunch_type::int * dl.sale_price)::FLOAT 
                                when dl.is_box_qty = TRUE and dl.qty < 1.00 then (dl.bunch_per_box * dl.bunch_type::int * dl.sale_price)::FLOAT else (dl.qty * dl.sale_price)::FLOAT end) as total,
                                pp."name" as subclient,
                                pt.id as product_id,
                                dl.box_id,   
                                case when dl.box_id is not null then                                
                                 (select sum(dl2.bunch_per_box) from detalle_lines dl2 where dl2.box_id = dl.box_id) 
                                else  
                                 sum(case when dl.is_box_qty = TRUE then dl.qty else dl.qty/(dl.bunch_type::INT * dl.bunch_per_box) end)
                                end as total_bunches,
                                dl.uom,
                                sum(case when dl.is_box_qty = TRUE then dl.qty 
                                else qty / (dl.bunch_per_box * dl.bunch_type::int) end) as qty_bxs
                                from
                                detalle_lines dl
                                inner join res_partner p on dl.supplier_id = p."id"
                                inner join product_variant v on v."id" = dl.variant_id
                                INNER JOIN product_template pt on pt."id" = dl.product_id
                                LEFT JOIN res_partner pp on dl.subclient_id = pp."id"                               
                                where dl.pedido_id = %s and dl.active = True
                                GROUP BY p.name, v."name", dl.lengths,pp."name",pt."name",pt.id,dl.box_id, dl.uom
                                order by pp.name, dl.box_id, v."name", dl.lengths, p."name"
                                ) lines""", (pedido.id,))         

            lines = cr.fetchall()

            summary = {}
            first = False
            subclient_tmp = lines[0][8] if lines else ''
            
            switch_hb = True
            switch_qb = True
            count_hb = 0
            count_qb = 0
            total_stems = 0
            total_bunch = 0
            total_qb = 0
            total_hb = 0
            total_price = 0
            
            line_number = 0
            print('---------------------------------------------------------------------------------------------')
            print(len(lines))
            jump_printed = False
            for line in lines:
               
                supplier = line[0]
                variety = line[1].replace('&', '&amp;')
                length = line[2]
                stems_cant = line[3]
                bunch_cant = line[4]

                qty_tmp = round(bunch_cant / line[11], 2) if line[10] else line[11]

                hb_cont = line[13] if line[12] == 'HB' else 0
                qb_cont = line[13] if line[12] == 'QB' else 0
                count_hb += hb_cont
                count_qb += qb_cont
                if count_hb > 0:
                    switch_qb = False
                if count_qb > 0:
                    switch_hb = False
                if count_hb >= 1:
                    switch_hb = False
                if count_qb >= 1:
                    switch_qb = False

                description = line[5]
                sale_price = line[6]
                total = line[7]
                subclient = line[8]
                taxes = line[13]

                if supplier not in summary:
                    summary[supplier] = [stems_cant, bunch_cant, hb_cont, qb_cont, total, taxes]
                else:
                    summary[supplier][0] += stems_cant
                    summary[supplier][1] += bunch_cant
                    summary[supplier][2] += hb_cont
                    summary[supplier][3] += qb_cont
                    summary[supplier][4] += total
                    summary[supplier][5] += taxes

                total_stems += stems_cant
                total_bunch += bunch_cant
                total_qb += qb_cont
                total_hb += hb_cont
                total_price += total

                if subclient != subclient_tmp:
                    first = True

                rml += """                       
                        <blockTable colWidths="120.0,50.0,45.0,40.0,40.0,25.0,25.0,75.0,70.0,30.0,40.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(supplier if supplier else '')) + """</para></td>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(variety[0:25] if variety else '')) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (ustr(length)[0:15]) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (str(round(stems_cant, 2))) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (str(round(bunch_cant, 2))) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + ('1.0' if switch_hb else '*' if hb_cont > 0 and hb_cont < 1 else str(round(hb_cont, 2))) + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + ('1.0' if switch_qb else '*' if qb_cont > 0 and qb_cont < 1 else str(round(qb_cont, 2))) + """</para></td>
                                <td><para style="P5_COURIER_JUSTIFY">""" + (ustr(description[0:20] if description else '')) + """</para></td>
								<td><para style="P5_COURIER_JUSTIFY">""" + ustr(subclient_tmp[0:20] if subclient_tmp else '') + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + (str(round(sale_price, 2)) if sale_price else '') + """</para></td>
                                <td><para style="P5_COURIER_CENTER">""" + str(round(total, 2)) + """</para></td>
                            </tr>
                        </blockTable>"""
                
                line_number += 1

                if line_number == 63:
                    jump_printed = True                   
                    rml += """ <nextPage/> <spacer length="1.0cm"/> """         

                if first:
                    rml += """<blockTable colWidths="120.0,50.0,45.0,40.0,40.0,25.0,25.0,75.0,70.0,30.0,40.0" rowHeights="10.0" style="AllBorders">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER_TITLE">Total Subclient</para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_stems, 2)) + """</para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_bunch, 2)) + """</para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_hb, 2)) + """</para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_qb, 2)) + """</para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                    <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_price, 2)) + """</para></td>
                                </tr>
                            </blockTable>"""
                    line_number += 1
                    
                    if line_number == 63:
                        jump_printed = True                       
                        rml += """ <nextPage/> <spacer length="1.0cm"/> """

                    first = False
                    subclient_tmp = subclient
                    total_stems = 0
                    total_bunch = 0
                    total_qb = 0
                    total_hb = 0
                    total_price = 0

                if count_hb >= 1:
                    count_hb = 0
                    switch_hb = True
                if count_qb >= 1:
                    count_qb = 0
                    switch_qb = True

            rml += """  <blockTable colWidths="120.0,50.0,45.0,40.0,40.0,25.0,25.0,75.0,70.0,30.0,40.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE">Total Subclient</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_stems, 2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_bunch, 2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_hb, 2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_qb, 2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_price, 2)) + """</para></td>
                            </tr>
                        </blockTable>"""
            line_number += 1
          
            total_stems = 0
            total_bunch = 0
            total_hb = 0
            total_qb = 0
            total_price = 0
            total_taxes = 0
            for vals in summary.values():
                total_stems += vals[0]
                total_bunch += vals[1]
                total_hb += vals[2]
                total_qb += vals[3]
                total_price += vals[4]
                total_taxes += vals[5]
            total_fb = total_hb / 2 + total_qb / 4

            rml += """  <blockTable colWidths="120.0,50.0,45.0,40.0,40.0,25.0,25.0,75.0,70.0,30.0,40.0" rowHeights="10.0" style="AllBorders">
                            <tr>
                                <td><para style="P6_BOLD_CENTER_TITLE">TOTAL</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_stems, 2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_bunch, 2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_hb, 2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_qb, 2)) + """</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE">""" + str(round(total_fb, 2)) + """ Full Box</para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                                <td><para style="P6_BOLD_CENTER_TITLE"></para></td>
                            </tr>
                        </blockTable>"""
            
            line_number += 1
            if line_number == 64:
                jump_printed = True
                rml += """ <nextPage/> <spacer length="1.0cm"/> """

            print('Total:')
            print(line_number)

            res_tipo_neg = pedido.partner_id.tipo_neg_id.name if pedido.partner_id.tipo_neg_id else ''
            tipo_flete = pedido.partner_id.tipo_flete
            flete_value = pedido.precio_flete if tipo_flete == 'fob_f_p' else 0.0
            
            rml += """                     
                       <blockTable colWidths="240.0,180.0,140.0" rowHeights="" style="TableX">
                            <tr>
                                <td>
                                    <blockTable colWidths="285.0,55.0,220.0" rowHeights="8.0,8.0" style="">
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
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round((total_price + total_taxes), 2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">I.V.A</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(total_taxes, 2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">SUBTOTAL</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(total_price, 2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td></td><td></td><td></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">""" + _('Freight') + ' ' + (ustr(pedido.freight_agency_id.name or '') if pedido.freight_agency_id else '') + """</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round(flete_value, 2)) + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P6_LEFT">TOTAL</para></td>
                                            <td><para style="P6_LEFT_1">USD</para></td>
                                            <td><para style="P6_LEFT_1">""" + ustr('$') + str(round((total_price + total_taxes + flete_value), 2)) + """</para></td>
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

            rml += """  <blockTable colWidths="560.0" rowHeights="" style="TableY">
                            <tr><td><para style="P10_CENTER">Think in flowers???, think about us "INFLOWERS"</para></td></tr>
                            <tr><td><para style="P6_CENTER">""" + (company.street + ', ' if company.street else '') + (
                company.street2 + ', ' if company.street2 else '') + (company.city + ', ' if company.city else '') + (
                       company.state_id.name + ', ' if company.state_id and company.state_id.name else '') + (
                       company.country_id.name if company.country_id and company.country_id.name else '') + """</para></td></tr>
                            <tr><td><para style="P6_CENTER">Phone: """ + (
                       company.phone + ',' if company.phone else '') + """ Mobile: 59399 821-2383</para></td></tr>
                            <tr><td><para style="P6_CENTER">Email/MSN: """ + (company.email if company.email else '') + """ Skype: Inflowers</para></td></tr>
                        </blockTable>"""
            
            if not jump_printed and line_number > 38:
                rml += """<nextPage/><spacer length="1.0cm"/> """
            else:
                rml += """<spacer length="0.5cm"/> """

            rml += """   
                        <blockTable colWidths="170.0,30.0,35.0,30.0,295.0" rowHeights="12.0" style="TableZ">
                            <tr>
                                <td><para style="P6_CENTER">FINCA</para></td>
                                <td><para style="P6_CENTER">HALF</para></td>
                                <td><para style="P6_CENTER">QUART</para></td>
                                <td><para style="P6_CENTER">FULL</para></td>
                                <td></td>
                            </tr>"""

            for key in summary.keys():
                total_fb_tmp = summary[key][2] / 2 + summary[key][3] / 4
                rml += """<tr>"""
                rml += """<td><para style="P6_CENTER">""" + ustr(key or '') + """</para></td>"""
                rml += """<td><para style="P6_CENTER">""" + (str(round(summary[key][2], 2))) + """</para></td>"""
                rml += """<td><para style="P6_CENTER">""" + (str(round(summary[key][3], 2))) + """</para></td>"""
                rml += """<td><para style="P6_CENTER">""" + (str(round(total_fb_tmp, 2))) + """</para></td>"""
                rml += """<td></td></tr>"""

            rml += """<tr>
                                <td><para style="P6_CENTER">TOTAL</para></td>
                                <td><para style="P6_CENTER">""" + str(round(total_hb, 2)) + """</para></td>
                                <td><para style="P6_CENTER">""" + str(round(total_qb, 2)) + """</para></td>
                                <td><para style="P6_CENTER">""" + str(round(float(total_fb), 2)) + """</para></td>
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
