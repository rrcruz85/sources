# -*- coding: utf-8 -*-

from openerp import pooler, tools
from openerp.report.interface import report_rml
from openerp.tools.translate import _


class ModuleReport(report_rml):
    def create(self, cr, uid, ids, datas, context):
        information_obj = pooler.get_pool(cr.dbname).get('oemedical.question_model')

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
                            <frame id="first" x1="50.0" y1="15.0" width="498" height="780"/>
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

                        <blockTableStyle id="Table1">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>

                            <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>

                            <blockSpan start="0,0" stop="0,4"/>
                            <blockSpan start="2,0" stop="3,0"/>
                            <blockSpan start="4,0" stop="5,0"/>
                            <blockSpan start="6,0" stop="7,0"/>
                            <blockSpan start="8,0" stop="9,0"/>

                            <blockSpan start="2,2" stop="3,2"/>
                            <blockSpan start="2,3" stop="3,3"/>
                            <blockSpan start="2,4" stop="3,4"/>

                            <blockSpan start="4,2" stop="5,2"/>
                            <blockSpan start="4,3" stop="5,3"/>
                            <blockSpan start="4,4" stop="5,4"/>

                            <blockSpan start="6,2" stop="7,2"/>
                            <blockSpan start="6,3" stop="7,3"/>
                            <blockSpan start="6,4" stop="7,4"/>

                            <blockSpan start="8,2" stop="9,2"/>
                            <blockSpan start="8,3" stop="9,3"/>
                            <blockSpan start="8,4" stop="9,4"/>
                        </blockTableStyle>

                        <blockTableStyle id="Table2">
                            <blockValign value="MIDDLE"/>
                            <blockAlignment value="CENTER"/>

                            <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                            <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>

                            <blockSpan start="0,0" stop="0,5"/>
                            <blockSpan start="2,0" stop="3,0"/>
                            <blockSpan start="4,0" stop="5,0"/>
                            <blockSpan start="6,0" stop="7,0"/>
                            <blockSpan start="8,0" stop="9,0"/>

                            <blockSpan start="2,2" stop="3,2"/>
                            <blockSpan start="2,3" stop="3,3"/>
                            <blockSpan start="2,4" stop="3,4"/>
                            <blockSpan start="2,5" stop="3,5"/>

                            <blockSpan start="4,2" stop="5,2"/>
                            <blockSpan start="4,3" stop="5,3"/>
                            <blockSpan start="4,4" stop="5,4"/>
                            <blockSpan start="4,5" stop="5,5"/>

                            <blockSpan start="6,2" stop="7,2"/>
                            <blockSpan start="6,3" stop="7,3"/>
                            <blockSpan start="6,4" stop="7,4"/>
                            <blockSpan start="6,5" stop="7,5"/>

                            <blockSpan start="8,2" stop="9,2"/>
                            <blockSpan start="8,3" stop="9,3"/>
                            <blockSpan start="8,4" stop="9,4"/>
                            <blockSpan start="8,5" stop="9,5"/>
                        </blockTableStyle>

                        <initialize>
                            <paraStyle name="all" alignment="justify"/>
                        </initialize>

                        <paraStyle name="info_label" fontName="Helvetica" fontSize="7.0" leading="9"
                                   alignment="justify" textColor="black"/>

                        <paraStyle name="info_text" fontName="Courier" fontSize="7.0" leading="9"
                                   alignment="justify" textColor="black"/>
                    </stylesheet>"""

            rml += """
                    <story>"""

            rml += """
                    <blockTable colWidths="50.0,480.0" rowHeights="12.0" style="AllBorders">
                        <tr>
                            <td>
                                <para style="info_label">Paciente:</para>
                            </td>
                            <td>
                                <para style="info_text">""" \
                                    + tools.ustr(info.patient_id.first_name + ' ' + info.patient_id.last_name + ' ' + info.patient_id.slastname) + """
                                </para>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_label">Fecha:</para>
                            </td>
                            <td>
                                <para style="info_text">
                                    """ + (format_date(info.date) if info.date else '') + """
                                </para>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <blockTable colWidths="50.0,96.0,54.0,54.0,48.0,48.0,45.0,45.0,45.0,45.0" rowHeights="12.0,12.0,17.0,17.0,17.0" style="Table1">
                        <tr>
                            <td>
                                <illustration width="20" height="50">
                                    <rotate degrees="90"/>
                                    <fill color="black"/>
                                    <setFont name="Helvetica" size="7"/>
                                    <drawString x="-75" y="-10">
                                        Preoperatorio
                                    </drawString>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Preguntas:</para>
                            </td>
                            <td>
                                <para style="info_label">Hipertension Arterial (HTA)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Diabetes Melitus (DM)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Dislipidemias</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Higado Graso</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.dislipidemias else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.dislipidemias else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.higado_graso else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.higado_graso else '') + """</para></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Medicación') + """</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.hipertension_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.diabetes_melitus_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dislipidemias_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.higado_graso_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Dosis</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.hipertension_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.diabetes_melitus_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dislipidemias_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.higado_graso_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.hipertension_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.diabetes_melitus_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dislipidemias_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.higado_graso_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <blockTable colWidths="50.0,96.0,54.0,54.0,48.0,48.0,45.0,45.0,45.0,45.0" rowHeights="12.0,12.0,17.0,17.0,17.0,17.0" style="Table2">
                        <tr>
                            <td>
                                <illustration width="20" height="50">
                                    <rotate degrees="90"/>
                                    <fill color="black"/>
                                    <setFont name="Helvetica" size="7"/>
                                    <drawString x="-90" y="-10">
                                        1er Mes Posoperatorio
                                    </drawString>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Preguntas:</para>
                            </td>
                            <td>
                                <para style="info_label">Hipertension Arterial (HTA)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Diabetes Melitus (DM)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Dislipidemias</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Higado Graso</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.primer_mes_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.primer_mes_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.primer_mes_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.primer_mes_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.primer_mes_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.primer_mes_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.primer_mes_higado_graso else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.primer_mes_higado_graso else '') + """</para></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Medicación') + """</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_hipertension_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_diabetes_melitus_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_dislipidemias_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_higado_graso_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Dosis</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_hipertension_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_diabetes_melitus_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_dislipidemias_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_higado_graso_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_hipertension_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_diabetes_melitus_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_dislipidemias_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_higado_graso_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_hipertension_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_diabetes_melitus_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_dislipidemias_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_mes_higado_graso_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <blockTable colWidths="50.0,96.0,54.0,54.0,48.0,48.0,45.0,45.0,45.0,45.0" rowHeights="12.0,12.0,17.0,17.0,17.0,17.0" style="Table2">
                        <tr>
                            <td>
                                <illustration width="20" height="50">
                                    <rotate degrees="90"/>
                                    <fill color="black"/>
                                    <setFont name="Helvetica" size="7"/>
                                    <drawString x="-90" y="-10">
                                        3er Mes Posoperatorio
                                    </drawString>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Preguntas:</para>
                            </td>
                            <td>
                                <para style="info_label">Hipertension Arterial (HTA)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Diabetes Melitus (DM)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Dislipidemias</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Higado Graso</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.tercer_mes_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.tercer_mes_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.tercer_mes_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.tercer_mes_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.tercer_mes_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.tercer_mes_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.tercer_mes_higado_graso else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.tercer_mes_higado_graso else '') + """</para></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Medicación') + """</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_hipertension_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_diabetes_melitus_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_dislipidemias_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_higado_graso_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Dosis</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_hipertension_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_diabetes_melitus_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_dislipidemias_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_higado_graso_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_hipertension_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_diabetes_melitus_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_dislipidemias_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_higado_graso_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_hipertension_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_diabetes_melitus_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_dislipidemias_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.tercer_mes_higado_graso_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <blockTable colWidths="50.0,96.0,54.0,54.0,48.0,48.0,45.0,45.0,45.0,45.0" rowHeights="12.0,12.0,17.0,17.0,17.0,17.0" style="Table2">
                        <tr>
                            <td>
                                <illustration width="20" height="50">
                                    <rotate degrees="90"/>
                                    <fill color="black"/>
                                    <setFont name="Helvetica" size="7"/>
                                    <drawString x="-90" y="-10">
                                        6to Mes Posoperatorio
                                    </drawString>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Preguntas:</para>
                            </td>
                            <td>
                                <para style="info_label">Hipertension Arterial (HTA)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Diabetes Melitus (DM)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Dislipidemias</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Higado Graso</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.sexto_mes_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.sexto_mes_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.sexto_mes_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.sexto_mes_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.sexto_mes_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.sexto_mes_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.sexto_mes_higado_graso else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.sexto_mes_higado_graso else '') + """</para></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Medicación') + """</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_hipertension_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_diabetes_melitus_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_dislipidemias_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_higado_graso_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Dosis</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_hipertension_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_diabetes_melitus_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_dislipidemias_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_higado_graso_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_hipertension_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_diabetes_melitus_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_dislipidemias_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_higado_graso_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_hipertension_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_diabetes_melitus_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_dislipidemias_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.sexto_mes_higado_graso_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <blockTable colWidths="50.0,96.0,54.0,54.0,48.0,48.0,45.0,45.0,45.0,45.0" rowHeights="12.0,12.0,17.0,17.0,17.0,17.0" style="Table2">
                        <tr>
                            <td>
                                <illustration width="20" height="50">
                                    <rotate degrees="90"/>
                                    <fill color="black"/>
                                    <setFont name="Helvetica" size="7"/>
                                    <drawString x="-90" y="-10">
                                        9no Mes Posoperatorio
                                    </drawString>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Preguntas:</para>
                            </td>
                            <td>
                                <para style="info_label">Hipertension Arterial (HTA)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Diabetes Melitus (DM)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Dislipidemias</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Higado Graso</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.noveno_mes_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.noveno_mes_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.noveno_mes_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.noveno_mes_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.noveno_mes_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.noveno_mes_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.noveno_mes_higado_graso else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.noveno_mes_higado_graso else '') + """</para></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Medicación') + """</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_hipertension_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_diabetes_melitus_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_dislipidemias_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_higado_graso_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Dosis</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_hipertension_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_diabetes_melitus_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_dislipidemias_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_higado_graso_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_hipertension_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_diabetes_melitus_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_dislipidemias_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_higado_graso_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_hipertension_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_diabetes_melitus_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_dislipidemias_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.noveno_mes_higado_graso_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <blockTable colWidths="50.0,96.0,54.0,54.0,48.0,48.0,45.0,45.0,45.0,45.0" rowHeights="12.0,12.0,17.0,17.0,17.0,17.0" style="Table2">
                        <tr>
                            <td>
                                <illustration width="20" height="50">
                                    <rotate degrees="90"/>
                                    <fill color="black"/>
                                    <setFont name="Helvetica" size="7"/>
                                    <drawString x="-90" y="-10">
                                        """ + tools.ustr('1 Año Posoperatorio') + """
                                    </drawString>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Preguntas:</para>
                            </td>
                            <td>
                                <para style="info_label">Hipertension Arterial (HTA)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Diabetes Melitus (DM)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Dislipidemias</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Higado Graso</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.primer_anno_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.primer_anno_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.primer_anno_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.primer_anno_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.primer_anno_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.primer_anno_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.primer_anno_higado_graso else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.primer_anno_higado_graso else '') + """</para></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Medicación') + """</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_hipertension_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_diabetes_melitus_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_dislipidemias_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_higado_graso_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Dosis</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_hipertension_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_diabetes_melitus_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_dislipidemias_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_higado_graso_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_hipertension_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_diabetes_melitus_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_dislipidemias_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_higado_graso_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_hipertension_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_diabetes_melitus_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_dislipidemias_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.primer_anno_higado_graso_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <blockTable colWidths="50.0,96.0,54.0,54.0,48.0,48.0,45.0,45.0,45.0,45.0" rowHeights="12.0,12.0,17.0,17.0,17.0,17.0" style="Table2">
                        <tr>
                            <td>
                                <illustration width="20" height="50">
                                    <rotate degrees="90"/>
                                    <fill color="black"/>
                                    <setFont name="Helvetica" size="7"/>
                                    <drawString x="-98" y="-10">
                                        """ + tools.ustr('1 Año y Medio Posoperatorio') + """
                                    </drawString>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Preguntas:</para>
                            </td>
                            <td>
                                <para style="info_label">Hipertension Arterial (HTA)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Diabetes Melitus (DM)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Dislipidemias</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Higado Graso</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.anno_medio_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.anno_medio_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.anno_medio_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.anno_medio_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.anno_medio_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.anno_medio_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.anno_medio_higado_graso else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.anno_medio_higado_graso else '') + """</para></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Medicación') + """</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_hipertension_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_diabetes_melitus_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_dislipidemias_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_higado_graso_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Dosis</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_hipertension_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_diabetes_melitus_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_dislipidemias_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_higado_graso_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_hipertension_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_diabetes_melitus_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_dislipidemias_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_higado_graso_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_hipertension_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_diabetes_melitus_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_dislipidemias_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.anno_medio_higado_graso_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    <blockTable colWidths="50.0,96.0,54.0,54.0,48.0,48.0,45.0,45.0,45.0,45.0" rowHeights="12.0,12.0,17.0,17.0,17.0,17.0" style="Table2">
                        <tr>
                            <td>
                                <illustration width="20" height="50">
                                    <rotate degrees="90"/>
                                    <fill color="black"/>
                                    <setFont name="Helvetica" size="7"/>
                                    <drawString x="-90" y="-10">
                                        """ + tools.ustr('2 Años Posoperatorio') + """
                                    </drawString>
                                </illustration>
                            </td>
                            <td>
                                <para style="info_label">Preguntas:</para>
                            </td>
                            <td>
                                <para style="info_label">Hipertension Arterial (HTA)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Diabetes Melitus (DM)</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Dislipidemias</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_label">Higado Graso</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.dos_annos_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.dos_annos_hipertension_arterial_hta else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.dos_annos_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.dos_annos_diabetes_melitus_dm else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.dos_annos_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.dos_annos_dislipidemias else '') + """</para></td>
                            <td><para style="info_label">SI""" + ('<u> X </u>' if info.dos_annos_higado_graso else '') + """</para></td>
                            <td><para style="info_label">NO""" + ('<u> X </u>' if not info.dos_annos_higado_graso else '') + """</para></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">""" + tools.ustr('Medicación') + """</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_hipertension_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_diabetes_melitus_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_dislipidemias_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_higado_graso_medication or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Dosis</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_hipertension_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_diabetes_melitus_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_dislipidemias_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_higado_graso_dosis or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_hipertension_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_diabetes_melitus_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_dislipidemias_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_higado_graso_values or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td>
                                <para style="info_label">Valores de Laboratorio</para>
                            </td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_hipertension_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_diabetes_melitus_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_dislipidemias_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                            <td>
                                <para style="info_text">""" + tools.ustr(info.dos_annos_higado_graso_evolution or '')[0:40] + """</para>
                            </td>
                            <td></td>
                        </tr>
                    </blockTable>"""

            rml += """
                    </story>
                </document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        return pdf, report_type
ModuleReport('report.module_report', 'oemedical.question_model', '', '')


def format_date(str_date):
    temp = str_date.split('-')
    return temp[2] + '/' + temp[1] + '/' + temp[0]
