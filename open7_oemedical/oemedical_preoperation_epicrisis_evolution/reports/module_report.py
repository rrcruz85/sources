# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import pooler, tools
from openerp.report.interface import report_rml
from openerp.tools.translate import _


class ModuleReport(report_rml):
    def create(self, cr, uid, ids, datas, context):
        information_obj = pooler.get_pool(cr.dbname).get('oemedical.operation_information')
        for info in information_obj.browse(cr, uid, ids, context):
            rml = """
                <document filename="test.pdf">
                    <docinit>
                        <color id="BLACK75" CMYK="[0,0,0,0.75]" spotName="BLACK" density=".75"/>
                        <color id="BLACK50" CMYK="[0,0,0,0.50]" spotName="BLACK" density=".50"/>
                        <color id="BLACK25" CMYK="[0,0,0,0.25]" spotName="BLACK" density=".25"/>
                    </docinit>

                    <template pageSize="(595.0,842.0)" title=" """ + _("Report") + """ " author="" allowSplitting="20">
                        <pageTemplate id="page1">
                            <frame id="first" x1="50.0" y1="405.0" width="498" height="410"/>
                            <frame id="two" x1="50.0" y1="370.0" width="498" height="100"/>
                            <frame id="three" x1="50.0" y1="0.0" width="498" height="400"/>
                            <frame id="four" x1="50.0" y1="0.0" width="498" height="100"/>
                        </pageTemplate>

                        <pageTemplate id="page2">
                            <frame id="section_header" x1="50.0" y1="760.0" width="498" height="60"/>
                            <frame id="section_one" x1="50.0" y1="670.0" width="498" height="90"/>
                            <frame id="section_two" x1="50.0" y1="600.0" width="498" height="90"/>
                            <frame id="section_three" x1="50.0" y1="530.0" width="498" height="90"/>
                            <frame id="section_four" x1="50.0" y1="460.0" width="498" height="90"/>
                            <frame id="section_five" x1="50.0" y1="385.0" width="498" height="100"/>
                            <frame id="section_six" x1="50.0" y1="295.0" width="498" height="100"/>
                            <frame id="section_seven" x1="50.0" y1="205.0" width="498" height="100"/>
                            <frame id="section_eight" x1="50.0" y1="115.0" width="498" height="100"/>
                            <frame id="section_nine" x1="50.0" y1="20.0" width="498" height="100"/>
                        </pageTemplate>

                        <pageTemplate id="page3">
                            <frame id="section_header" x1="50.0" y1="740.0" width="498" height="80"/>
                            <frame id="section_two" x1="29.0" y1="50.0" width="280" height="700"/>
                            <frame id="section_three" x1="300.0" y1="50.0" width="280" height="700"/>
                            <frame id="section_four" x1="430.0" y1="15.0" width="150" height="40"/>
                        </pageTemplate>
						
						<pageTemplate id="page4">
                            <frame id="section_header" x1="50.0" y1="740.0" width="498" height="80"/>
                            <frame id="section_two" x1="29.0" y1="50.0" width="280" height="700"/>
                            <frame id="section_three" x1="300.0" y1="50.0" width="280" height="700"/>
                            <frame id="section_four" x1="430.0" y1="15.0" width="150" height="40"/>
                        </pageTemplate>
						
                    </template>"""

            rml += """
                    <stylesheet>
                        <blockTableStyle id="TableLineBelow">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="LEFT"/>
                            <lineStyle kind="LINEBELOW" colorName="#3d3d3d" start="0,0" stop="0,0" thickness="0.1"/>
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

                        <blockTableStyle id="FirstTableSecondPage">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>

                            <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>

                            <blockSpan start="0,0" stop="2,0"/>
                            <blockSpan start="2,1" stop="3,1"/>
                        </blockTableStyle>

                        <blockTableStyle id="FirstTablePageThree">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockBackground colorName="gray" start="0,0" stop="5,0"/>

                            <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                        </blockTableStyle>

                        <blockTableStyle id="SecondTablePageThree">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockSpan start="0,0" stop="2,0"/>
                            <blockBackground colorName="gray" start="0,0" stop="2,0"/>

                            <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                        </blockTableStyle>

                        <blockTableStyle id="ThirdTablePageThree">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>
                            <blockSpan start="0,0" stop="1,0"/>
                            <blockBackground colorName="gray" start="0,0" stop="1,0"/>

                            <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                        </blockTableStyle>

                        <initialize>
                            <paraStyle name="all" alignment="justify"/>
                        </initialize>

                        <paraStyle name="info_label" fontName="Helvetica" fontSize="7.0" leading="9"
                                   alignment="justify" textColor="black"/>

                         <paraStyle name="info_label2" fontName="Helvetica" fontSize="7.0" leading="9"
                                   alignment="right" textColor="black"/>

                        <paraStyle name="info_label_center" fontName="Helvetica" fontSize="7.0" leading="9"
                                   alignment="center" textColor="black"/>

                        <paraStyle name="info_label_center_two" fontName="Helvetica" fontSize="5.0" leading="7"
                                   alignment="center" textColor="black"/>

                        <paraStyle name="info_label_center_two_justify" fontName="Helvetica" fontSize="5.0" leading="7"
                                   alignment="justify" textColor="black"/>

                        <paraStyle name="info_text" fontName="Courier" fontSize="8.0" leading="9"
                                   alignment="justify" textColor="black"/>

                        <paraStyle name="info_text_center" fontName="Courier" fontSize="8.0" leading="9"
                                   alignment="center" textColor="black"/>

                        <paraStyle name="info_text_para" fontName="Courier" fontSize="8.0" leading="12"
                                   alignment="justify" textColor="black"/>

                        <paraStyle name="title_center" alignment="center" textColor="black"/>
                    </stylesheet>"""

            rml += """
                    <story>"""

            rml += """
                    <para alignment="center">PROTOCOLO OPERATORIO</para>
                    <spacer length="1.0cm"/>

                    <blockTable colWidths="50.0,380.0,40.0,60.0" rowHeights="12.0" style="">
                        <tr>
                            <td>
                                <para style="info_label">Paciente:</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.patient_id.partner_id.name) + """</para>
                                <illustration height="1" width="370" align="left">
                                    <rect x="0" y = "0" width="370" height="0.1" round="0" fill="1" stroke="no"/>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Fecha:</para>
                            </td>
                            <td>
                                <para style="info_text">
                                    """ + (format_date(info.date) if info.date else '') + """
                                </para>
                                <illustration height="1" width="50" align="left">
                                    <rect x="0" y = "0" width="50" height="0.1" round="0" fill="1" stroke="no"/>
                                </illustration>
                            </td>
                        </tr>
                    </blockTable>

                    <blockTable colWidths="120.0,410.0" rowHeights="12.0" style="">
                        <tr>
                            <td>
                                <para style="info_label">Procedimiento programado:</para>
                            </td>
                            <td>
                                <para style="info_text">""" \
                                    + (tools.ustr(info.medical_procedure) if info.medical_procedure else '') + """
                                </para>
                                <illustration height="1" width="400" align="left">
                                    <rect x="0" y = "0" width="400" height="0.1" round="0" fill="1" stroke="no"/>
                                </illustration>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <spacer length="0.4cm"/>
                    <blockTable colWidths="55.0,475.0" rowHeights="12.0" style="">
                        <tr>
                            <td>
                                <para style="info_label">Dx PreQx:</para>
                            </td>
                            <td>
                                <para style="info_text">""" \
                                    + (tools.ustr(info.dx_pre_qx) if info.dx_pre_qx else '') + """
                                </para>
                                <illustration height="1" width="465" align="left">
                                    <rect x="0" y = "0" width="465" height="0.1" round="0" fill="1" stroke="no"/>
                                </illustration>
                            </td>
                        </tr>
                    </blockTable>

                    <blockTable colWidths="55.0,475.0" rowHeights="12.0" style="">
                        <tr>
                            <td>
                                <para style="info_label">Dx PostQx:</para>
                            </td>
                            <td>
                                <para style="info_text">""" \
                                    + (tools.ustr(info.dx_post_qx) if info.dx_post_qx else '') + """
                                </para>
                                <illustration height="1" width="465" align="left">
                                    <rect x="0" y = "0" width="465" height="0.1" round="0" fill="1" stroke="no"/>
                                </illustration>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <spacer length="0.4cm"/>
                    <blockTable colWidths="275.0,265.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <blockTable colWidths="50.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Cirujano:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.doctor_id.physician_id.name) if info.doctor_id else '') + """
                                            </para>
                                            <illustration height="1" width="180" align="left">
                                                <rect x="0" y = "0" width="180" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                            <td>
                                <blockTable colWidths="70.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Instrumentista:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.instrumentista.physician_id.name) if info.instrumentista else '') + """
                                            </para>
                                            <illustration height="1" width="175" align="left">
                                                <rect x="0" y = "0" width="175" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>

                    <blockTable colWidths="275.0,265.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <blockTable colWidths="80.0,220.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Primer ayudante:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.primer_ayudante.physician_id.name) if info.primer_ayudante else '') + """
                                            </para>
                                            <illustration height="1" width="150" align="left">
                                                <rect x="0" y = "0" width="150" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                            <td>
                                <blockTable colWidths="70.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Circulante:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.circulante.physician_id.name) if info.circulante else '') + """
                                            </para>
                                            <illustration height="1" width="175" align="left">
                                                <rect x="0" y = "0" width="175" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>

                    <blockTable colWidths="275.0,265.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <blockTable colWidths="85.0,220.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Segundo ayudante:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.segundo_ayudante.physician_id.name) if info.segundo_ayudante else '') + """
                                            </para>
                                            <illustration height="1" width="145" align="left">
                                                <rect x="0" y = "0" width="145" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>

                    <blockTable colWidths="275.0,265.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <blockTable colWidths="80.0,220.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">""" + tools.ustr('Anestesiólogo:') + """</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.anestesiologo.physician_id.name) if info.anestesiologo else '') + """
                                            </para>
                                            <illustration height="1" width="150" align="left">
                                                <rect x="0" y = "0" width="150" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                            <td>
                                <blockTable colWidths="80.0,230.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Tipo de anestesia:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.tipo_anestesia.name) if info.tipo_anestesia else '') + """
                                            </para>
                                            <illustration height="1" width="165" align="left">
                                                <rect x="0" y = "0" width="165" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <spacer length="0.4cm"/>
                    <blockTable colWidths="275.0,265.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <blockTable colWidths="50.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Sangrado:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.sangrado) if info.sangrado else '') + """
                                            </para>
                                            <illustration height="1" width="180" align="left">
                                                <rect x="0" y = "0" width="180" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                            <td>
                                <blockTable colWidths="70.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Diuresis:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.diuresis) if info.diuresis else '') + """
                                            </para>
                                            <illustration height="1" width="175" align="left">
                                                <rect x="0" y = "0" width="175" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>

                    <blockTable colWidths="275.0,265.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <blockTable colWidths="50.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">""" + tools.ustr('Líquidos:') + """</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.liquidos) if info.liquidos else '') + """
                                            </para>
                                            <illustration height="1" width="180" align="left">
                                                <rect x="0" y = "0" width="180" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                            <td>
                                <blockTable colWidths="70.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Complicaciones:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.complicaciones) if info.complicaciones else '') + """
                                            </para>
                                            <illustration height="1" width="175" align="left">
                                                <rect x="0" y = "0" width="175" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>

                    <blockTable colWidths="275.0,265.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <blockTable colWidths="70.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">""" + tools.ustr('Histopatológico:') + """</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.histopatologico) if info.histopatologico else '') + """
                                            </para>
                                            <illustration height="1" width="160" align="left">
                                                <rect x="0" y = "0" width="160" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                            <td>
                                <blockTable colWidths="70.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Drenes:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (tools.ustr(info.drenes) if info.drenes else '') + """
                                            </para>
                                            <illustration height="1" width="175" align="left">
                                                <rect x="0" y = "0" width="175" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <spacer length="0.2cm"/>
                    <illustration height="1" width="50" align="left">
                        <rect x="23" y = "-16" width="477" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-27" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-38" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-49" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-60" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <blockTable colWidths="530.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text_para">
                                    <font face="Helvetica" size="7">Hallazgos: </font>
                                    """ + (tools.ustr(info.hallazgos)[:515] if info.hallazgos else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <nextFrame/>
                    <para alignment="center">""" + tools.ustr('Descripción de la Operación') + """</para>
                    <spacer length="0.5cm"/>
                    <blockTable colWidths="275.0,265.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <blockTable colWidths="65.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">Hora de inicio:</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (hours_time_string(info.hora_inicio) if info.hora_inicio else '') + """
                                            </para>
                                            <illustration height="1" width="100" align="left">
                                                <rect x="0" y = "0" width="100" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                            <td>
                                <blockTable colWidths="90.0,250.0" rowHeights="12.0" style="">
                                    <tr>
                                        <td>
                                            <para style="info_label">""" + tools.ustr('Hora de finalización:') + """</para>
                                        </td>
                                        <td>
                                            <para style="info_text">""" \
                                                + (hours_time_string(info.hora_finalizacion) if info.hora_finalizacion else '') + """
                                            </para>
                                            <illustration height="1" width="154" align="left">
                                                <rect x="0" y = "0" width="154" height="0.1" round="0" fill="1" stroke="no"/>
                                            </illustration>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>

                    <illustration height="1" width="50" align="left">
                        <rect x="17" y = "-15" width="483" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-26" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <blockTable colWidths="530.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text_para">
                                    <font face="Helvetica" size="7">""" + tools.ustr('Diéresis:') + """</font>
                                    """ + (tools.ustr(info.dieresis)[:207] if info.dieresis else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>

                    <spacer length="0.1cm"/>"""

            rml += """
                    <nextFrame/>
                    <illustration height="1" width="50" align="left">
                        <rect x="40" y = "-36" width="460" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-47" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-58" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-69" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-80" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-91" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-102" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-112" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-123" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-134" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-145" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-156" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-166" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-177" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-188" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-199" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-210" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-221" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-232" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-243" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-254" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-265" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>"""

            rml += """
                    <blockTable colWidths="530.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text_para">
                                    <font face="Helvetica" size="7">""" + tools.ustr('Procedimiento:') + """</font>
                                    """ + (tools.ustr(info.procedimiento)[:2223] if info.procedimiento else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <nextFrame/>
                    <illustration height="1" width="50" align="left">
                        <rect x="17" y = "-15" width="483" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-26" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <blockTable colWidths="530.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text_para">
                                    <font face="Helvetica" size="7">""" + tools.ustr('Sintesis:') + """</font>
                                    """ + (tools.ustr(info.sintesis)[:205] if info.sintesis else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>

                    <blockTable colWidths="270.0,70.0,190.0" rowHeights="" style="">
                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Realizado por:') + """</para>
                            </td>
                            <td>
                                <para style="info_text">
                                    """ + (tools.ustr(info.realizado_por) if info.realizado_por else '') + """
                                </para>
                                <illustration height="1" width="175" align="left">
                                    <rect x="0" y = "0" width="175" height="0.1" round="0" fill="1" stroke="no"/>
                                </illustration>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <setNextTemplate name="page2"/>
                    <nextFrame/>"""

            rml += """
                    <blockTable colWidths="" rowHeights="" style="FirstTableSecondPage">
                        <tr>
                            <td><para style="title_center">EPICRISIS</para></td>
                            <td></td>
                            <td></td>
                            <td>
                                <para style="info_label">EDAD: """ \
                                    + """<font face = "Courier" size = "8">""" + str(get_year(info.patient_id)) + """ </font>
                                </para>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_label">APELLIDO PATERNO</para>
                                <para style="info_text">""" + tools.ustr(info.patient_id.last_name) + """</para>
                            </td>
                            <td>
                                <para style="info_label">MATERNO</para>
                                <para style="info_text">""" + tools.ustr(info.patient_id.slastname) + """</para>
                            </td>
                            <td>
                                <para style="info_label">NOMBRE</para>
                                <para style="info_text">""" + tools.ustr(info.patient_id.first_name) + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <nextFrame/>
                    <illustration height="1" width="50" align="left">
                        <rect x="90" y = "-15" width="410" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-26" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-37" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-48" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <blockTable colWidths="530.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text_para">
                                    <font face="Helvetica" size="7">""" + tools.ustr('DIAGNOSTICO PROVISIONAL:') + """</font>
                                    """ + (tools.ustr(info.diagnostico_provisional)[:408] if info.diagnostico_provisional else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <nextFrame/>
                    <illustration height="1" width="50" align="left">
                        <rect x="120" y = "-15" width="380" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-26" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-37" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-48" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <blockTable colWidths="530.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text_para">
                                    <font face="Helvetica" size="7">""" + tools.ustr('DIAGNOSTICO DEFINITIVO PRIMARIO:') + """</font>
                                    """ + (tools.ustr(info.diagnostico_definitivo_primario)[:395] if info.diagnostico_definitivo_primario else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <nextFrame/>
                    <illustration height="1" width="50" align="left">
                        <rect x="90" y = "-15" width="410" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-26" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-37" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-48" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <blockTable colWidths="530.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text_para">
                                    <font face="Helvetica" size="7">""" + tools.ustr('DIAGNOSTICO SECUNDARIO:') + """</font>
                                    """ + (tools.ustr(info.diagnostico_secundario)[:400] if info.diagnostico_secundario else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <nextFrame/>
                    <illustration height="1" width="50" align="left">
                        <rect x="40" y = "-15" width="460" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-26" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-37" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <illustration height="1" width="50" align="left">
                        <rect x="-16" y = "-48" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                    </illustration>

                    <blockTable colWidths="530.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text_para">
                                    <font face="Helvetica" size="7">""" + tools.ustr('OPERACIONES:') + """</font>
                                    """ + (tools.ustr(info.operaciones)[:405] if info.operaciones else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                <nextFrame/>
                <illustration height="1" width="50" align="left">
                    <rect x="225" y = "-17" width="275" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-28" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-39" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-50" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-61" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-72" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <blockTable colWidths="530.0" rowHeights="" style="">
                    <tr>
                        <td>
                            <para style="info_text_para">
                                <font face="Helvetica" size="7">""" + tools.ustr('HISTORIA BREVE Y HALLAZGOS ESPECIALES DE EXAMEN FISICO:') + """</font>
                                """ + (tools.ustr(info.historial_breve)[:582] if info.historial_breve else '') + """
                            </para>
                        </td>
                    </tr>
                </blockTable>"""

            rml += """
                <nextFrame/>
                <illustration height="1" width="50" align="left">
                    <rect x="220" y = "-17" width="280" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-28" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-39" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-50" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-61" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-72" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <blockTable colWidths="530.0" rowHeights="" style="">
                    <tr>
                        <td>
                            <para style="info_text_para">
                                <font face="Helvetica" size="7">""" + tools.ustr('HALLAZGOS DE LABORATORIO, RAYOS X E INTERCONSULTAS:') + """</font>
                                """ + (tools.ustr(info.hallasgos_laboratorio)[:582] if info.hallasgos_laboratorio else '') + """
                            </para>
                        </td>
                    </tr>
                </blockTable>"""

            rml += """
                <nextFrame/>
                <illustration height="1" width="50" align="left">
                    <rect x="155" y = "-17" width="345" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-28" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-39" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-50" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-61" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-72" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <blockTable colWidths="530.0" rowHeights="" style="">
                    <tr>
                        <td>
                            <para style="info_text_para">
                                <font face="Helvetica" size="7">""" + tools.ustr('EVOLUCION, COMPLICACIONES SI LAS HUBO:') + """</font>
                                """ + (tools.ustr(info.evolucion)[:595] if info.evolucion else '') + """
                            </para>
                        </td>
                    </tr>
                </blockTable>"""

            rml += """
                <nextFrame/>
                <illustration height="1" width="50" align="left">
                    <rect x="268" y = "-17" width="232" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-28" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-39" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-50" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-61" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <illustration height="1" width="50" align="left">
                    <rect x="-16" y = "-72" width="516" height="0.1" round="0" fill="1" stroke="no"/>
                </illustration>

                <blockTable colWidths="530.0" rowHeights="" style="">
                    <tr>
                        <td>
                            <para style="info_text_para">
                                <font face="Helvetica" size="7">""" + tools.ustr('CONDICION, TRATAMIENTO, REFERENCIA FINAL AL DAR EL ALTA Y PRONOSTICO:') + """</font>
                                """ + (tools.ustr(info.condicion_tratamiento)[:575] if info.condicion_tratamiento else '') + """
                            </para>
                        </td>
                    </tr>
                </blockTable>"""

            rml += """
                <nextFrame/>
                <blockTable colWidths="530.0" rowHeights="" style="">
                    <tr>
                        <td>
                            <para style="info_label">EN CASO DE INTERNACION</para>
                        </td>
                    </tr>
                </blockTable>

                <spacer length="0.5cm"/>
                <blockTable colWidths="120.0,80.0,330.0" rowHeights="" style="">
                    <tr>
                        <td>
                            <para style="info_label">DIAS DE HOSPITALIZACION</para>
                            <para style="info_text">
                                """ + (str(info.dias_en_hospital) if info.dias_en_hospital else ' ') + """
                            </para>
                        </td>
                        <td>
                            <para style="info_label">FECHA:</para>
                            <para style="info_text">
                                """ + (format_date(info.fecha_internacion) if info.fecha_internacion else ' ') + """
                            </para>
                        </td>
                        <td>
                            <para style="info_label">FIRMA Y NOMBRE DEL MEDICO</para>
                            <para style="info_text">
                                """ + (tools.ustr(info.medico_internacion.physician_id.name) if info.medico_internacion else ' ') + """
                            </para>
                        </td>
                    </tr>
                </blockTable>"""

            rml += """
                <setNextTemplate name="page3"/>
                <nextFrame/>"""

            company_obj = pooler.get_pool(cr.dbname).get('res.company')
            company_ids_list = company_obj.search(cr, uid, [], context=context)
            company = company_obj.browse(cr, uid, company_ids_list[0], context) if len(company_ids_list) > 0 else False

            rml += """
                <para alignment="center">ENDOSCOPIA</para>
                <spacer length="0.5cm"/>
                <blockTable colWidths="120.0,120.0,100.0,40.0,50.0,100.0" rowHeights="15.0,12.0" style="FirstTablePageThree">
                    <tr>
                        <td>
                            <para style="info_label_center">ESTABLECIMIENTO</para>
                        </td>
                        <td>
                            <para style="info_label_center">NOMBRE</para>
                        </td>
                        <td>
                            <para style="info_label_center">APELLIDO</para>
                        </td>
                        <td>
                            <para style="info_label_center">SEXO</para>
                        </td>
                        <td>
                            <para style="info_label_center">NO. HOJA</para>
                        </td>
                        <td>
                            <para style="info_label_center">NO. HISTORIA CLINICA</para>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <para style="info_text_center">""" \
                                + (tools.ustr(company.name) if company and company.name else "") + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + tools.ustr(info.patient_id.first_name or "") + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + tools.ustr(info.patient_id.last_name or "") + ' ' + tools.ustr(info.patient_id.slastname or "") + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + ('F' if info.patient_id.sex == 'f' else 'M') + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + str(1) + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + (tools.ustr(info.patient_id.identification_code) if info.patient_id.identification_code else "") + """
                            </para>
                        </td>
                    </tr>
                </blockTable>"""

            max_tr = 43
            row_heights = '15.0,17.0'

            cont = 0
            for ev in info.endoscopy_evolution_ids:
                if cont < max_tr:
                    if len(tools.ustr(ev.notes)) > 100:
                        rows = (len(tools.ustr(ev.notes)) /100 + 1)
                        cont += rows
                        row_heights += ',' + str(15.0 * rows)
                    else:
                        row_heights += ',15.0'
                        cont += 1

            while cont < max_tr:
                row_heights += ',15.0'
                cont += 1

            rml += """
                <nextFrame/>
                <blockTable colWidths="45.0,30.0,195.0" rowHeights=" """ + row_heights + """" style="SecondTablePageThree">
                    <tr>
                        <td><para style="info_label">1. EVOLUCION</para></td>
                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><para style="info_label_center_two">FECHA</para></td>
                        <td><para style="info_label_center_two">HORA</para></td>
                        <td><para style="info_label_center_two">NOTAS DE EVOLUCION</para></td>
                    </tr>"""

            cont = 0
            for ev in info.endoscopy_evolution_ids:
                if cont < max_tr:
                    if len(tools.ustr(ev.notes)) > 100:
                        rows = (len(tools.ustr(ev.notes)) / 100 + 1)
                        cont += rows
                    else:
                        cont += 1

                    rml += """
                    <tr>
                        <td>
                            <para style="info_label_center_two">
                                """ + (format_date(ev.date) if ev.date else '') + """
                            </para>
                        </td>
                        <td><para style="info_label_center_two">""" + hours_time_string(ev.time) + """</para></td>
                        <td>
                            <para style="info_label_center_two_justify">""" + (tools.ustr(ev.notes) if ev.notes else "") + """</para>
                        </td>
                    </tr>"""

            while cont < max_tr:
                cont += 1
                rml += """
                    <tr>
                        <td><para style="info_label_center_two_justify"></para></td>
                        <td><para style="info_label_center_two_justify"></para></td>
                    </tr>"""

            rml += """
                </blockTable>"""

            row_heights = '15.0,17.0'
            cont = 0
            for ev in info.endoscopy_prescription_ids:
                if cont < max_tr:
                    length1 = len(tools.ustr(ev.indication))
                    length2 = len(tools.ustr(ev.administration))
                    rows1 = length1/55 + 1
                    rows2 = length2/25 + 1
                    max_row = max(rows1,rows2)
                    if max_row > 1:
                        cont += max_row
                        row_heights += ',' + str(15.0 * max_row)
                    else:
                        row_heights += ',15.0'
                        cont += 1

            while cont < max_tr:
                row_heights += ',15.0'
                cont += 1

            rml += """
                <nextFrame/>
                <blockTable colWidths="168.0,80.0" rowHeights=" """ + row_heights + """" style="ThirdTablePageThree">
                    <tr>
                        <td><para style="info_label">2. PRESCRIPCIONES</para></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>
                            <para style="info_label_center_two">
                                FARMACOTERAPIA E INDICACIONES PARA ENFERMERIA Y OTRO PERSONAL
                            </para>
                        </td>
                        <td>
                            <para style="info_label_center_two">ADMINISTRACION</para>
                        </td>
                    </tr>"""

            cont = 0
            for ind in info.endoscopy_prescription_ids:
                if cont < max_tr:
                    length1 = len(tools.ustr(ind.indication))
                    length2 = len(tools.ustr(ind.administration))
                    rows1 = length1 / 55 + 1
                    rows2 = length2 / 25 + 1
                    max_row = max(rows1, rows2)
                    if max_row > 1:
                        cont += max_row
                    else:
                        cont += 1

                    ind_str = tools.ustr(ind.indication) or ''
                    if rows1 > 1:
                        lst = list(ind_str)
                        counter = 1
                        pos_inserted = 0
                        while counter <= rows1 - 1:
                            lst.insert(54 * counter + pos_inserted, '\n')
                            pos_inserted += 1
                            counter += 1
                        ind_str = "".join(lst)

                    admin = tools.ustr(ind.administration) or ''
                    if rows2 > 1:
                        lst = list(admin)
                        counter = 1
                        pos_inserted = 0
                        while counter <= rows2 - 1:
                            lst.insert(24 * counter + pos_inserted, '\n')
                            pos_inserted += 1
                            counter += 1
                        admin = "".join(lst)

                    rml += """
                    <tr>
                        <td>
                            <para style="info_label_center_two_justify">
                                """ + ind_str + """
                            </para>
                        </td>
                        <td>
                            <para style="info_label_center_two_justify">
                                """ + admin + """
                            </para>
                        </td>
                    </tr>"""

            while cont < max_tr:
                cont += 1
                rml += """
                    <tr>
                        <td><para style="info_label_center_two_justify"></para></td>
                        <td><para style="info_label_center_two_justify"></para></td>
                    </tr>"""

            rml += """
                </blockTable>"""

            rml += """
                <nextFrame/>
                <para style="info_label2">ENDOSCOPIA(1)</para>
                """

            rml += """
                <setNextTemplate name="page4"/>
                <nextFrame/>"""

            rml += """
                <para alignment="center">EVOLUCION</para>
                <spacer length="0.5cm"/>
                <blockTable colWidths="120.0,120.0,100.0,40.0,50.0,100.0" rowHeights="15.0,12.0" style="FirstTablePageThree">
                    <tr>
                        <td>
                            <para style="info_label_center">ESTABLECIMIENTO</para>
                        </td>
                        <td>
                            <para style="info_label_center">NOMBRE</para>
                        </td>
                        <td>
                            <para style="info_label_center">APELLIDO</para>
                        </td>
                        <td>
                            <para style="info_label_center">SEXO</para>
                        </td>
                        <td>
                            <para style="info_label_center">NO. HOJA</para>
                        </td>
                        <td>
                            <para style="info_label_center">NO. HISTORIA CLINICA</para>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <para style="info_text_center">""" \
                                    + (tools.ustr(company.name) if company and company.name else "") + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + tools.ustr(info.patient_id.first_name) + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + tools.ustr(info.patient_id.last_name) + ' ' + tools.ustr(info.patient_id.slastname) + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + ('F' if info.patient_id.sex == 'f' else 'M') + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + str(1) + """
                            </para>
                        </td>
                        <td>
                            <para style="info_text_center">
                                """ + (tools.ustr(info.patient_id.identification_code) if info.patient_id.identification_code else "") + """
                            </para>
                        </td>
                    </tr>
                </blockTable>"""

            max_tr = 43
            row_heights = '15.0,17.0'
            cont = 0
            for ev in info.evolution_ids:
                if cont < max_tr:
                    if len(tools.ustr(ev.notes)) > 100:
                        rows = (len(tools.ustr(ev.notes)) / 100 + 1)
                        cont += rows
                        row_heights += ',' + str(15.0 * rows)
                    else:
                        row_heights += ',15.0'
                        cont += 1

            while cont < max_tr:
                row_heights += ',15.0'
                cont += 1

            rml += """
                <nextFrame/>
                <blockTable colWidths="45.0,30.0,195.0" rowHeights=" """ + row_heights + """" style="SecondTablePageThree">
                    <tr>
                        <td><para style="info_label">1. EVOLUCION</para></td>
                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><para style="info_label_center_two">FECHA</para></td>
                        <td><para style="info_label_center_two">HORA</para></td>
                        <td><para style="info_label_center_two">NOTAS DE EVOLUCION</para></td>
                    </tr>"""

            cont = 0
            for ev in info.evolution_ids:
                if cont < max_tr:
                    if len(tools.ustr(ev.notes)) > 100:
                        rows = (len(tools.ustr(ev.notes)) / 100 + 1)
                        cont += rows
                    else:
                        cont += 1
                    rml += """
                    <tr>
                        <td>
                            <para style="info_label_center_two">
                                """ + (format_date(ev.date) if ev.date else '') + """
                            </para>
                        </td>
                        <td><para style="info_label_center_two">""" + hours_time_string(ev.time) + """</para></td>
                        <td>
                            <para style="info_label_center_two_justify">""" + tools.ustr(ev.notes) + """</para>
                        </td>
                    </tr>"""

            while cont < max_tr:
                cont += 1
                rml += """
                    <tr>
                        <td><para style="info_label_center_two_justify"></para></td>
                        <td><para style="info_label_center_two_justify"></para></td>
                    </tr>"""

            rml += """
                </blockTable>"""

            row_heights = '15.0,17.0'

            cont = 0
            for ev in info.prescription_ids:
                if cont < max_tr:
                    length1 = len(tools.ustr(ev.indication))
                    length2 = len(tools.ustr(ev.administration))
                    rows1 = length1 / 55 + 1
                    rows2 = length2 / 25 + 1
                    max_row = max(rows1, rows2)
                    if max_row > 1:
                        cont += max_row
                        row_heights += ',' + str(15.0 * max_row)
                    else:
                        row_heights += ',15.0'
                        cont += 1

            while cont < max_tr:
                row_heights += ',15.0'
                cont += 1

            rml += """
                <nextFrame/>
                <blockTable colWidths="168.0,80.0" rowHeights=" """ + row_heights + """" style="ThirdTablePageThree">
                    <tr>
                        <td><para style="info_label">2. PRESCRIPCIONES</para></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>
                            <para style="info_label_center_two">
                                FARMACOTERAPIA E INDICACIONES PARA ENFERMERIA Y OTRO PERSONAL
                            </para>
                        </td>
                        <td>
                            <para style="info_label_center_two">ADMINISTRACION</para>
                        </td>
                    </tr>"""

            cont = 0
            for ind in info.prescription_ids:
                if cont < max_tr:
                    length1 = len(tools.ustr(ind.indication))
                    length2 = len(tools.ustr(ind.administration))
                    rows1 = length1 / 55 + 1
                    rows2 = length2 / 25 + 1
                    max_row = max(rows1, rows2)
                    if max_row > 1:
                        cont += max_row
                    else:
                        cont += 1

                    ind_str = tools.ustr(ind.indication) or ''
                    if rows1 > 1:
                        lst = list(ind_str)
                        counter = 1
                        pos_inserted = 0
                        while counter <= rows1 - 1:
                            lst.insert(54 * counter + pos_inserted, '\n')
                            pos_inserted += 1
                            counter += 1
                        ind_str = "".join(lst)

                    admin = tools.ustr(ind.administration) or ''
                    if rows2 > 1:
                        lst = list(admin)
                        counter = 1
                        pos_inserted = 0
                        while counter <= rows2 - 1:
                            lst.insert(24 * counter + pos_inserted, '\n')
                            pos_inserted += 1
                            counter += 1
                        admin = "".join(lst)

                    rml += """
                    <tr>
                        <td>
                            <para style="info_label_center_two_justify">
                                """ + ind_str + """
                            </para>
                        </td>
                        <td>
                            <para style="info_label_center_two_justify">
                                """ + admin + """
                            </para>
                        </td>
                    </tr>"""

            while cont < max_tr:
                cont += 1
                rml += """
                    <tr>
                        <td><para style="info_label_center_two_justify"></para></td>
                        <td><para style="info_label_center_two_justify"></para></td>
                    </tr>"""

            rml += """
                </blockTable>"""

            rml += """
                <nextFrame/>
                <para style="info_label">EVOLUCION Y PRESCRIPCIONES (1)</para>
                """

            rml += """
                    </story>
                </document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        return pdf, report_type

ModuleReport('report.operation_information_report', 'oemedical.operation_information', '', '')


def hours_time_string(hours):
    minutes = int(round(hours * 60))
    return "%02d:%02d" % divmod(minutes, 60)


def get_year(record):
    if record.dob:
        now = datetime.now()
        dob = datetime.strptime(str(record.dob), '%Y-%m-%d')
        delta = relativedelta(now, dob)
        return delta.years


def format_date(str_date):
    temp = str_date.split('-')
    return temp[2] + '/' + temp[1] + '/' + temp[0]