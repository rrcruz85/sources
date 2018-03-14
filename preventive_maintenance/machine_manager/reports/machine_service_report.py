# -*- coding: utf-8 -*-

import io
import os
from random import choice

from PIL import Image
from openerp import pooler, modules, tools
from openerp.report.interface import report_rml
from openerp.tools.translate import _


class MachineReparationReport(report_rml):
    def create(self, cr, uid, ids, datas, context):
        report_obj_model = pooler.get_pool(cr.dbname).get('machinery')
        odometer_obj = pooler.get_pool(cr.dbname).get('fleet.vehicle.odometer')
        user = pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, uid, context=context)

        for service in report_obj_model.browse(cr, uid, ids, context):
            rml = """
                <document filename="test.pdf">
                    <template pageSize="(595.0,842.0)" title="" author="" allowSplitting="20">
                        <pageTemplate id="page1">
                            <frame id="first" x1="50.0" y1="20.0" width="498" height="800"/>
                        </pageTemplate>
                    </template>"""

            rml += """
                    <stylesheet>
                        <blockTableStyle id="NoneBorders">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <lineStyle kind="LINEABOVE" colorName="white" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBELOW" colorName="white" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="white" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="white" start="0,0" stop="-1,-1" thickness="0.1"/>
                        </blockTableStyle>

                        <blockTableStyle id="AllBorders">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <lineStyle kind="LINEABOVE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBELOW" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                        </blockTableStyle>

                        <blockTableStyle id="MainTable">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>

                            <blockSpan start="0,1" stop="2,1"/>
                            <blockSpan start="0,2" stop="2,2"/>
                            <blockSpan start="0,3" stop="2,3"/>
                        </blockTableStyle>

                        <blockTableStyle id="Table1">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockSpan start="0,1" stop="-1,-1"/>

                            <lineStyle kind="LINEABOVE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBELOW" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="-1,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="0,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="-1,0" stop="-1,-1" thickness="1.0"/>
                        </blockTableStyle>

                        <blockTableStyle id="Table1L">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>

                            <blockSpan start="0,0" stop="1,0"/>
                            <blockSpan start="2,0" stop="3,0"/>

                            <blockSpan start="0,1" stop="1,1"/>
                            <blockSpan start="2,1" stop="3,1"/>
                            <blockSpan start="1,2" stop="2,2"/>
                            <blockSpan start="0,3" stop="3,3"/>
                            <blockSpan start="0,4" stop="3,4"/>

                            <lineStyle kind="LINEABOVE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBELOW" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="-1,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="0,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="-1,0" stop="-1,-1" thickness="1.0"/>
                        </blockTableStyle>

                        <blockTableStyle id="Table2">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockSpan start="0,1" stop="1,1"/>

                            <lineStyle kind="LINEABOVE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBELOW" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="-1,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="0,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="-1,0" stop="-1,-1" thickness="1.0"/>
                        </blockTableStyle>

                        <blockTableStyle id="TableDetails">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockSpan start="3,1" stop="3,2"/>

                            <lineStyle kind="LINEABOVE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBELOW" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="-1,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="0,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="-1,0" stop="-1,-1" thickness="1.0"/>
                        </blockTableStyle>

                        <blockTableStyle id="checkBox">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>

                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="0,0" thickness="0.8"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="0,0" stop="0,0" thickness="0.8"/>
                            <lineStyle kind="LINEABOVE" colorName="#244d70" start="0,0" stop="0,0" thickness="0.8"/>
                            <lineStyle kind="LINEBELOW" colorName="#244d70" start="0,0" stop="0,0" thickness="0.8"/>
                        </blockTableStyle>

                        <blockTableStyle id="TablePhoto">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockSpan start="0,0" stop="0,-1"/>

                            <lineStyle kind="LINEABOVE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBELOW" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEAFTER" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                            <lineStyle kind="LINEBEFORE" colorName="#244d70" start="0,0" stop="-1,-1" thickness="1.0"/>
                        </blockTableStyle>

                        <blockTableStyle id="LastTable">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockSpan start="0,0" stop="0,-1"/>

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

            rml += """
                    <story>"""

            logo = user.company_id.logo_web
            list_to_delete = []

            img_logo_path = modules.get_module_path('machine_manager')
            img_logo_path += '/static/img/'
            img_logo_path = os.path.normpath(img_logo_path)
            img_logo_path = os.path.join(img_logo_path, 'logo.png')

            img_oil_path = modules.get_module_path('machine_manager')
            img_oil_path += '/static/img/'
            img_oil_path = os.path.normpath(img_oil_path)
            img_oil_path = os.path.join(img_oil_path, 'oil.png')

            img_car_path = modules.get_module_path('machine_manager')
            img_car_path += '/static/img/'
            img_car_path = os.path.normpath(img_car_path)
            img_car_path = os.path.join(img_car_path, 'car.png')

            if user.company_id.logo_web:
                path = modules.get_module_path('machine_manager')
                path += '/static/temp/'
                path = os.path.normpath(path)

                name = 'photo' + str(choice(range(1, 100)))
                img_path = os.path.join(path, name + '.png')
                img_logo_path = img_path
                list_to_delete.append(img_path)

                image_stream = io.BytesIO(user.company_id.logo_web.decode('base64'))
                img = Image.open(image_stream)
                img.save(img_path, "PNG")

            rml += """  <section>
                            <blockTable colWidths="340.0,200.0" rowHeights="" style="">
                                <tr>
                                    <td>
                                        <illustration width="240" height="50">
                                            <image file="file:""" + img_logo_path + """ " x="0" y="0" width="240" height="50"/>
                                        </illustration>
                                    </td>

                                    <td>
                                        <para style="title_top_center">R.U.C.: """ + (tools.ustr(user.company_id.ruc or '')) +"""</para>
                                        <para style="title_top_center">
                                            """ + (tools.ustr(user.company_id.street or '')) + ' ' + (tools.ustr(user.company_id.street2 or '')) + """
                                        </para>
                                        <para style="title_top_center">
                                            """ + 'Telef.: ' + (user.company_id.phone or '') + ' ' + (tools.ustr(user.company_id.city or '')) + (' - ' if user.company_id.country_id.name else '') + (tools.ustr(user.company_id.country_id.name or '')) + """
                                        </para>
                                        <para style="title_top_center">""" + (user.company_id.website or '') + """</para>
                                    </td>
                                </tr>
                            </blockTable>"""

            _date = service.reception_date.split('-')
            year, month, day = _date[0], _date[1], _date[2]
            odometer_ids = odometer_obj.search(cr, uid, [('vehicle_id', '=', service.vehicle_id.id)], limit=1, order='date desc')
            odometer = odometer_obj.browse(cr, uid, odometer_ids, context=context)

            rml += """      <blockTable colWidths="330.0,10.0,200" rowHeights="" style="MainTable">
                                <tr>
                                    <td>
                                        <blockTable colWidths="60.0,20.0,20.0,30.0,200.0" rowHeights="25.0,20.0" style="Table1">
                                            <tr>
                                                <td>
                                                    <para style="title_top_center">FECHA DE RECEPCION</para>
                                                </td>
                                                <td>
                                                    <para style="title_top_left">DIA</para>
                                                    <para style="text_information2">""" + day + """</para>
                                                </td>
                                                <td>
                                                    <para style="title_top_left">MES</para>
                                                    <para style="text_information2">""" + month + """</para>
                                                </td>
                                                <td>
                                                    <para style="title_top_left">""" + tools.ustr('AÑO') + """</para>
                                                    <para style="text_information2">""" + year + """</para>
                                                </td>
                                                <td>
                                                    <para style="title_top_left">ASESOR</para>
                                                    <para style="text_information">
                                                        """ + (tools.ustr(service.consultant_id.name) if service.consultant_id else '') + """
                                                    </para>
                                                </td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <para style="title_top_left">CIA. DE SEGUROS </para>
                                                    <para style="text_information2_left">""" + (tools.ustr(service.cia or '')) + """</para>
                                                </td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                            </tr>
                                        </blockTable>

                                        <spacer length="0.1cm"/>
                                        <blockTable colWidths="165.0,165.0" rowHeights="20.0,20.0,20.0" style="Table2">
                                            <tr>
                                                <td>
                                                    <para style="title_top_left">NOMBRE DEL CLIENTE</para>
                                                    <para style="text_information2_left">
                                                        """ + (tools.ustr(service.customer_id.name or '')) + """
                                                    </para>
                                                </td>
                                                <td>
                                                    <para style="title_top_left">BROKER</para>
                                                    <para style="text_information2_left">
                                                        """ + (tools.ustr(service.broker_id.name or '')) + """
                                                    </para>
                                                </td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <para style="title_top_left">DIRECCION</para>
                                                    <para style="text_information2_left">
                                                        """ + (tools.ustr(service.customer_id.street or '') + ' ' + tools.ustr(service.customer_id.street2 or '')) + """
                                                    </para>
                                                </td>
                                                <td></td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <para style="title_top_left">TELEF. CELULAR</para>
                                                    <para style="text_information2_left">
                                                        """ + (service.customer_id.mobile or '') + """
                                                    </para>
                                                </td>
                                                <td>
                                                    <para style="title_top_left">TELEF. OFICINA</para>
                                                    <para style="text_information2_left">
                                                        """ + (service.customer_id.phone or '') + """
                                                    </para>
                                                </td>
                                            </tr>
                                        </blockTable>

                                        <spacer length="0.1cm"/>
                                        <blockTable colWidths="330.0" rowHeights="20.0" style="AllBorders">
                                            <tr>
                                                <td>
                                                    <para style="title_top_left">CORREO</para>
                                                    <para style="text_information2_left">
                                                        """ + (service.customer_id.email or '') + """
                                                    </para>
                                                </td>
                                            </tr>
                                        </blockTable>
                                    </td>

                                    <td></td>

                                    <td>
                                        <blockTable colWidths="50.0,50.0,50.0,50.0" rowHeights="30.0,25.0,25.0,25.0,25.0" style="Table1L">
                                            <tr>
                                                <td>
                                                    <para style="title_top_left">PLACA</para>
                                                    <para style="text_information_12">""" + (service.vehicle_id.license_plate or '') + """</para>
                                                </td>
                                                <td></td>
                                                <td>
                                                    <para style="title_top_left">OT</para>
                                                    <para style="text_information_12">""" + (service.work_order or '') + """</para>
                                                </td>
                                                <td></td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <para style="title_top_left">MARCA</para>
                                                    <para style="text_information">
                                                        """ + (tools.ustr(service.vehicle_id.model_id.modelname or '')) + """
                                                    </para>
                                                </td>
                                                <td></td>
                                                <td>
                                                    <para style="title_top_left">MODELO</para>
                                                    <para style="text_information">
                                                        """ + (tools.ustr(service.vehicle_id.model_id.brand_id.name or '')) + """
                                                    </para>
                                                </td>
                                                <td></td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <para style="title_top_left">""" + tools.ustr('AÑO') + """</para>
                                                    <para style="text_information">""" + (service.vehicle_id.model_id.year or '') + """</para>
                                                </td>
                                                <td>
                                                    <para style="title_top_left">COLOR</para>
                                                    <para style="text_information">""" + (tools.ustr(_(service.vehicle_id.color) if service.vehicle_id.color else '')) + """</para>
                                                </td>
                                                <td></td>
                                                <td>
                                                    <para style="title_top_left">KMS</para>
                                                    <para style="text_information">""" + (str(odometer.value or '')) + """</para>
                                                </td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <para style="title_top_left">No MOTOR</para>
                                                    <para style="text_information">""" + (service.vehicle_id.motor_nro or '') + """</para>
                                                </td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <para style="title_top_left">CHASIS No</para>
                                                    <para style="text_information">""" + (service.vehicle_id.body_nro or '') + """</para>
                                                </td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                            </tr>
                                        </blockTable>
                                    </td>
                                </tr>

                                <tr>
                                    <td>
                                        <blockTable colWidths="77.14,77.14,77.14,77.14,77.14,77.14,77.14" rowHeights="20.0,20.0,20.0" style="TableDetails">
                                            <tr>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">ANTENA</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.antenna else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">RADIO</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.radio else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">PLUMAS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.plumas else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">EXTINGUIDOR</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.extinguidor else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">TRIANGULOS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.triangulos else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">SEGURO AROS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.seguro_aros else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">SIGNOS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.signos else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">ENCENDEDOR</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.encendedor else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">MOQUETAS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.moquetas else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">ESPEJOS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.espejos else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <illustration width="120" height="50">
                                                        <image file="file:""" + img_oil_path + """ " x="23" y="5" width="120" height="40"/>
                                                        <fill color="#244d70"/>
                                                        <setFont name="Helvetica-Bold" size="5"/>
                                                        <drawString x="42" y="8">COMBUSTIBLE</drawString>

                                                        <fill color="red"/>
                                                        <setFont name="Helvetica-Bold" size="8"/>"""

            if service.fuel_level_0:
                rml += """                              <drawString x="23" y="12">X</drawString>"""

            #elif service.fuel_level_1_8:
            #    rml += """                              <drawString x="25" y="21">X</drawString>"""

            #elif service.fuel_level_1_4:
            #   rml += """                              <drawString x="32" y="31">X</drawString>"""

            #elif service.fuel_level_3_8:
            #    rml += """                              <drawString x="42" y="37">X</drawString>"""

            elif service.fuel_level_1_2:
                rml += """                              <drawString x="57" y="40">X</drawString>"""

            #elif service.fuel_level_5_8:
            #    rml += """                              <drawString x="73" y="37">X</drawString>"""

            #elif service.fuel_level_3_4:
            #    rml += """                              <drawString x="82" y="31">X</drawString>"""

            #elif service.fuel_level_7_8:
            #    rml += """                              <drawString x="89" y="21">X</drawString>"""

            elif service.fuel_level_1:
                rml += """                              <drawString x="92" y="12">X</drawString>"""

            rml += """                              </illustration>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">LLAVE RUEDAS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.llave_ruedas else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">COMPAC</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.compac else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">TAPACUBOS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + (str(service.tapacubos or '')) + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                            </tr>

                                            <tr>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">LLANTA</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.llanta else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">GATA</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.gata else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">HERRAMIENTAS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.herramientas else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td></td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td>
                                                                <para style="title_middle_left">
                                                                    """ + (tools.ustr(service.otros_description) if service.otros else '........') + """
                                                                </para>
                                                            </td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.otros else '') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">BOTIQUIN</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.botiquin else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                                <td>
                                                    <blockTable colWidths="58.0,17.0" rowHeights="20" style="NoneBorders">
                                                        <tr>
                                                            <td><para style="title_middle_left">TAPAGAS</para></td>
                                                            <td>
                                                                <blockTable colWidths="15.0" rowHeights="13.0" style="checkBox">
                                                                    <tr>
                                                                        <td>
                                                                            <para style="x_mark">
                                                                                """ + ('X' if service.tapagas else 'No') + """
                                                                            </para>
                                                                        </td>
                                                                    </tr>
                                                                </blockTable>
                                                            </td>
                                                        </tr>
                                                    </blockTable>
                                                </td>
                                            </tr>
                                        </blockTable>
                                    </td>

                                    <td></td>
                                    <td></td>
                                </tr>"""

            x = len(service.work_to_realize_ids)
            rowHeights = '15.0'
            max_rows = 12

            for obs in service.work_to_realize_ids:
                rowHeights += ',15.0'

            while x < max_rows:
                rowHeights += ',15.0'
                x += 1

            rml += """
                                <tr>
                                    <td>
                                        <blockTable colWidths="540.0" rowHeights=" """ + rowHeights + """ " style="AllBorders">
                                            <tr>
                                                <td>
                                                    <para style="title_top_center">DESCRIPCION DE TRABAJOS A REALIZAR</para>
                                                </td>
                                            </tr>"""

            for work in service.work_to_realize_ids:
                rml += """                  <tr>
                                                <td>
                                                    <para style="text_information3_left">""" + (tools.ustr(work.name)) + """</para>
                                                </td>
                                            </tr>"""

            x = len(service.work_to_realize_ids)
            while x < max_rows:
                x += 1
                rml += """                  <tr>
                                                <td>
                                                    <para style="text_information3_left"></para>
                                                </td>
                                            </tr>"""

            rml += """                  </blockTable>

                                        <blockTable colWidths="290.0,250.0" rowHeights="15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0" style="TablePhoto">
                                            <tr>
                                                <td>
                                                    <illustration width="200" height="140">
                                                        <image file="file:""" + img_car_path + """ " x="-30" y="5" width="200" height="140"/>
                                                        <fill color="#244d70"/>
                                                        <setFont name="Helvetica-Bold" size="6"/>
                                                        <drawString x="-10" y="-5">ROTURAS, FALTANTES, ABOLLADURAS Y RASPONES MARCADOS CON "X"</drawString>
                                                        <fill color="#244d70"/>
                                                        <setFont name="Helvetica-Bold" size="14"/>"""

            def _get_draw_string_rep(_x, _y):
                return '<drawString x="%s" y="%s">X</drawString>' % (str(_x), str(_y))

            values = service.coordinates.split(';')
            for cord in values:
                _cord = cord.split(',')
                if len(_cord) == 2:
                    x = int(float(_cord[0]) / 2) - 29 if _cord[0] else 0.0
                    if x > 100:
                        x += 5

                    y = 150 - int(float(_cord[1]) / 2) - 6
                    if y < 40:
                        y += 5

                    rml += _get_draw_string_rep(x, y)

            rml += """
                                                    </illustration>
                                                </td>
                                                <td></td>
                                            </tr>"""

            for x in range(8):
                rml += """
                                            <tr>
                                                <td></td>
                                                <td></td>
                                            </tr>"""

            rml += """
                                            <tr>
                                                <td></td>
                                                <td>
                                                    <para style="text_information">""" + """</para>
                                                </td>
                                            </tr>

                                            <tr>
                                                <td></td>
                                                <td>
                                                    <illustration width="200" height="10">
                                                        <fill color="#244d70"/>
                                                        <setFont name="Helvetica-Bold" size="6"/>
                                                        <drawString x="30" y="2">(F) CLIENTE</drawString>
                                                        <drawString x="150" y="2">C.I.</drawString>
                                                    </illustration>
                                                </td>
                                            </tr>
                                        </blockTable>
                                    </td>

                                    <td></td>
                                    <td></td>
                                </tr>

                                <tr>
                                    <td>"""

            x = len(service.observation_ids)
            rowHeights = '15.0'
            max_rows = 9

            for obs in service.observation_ids:
                rowHeights += ',15.0'

            while x < max_rows:
                rowHeights += ',15.0'
                x += 1

            rml += """
                                        <blockTable colWidths="270.0,270.0" rowHeights=" """ + rowHeights + """ " style="LastTable">
                                            <tr>
                                                <td>
                                                    <para style="title_top_center10">AUTORIZACION</para>

                                                    <para style="adv_text">""" + \
                                                        tools.ustr("1. La presente autorización expresa que: Siendo el \
                                                        propietario o actuando como representante del mismo estoy en \
                                                        condiciones de autorizar los servicios anotados, así como el \
                                                        reemplazo de las partes que fueren necesarias para la ejecución \
                                                        de dichos servicios.") + """
                                                    </para>

                                                    <para style="adv_text">""" + \
                                                        tools.ustr("2. El vehículo será retirado previo el pago de los \
                                                        servicios.") + """
                                                    </para>

                                                    <para style="adv_text">""" + \
                                                        tools.ustr("3. La demora del pago recargará intereses bancarios \
                                                        y bodegaje.") + """
                                                    </para>

                                                    <para style="adv_text">""" + \
                                                        tools.ustr("4. El taller no puede ser responsable por vicios \
                                                        ocultos.") + """
                                                    </para>

                                                    <para style="adv_text">""" + \
                                                        tools.ustr("5. El cliente autoriza que su vehículo sea probado \
                                                        en la vía pública.") + """
                                                    </para>

                                                    <para style="adv_text">""" + \
                                                        tools.ustr("6. El cliente autoriza trabajos adicionales con \
                                                        terceros.") + """
                                                    </para>

                                                    <para style="adv_text">
                                                        """ + tools.ustr("7. Cualquier reclamación relacionadas con los \
                                                        servicios prestados, solo se aceptará ser presentada dentro de \
                                                        las 48 horas de retirado el vehículo.") + """
                                                    </para>

                                                    <para style="adv_text">""" + \
                                                        tools.ustr("8. El taller no se responsabiliza por objetos \
                                                        olvidados en el vehículo.") + """
                                                    </para>

                                                    <para style="adv_text">
                                                        """ + tools.ustr("9. Los riesgos de incendio, robo y accidentes serán \
                                                        asumidos por el cliente.") + """
                                                    </para>
                                                </td>
                                                <td>
                                                    <para style="title_middle_left">OBSERVACIONES</para>
                                                </td>
                                            </tr>"""

            for obs in service.observation_ids:
                rml += """
                                            <tr>
                                                <td></td>
                                                <td>
                                                    <para style="text_information3_left" bulletText="">
                                                        """ + (tools.ustr(obs.name)) + """
                                                    </para>
                                                </td>
                                            </tr>"""

            x = len(service.observation_ids)
            while x < max_rows:
                x += 1
                rml += """
                                            <tr>
                                                <td></td>
                                                <td><para style="text_information3_left"></para></td>
                                            </tr>"""

            rml += """                  </blockTable>
                                    </td>

                                    <td></td>
                                    <td></td>
                                </tr>
                            </blockTable>"""

            rml += """  </section>"""

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

MachineReparationReport('report.machine_manager_machinery_breaking_report', 'machinery', '', '')
