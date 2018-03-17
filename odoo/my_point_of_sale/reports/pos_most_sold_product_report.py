# -*- coding: utf-8 -*-

import io
import os
from random import choice

from PIL import Image
from openerp import pooler, modules, tools
from openerp.report.interface import report_rml
from openerp.tools.translate import _


class MostSoldProductReport(report_rml):
    def create(self, cr, uid, ids, datas, context):
        report_obj_model = pooler.get_pool(cr.dbname).get('pos.most.sold.product')
        report_obj_line_model = pooler.get_pool(cr.dbname).get('pos.most.sold.product.line')
        res_partnet_model = pooler.get_pool(cr.dbname).get('res.partner')
        product_model = pooler.get_pool(cr.dbname).get('product.product')
        user = pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, uid, context=context)

        for obj in report_obj_model.browse(cr, uid, ids, context):
            rml = """
                <document filename="test.pdf">
                    <template pageSize="(595.0,842.0)" title="Most Sold Products" author="Reynaldo Rodriguez" allowSplitting="20">
                        <pageTemplate id="page1">
                            <frame id="first" x1="50.0" y1="20.0" width="498" height="800"/>
                        </pageTemplate>
                    </template>"""

            rml += """
                    <stylesheet>
                        
                        <blockTableStyle id="MainTable">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockSpan start="0,1" stop="2,1"/>
                            <blockSpan start="0,2" stop="2,2"/>
                            <blockSpan start="0,3" stop="2,3"/>
                        </blockTableStyle>
                        
                        <blockTableStyle id="MainTable2">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="LEFT"/>
                            <blockSpan start="0,0" stop="2,0"/>                                                        
                            blockSpanReplace                            
                            <lineStyle kind="LINEABOVE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBELOW" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>                       
                            
                        </blockTableStyle>                      
                        
                        <initialize>
                            <paraStyle name="all" alignment="justify"/>
                        </initialize>

                        <paraStyle name="title_top_left" fontName="Helvetica-Bold" fontSize="7.0" leading="8"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="left" textColor="#244d70"/>
                        
                        <paraStyle name="title_top_left_10" fontName="Helvetica-Bold" fontSize="10.0" leading="8"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="left" textColor="#244d70"/>
                                   
                        <paraStyle name="title_top_center_10" fontName="Helvetica-Bold" fontSize="10.0" leading="8"
                                                           spaceBefore="0.0" spaceAfter="0.0" alignment="center" textColor="#244d70"/>

                        <paraStyle name="title_top_center" fontName="Helvetica-Bold" fontSize="7.0" leading="8"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center" textColor="#244d70"/>

                        <paraStyle name="title_top_center10" fontName="Helvetica-Bold" fontSize="10.0" leading="15"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center" textColor="#244d70"/>

                        <paraStyle name="title_middle_left" fontName="Helvetica-Bold" fontSize="6.0" leading="8"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="left" textColor="#244d70" leftIndent="0.0cm"/>

                        <paraStyle name="title_bottom_center" fontName="Helvetica-Bold" fontSize="7.0" leading="10"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center" textColor="#244d70" leftIndent="0.0cm"/>

                        <paraStyle name="title_top_center" fontName="Helvetica-Bold" fontSize="7.0" leading="10"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center" textColor="#244d70" leftIndent="0.0cm"/>

                        <paraStyle name="helvetica_bold_8_center" fontName="Helvetica-Bold" fontSize="8.0" leading="9"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center"/>

                        <paraStyle name="helvetica_bold_8_justify" fontName="Helvetica-Bold" fontSize="8.0" leading="9"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="justify"/>

                        <paraStyle name="helvetica_8_justify" fontName="Helvetica" fontSize="8.0" leading="9"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="justify"/>

                        <paraStyle name="text_information_12" fontName="Helvetica" fontSize="12.0" leading="10"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center"/>

                        <paraStyle name="text_information" fontName="Helvetica" fontSize="11.0" leading="10"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center"/>

                        <paraStyle name="text_information2" fontName="Helvetica" fontSize="9.0" leading="8"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center"/>

                        <paraStyle name="x_mark" fontName="Helvetica" fontSize="6.0" leading="8"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="center" textColor="#1D3E58"/>

                        <paraStyle name="text_information2_left" fontName="Helvetica" fontSize="9.0" leading="12"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="left" leftIndent="0.5cm"/>

                        <paraStyle name="text_information3_left" fontName="Helvetica" fontSize="8.0" leading="12"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="left" leftIndent="0.5cm"
                                   bulletFontName="ZapfDingbats" bulletFontSize="5"/>

                        <paraStyle name="adv_text" fontName="Helvetica" fontSize="6.0" leading="10" textColor="#244d70"
                                   spaceBefore="0.0" spaceAfter="0.0" alignment="justify"/>
                    </stylesheet>"""

            rml += """<story>"""

            list_to_delete = []

            if user.company_id.logo_web:
                img_logo_path = modules.get_module_path('my_point_of_sale')
                img_logo_path += '/static/src/img/'
                img_logo_path = os.path.normpath(img_logo_path)

                name = 'company_logo' + str(choice(range(1, 1000)))
                img_logo_path = os.path.join(img_logo_path, name + '.png')
                if os.path.isfile(img_logo_path):
                    os.remove(img_logo_path)

                list_to_delete.append(img_logo_path)

                image_stream = io.BytesIO(user.company_id.logo_web.decode('base64'))
                img = Image.open(image_stream)
                img.save(img_logo_path, "PNG")

            rml += """
                        <section>
                            <blockTable colWidths="340.0,200.0" rowHeights="" style="">
                                <tr>
                                    <td>
                                        <illustration width="240" height="50">
                                            <image file="file:""" + img_logo_path + """ " x="0" y="0" width="240" height="50"/>
                                        </illustration>
                                    </td>
                                    <td>
                                        <para style="title_top_center">
                                            """ + (tools.ustr(user.company_id.street or '')) + ' ' + (tools.ustr(user.company_id.street2 or '')) + """
                                        </para>
                                        <para style="title_top_center">
                                            """ + 'Telef.: ' + (user.company_id.phone or '') + ' ' + (tools.ustr(user.company_id.city or '')) + (' - ' if user.company_id.country_id.name else '') + (tools.ustr(user.company_id.country_id.name or '')) + """
                                        </para>
                                        <para style="title_top_center">""" + (user.company_id.website or '') + """</para>
                                    </td>
                                </tr>
                                <tr>                                     
                                    <td>
                                          <para style="title_top_left">FECHA INICIO: """ + (tools.ustr(obj.date_start or '')) + """</para>
                                          <para style="title_top_left">FECHA FIN: """ + (tools.ustr(obj.date_end or '')) + """ </para>                                                                                                           
                                    </td>
                                    <td></td>
                                </tr>
                            </blockTable>"""

            str_descripcion = tools.ustr("PRODUCTO MÁS VENDIDO POR CLIENTE") if obj.nbr_product == 1 else tools.ustr(obj.nbr_product) + tools.ustr(" PRODUCTOS MÁS VENDIDOS POR CLIENTE")

            rml += """
                            <spacer length="0.4cm"/> 
                            <blockTable colWidths="270.0,220.0,50.0" rowHeights="" style="MainTable2"> 
                                <tr>
                                     <td>
                                        <para style="title_top_center_10">""" + str_descripcion + """</para>
                                     </td>
                                     <td></td>
                                     <td></td>
                                </tr> 
                                <tr>
                                    <td>
                                        <para style="title_top_left">CLIENTE</para>
                                    </td>
                                    <td>
                                        <para style="title_top_left">PRODUCTO</para>
                                    </td>
                                    <td>
                                        <para style="title_top_center">CANTIDAD</para>
                                    </td>
                                </tr>"""
            if obj.line_ids:

                cr.execute("""
                    SELECT p."name",p.email,pd.name_template,
                    sum(l.product_qty) as product_qty
                    from pos_most_sold_product_line l
                    INNER JOIN res_partner p on p.id = l.partner_id
                    INNER JOIN product_product pd on pd.id = l.product_id
                    where l.parent_id = %s
                    GROUP BY p."name",p.email,pd.name_template 
                    order by p."name", sum(l.product_qty) DESC""" % (str(obj.id),))
                lines = cr.fetchall()

                def count(record, init_pos, records):
                    cont = 0
                    pos = 0
                    for r in records:
                        if pos >= init_pos and r[0] == record:
                            cont += 1
                        pos += 1
                    return cont

                row = 2
                rowspan = []
                pos = 0
                for line in lines:
                    client_name = line[0] + ' &lt;' + line[1] + '&gt;'
                    cant_prod_repet = count(line[0], pos, lines)
                    if cant_prod_repet > 1:
                        rowspan.append((row, row + cant_prod_repet - 1))
                        row = row + cant_prod_repet
                    else:
                        row += 1

                    product_name = line[2]
                    product_qty = line[3]
                    rml += """<tr>
                                        <td><para style="title_top_left">""" + tools.ustr(client_name) + """</para></td>
                                        <td><para style="title_top_left">""" + tools.ustr(product_name) + """</para></td>
                                        <td><para style="title_top_center">""" + tools.ustr(product_qty) + """</para></td>
                                    </tr>"""
                    pos += 1

                if rowspan:
                    rowspan = map(lambda a:  '<blockSpan start="0,' + tools.ustr(a[0]) + '" stop="0,' + tools.ustr(a[1]) +'"/>\n', rowspan)
                rml = rml.replace('blockSpanReplace', ''.join(rowspan))

            rml +="""
                    
                    </blockTable>"""
            rml += """
                     </section>"""
            rml += """
                    </story>"""
            rml += """
                </document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)

        for path in list_to_delete:
            os.remove(path)
        return pdf, report_type

MostSoldProductReport('report.pos_most_sold_product_report', 'pos.most.sold.product', '', '')
