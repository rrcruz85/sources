# -*- coding: utf-8 -*-

import os

from openerp import pooler, addons
from openerp.modules.module import get_module_path
from openerp.report.interface import report_rml
from openerp.tools import ustr
from openerp.tools.translate import _


class TestOrderReport(report_rml):
    def create(self, cr, uid, ids, datas, context):
        test_order_obj = pooler.get_pool(cr.dbname).get('oemedical.test_order')
        test_order = test_order_obj.browse(cr, uid, datas['test_order_id'], context)

        path = get_module_path('oemedical_test_order')
        path += '/static/src/img/'
        path = os.path.normpath(path)

        img_path_mail = os.path.join(path, 'mail.png')
        img_path_face = os.path.join(path, 'face.png')
        img_path_cell = os.path.join(path, 'cell.png')
        img_path_house = os.path.join(path, 'home.png')
        img_path_world = os.path.join(path, 'world.png')

        temp = test_order.date.split('-')
        date = temp[2] + '/' + temp[1] + '/' + temp[0]

        rml_header = """
                <blockTable colWidths="180.0,80.0,300.0" rowHeights="" style="FirstTable">
                    <tr>
                        <td>
                            <illustration height="80" width="80" align="left">
                                <fill color="grey"/>
                                <rect x="-15" y = "0" width="60" height="60" round="0" fill="1" stroke="No"/>
                                <fill color="#448DDB"/>
                                <rect x="45" y = "0" width="60" height="60" round="0" fill="1" stroke="No"/>
                                <fill color="#FFFFFF"/>
                                <drawString x="50" y="25">Dr.</drawString>
                                <drawString x="50" y="15">""" + ustr('Napoleón') + """</drawString>
                                <drawString x="50" y="5">Salgado</drawString>
                            </illustration>
                        </td>
                        <td></td>
                        <td>
                            <para style="title_blue"><i>Pedidos de examen</i></para>
                        </td>
                    </tr>

                    <tr>
                        <td></td><td></td><td></td>
                    </tr>

                    <tr>
                        <td></td>
                        <td></td>
                        <td>
                            <para style="title_grey">
                                <i>_title_</i>
                            </para>
                        </td>
                    </tr>

                    <tr>
                        <td></td>
                        <td></td>
                        <td>
                            <illustration height="1" width="200" align="center">
                                <fill color="grey"/>
                                <rect x="32" y = "0" width="400" height="1" round="0" fill="1" stroke="No"/>
                            </illustration>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <blockTable colWidths="" rowHeights="" style="">
                                <tr>
                                    <td>
                                        <para style="title_black">Fecha: <u>""" + date + """</u></para>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <para style="title_black">
                                            Nombre del paciente: <u>""" + ustr(test_order.patient_id.partner_id.name) + """</u>
                                        </para>
                                    </td>
                                </tr>
                            </blockTable>
                        </td>
                        <td></td>
                        <td>
                            <blockTable colWidths="280.0,20.0" rowHeights="" style="">
                                <tr>
                                    <td>
                                        <para style="subtitle_grey">
                                            """ + ustr('Av. Mariana de Jesús OE7 – 02 y Nuño de Valderrama') + """
                                            Edificio CITIMED, piso 5, consultorio 561
                                        </para>
                                    </td>
                                    <td>
                                        <illustration width="10" height="10">
                                            <image file="file:""" + img_path_house + """ " x="0" y="2" width="12" height="12"/>
                                        </illustration>
                                    </td>
                                </tr>

                                <tr>
                                    <td>
                                        <para style="subtitle_grey">
                                            """ + ustr('(02) 600 4510 / 099 452 7198') + """
                                        </para>
                                    </td>
                                    <td>
                                        <illustration width="10" height="10">
                                            <image file="file:""" + img_path_cell + """ " x="0" y="-2" width="12" height="12"/>
                                        </illustration>
                                    </td>
                                </tr>

                                <tr>
                                    <td>
                                        <para style="subtitle_grey">
                                            """ + ustr('info@napoleonsalgado.com / admin@napoleonsalgado.com') + """
                                        </para>
                                    </td>
                                    <td>
                                        <illustration width="10" height="10">
                                            <image file="file:""" + img_path_mail + """ " x="0" y="-2" width="12"
                                                   height="12"/>
                                        </illustration>
                                    </td>
                                </tr>

                                <tr>
                                    <td>
                                        <para style="subtitle_grey">
                                            """ + ustr('DrNapoleonSalgadoMacias') + """
                                        </para>
                                    </td>
                                    <td>
                                        <illustration width="10" height="10">
                                            <image file="file:""" + img_path_face + """ " x="0" y="-2" width="12" height="12"/>
                                        </illustration>
                                    </td>
                                </tr>

                                <tr>
                                    <td>
                                        <para style="subtitle_grey">
                                            """ + ustr('www.napoleonsalgado.com') + """
                                        </para>
                                    </td>
                                    <td>
                                        <illustration width="10" height="10">
                                            <image file="file:""" + img_path_world + """ " x="0" y="-2" width="12" height="12"/>
                                        </illustration>
                                    </td>
                                </tr>
                            </blockTable>
                        </td>
                    </tr>
                </blockTable>

                <blockTable colWidths="560.0" rowHeights="" style="">
                    <tr>
                        <td>
                            <para style="subtitle_blue">
                                """ + ustr('Señores ECUAMERICAN, Av. América y Rumipamba (Frente al Colegio San Gabriel)') + """
                            </para>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <para style="subtitle_blue_bold">
                                """ + ustr('Favor realizar los siguientes exámenes en ayunas:') + """
                            </para>
                        </td>
                    </tr>
                </blockTable>

                <illustration height="3" width="700" align="center">
                    <fill color="#448DDB"/>
                    <rect x="-100" y = "-12" width="700" height="3" round="0" fill="1" stroke="no"/>
                </illustration>"""

        rml_footer = """
                <illustration height="3" width="700" align="center">
                    <fill color="grey"/>
                    <rect x="-100" y = "0" width="700" height="1" round="0" fill="1" stroke="no"/>
                </illustration>

                <blockTable colWidths="560.0" rowHeights="" style="">
                    <tr>
                        <td>
                            <para style="footer_black">
                                """ + ustr('Favor enviar los exámenes a los siguientes e-mails:') + """
                            </para>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <para style="footer_blue">
                                """ + ustr('nutricion@napoleonsalgado.com / napoleon@napoleonsalgado.com / psicologia@napoleonsalgado.com') + """
                            </para>
                        </td>
                    </tr>
                </blockTable>

                <para style="footer_footer">Atentamente, </para>
                <para style="footer_footer">""" + ustr('Dr. Napoleón Salgado M.') + """</para>
                <para style="footer_footer">""" + ustr('Cirujano General y Bariátrico') + """</para>
                <para style="footer_footer">""" + ustr('Libro 2 "U" Folio 49 #150') + """</para>
                """

        rml = """
            <document filename="test.pdf">
                <template pageSize="(595.0,842.0)" title=" """ + _("Test Order") + """ " author="" allowSplitting="20">
                    <pageTemplate id="page1">
                        <frame id="first" x1="40.0" y1="570.0" width="498" height="290"/>
                        <frame id="second" x1="48.0" y1="95.0" width="498" height="545"/>
                        <frame id="third" x1="40.0" y1="0.0" width="498" height="90"/>
                    </pageTemplate>
                </template>"""

        rml += """
                <stylesheet>
                    <blockTableStyle id="FirstTable">
                        <blockValign value="BOTTOM"/>
                        <blockSpan start="0,0" stop="0,3"/>
                        <blockSpan start="0,4" stop="1,4"/>
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

                    <blockTableStyle id="checkBox">
                        <blockValign value="MIDDLE"/>
                        <blockAlignment value="CENTER"/>
                        <lineStyle kind="LINEBEFORE" colorName="grey" start="0,0" stop="0,0" thickness="0.1"/>
                        <lineStyle kind="LINEAFTER" colorName="grey" start="0,0" stop="0,0" thickness="0.1"/>
                        <lineStyle kind="LINEABOVE" colorName="grey" start="0,0" stop="0,0" thickness="0.1"/>
                        <lineStyle kind="LINEBELOW" colorName="grey" start="0,0" stop="0,0" thickness="0.1"/>
                    </blockTableStyle>

                    <initialize>
                        <paraStyle name="all" alignment="justify"/>
                    </initialize>

                    <paraStyle name="title_blue" fontName="Helvetica-Oblique" fontSize="22.0" leading="0"
                               alignment="RIGHT" textColor="#448DDB"/>

                    <paraStyle name="subtitle_blue" fontName="Helvetica" fontSize="8.0" alignment="LEFT"
                               textColor="#448DDB" leftIndent="6" leading="5"/>

                    <paraStyle name="subtitle_blue_bold" fontName="Helvetica-Bold" fontSize="8.0" alignment="LEFT"
                               textColor="#448DDB" leftIndent="6" leading="0"/>

                    <paraStyle name="title_grey" fontName="Helvetica-Oblique" fontSize="10.0" leading="0"
                               alignment="RIGHT" textColor="grey"/>

                    <paraStyle name="subtitle_grey" fontName="Helvetica" fontSize="7.0" alignment="RIGHT"
                               textColor="grey" leading="8"/>

                    <paraStyle name="title_black" fontName="Helvetica-Bold" fontSize="8.0" leading="10"
                               alignment="left" textColor="black"/>

                    <paraStyle name="info_text" fontName="Helvetica" fontSize="8.0" leading="10"
                               alignment="justify" textColor="black"/>

                    <paraStyle name="footer_black" fontName="Helvetica-Bold" fontSize="8.0" leading="6"
                               alignment="left" textColor="black"/>

                    <paraStyle name="footer_blue" fontName="Helvetica" fontSize="8.0" leading="15"
                               alignment="left" textColor="#448DDB"/>

                    <paraStyle name="footer_footer" fontName="Helvetica" fontSize="8.0" leading="10"
                               alignment="center" textColor="black"/>

                    <paraStyle name="label_px" fontName="Helvetica" fontSize="8.0" leading="10" alignment="RIGHT"
                               textColor="grey"/>

                    <paraStyle name="px" fontName="Helvetica" fontSize="10.0" leading="13" alignment="LEFT"
                               textColor="grey"/>
                </stylesheet>"""

        rml += """
                <story>"""

        if datas.get('preoperatorio', False):
            # PAGE ONE...
            # SECTION ONE
            rml_header = rml_header.replace('_title_', ustr('EXÁMENES PREOPERATORIOS (ANTES DE CIRUGÍA)'))
            rml += "<section>" + rml_header + "</section>" + "<nextFrame/>"

            # SECTION TWO
            rml += """
                    <section>
                    <blockTable colWidths="540.0,20.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Biometría hemática') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_biometria_hematica else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Plaquetas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_plaquetas else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Globulos blancos') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_globulos_blancos else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Linfocitos') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_linfocitos else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Hematocritos') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_hematocritos else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Hemoglobina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_hemoglobina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Urea') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_urea else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Creatinina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_creatinina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Glucosa (añadir hemoglobina glicosilada en caso de diabetes)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_glucosa else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('TP TTP INR') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_tp_ttp_inr else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Ácido úrico') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_acido_urico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('BUN') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_bun else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Proteínas totales') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_proteinas_totales else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Albúmina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_albumina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil lipídico (Triglicéridos, colesterol, HDL, LDL)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_perfil_lipidico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_perfil_hepatico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil de anemia (hierro sérico, transferrina, ferritina, capacidad de fijación de hierro, vitamina B12, ácido fólico)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_perfil_anemia else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('MineralesSodio, Potasio, Calcio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_minerales else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Pruebas tiroideasTSH, FT4, (beta HCG si es mujer)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_pruebas_tiroideas else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('EMO') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_emo else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Ecografía abdominal') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_ecografia_abdominal else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Composición DEXA') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_composicion_dexa else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Radiografía de tórax PA-L') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_radiografia_torax else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Evaluación cardiológica preoperatoria + test de esfuerzo si amerita') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_evaluacion_cardiologica else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Evaluación neumológica preoperatoria') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_evaluacion_neumologica else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Endoscopía digestiva alta (Dr. Napoleón Salgado) Clínica Sandoval. (En ayunas)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_endoscopia_digestiva_alta else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Evaluación nutricional') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_evaluacion_nutricional else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Evaluación psicológica') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_evaluacion_psicologica else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('OMA') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_oma else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Peptido C') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_peptido_c else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 2 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_curva_glucosa_dos else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 4 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_curva_glucosa_cuatro else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Otros: ') + ustr(test_order.pre_others_text or '') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.pre_others else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    </section>
                    <nextFrame/>"""

            # SECTION THREE
            rml += "<section>" + rml_footer + "</section>"
            rml_header = rml_header.replace(ustr('EXÁMENES PREOPERATORIOS (ANTES DE CIRUGÍA)'), '_title_')

        if datas.get('primer_mes', False):
            # PAGE TWO...
            # SECTION ONE
            rml_header = rml_header.replace('_title_', ustr('EXÁMENES PRIMER MES'))
            rml += "<section>" + rml_header + "</section>" + "<nextFrame/>"

            # SECTION TWO
            rml += """
                    <section>
                    <blockTable colWidths="540.0,20.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Biometría hemática') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_biometria_hematica else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Urea') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_urea else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Creatinina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_creatinina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Glucosa') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_glucosa else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Ácido úrico') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_acido_urico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('BUN') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_bun else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Proteínas totales') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_proteinas_totales else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Albúmina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_albumina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil lipídico (Triglicéridos, colesterol, HDL, LDL)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_perfil_lipidico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_perfil_hepatico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Sodio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_sodio else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Potasio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_potasio else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('OMA') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_oma else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Peptido C') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_peptido_c else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 2 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_curva_glucosa_dos else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 4 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_curva_glucosa_cuatro else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Otros: ') + ustr(test_order.one_others_text or '') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.one_others else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    </section>
                    <nextFrame/>"""

            # SECTION THREE
            rml += "<section>" + rml_footer + "</section>"
            rml_header = rml_header.replace(ustr('EXÁMENES PRIMER MES'), '_title_')

        if datas.get('tercer_mes', False):
            # PAGE THREE...
            # SECTION ONE
            rml_header = rml_header.replace('_title_', ustr('EXÁMENES TERCER MES'))
            rml += "<section>" + rml_header + "</section>" + "<nextFrame/>"

            # SECTION TWO
            rml += """
                    <section>
                    <blockTable colWidths="540.0,20.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Biometría hemática') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_biometria_hematica else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Urea') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_urea else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Creatinina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_creatinina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Glucosa') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_glucosa else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Ácido úrico') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_acido_urico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('BUN') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_bun else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Proteínas totales') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_proteinas_totales else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Albúmina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_albumina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil lipídico (Triglicéridos, colesterol, HDL, LDL)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_perfil_lipidico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_perfil_hepatico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Sodio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_sodio else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Potasio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_potasio else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Calcio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_calcio else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('OMA') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_oma else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Peptido C') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_peptido_c else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 2 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_curva_glucosa_dos else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 4 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_curva_glucosa_cuatro else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Otros: ') + ustr(test_order.three_others_text or '') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.three_others else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    </section>
                    <nextFrame/>"""

            # SECTION THREE
            rml += "<section>" + rml_footer + "</section>"
            rml_header = rml_header.replace(ustr('EXÁMENES TERCER MES'), '_title_')

        if datas.get('sexto_o_neoveno_mes', False):
            # PAGE FOUR...
            # SECTION ONE
            rml_header = rml_header.replace('_title_', ustr('EXÁMENES SEXTO O NOVENO MES'))
            rml += "<section>" + rml_header + "</section>" + "<nextFrame/>"

            rml += """
                    <blockTable colWidths="460.0,80.0,20.0" rowHeights="12.0" style="">
                        <tr>
                            <td></td>
                            <td><para style="label_px">SEXTO MES</para></td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_month == 'six' else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td></td>
                            <td><para style="label_px">NOVENO MES</para></td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_month == 'nine' else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>"""

            # SECTION TWO
            rml += """
                    <section>
                    <blockTable colWidths="540.0,20.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Biometría hemática') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_biometria_hematica else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Urea') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_urea else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Creatinina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_creatinina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Glucosa') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_glucosa else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Hemoglobina glicosilada (en caso de Diabetes)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_hemoglobina_glicosilada else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Ácido úrico') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_acido_urico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('BUN') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_bun else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Proteínas totales') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_proteinas_totales else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Albúmina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_albumina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil lipídico (Triglicéridos, colesterol, HDL, LDL)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_perfil_lipidico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_perfil_hepatico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil de hierro (Hierro sérico, ferritinina, transferrina, \
                                                ácido fólico, capacidad de fijación de hierro)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_perfil_hierro else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Sodio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_sodio else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Potasio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_potasio else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Calcio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_calcio else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>"""

            if test_order.six_or_nine_month == 'six':
                rml += """
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Eco de abdomen superior') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_eco_abdomen else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>"""

            rml += """  <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('OMA') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_oma else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Peptido C') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_peptido_c else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 2 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_curva_glucosa_dos else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 4 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_curva_glucosa_cuatro else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Otros: ') + ustr(test_order.six_or_nine_others_text or '') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_others else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>"""

            rml += """
                    </blockTable>"""

            rml += """
                    </section>
                    <nextFrame/>"""

            # SECTION THREE
            rml += "<section>" + rml_footer + "</section>"
            rml_header = rml_header.replace(ustr('EXÁMENES SEXTO O NOVENO MES'), '_title_')

        if datas.get('primer_anno', False):
            # PAGE FIVE...
            # SECTION ONE
            rml_header = rml_header.replace('_title_', ustr('EXÁMENES PRIMER AÑO'))
            rml += "<section>" + rml_header + "</section>" + "<nextFrame/>"

            # SECTION TWO
            rml += """
                    <section>
                    <blockTable colWidths="540.0,20.0" rowHeights="" style="">
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Biometría hemática') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_biometria_hematica else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Urea') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_urea else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Creatinina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_creatinina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Glucosa, (si es diabético Hemoglobina glicosilada)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_glucosa else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('TP TTP INR') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_tp_ttp_inr else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Ácido úrico') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_acido_urico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('BUN') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_bun else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Proteínas totales') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_proteinas_totales else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Albúmina') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_albumina else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil lipídico (Triglicéridos, colesterol, HDL, LDL)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_perfil_lipidico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, \
                                                bilirrubinas)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_perfil_hepatico else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Perfil de hierro (Hierro sérico, ferritinina, transferrina, \
                                                ácido fólico, capacidad de fijación de hierro)') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_perfil_hierro else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Mineales: sodio, potasio, calcio') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_minerales else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Pruebas tiroideas: TSH, FT4') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_pruebas_tiroideas else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('EMO') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_emo else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Ecografía abdomen superior') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_ecografia_abdominal else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Composición corporal DEXA') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_composicion_dexa else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('OMA') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.six_or_nine_oma else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Peptido C') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_peptido_c else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 2 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_curva_glucosa_dos else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Curva de Glucosa 4 horas') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_curva_glucosa_cuatro else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <para style="info_text">
                                    """ + ustr('Otros: ') + ustr(test_order.first_year_others_text or '') + """
                                </para>
                            </td>
                            <td>
                                <blockTable colWidths="10.0" rowHeights="10.0" style="checkBox">
                                    <tr>
                                        <td>
                                            <para style="px">
                                                """ + ('X' if test_order.first_year_others else '') + """
                                            </para>
                                        </td>
                                    </tr>
                                </blockTable>
                            </td>
                        </tr>
                    </blockTable>"""

            rml += """
                    </section>
                    <nextFrame/>"""

            # SECTION THREE
            rml += "<section>" + rml_footer + "</section>"

        rml += """
                </story>
            </document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)

        if datas['send_report']:
            body = _("""Hello %s. \n\n
                        Here we send you the Test Order Request you needed... \n\n
                        Thanks.""")

            file_name = 'report_to_' + ustr(test_order.patient_id.partner_id.name)
            attachments = {file_name + ".pdf": pdf}

            vals = {
                'auto_delete': True,
                'state': 'outgoing',
                'subject': _('Test order request...'),
                'body_html': body % (ustr(test_order.patient_id.partner_id.name),),
                'email_from': test_order.doctor_id.physician_id.email or False,
                'email_to': test_order.patient_id.email,
                'attachment_ids': [
                    (0, 0, {'name': a_name,
                            'datas_fname': a_name,
                            'datas': str(a_content).encode('base64')}) for a_name, a_content in attachments.items()
                ]
            }

            mail_obj = pooler.get_pool(cr.dbname).get('mail.mail')
            mail_id = mail_obj.create(cr, uid, vals, context=context)
            mail_obj.send(cr, uid, [mail_id])

        return pdf, report_type

TestOrderReport('report.test_order_report', 'oemedical.test_order', '', '')
