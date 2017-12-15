# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import io
import os
import time
import string
import openerp

from openerp import pooler, tools
from openerp.report import report_sxw
from openerp.report.interface import report_rml

from openerp.tools import to_xml
from openerp.tools.translate import _

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from PIL import Image
from PIL.Image import fromstring
from random import choice

class oemedical_nutritional_report(report_rml):

    def create(self, cr, uid, ids, datas, context):
        nutritional_obj = pooler.get_pool(cr.dbname).get('oemedical.nutritional')
        list_to_delete = []

        for nutritional in nutritional_obj.browse(cr, uid, ids, context):
            rml = """
                    <document filename="test.pdf">
                        <template pageSize="(595.0,842.0)" title=" """ + _("Nutritional Report") + """ " author="Reynaldo Rodriguez Cruz" allowSplitting="20">
                            <pageTemplate id="page1">
                                <frame id="first" x1="47.0" y1="50.0" width="500" height="780"/>
                            </pageTemplate>
                        </template>"""
            
            rml += """
                        <stylesheet>
                            <blockTableStyle id="Table0">
                                <blockAlignment value="CENTER"/>
                                <blockValign value="MIDDLE"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="1,1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="1,1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="1,1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="1,1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="TableI">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="MIDDLE"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="TableTT">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="MIDDLE"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table1">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>
                                
                                <blockSpan start="0,0" stop="4,0"/>
                                <blockSpan start="0,1" stop="1,1"/>
                                <blockSpan start="0,2" stop="3,2"/>
                                <blockSpan start="0,3" stop="3,3"/>
                                <blockSpan start="0,7" stop="1,7"/>
                                <blockSpan start="0,8" stop="2,8"/>
                                <blockSpan start="3,8" stop="4,8"/>
                                <blockSpan start="0,6" stop="3,6"/>
                                <blockSpan start="1,4" stop="2,4"/>
                                <blockSpan start="1,5" stop="2,5"/>
                                <blockSpan start="4,2" stop="4,7"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="4,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="4,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="4,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="4,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table2">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>
                                <blockSpan start="0,0" stop="0,1"/>
                                <blockSpan start="1,1" stop="3,1"/>
                                <blockSpan start="4,1" stop="10,1"/>
                                <blockSpan start="12,1" stop="13,1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table4">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>
                                <blockBackground colorName="gray" start="0,0" stop="-1,0"/>
                                <blockBackground colorName="gray" start="0,6" stop="4,6"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="1"/>
                                
                                <blockSpan start="1,1" stop="3,1"/>
                                <blockSpan start="1,2" stop="3,2"/>
                                <blockSpan start="1,3" stop="3,3"/>
                                <blockSpan start="1,4" stop="3,4"/>
                                <blockSpan start="1,5" stop="3,5"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table5">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="MIDDLE"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="4,0" stop="4,-1" thickness="1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="10,0" stop="10,-1" thickness="1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,0" thickness="1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="10,-1" thickness="1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="1"/>
                                
                                <blockSpan start="0,3" stop="0,4"/>
                                <blockSpan start="1,3" stop="4,4"/>
                                <blockSpan start="6,2" stop="6,3"/>
                                <blockSpan start="6,4" stop="6,5"/>
                                
                                <blockSpan start="7,4" stop="7,5"/>
                                <blockSpan start="8,4" stop="8,5"/>
                                <blockSpan start="9,4" stop="9,5"/>
                                <blockSpan start="10,4" stop="10,5"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table6">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>
                                <blockBackground colorName="gray" start="0,0" stop="-1,0"/>
                                
                                <blockSpan start="2,0" stop="4,0"/>
                                <blockSpan start="5,0" stop="6,0"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="8,0" stop="8,-1" thickness="1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,0" thickness="1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="10,-1" thickness="1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table7">
                                <blockValign value="MIDDLE"/>
                                <blockValign value="TOP" start="1,2" stop="4,2"/>
                                <blockValign value="TOP" start="5,2" stop="6,2"/>
                                <blockAlignment value="CENTER"/>
                                
                                <blockSpan start="0,0" stop="0,1"/>
                                <blockSpan start="1,0" stop="1,1"/>
                                <blockSpan start="2,0" stop="2,1"/>
                                <blockSpan start="3,0" stop="3,1"/>
                                <blockSpan start="4,0" stop="4,1"/>
                                <blockSpan start="5,0" stop="6,1"/>
                                
                                <blockSpan start="1,2" stop="4,2"/>
                                <blockSpan start="1,3" stop="4,3"/>
                                
                                <blockSpan start="5,2" stop="6,2"/>
                                <blockSpan start="5,3" stop="6,3"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="6,0" stop="6,-1" thickness="1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,0" thickness="1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="10,-1" thickness="1"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="TableX">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="TOP"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="TableY">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="TOP"/>
                                <blockSpan start="0,0" stop="2,0"/>
                            </blockTableStyle>
                            
                            <initialize>
                                <paraStyle name="all" alignment="justify"/>
                            </initialize>
                            
                            <paraStyle name="P5_CENTER" fontName="Helvetica" fontSize="5.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P5_LEFT" fontName="Helvetica" fontSize="5.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P5_BOLD_LEFT" fontName="Helvetica-Bold" fontSize="5.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P5_BOLD_LEFT2" fontName="Helvetica-Bold" fontSize="5.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P5_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="5.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P5_CENTER_8" fontName="Helvetica" fontSize="5.0" spaceBefore="0.0" leading="5" alignment="CENTER"/>
                            
                            <paraStyle name="P5_LEFT_8" fontName="Helvetica" fontSize="5.0" spaceBefore="0.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P5_CENTER_15" fontName="Helvetica" fontSize="5.0" spaceBefore="0.0" leading="8.5" alignment="CENTER"/>
                            <paraStyle name="P5_CENTER_20" fontName="Helvetica" fontSize="5.0" leading="15" alignment="LEFT"/>
                            
                            <paraStyle name="P6_LEFT" fontName="Helvetica" fontSize="6.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P6_LEFT_1" fontName="Helvetica" fontSize="5.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P6_CENTER" fontName="Helvetica" fontSize="6.0" leading="8" alignment="CENTER"/>
                            
							<paraStyle name="P6_CENTER_8" fontName="Helvetica" fontSize="6.0" spaceBefore="0.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P6_CENTER_15" fontName="Helvetica" fontSize="6.0" spaceBefore="0.0" leading="8.5" alignment="CENTER"/>
                            
                            <paraStyle name="P7_LEFT" fontName="Helvetica" fontSize="7.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P7_CENTER" fontName="Helvetica" fontSize="7.0" leading="8" alignment="CENTER"/>
                            <paraStyle name="P7_BOLD_LEFT" fontName="Helvetica-Bold" fontSize="7.0" leading="8" alignment="LEFT"/>
                            
                            <paraStyle name="P6_BOLD_LEFT" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P6_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="CENTER"/>
                            <paraStyle name="P9_BOLD_LEFT" fontName="Helvetica-Bold" fontSize="9.0" alignment="LEFT"/>
                            <paraStyle name="P14_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="14.0" alignment="CENTER"/>
                            
                            <paraStyle name="P5_COURIER_JUSTIFY" fontName="Courier" fontSize="5.0" leading="5" alignment="JUSTIFY"/>
                        </stylesheet>"""
            
            rml += """  <story>"""
            
            rml += """
                        <blockTable colWidths="500.0" rowHeights="20.0,20.0" style="">
                            <tr><td><para style="P14_BOLD_CENTER">HISTORIA CLINICA NUTRICIONAL</para></td></tr>
                            <tr><td><para style="P14_BOLD_CENTER">BARIATRICA</para></td></tr>
                        </blockTable>"""
            
            dob = nutritional.patient_id.dob if nutritional.patient_id.dob else False
            if dob:
                strs = dob.split('-')
                if len(strs) >= 3:
                    dob = strs[2] + '/' + strs[1] + '/' + strs[0]
                else:
                    dob = ""
            else:
                dob = ""
            
            marital_status = False
            if nutritional.patient_id.marital_status:
                if nutritional.patient_id.marital_status == 's': marital_status = 'Soltero(a)'
                if nutritional.patient_id.marital_status == 'm': marital_status = 'Casado(a)'
                if nutritional.patient_id.marital_status == 'w': marital_status = 'Viudo(a)'
                if nutritional.patient_id.marital_status == 'd': marital_status = 'Divorciado(a)'
                if nutritional.patient_id.marital_status == 'x': marital_status = 'Separado(a)'
                if nutritional.patient_id.marital_status == 'z': marital_status = 'Casado(a) x ley'
  
            eva_date = False
            if nutritional.eva_date and len(nutritional.eva_date.split('-')) >= 3:
                eva_date = nutritional.eva_date.split('-')[2] + '-' + nutritional.eva_date.split('-')[1] + '-' + nutritional.eva_date.split('-')[0]
            
            fec_cir = False
            if nutritional.fec_cir and len(nutritional.fec_cir.split('-')) >= 3:
                fec_cir = nutritional.fec_cir.split('-')[2] + '-' + nutritional.fec_cir.split('-')[1] + '-' + nutritional.fec_cir.split('-')[0]
            
            contacto_info = ''
            #if nutritional.patient_id.email: contacto_info += _('Correo: ') + nutritional.patient_id.email + '. '
            if nutritional.patient_id.contacto: contacto_info += _(' ') + nutritional.patient_id.contacto + '/ '
            if nutritional.patient_id.telefono: contacto_info += _('Teléfono: ') + nutritional.patient_id.telefono + '/ '
            if nutritional.patient_id.celular: contacto_info += _('Celular: ') + nutritional.patient_id.celular + ' '
            
            residencia = ''
            if nutritional.patient_id.street: residencia += tools.ustr(nutritional.patient_id.street) + '. '
            if nutritional.patient_id.city: residencia += tools.ustr(nutritional.patient_id.city) + '. '
            if nutritional.patient_id.state_id and nutritional.patient_id.state_id.name: residencia += tools.ustr(nutritional.patient_id.state_id.name) + '. '
            if nutritional.patient_id.country_id and nutritional.patient_id.country_id.name: residencia += tools.ustr(nutritional.patient_id.country_id.name) + '. '
            
            rml += """
                        <spacer length="0.3cm"/>
                        <blockTable colWidths="100.0,30.0,130.0,170.0,100.0" rowHeights="20.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0" style="Table1">
                            <tr>
                                <td><para style="P9_BOLD_LEFT">1. <u>Datos generales del paciente</u>:</para></td>
                                <td></td><td></td><td></td><td></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable colWidths="40.0,80.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">Fecha: </para></td>
                                            <td><para style="P7_LEFT">""" + (eva_date if eva_date else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                                <td>
                                    <blockTable colWidths="70.0,55.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">""" + tools.ustr("Fecha cirugía:") + """</para></td>
                                            <td><para style="P7_LEFT">""" + (fec_cir if fec_cir else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td>
                                    <blockTable colWidths="60.0,100.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">Residencia:</para></td>
                                            <td><para style="P6_LEFT">""" + (tools.ustr(residencia) if residencia else '') +  """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td>
                                    <blockTable colWidths="45.0,60">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">Nacido:</para></td>
                                            <td><para style="P7_LEFT">""" + (tools.ustr(nutritional.patient_id.city) if nutritional.patient_id.city else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                            </tr>"""
            
            if (nutritional.patient_id.photo):
                path = openerp.modules.get_module_path('oemedical_nutritional')
                path += '/static/temp/'
                path = os.path.normpath(path)
                
                name = 'photo' + str(choice(range(1, 100)))
                img_path = os.path.join(path, name + '.png')
                list_to_delete.append(img_path)
                
                image_stream = io.BytesIO(nutritional.patient_id.photo.decode('base64'))
                img = Image.open(image_stream)
                img.save(img_path, "PNG")
            
            rml += """      <tr>
                                <td>
                                    <blockTable colWidths="90.0,250.0,90.0" style="TableI">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">""" + tools.ustr("Método quirúrgico:") + """</para></td>
                                            <td><para style="P7_LEFT">""" + (tools.ustr(nutritional.met_qur) if nutritional.met_qur else '') + """</para></td>
                                            <td><para style="P8_BOLD_LEFT" textColor="red">""" + ('DIABETICO' if nutritional.pro_dia else '') + ('PRE-DIABETICO' if nutritional.pre_dia else '') +"""</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td><td></td><td></td>"""
			
            if (nutritional.patient_id.photo):
                rml += """    	<td>
								    <illustration width="85" height="85" borderStrokeWidth="1" borderStrokeColor="black">
                                        <image file="file:""" + img_path + """ " x="0" y="0" width="85" height="85"/>
                                    </illustration>
							    </td>"""
            else:
                rml += """      <td></td>"""
            
            rml += """      </tr>
                            
                            <tr>
                                <td>
                                    <blockTable colWidths="102.0,330.0" style="TableI">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT" >Nombres y apellidos: </para></td>
                                            <td><para style="P8_LEFT">"""
            names = ''
            if nutritional.patient_id.first_name:
                names +=  tools.ustr(nutritional.patient_id.first_name)
            if nutritional.patient_id.last_name:
                names += ' ' + tools.ustr(nutritional.patient_id.last_name) 
            if nutritional.patient_id.slastname:
                names += ' ' + tools.ustr(nutritional.patient_id.slastname)  
                                                
            rml+= names + """</para></td>                                            
                                        </tr>
                                    </blockTable>
                                </td><td></td><td></td><td></td><td></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable colWidths="40.0,50.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">Edad:</para></td>
                                            <td><para style="P7_LEFT">""" + str(self._get_year(nutritional.patient_id)) + tools.ustr(' años') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td>
                                    <blockTable colWidths="43.0,116.0" style="TableI">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">Correo:</para></td>
                                            <td><para style="P6_LEFT_1">""" + (nutritional.patient_id.email if nutritional.patient_id.email else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                                <td>
                                    <blockTable colWidths="90.0,70.0" style="TableI">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">Fecha nacimiento:</para></td>
                                            <td><para style="P7_LEFT">""" + (dob if dob else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable colWidths="45.0,50.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">""" + tools.ustr('Género: ')+ """</para></td>
                                            <td><para style="P7_LEFT">""" + ('M' if nutritional.patient_id.sex == 'm' else 'F') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td>
                                    <blockTable colWidths="70.0,80.0" style="TableI">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">""" + tools.ustr("Teléfono casa:") + """</para></td>
                                            <td><para style="P7_LEFT">""" + (nutritional.patient_id.phone if nutritional.patient_id.phone else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                                <td>
                                    <blockTable colWidths="80.0,80.0" style="TableI">
                                        <tr>
                                            <td><para style="P8_BOLD_LEFT">Celular:</para></td>
                                            <td><para style="P8_LEFT">""" + (nutritional.patient_id.mobile if nutritional.patient_id.mobile else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable colWidths="55.0,370.0" style="TableI">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">Contacto:</para></td>
                                            <td><para style="P7_LEFT">""" + (contacto_info) + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td><td></td><td></td><td></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable colWidths="60.0,60.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">Estado civil:</para></td>
                                            <td><para style="P7_LEFT">""" + (tools.ustr(marital_status) if marital_status else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                                <td>
                                    <blockTable colWidths="55.0,70.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">""" + tools.ustr('Profesión:') + """</para></td>
                                            <td><para style="P7_LEFT">""" + (tools.ustr(nutritional.patient_id.occupation.name) if nutritional.patient_id.occupation and nutritional.patient_id.occupation.name else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td>
                                    <blockTable colWidths="102.0,65.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">""" + tools.ustr('Como llegó a consulta:') + """</para></td>
                                            <td><para style="P6_LEFT">""" + (tools.ustr(nutritional.com_con) if nutritional.com_con else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable colWidths="90.0,160.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">""" + tools.ustr('Dirección domicilio:') + """</para></td>
                                            <td><para style="P7_LEFT">""" + (tools.ustr(nutritional.patient_id.street) if nutritional.patient_id.street else '' + ' ' + tools.ustr(nutritional.patient_id.city) if nutritional.patient_id.city else '' + ' ' ) + """</para></td>                                                      
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                                <td></td>
                                <td>
                                    <blockTable colWidths="70.0,190.0">
                                        <tr>
                                            <td><para style="P7_BOLD_LEFT">""" + tools.ustr('No. de cedula:') + """</para></td>
                                            <td><para style="P7_LEFT">""" + (tools.ustr(nutritional.patient_id.ced_ruc) if nutritional.patient_id.ced_ruc else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.1cm"/>
                        <blockTable colWidths="530.0" rowHeights="20.0">
                            <tr>
                                <td><para style="P9_BOLD_LEFT">2. <u>""" + tools.ustr('Antecedentes alimenticios, enfermedad presente y práctica de ejercicio') + """</u>:</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="110.0,55.0,120.0,20.0,10.0,25.0,10.0,40.0,10.0,130.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Cuántas veces al día come?') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.vec_com) if nutritional.vec_com else '') + ' ' + _('comidas') + """</para></td>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Tiene el hábito de desayunar?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.hab_des and nutritional.hab_des == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.hab_des and nutritional.hab_des == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('A veces:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.hab_des and nutritional.hab_des == 'a' else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="115.0,30.0,10.0,55.0,10.0,40.0,10.0,100.0,10.0,150.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Regularmente donde come?:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Casa:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.reg_com and nutritional.reg_com == 'c' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Restaurante:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.reg_com and nutritional.reg_com == 'r' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Oficina:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.reg_com and nutritional.reg_com == 'o' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Se lleva comida de casa:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.reg_com and nutritional.reg_com == 'l' else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="35.0,30.0,10.0,28.0,10.0,35.0,10.0,42.0,20.0,10.0,20.0,10.0,65.0,20.0,10.0,20.0,10.0,85.0,20.0,10.0,20.0,10.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Come:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('rápido:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.com_com and nutritional.com_com == 'r' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('lento:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.com_com and nutritional.com_com == 'l' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('normal:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.com_com and nutritional.com_com == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Ansiedad:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ans_com and nutritional.ans_com == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ans_com and nutritional.ans_com == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Pica durante el día:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pic_dia and nutritional.pic_dia == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pic_dia and nutritional.pic_dia == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Síndrome comedor nocturno:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.sin_cnt and nutritional.sin_cnt == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.sin_cnt and nutritional.sin_cnt == 'n' else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="210.0,20.0,10.0,22.0,10.0,40.0,218.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Ha modificado sus hábitos alimentarios últimamente?:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.mod_hal and nutritional.mod_hal == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.mod_hal and nutritional.mod_hal == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Porque') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.por_qha) if nutritional.por_qha else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="150.0,20.0,10.0,22.0,10.0,40.0,278.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Intolerancias o alergias alimentarias:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ioa_alm and nutritional.ioa_alm == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ioa_alm and nutritional.ioa_alm == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Cuales') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.cua_ioa) if nutritional.cua_ioa else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="90.0,20.0,10.0,22.0,10.0,50.0,66.0,84.0,20.0,10.0,22.0,10.0,50.0,66.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Mezcla carbohidratos:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.mez_car and nutritional.mez_car == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.mez_car and nutritional.mez_car == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + tools.ustr('Frecuencia:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (nutritional.frq_car if nutritional.frq_car else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Consumo de frituras') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_frt and nutritional.con_frt == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_frt and nutritional.con_frt == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + tools.ustr('Frecuencia:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.frq_frt) if nutritional.frq_frt else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="180.0,20.0,10.0,22.0,10.0,50.0,238.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT"><b>""" + tools.ustr('¿Al comer toma agua o jugo junto a la comida?') + """</b></para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.tom_joa and nutritional.tom_joa == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.tom_joa and nutritional.tom_joa == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Frecuencia') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.frq_tom) if nutritional.frq_tom else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="60.0,35.0,10.0,23.0,10.0,23.0,10.0,60.0,20.0,10.0,20.0,10.0,60.0,20.0,10.0,20.0,10.0,42.0,77.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Consumo de sal') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Normal') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_sal and nutritional.con_sal == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Alto') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_sal and nutritional.con_sal == 'a' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Bajo') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_sal and nutritional.con_sal == 'b' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Pone sal extra?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.sal_ext and nutritional.sal_ext == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.sal_ext and nutritional.sal_ext == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Consumo snacks') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_snk and nutritional.con_snk == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_snk and nutritional.con_snk == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Frecuencia:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.frq_snk) if nutritional.frq_snk else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="90.0,35.0,10.0,23.0,10.0,23.0,10.0,70.0,20.0,10.0,20.0,10.0,60.0,139.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Su consumo de azúcar es:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Normal') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_azu and nutritional.con_azu == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Alto') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_azu and nutritional.con_azu == 'a' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Bajo') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_azu and nutritional.con_azu == 'b' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Pone azúcar extra?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.azu_ext and nutritional.azu_ext == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.azu_ext and nutritional.azu_ext == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Consumo dulces') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.con_dlc) if nutritional.con_dlc else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="60.0,20.0,10.0,22.0,10.0,65.0,20.0,140.0,40.0,10.0,40.0,10.0,40.0,10.0,33.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Consume café?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_cfe and nutritional.con_cfe == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_cfe and nutritional.con_cfe == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + tools.ustr('Cuantas tazas al día:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.cta_dia) if nutritional.cta_dia else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Consumo de bebidas azucaradas/gaseosas:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Diario') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_baz and nutritional.con_baz == 'd' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Semanal') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_baz and nutritional.con_baz == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Ocasional') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_baz and nutritional.con_baz == 'o' else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="105.0,50.0,10.0,25.0,10.0,50.0,10.0,30.0,10.0,40.0,10.0,85.0,10.0,45.0,10.0,30.0" rowHeights="12.0,12.0" style="Table2">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Con qué endulza sus comidas?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Azúcar blanca') + """</para></td>
                                <td><para style="P5_CENTER_20">""" + ('X' if nutritional.azc_bln else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Miel') + """</para></td>
                                <td><para style="P5_CENTER_20">""" + ('X' if nutritional.miel else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Azúcar morena') + """</para></td>
                                <td><para style="P5_CENTER_20">""" + ('X' if nutritional.azc_mor else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Panela') + """</para></td>
                                <td><para style="P5_CENTER_20">""" + ('X' if nutritional.pan_ras else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Sin azúcar') + """</para></td>
                                <td><para style="P5_CENTER_20">""" + ('X' if nutritional.sin_azu else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Mixto, edulcorante + azúcar') + """</para></td>
                                <td><para style="P5_CENTER_20">""" + ('X' if nutritional.edu_azu else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Edulcorante') + """</para></td>
                                <td><para style="P5_CENTER_20">""" + ('X' if nutritional.tip_edu else '') + """</para></td>
                                <td></td>
                            </tr>                            
                            <tr>
                                <td></td>
                                <td><para style="P5_BOLD_LEFT">""" + _('¿Qué edulcorante usa?') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.edu_usa) if nutritional.edu_usa else '') + """</para></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td><para style="P5_BOLD_LEFT">""" + _('¿Cuántos sobres diarios?') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.sbe_dia) if nutritional.sbe_dia else '') + """</para></td>
                                <td></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="140.0,390.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Cuántos vasos de agua pura toma al día?') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.vda_dia1) if nutritional.vda_dia1 else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="90.0,440.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Preferencias alimentarias:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.prf_ali) if nutritional.prf_ali else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,450.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Disgustos alimentarios:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.dis_ali) if nutritional.dis_ali else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="40.0,45.0,20.0,10.0,20.0,10.0,40.0,100.0,30.0,30.0,20.0,10.0,20.0,10.0,40.0,50.0,35.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Hábitos:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Bebe alcohol') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_alc and nutritional.con_alc == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_alc and nutritional.con_alc == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Frecuencia') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.frq_cal) if nutritional.frq_cal else '') + """</para></td>
                                
                                <td></td>
                                <td><para style="P5_LEFT">""" + _('Fuma') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_cig and nutritional.con_cig == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_cig and nutritional.con_cig == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Frecuencia') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.frq_cig) if nutritional.frq_cig else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="90.0,20.0,10.0,22.0,10.0,25.0,353.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Alergias a medicamentos?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ale_mdc and nutritional.ale_mdc == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ale_mdc and nutritional.ale_mdc == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Cual') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.que_mdc) if nutritional.que_mdc else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="170.0,20.0,10.0,22.0,10.0,30.0,268.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Toma medicación continua/suplementos alimentarios?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.tom_mdc and nutritional.tom_mdc == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.tom_mdc and nutritional.tom_mdc == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Cuales') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.cal_mdc) if nutritional.cal_mdc else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="60.0,20.0,10.0,22.0,10.0,50.0,358.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Toma aspirina?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.tom_asp and nutritional.tom_asp == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.tom_asp and nutritional.tom_asp == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('¿Que tiempo?') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.tmp_tap) if nutritional.tmp_tap else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="70.0,20.0,10.0,22.0,10.0,50.0,80.0,90.0,180.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Planea tener hijos?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pln_tnh and nutritional.pln_tnh == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pln_tnh and nutritional.pln_tnh == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('en que tiempo') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.can_tnh) if nutritional.can_tnh else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Método anticonceptivo?') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.met_ant) if nutritional.met_ant else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="160.0,20.0,10.0,22.0,10.0,35.0,273.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Tiene algún familiar que se haya realizado la CB?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.fam_hcb and nutritional.fam_hcb == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.fam_hcb and nutritional.fam_hcb == 'n' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('¿Quién?') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.fam_qun) if nutritional.fam_qun else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="60.0,50.0,50.0,10.0,50.0,10.0,50.0,10.0,50.0,10.0,50.0,10.0,120.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Actividad física:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Te consideras:') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Sedentario') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_dep and nutritional.con_dep == 's' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Moderado') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_dep and nutritional.con_dep == 'm' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Activo') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_dep and nutritional.con_dep == 'a' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Muy activo') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_dep and nutritional.con_dep == 't' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Deportista') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.con_dep and nutritional.con_dep == 'd' else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.1cm"/>
                        <blockTable colWidths="530.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Práctica de ejercicio físico:') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="85.0,20.0,10.0,20.0,10.0,85.0,20.0,10.0,20.0,10.0,240.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Le gusta hacer ejercicio?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.lgh_eje and nutritional.lgh_eje == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.lgh_eje and nutritional.lgh_eje == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Practica algún ejercicio?') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pct_eje and nutritional.pct_eje == 's' else '') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pct_eje and nutritional.pct_eje == 'n' else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="100.0,165.0,85.0,180.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Cuántas veces a la semana?') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.cvs_pre) if nutritional.cvs_pre else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Qué deportes practica?') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.qdp_pra) if nutritional.qdp_pra else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="50.0,100.0,160.0,35.0,10.0,35.0,10.0,35.0,10.0,85.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Profesión') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.pro_pac) if nutritional.pro_pac else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT"><b>En su trabajo</b>, la mayor parte del tiempo lo pasa:</para></td>
                                <td><para style="P5_LEFT">""" + _('Sentado') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ofi_cmp and nutritional.ofi_cmp == 's' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('de pie') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ofi_cmp and nutritional.ofi_cmp == 'p' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('mixto') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ofi_cmp and nutritional.ofi_cmp == 'm' else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="530.0" rowHeights="20.0">
                            <tr>
                                <td><para style="P8_BOLD_LEFT">3. <u>""" + tools.ustr('Enfermedades y antecedentes patológicos familiares') + """</u>:</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="530.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('3.1 Personales') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="100.0,35.0,10.0,35.0,10.0,35.0,10.0,35.0,10.0,45.0,10.0,50.0,10.0,75.0,20.0,40.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Problemas gastrointestinales:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Vomito') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_vom else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Náuseas') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_nau else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Diarrea') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_dia else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Acides') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_aci else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Flatulencia') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_flt else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Estreñimiento') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_est else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Frecuencia deposición:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.frq_dep1) if nutritional.frq_dep1 else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,35.0,10.0,80.0,10.0,120.0,10.0,45.0,10.0,50.0,10.0,70.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Problemas digestivos:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Gastritis') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_gas else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Helicobacter') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_hel else '') + """</para></td>
                               
                                <td><para style="P5_LEFT">""" + _('Reflujo gastro-esofágico') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_rge else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Úlceras') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_ulc else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Colon irritable') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_cir else '') + """</para></td>
                                <td></td>
                            </tr>
                            
                        </blockTable>"""
            #rml += """
                        #<spacer length="0.0cm"/>
                        #<blockTable colWidths="80.0,450.0" rowHeights="12.0">
                            #<tr>
                               #<td><para style="P5_LEFT">""" + _('Evaluacion Colonoscopia :') + """</para></td>
                               #<td><para style="P5_LEFT">""" + (str(nutritional.des_hel) if nutritional.des_hel else '') + """</para></td>
                            #</tr>
                        #</blockTable>"""
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="50.0,10.0,55.0,10.0,75.0,10.0,70.0,10.0,35.0,10.0,50.0,10.0,50.0,10.0,65.0,10.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_LEFT">""" + _('Higado graso') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_hgr else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Apnea del sueño') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_aps else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Artrosis o dolor articular') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_aod else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Problemas coronarios') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_pco else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Hernias') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_her else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Divertículos') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_dvr else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Colon irritable') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_cir else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Problemas tiroideos') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.pro_tir else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="30.0,500.0" rowHeights="12.0,12.0">
                            <tr>
                                <td><para style="P5_LEFT">""" + _('Otras:') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + (tools.ustr(nutritional.pro_otr) if nutritional.pro_otr else '') + """</para></td>
                            </tr>
                            <tr>
                                <td><para style="P5_LEFT"></para></td>
                                <td><para style="P5_CENTER_15">""" + (tools.ustr(nutritional.pro_dot) if nutritional.pro_dot else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.1cm"/>
                        <blockTable colWidths="530.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('3.2 Alguien de su familia cercana sufre de alguna enfermedad como:') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,20.0,10.0,20.0,10.0,45.0,75.0,10.0,80.0,20.0,10.0,20.0,10.0,45.0,75.0,0.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Diabetes:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_dia and nutritional.prf_dia == 's' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_dia and nutritional.prf_dia == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Parentesco:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.par_dia) if nutritional.par_dia else '') + """</para></td>
                                <td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Hipertensión:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_hip and nutritional.prf_hip == 's' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_hip and nutritional.prf_hip == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Parentesco:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.par_hip) if nutritional.par_hip else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,20.0,10.0,20.0,10.0,45.0,75.0,10.0,80.0,20.0,10.0,20.0,10.0,45.0,75.0,0.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Problemas tiroideos:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_ptr and nutritional.prf_ptr == 's' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_ptr and nutritional.prf_ptr == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Parentesco:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.par_prt) if nutritional.par_prt else '') + """</para></td>
                                <td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Obesidad / Sobrepeso:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_oys and nutritional.prf_oys == 's' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_oys and nutritional.prf_oys == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Parentesco:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.par_oys) if nutritional.par_oys else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,20.0,10.0,20.0,10.0,45.0,75.0,10.0,80.0,20.0,10.0,20.0,10.0,45.0,75.0,0.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Problemas Cardiacos:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_car and nutritional.prf_car == 's' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_car and nutritional.prf_car == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Parentesco:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.par_car) if nutritional.par_car else '') + """</para></td>
                                <td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Dislipidemias:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_dis and nutritional.prf_dis == 's' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.prf_dis and nutritional.prf_dis == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('Parentesco:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.par_dis) if nutritional.par_dis else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
                        
            rml += """          
                        <spacer length="0.1cm"/>
                        <blockTable colWidths="530.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('3.3.- Patologías del Preoperatorio :') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="64.0,95.0,10.0,80.0,20.0,77.0,10.0,77.0,10.0,50.0,10.0,60.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr(' ') + """</para></td>
                                <td><para style="P5_BOLD_LEFT">""" + _('Hipertensión arterial (HTA)') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.preop_hta else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Diabetes Melitus (DM)') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.diab_mel_dm else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Dislipidemias') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.preop_dis else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Higado Graso') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.hig_gra else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Otras') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.otr_pat else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>""" 

            rml += """
                        <spacer length="0.05cm"/>
                        <blockTable colWidths="64.0,95.0,10.0,80.0,20.0,77.0,10.0,77.0,10.0,50.0,10.0,60.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Medicación :') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.preop_dis_med) if nutritional.preop_dis_med else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.diab_mel_med) if nutritional.diab_mel_med else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.preop_dis_med) if nutritional.preop_dis_med else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.hig_gra_med) if nutritional.hig_gra_med else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.otr_pat_med) if nutritional.otr_pat_med else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
                        
            rml += """
                        <spacer length="0.05cm"/>
                        <blockTable colWidths="64.0,95.0,10.0,80.0,20.0,77.0,10.0,77.0,10.0,50.0,10.0,60.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Dosis :') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.hip_preop_dos) if nutritional.hip_preop_dos else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.diab_mel_dos) if nutritional.diab_mel_dos else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.preop_dis_dos) if nutritional.preop_dis_dos else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.hig_gra_dos) if nutritional.hig_gra_dos else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.otr_pat_dos) if nutritional.otr_pat_dos else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>""" 
                        
            rml += """
                        <spacer length="0.05cm"/>
                        <blockTable colWidths="64.0,95.0,10.0,80.0,20.0,77.0,10.0,77.0,10.0,50.0,10.0,60.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Valores de laboratorio:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.hip_preop_val) if nutritional.hip_preop_val else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.diab_mel_val) if nutritional.diab_mel_val else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.preop_dis_val) if nutritional.preop_dis_val else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.hig_gra_val) if nutritional.hig_gra_val else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.otr_pat_val) if nutritional.otr_pat_val else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>""" 
           
            rml += """
                        <spacer length="0.05cm"/>
                        <blockTable colWidths="64.0,95.0,10.0,80.0,20.0,77.0,10.0,77.0,10.0,50.0,10.0,60.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Hace que tiempo :') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.hip_preop_hac) if nutritional.hip_preop_hac else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.diab_mel_hac) if nutritional.diab_mel_hac else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.preop_dis_hac) if nutritional.preop_dis_hac else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.hig_gra_hac) if nutritional.hig_gra_hac else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.otr_pat_hac) if nutritional.otr_pat_hac else '') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + tools.ustr(' ') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""                     
                        
            rml += """      <pageBreak></pageBreak> """
            
            rowHeights = '20.0'
                        
            rml += """
                        <spacer length="0.4cm"/>
                        <blockTable colWidths="530.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P9_BOLD_LEFT">4.<u>""" + tools.ustr(' Complicaciones quirurgicas y Tratamiento') + """</u></para></td>
                            </tr>
                        </blockTable>"""
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="530.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.par_dis) if nutritional.par_dis else '') + """</para></td>
                            </tr>
                        </blockTable>"""
                        
            
            rml += """
                        <spacer length="0.3cm"/>
                        <blockTable colWidths="530.0" rowHeights=" """ + rowHeights + """ ">
                            <tr>
                                <td><para style="P9_BOLD_LEFT">5. <u>""" + tools.ustr('Horarios de trabajo o estudio que impidan alimentarse correctamente') + """</u>:</para></td>
                            </tr>"""
            rml += """  </blockTable>"""
            
            rml += """
                        <spacer length="0.3cm"/>
                        <blockTable colWidths="530.0" rowHeights="20.0">
                            <tr>
                                <td><para style="P9_BOLD_LEFT">6. <u>""" + tools.ustr('Recordatorio de 24 horas') + """</u>:</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.3cm"/>
                        <blockTable colWidths="40.0,330.0,70.0,50.0,40.0" rowHeights="15.0,100.0,35.0,112.0,35.0,40.0,12.0" style="Table4">
                            <tr>
                                <td><para style="P6_BOLD_CENTER">Tiempo Comida</para></td>
                                <td><para style="P6_BOLD_CENTER">Alimento</para></td>
                                <td><para style="P6_BOLD_CENTER">""" + tools.ustr("Preparación") + """</para></td>
                                <td><para style="P6_BOLD_CENTER">""" + tools.ustr("Porción") + """</para></td>
                                <td><para style="P6_BOLD_CENTER">Kcal</para></td>
                            </tr>
                            <tr>
                                <td>
                                    <blockTable>
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('Desayuno') + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('Hora:') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + (str(nutritional.des_hor) if nutritional.des_hor else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td>
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="60.0,10.0,40.0,10.0,40.0,10.0,280.0" rowHeights="12.0,12.0">
                                        <tr></tr>
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Agua aromática:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_aar else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Batidos:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_bat else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Ayunas:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_ayu else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="55.0,10.0,55.0,10.0,65.0,40.0,30.0,60.0,35.0,10.0,80.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Café en agua:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_cea else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Café en leche:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_cel else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('leche: cantidad') + """</para></td>
                                            <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.des_lec) if nutritional.des_lec else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Tipo:') + """</para></td>
                                            <td><para style="P5_CENTER_8">""" + ('Entera' if nutritional.des_tle == 'e' else 'Semidescremada' if nutritional.des_tle == 's' else 'Descremada' if nutritional.des_tle == 'd' else 'Deslactosada semidescremada' if nutritional.des_tle == 'm' else 'Deslactosada descremada' if nutritional.des_tle == 'n' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Azucar:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_azu else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="40.0,55.0,10.0,55.0,10.0,35.0,40.0,30.0,60.0,35.0,10.0,70.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Lácteos:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Leche sola:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_lsl else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Leche y café:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_lyc else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Yogurt:') + """</para></td>
                                            <td><para style="P5_CENTER_8">""" + ('X' if nutritional.des_yog else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Tipo:') + """</para></td>
                                            <td><para style="P5_CENTER_8">""" + ('Entera' if nutritional.des_tla == 'e' else 'Semidescremada' if nutritional.des_tla == 's' else 'Descremada' if nutritional.des_tla == 'd' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Azucar:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_azl else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="25.0,45.0,55.0,40.0,55.0,35.0,10.0,30.0,10.0,35.0,10.0,100.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Cho:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Pan entero:') + """</para></td>
                                            <td><para style="P5_CENTER_8">""" + ('Integral' if nutritional.des_pae == 'i' else 'Blanco' if nutritional.des_pae == 's' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Pan rbn:') + """</para></td>
                                            <td><para style="P5_CENTER_8">""" + ('Integral' if nutritional.des_rbn == 'i' else 'Blanco' if nutritional.des_rbn == 's' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Cereal:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_cer else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Arroz:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_arr else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Otro:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_otr else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="40.0,35.0,10.0,30.0,35.0,35.0,10.0,50.0,10.0,35.0,10.0,50.0,100.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Proteína:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Queso:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_que else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Tipo:') + """</para></td>
                                            <td><para style="P5_CENTER_8">""" + (tools.ustr(nutritional.des_tqu) if nutritional.des_tqu else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Jamón:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_jam else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Pollo/Carne:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_pyc else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Huevo:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_hue else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Preparación:') + """</para></td>
                                            <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.des_pre) if nutritional.des_pre else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="50.0,10.0,50.0,10.0,50.0,10.0,55.0,10.0,35.0,10.0,160.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Fruta entera:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_fre else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Fruta picada:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_frp else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Jugo puro:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_jup else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Jugo con agua:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_jua else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Azúcar:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_azf else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="35.0,50.0,10.0,45.0,10.0,35.0,10.0,70.0,10.0,175.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Grasa:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Mantequilla:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_man else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Margarina:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_mar else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Aceite:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_ace else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Manteca de cerdo:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.des_mcr else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    <blockTable colWidths="450.0" rowHeights="12.0,12.0,12.0">
                                        <tr>
                                            <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.ext_inf) if nutritional.ext_inf else '') + """</para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P5_LEFT_8"></para></td>
                                        </tr>
                                        <tr>
                                            <td><para style="P5_LEFT_8"></para></td>
                                        </tr>
                                    </blockTable>                                   

                                </td>
                                
                                <td></td><td></td>
                                <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.des_kca) if nutritional.des_kca else '') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable>
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('½ Mañana') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('Hora:') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + (str(nutritional.mma_hor) if nutritional.mma_hor else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td>
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="35.0,50.0,35.0,10.0,35.0,10.0,275.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Snack:') + """</para></td>
                                            <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.mma_snc) if nutritional.mma_snc else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Fruta:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.mma_frt else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Yogurt:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.mma_ygt else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="30.0,420.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Otros:') + """</para></td>
                                            <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.mma_otr) if nutritional.mma_otr else '') + """</para></td>
                                        </tr>                                       
                                    </blockTable>
                                </td>                                
                                <td>
                                </td>
                                <td></td>
                                <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.mma_kca) if nutritional.mma_kca else '') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable>
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('Almuerzo') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('Hora:') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + (str(nutritional.alm_hor) if nutritional.alm_hor else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td>
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="30.0,20.0,10.0,22.0,10.0,35.0,10.0,30.0,40.0,10.0,25.0,10.0,40.0,10.0,40.0,10.0,40.0,10.0,48.0" rowHeights="12.0,12.0">
                                        <tr></tr>
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Sopa:') + """</para></td>
                                            <td><para style="P5_CENTER_8">""" + _('Si') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_sop and nutritional.alm_sop == 's' else '') + """</para></td>
                                            
                                            <td><para style="P5_CENTER_8">""" + _('No') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_sop and nutritional.alm_sop == 'n' else '') + """</para></td>
                                            
                                            <td><para style="P5_CENTER_8">""" + _('a veces') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_sop and nutritional.alm_sop == 'a' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Lleva:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Proteínas') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_con and nutritional.alm_con == 'p' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('CHO') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_con and nutritional.alm_con == 'c' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Verduras') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_con and nutritional.alm_con == 'v' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Espesa') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_asp and nutritional.alm_asp == 'e' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Líquida') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_asp and nutritional.alm_asp == 'l' else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="50.0,30.0,10.0,50.0,10.0,45.0,10.0,30.0,10.0,30.0,10.0,35.0,10.0,120.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Plato fuerte:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Arroz') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_arr else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Papa cocida') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_pco else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Papa frita') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_pfr else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Fideo') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_fid else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Pasta') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_pas else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Camote') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_cam else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="50.0,70.0,10.0,30.0,290.0" rowHeights="12.0">
                                        <tr>
                                            <td></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Granos o menestras') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_grm else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Otros') + """</para></td>
                                            <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.alm_otr) if nutritional.alm_otr else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="40.0,40.0,10.0,45.0,10.0,35.0,10.0,30.0,10.0,25.0,35.0,10.0,30.0,10.0,40.0,10.0,60.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Verduras:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Siempre') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_ver and nutritional.alm_ver == 's' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('No siempre') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_ver and nutritional.alm_ver == 'n' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('A veces') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_ver and nutritional.alm_ver == 'a' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Nunca') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_ver and nutritional.alm_ver == 'u' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Con:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Granos') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_grn else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Pollo') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_pol else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Pescado') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_pes else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="30.0,30.0,10.0,30.0,10.0,45.0,10.0,45.0,10.0,230.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Atún:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Agua') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_atn == 'g' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Aceite') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_atn == 'c' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Carne roja') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_cro else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Embutidos') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_emb else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="35.0,415.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Grasa:') + """</para></td>
                                            <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.alm_grs) if nutritional.alm_grs else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="50.0,30.0,10.0,25.0,10.0,40.0,10.0,40.0,10.0,55.0,10.0,35.0,10.0,115.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Para tomar:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Agua') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_agu else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Té') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_te else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Coca Cola') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_coc else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Jugo puro') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_jup else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Jugo con agua') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_jua else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Azúcar') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_azb else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="35.0,20.0,10.0,22.0,10.0,25.0,40.0,45.0,243.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Postre:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Si') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_pos else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('No') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.alm_pos else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Cual') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + (tools.ustr(str(nutritional.des_tqu)) if nutritional.des_tqu else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('Frecuencia:') + """</para></td>
                                            <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.alm_frp) if nutritional.alm_frp else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                    <blockTable colWidths="450.0" rowHeights="12.0,12.0,12.0">
                                        <tr>
                                            <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.exi_alm) if nutritional.exi_alm else '') + """</para></td>
                                        </tr>
                                        <tr>
                                        </tr>
                                        <tr>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td></td>
                                <td></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.alm_kca) if nutritional.alm_kca else '') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable>
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('½ Tarde') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('Hora:') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + (str(nutritional.mta_hor) if nutritional.mta_hor else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td>
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="35.0,50.0,35.0,10.0,35.0,10.0,275.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Snack:') + """</para></td>
                                            <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.mta_snc) if nutritional.mta_snc else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Fruta:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.mta_frt else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Yogurt:') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.mta_ygt else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="30.0,420.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Otros:') + """</para></td>
                                            <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.mta_otr) if nutritional.mta_otr else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td></td>
                                <td></td>
                                <td><para style="P5_LEFT_8">""" + (tools.ustr(nutritional.mta_kca) if nutritional.mta_kca else '') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <blockTable>
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('Cena') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + tools.ustr('Hora:') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_CENTER">""" + (str(nutritional.cen_hor) if nutritional.cen_hor else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td>
                                    <spacer length="0.0cm"/>
                                    <blockTable colWidths="90.0,20.0,10.0,22.0,10.0,298.0" rowHeights="12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Come como un almuerzo:') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Si') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.cen_alm and nutritional.cen_alm == 's' else '') + """</para></td>
                                            
                                            <td><para style="P5_BOLD_LEFT">""" + _('No') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.cen_alm and nutritional.cen_alm == 'n' else '') + """</para></td>
                                            <td></td>
                                        </tr>
                                    </blockTable>
                                    <blockTable colWidths="450.0" rowHeights="12.0,12.0,12.0">
                                        <tr>
                                            <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.exi_cen) if nutritional.exi_cen else '') + """</para></td>
                                        </tr>
                                        <tr>
                                        </tr>
                                        <tr>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td></td>
                                <td></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.cen_kca) if nutritional.cen_kca else '') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td></td>
                                <td><para style="P6_BOLD_LEFT">""" + tools.ustr("TOTAL") + """</para></td>
                                <td></td>
                                <td></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.tot_kca) if nutritional.tot_kca else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.3cm"/>
                        <blockTable colWidths="80.0,30.0,10.0,35.0,10.0,100.0,20.0,245.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('El fin de semana come:') + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Fuera') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.fds_com and nutritional.fds_com == 'f' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('En casa') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.fds_com and nutritional.fds_com == 'e' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + _('¿Cuántos días sale a comer fuera?') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.fds_dia) if nutritional.fds_dia else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,450.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Qué come por fuera?') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.fds_cpf) if nutritional.fds_cpf else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.3cm"/>
                        <blockTable colWidths="530.0" rowHeights="20.0">
                            <tr>
                                <td><para style="P9_BOLD_LEFT">7. <u>""" + tools.ustr('Datos antropométricos y cronopatología del peso corporal') + """</u>:</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,40.0,10.0,50.0,10.0,35.0,10.0,50.0,10.0,90.0,10.0,135.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Inicio de la obesidad') + """:</para></td>
                                <td><para style="P5_LEFT">""" + tools.ustr('Infancia') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ini_obe and nutritional.ini_obe == 'i' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + tools.ustr('Adolescencia') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ini_obe and nutritional.ini_obe == 'd' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + tools.ustr('Adultez') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ini_obe and nutritional.ini_obe == 'a' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + tools.ustr('Post embarazo') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ini_obe and nutritional.ini_obe == 'l' else '') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + tools.ustr('Sociales (divorcio/casamiento)') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.ini_obe and nutritional.ini_obe == 's' else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,35.0,120.0,120.0,175.0" rowHeights="12.0">
                            <tr>
                                <td></td>
                                <td><para style="P5_LEFT">""" + tools.ustr('Otros:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.int_otr) if nutritional.int_otr else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Intentos previos de perdida de peso:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.int_ppp) if nutritional.int_ppp else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="95.0,20.0,10.0,22.0,10.0,140.0,233.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿A visitado al nutricionista?') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + _('Si') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.vis_nut and nutritional.vis_nut == 's' else '') + """</para></td>
                                            
                                <td><para style="P5_CENTER_8">""" + _('No') + """</para></td>
                                <td><para style="P5_CENTER_15">""" + ('X' if nutritional.vis_nut and nutritional.vis_nut == 'n' else '') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Motivaciones para perder peso/cirugía:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(nutritional.mot_ppp) if nutritional.mot_ppp else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="90.0,30.0,25.0,30.0,25.0,140.0,30.0,25.0,30.0,25.0,25.0,30.0,25.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Máximo peso alcanzado?') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.max_pak) if nutritional.max_pak else '') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + _('Kg') + """</para></td>
                                
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.max_pal) if nutritional.max_pal else '') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + _('lbs') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('¿Cúal es el peso mínimo en la vida adulta?') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.min_pak) if nutritional.min_pak else '') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + _('Kg') + """</para></td>
                                
                                <td><para style="P5_LEFT_8">""" + (str(nutritional.min_pal) if nutritional.min_pal else '') + """</para></td>
                                <td><para style="P5_LEFT_8">""" + _('lbs') + """</para></td>
                                
                                <td><para style="P5_LEFT_8">""" + _('Hace') + """</para></td>
                                <td><para style="P5_LEFT_8">""" + (str(nutritional.min_hac) if nutritional.min_hac else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="85.0,30.0,25.0,30.0,25.0,25.0,30.0,25.0,255.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Peso antes de la cirugía:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.pes_pak) if nutritional.pes_pak else '') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + _('Kg') + """</para></td>
                                
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.pes_pal) if nutritional.pes_pal else '') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + _('lbs') + """</para></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('IMC:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (str(round(nutritional.imc,2)) if nutritional.imc else '') + """</para></td>
                                <td><para style="P5_CENTER_8">Kg/m<super>2</super>:</para></td>
                                <td><para style="P5_CENTER_8">""" + (str(round(nutritional.pes_kgm2,2)) if nutritional.pes_kgm2 else '') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="240.0,30.0,25.0,30.0,25.0,30.0,25.0,30.0,25.0,70.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT"><b>""" + tools.ustr('Exceso de peso:') + """</b>""" + _('peso actual preoperatorio - peso ideal (peso ideal permitido) =') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.pea_pok) if nutritional.pea_pok else '') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + _('Kg -') + """</para></td>
                                
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.pei_pek1) if nutritional.pei_pek1 else '') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + _('Kg =') + """</para></td>
                                
                                <td><para style="P5_CENTER_8">""" + (str(round(nutritional.pea_pok - nutritional.pei_pek1,2)) if nutritional.pea_pok and nutritional.pei_pek1 else '') + """</para></td>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Kg,') + """</para></td>
                                
                                <td><para style="P5_CENTER_8">""" + (str(round((nutritional.pea_pok - nutritional.pei_pek1) * 2.2, 2)) if nutritional.pea_pol and nutritional.pei_pel else '') + """</para></td>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('lbs.') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
                        
            rml += """
                        <spacer length="0.0cm"/>
                        <blockTable colWidths="80.0,60.0,60.0,60.0,135.0,135.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('% de grasa DEXA:') + """</para></td>
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.por_gde) if nutritional.por_gde else '') + """</para></td>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('% de grasa BIO:') + """</para></td>                    
                                <td><para style="P5_CENTER_8">""" + (str(nutritional.por_gbi) if nutritional.por_gbi else '') +  """</para></td>
                                <td></td>
                                <td></td>
                            </tr>
                        </blockTable>"""
            
            rml += """
                        <spacer length="0.2cm"/>
                        <blockTable colWidths="50.0,100.0,40.0,50.0,100.0,0.0,55.0,35.0,25.0,35.0,25.0" rowHeights="12.0,12.0,12.0,12.0,12.0,12.0" style="Table5">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + _('Edad') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.pac_age) if nutritional.pac_age else '' ) + tools.ustr(' años.') + """</para></td>
                                <td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Talla') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.est_pac) if nutritional.est_pac else '' ) + (' mts.' if nutritional.est_pac else '') + """</para></td>
                                <td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Peso ideal') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.pei_pek,2)) if nutritional.pei_pek else '' ) + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Kg') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.pei_pel,2)) if nutritional.pei_pel else '' ) + """</para></td>
                                <td><para style="P5_LEFT">""" + _('lbs') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + _('Peso actual') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.pea_pok,2)) if nutritional.pea_pok else '' ) + (' Kg, ' if nutritional.pea_pok else '') + (str(round(nutritional.pea_pol,2)) if nutritional.pea_pol else '') + (' lbs.' if nutritional.pea_pol else '') + """</para></td>
                                <td></td><td></td><td></td><td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Peso objetivo') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.pob_pok,2)) if nutritional.pob_pok else '' ) + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Kg') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.pob_pol,2)) if nutritional.pob_pol else '' ) + """</para></td>
                                <td><para style="P5_LEFT">""" + _('lbs') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + _('IMC') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.imc2,2)) if nutritional.imc2 else '') +  """ Kg/m<super>2</super>.</para></td>
                                <td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr(_('% de grasa')) + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.por_gra,2)) if nutritional.por_gra else '' ) + (' %.' if nutritional.por_gra else '') + """</para></td>
                                <td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Rango de peso') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.min_prl) if nutritional.min_prl else '' ) + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Kg') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (str(nutritional.min_prk) if nutritional.min_prk else '' ) + """</para></td>
                                <td><para style="P5_LEFT">""" + _('lbs') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + _('Estado') + """</para></td>
                                <td>
                                    <blockTable colWidths="45.0,10.0,50.0,10.0,60.0,10.0,80.0,10.0" rowHeights="12.0,12.0">
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Normopeso') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.est_obe and nutritional.est_obe == 'n' else '') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Sobrepeso I') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.est_obe and nutritional.est_obe == 's' else '') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Sobrepeso II') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.est_obe and nutritional.est_obe == 's2' else '') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Obesidad I') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.est_obe and nutritional.est_obe == 'o' else '') + """</para></td>
                                        </tr>
                                        
                                        <tr>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Obesidad II') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.est_obe and nutritional.est_obe == 'o2' else '') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Obesidad III') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.est_obe and nutritional.est_obe == 's3' else '') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Super obesidad') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.est_obe and nutritional.est_obe == 'so' else '') + """</para></td>
                                            <td><para style="P5_BOLD_LEFT">""" + _('Super super obesidad') + """</para></td>
                                            <td><para style="P5_CENTER_15">""" + ('X' if nutritional.est_obe and nutritional.est_obe == 'sso' else '') + """</para></td>
                                        </tr>
                                    </blockTable>
                                </td>
                                
                                <td></td><td></td><td></td><td></td>
                                <td></td>
                                
                                <td><para style="P5_LEFT">""" + _('mínimo' ) + """</para></td>
                                <td><para style="P5_LEFT"></para></td>
                                
                                <td><para style="P5_LEFT">""" + _('máximo' ) + """</para></td>
                                <td><para style="P5_LEFT"></para></td>
                            </tr>
                            
                            <tr>
                                <td></td><td></td><td></td><td></td><td></td><td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + _('Máximo peso recomendado') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.max_prk,2)) if nutritional.max_prk else '' ) + """</para></td>
                                <td><para style="P5_LEFT">""" + _('Kg') + """</para></td>
                                
                                <td><para style="P5_LEFT">""" + (str(round(nutritional.max_prl,2)) if nutritional.max_prl else '' ) + """</para></td>
                                <td><para style="P5_LEFT">""" + _('lbs') + """</para></td>
                            </tr>
                            
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + _('Perímetro abdominal') + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.cin_pac) if nutritional.cin_pac else '' ) + (' cm.' if nutritional.cin_pac else '') + """</para></td>
                                <td></td>
                                
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr(_('Cadera')) + """</para></td>
                                <td><para style="P5_LEFT">""" + (str(nutritional.cad_pac) if nutritional.cad_pac else '' ) + (' cm.' if nutritional.cad_pac else '') + """</para></td>
                                <td></td>
                                <td></td><td></td><td></td><td></td><td></td>
                            </tr>
                        </blockTable>
                        
                        <spacer length="0.2cm"/>
                        <blockTable colWidths="110.0,50.0,370.0" rowHeights="12.0">
                            <tr>
                                <td><para style="P5_BOLD_LEFT">""" + tools.ustr('Indice de Cintura-Cadera:') + """</para></td>
                                <td><para style="P5_LEFT">""" + (tools.ustr(round(nutritional.icc,2)) if nutritional.icc else '') + """</para></td>
                                <td></td>
                            </tr>
                        </blockTable>"""

            
            rml += """      <pageBreak></pageBreak> """
            
            rrT = 0
            trT = 62
            rowHeights = '15.0'
            for x in range(len(nutritional.evolution_ids)):
                rowHeights += ',12.0'
                rrT = rrT + 1
            
            for xxx in range(rrT, trT):
                rowHeights += ',12.0'
            
            rml += u"""
                        <spacer length="0.3cm"/>
                        <blockTable colWidths="50.0,55.0,38.0,38.0,38.0,38.0,30.0,42.0,42.0,110.0,45.0,50.0" rowHeights=" """ + rowHeights + u""" " style="Table6">
                            <tr>
                                <td><para style="P5_BOLD_CENTER">Fecha</para></td>
                                <td><para style="P5_BOLD_CENTER">Peso actual</para></td>
                                <td><para style="P5_BOLD_CENTER">""" + tools.ustr("Pérdida de peso y % de grasa") + u"""</para></td>
                                <td><para style="P5_BOLD_CENTER"></para></td>
                                <td><para style="P5_BOLD_CENTER"></para></td>
                                <td><para style="P5_BOLD_CENTER">Perímetro Abdominal (cm)</para></td>
                                <td><para style="P5_BOLD_CENTER"></para></td>
                                <td><para style="P5_BOLD_CENTER">% Grasa DEXA</para></td>
                                <td><para style="P5_BOLD_CENTER">% Grasa BIO</para></td>
                                <td><para style="P5_BOLD_CENTER">Observaciones</para></td>
                                <td><para style="P5_BOLD_CENTER">Tiempo Cirugía</para></td>
                                <td><para style="P5_BOLD_LEFT">Exceso de peso perdido</para></td>
                            </tr>"""
            
            for data in nutritional.evolution_ids:
                fecha = data.date_nut if data.date_nut else False
                if fecha: 
                    fecha = fecha.split('-')[2] + '/' + fecha.split('-')[1] + '/' + fecha.split('-')[0]
                r1 = pooler.get_pool(cr.dbname).get('oemedical.nutritional.evolution').get_epp(cr,uid,[data.id],'exp_per',[])
                r2 = pooler.get_pool(cr.dbname).get('oemedical.nutritional.evolution').get_imc2(cr,uid,[data.id],'imc_cot',[])
                rml += """  <tr>
                                <td><para style="P6_CENTER">""" + (fecha if fecha else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + ((str(data.pso_act) + 'Kg.') if data.pso_act else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + ((str(data.pso_per) + 'Kg.')if data.pso_per else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + ((str(data.pgr_act) + '%.') if data.pgr_act else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + ((str(data.pgr_ant) + '%.') if data.pgr_ant else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + (str(data.cin_act) if data.cin_act else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + (str(data.cin_act1) if data.cin_act1 else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + (str(data.por_gdec) if data.por_gdec else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + (str(data.por_gbic) if data.por_gbic else '') + """</para></td>
                                <td><para style="P6_LEFT">""" + (('IMC: ' + str(round(r2[data.id],2)) + tools.ustr('Kg/m².')) if r2[data.id] else '') + ('   ') + ('Normopeso' if data.tip_obe == 'n' else 'Sobrepeso I' if data.tip_obe == 's' else 'Sobrepeso II' if data.tip_obe == 's2' else '') + """</para></td>
                                <td><para style="P6_LEFT">""" + (str(data.tmp_cir) if data.tmp_cir else '') + """</para></td>
                                <td><para style="P6_CENTER">""" + ((str(round(r1[data.id],2)) + '%.') if r1[data.id] else '') + """</para></td>
                            </tr>"""
            
            for xxx in range(rrT, trT):
                rml += """  <tr>
                                <td><para style="P6_CENTER"></para></td>
                                <td><para style="P6_CENTER"></para></td>
                                <td><para style="P6_CENTER"></para></td>
                                <td><para style="P6_CENTER"></para></td>
                                <td><para style="P6_CENTER"></para></td>
                                <td><para style="P6_CENTER"></para></td>
                                <td><para style="P6_CENTER"></para></td>
                                <td><para style="P6_LEFT"></para></td>
                                <td><para style="P6_CENTER"></para></td>
                            </tr>"""
            
            rml += """  </blockTable>"""
            
            rml += """
                        <spacer length="0.3cm"/>
                        <blockTable colWidths="530.0" rowHeights="20.0">
                            <tr>
                                <td><para style="P9_BOLD_LEFT">""" + _('CONTROL') + """</para></td>
                            </tr>
                        </blockTable>"""
            
            cant = 0
            for control in nutritional.evolution_ids:
                cant = cant + 1
                fecha = control.date_nut
                if fecha: fecha = fecha.split('-')[2] + '/' + fecha.split('-')[1] + '/' + fecha.split('-')[0]
            
                rml += """  <condPageBreak height="100"/>"""
                
                observ = self._get_list_words(control.observ, 282)
                hydration = self._get_list_words(control.hidratacion, 35)
                supplement = self._get_list_words((control.sup_vit + '/' if control.sup_vit else '') + (control.sup_prt if control.sup_prt else '') , 220)
                
                rml += """
                            <spacer length="0.2cm"/>
                            <blockTable colWidths="70.0,50.0,20.0,60.0,215.0,50.0,50.0" rowHeights="10.0,10.0,45.0,30.0" style="Table7">
                                <tr>
                                    <td>
                                        <blockTable rowHeights="15.0,6.0">
                                            <tr><td><para style="P6_BOLD_CENTER">Fecha</para></td></tr>
                                            <tr><td><para style="P6_CENTER">""" + (fecha if fecha else '') + """</para></td></tr>
                                        </blockTable>
                                    </td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('Control N°') + """</para></td>
                                    <td><para style="P6_LEFT">""" + (str(control.cita) if control.cita else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">Tipo de dieta</para></td>
                                    <td><para style="P6_LEFT">""" + (tools.ustr(control.tip_dta) if control.tip_dta else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">Vitaminas/Suplemento</para></td>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('Catacterísticas de la dieta') + """</para></td>
                                    <td>
                                        <blockTable colWidths="50.0,300.0" rowHeights="" style="TableX">
                                            <tr>
                                                <td><para style="P6_BOLD_CENTER"> </para></td>
                                                <td><para style="P5_COURIER_JUSTIFY">""" + (tools.ustr(control.car_die) if control.car_die else '') + """</para></td>
                                            </tr>
                                        </blockTable>
                                    </td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td></td>
                                    <td><para style="P5_COURIER_JUSTIFY">""" + (tools.ustr(supplement[0]) if len(supplement) >=1 else '') + """</para></td>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">Observaciones</para></td>
                                    <td>
                                        <blockTable colWidths="190.0,60.0,100.0" rowHeights="15.0,8.0" style="TableY">
                                            <tr>
                                                <td><para style="P5_COURIER_JUSTIFY">""" + (tools.ustr(observ[0]) if len(observ) >= 1 else '') + """</para></td>
                                                <td></td>
                                                <td></td>
                                            </tr>
                                            <tr>
                                                <td></td>
                                                <td><para style="P6_BOLD_CENTER">""" + tools.ustr('Hidratación:') + """</para></td>
                                                <td><para style="P5_COURIER_JUSTIFY">""" + (tools.ustr(hydration[0]) if len(hydration) >= 1 else '') + """</para></td>
                                            </tr>
                                        </blockTable>
                                    </td>
                                    <td></td><td></td><td></td>
                                    <td>
                                        <blockTable colWidths="" rowHeights="">
                                            <tr>
                                                <td><para style="P5_LEFT">""" + tools.ustr('Ejercicio:') + """</para></td>
                                                <td><para style="P5_COURIER_JUSTIFY">""" + (tools.ustr(control.eje_prc) if control.eje_prc else '') + """</para></td>
                                            </tr>
                                            <tr>
                                                <td><para style="P5_LEFT">""" + tools.ustr('N° veces: ') + (str(control.eje_freq) if control.eje_freq and control.eje_freq != 0 else '') + """</para></td>
                                                <td><para style="P5_LEFT">""" + (tools.ustr('Tiempo: ') + tools.ustr(control.tie_eje) if control.tie_eje and control.tie_eje != 0 else '') + """</para></td>
                                            </tr>
                                        </blockTable>
                                    </td>
                                    <td></td>
                                </tr>
                            </blockTable>"""
            
            i = 1
            maxCant = 0
            
            while True:
                if cant > 7 * i: 
                    maxCant = 7 * i+1
                    i = i + 1
                else: 
                    maxCant = 7 * i
                    break
            
            while cant < maxCant:
                cant = cant + 1
                rml += """  <condPageBreak height="100"/>"""
                rml += """
                            <spacer length="0.2cm"/>
                            <blockTable colWidths="70.0,50.0,20.0,60.0,215.0,50.0,50.0" rowHeights="10.0,10.0,45.0,30.0" style="Table7">
                                <tr>
                                    <td>
                                        <blockTable rowHeights="15.0,6.0">
                                            <tr><td><para style="P6_BOLD_CENTER">Fecha</para></td></tr>
                                            <tr><td><para style="P6_CENTER"></para></td></tr>
                                        </blockTable>
                                    </td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('Control N°') + """</para></td>
                                    <td><para style="P6_LEFT"></para></td>
                                    <td><para style="P6_BOLD_CENTER">Tipo de dieta</para></td>
                                    <td><para style="P6_LEFT"></para></td>
                                    <td><para style="P6_BOLD_CENTER">Vitaminas/Suplemento</para></td>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('Catacterísticas de la dieta') + """</para></td>
                                    <td>
                                        <blockTable colWidths="50.0,300.0" rowHeights="" style="TableX">
                                            <tr>
                                                <td><para style="P6_BOLD_CENTER"> </para></td>
                                                <td><para style="P6_LEFT"></para></td>
                                            </tr>
                                        </blockTable>
                                    </td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td></td>
                                    <td><para style="P5_LEFT"></para></td>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">Observaciones</para></td>
                                    <td>
                                        <blockTable colWidths="190.0,60.0,100.0" rowHeights="15.0,8.0" style="TableY">
                                            <tr>
                                                <td><para style="P5_LEFT"></para></td>
                                                <td></td>
                                                <td></td>
                                            </tr>
                                            <tr>
                                                <td></td>
                                                <td><para style="P6_BOLD_CENTER">""" + tools.ustr('Hidratación:') + """</para></td>
                                                <td><para style="P6_LEFT"></para></td>
                                            </tr>
                                        </blockTable>
                                    </td>
                                    <td></td><td></td><td></td>
                                    <td>
                                        <blockTable colWidths="" rowHeights="">
                                            <tr>
                                                <td><para style="P5_LEFT">""" + tools.ustr('Ejercicio:') + """</para></td>
                                                <td><para style="P5_LEFT"></para></td>
                                            </tr>
                                            <tr>
                                                <td><para style="P5_LEFT">""" + tools.ustr('N° veces: ') + """</para></td>
                                                <td><para style="P5_LEFT">""" + tools.ustr('Tiempo: ') + """</para></td>
                                            </tr>
                                        </blockTable>
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
        
        for path in list_to_delete:
            os.remove(path)
        
        return (pdf, report_type)
    
    def _get_year(self, record):
        if (record.dob):
            now = datetime.now()
            dob = datetime.strptime(str(record.dob), '%Y-%m-%d')
            delta = relativedelta(now, dob)
            return delta.years
    
    def _get_list_words(self, data, size):
        if not data: return []
        text = data.replace('\n', ' ')
        if len(text) <= size: return [text]
        
        text = text.split(' ')
        word_list = []
        temp = ''
        
        for x in xrange(len(text)):
            if len(temp) + len(text[x]) + 1 <= size:
                if text[x] != ' ': temp += text[x] + ' '
            else:
                word_list.append(temp)
                temp = ''
            
            if x == len(text) - 1: word_list.append(temp)
        return word_list
    
oemedical_nutritional_report('report.oemedical_nutritional_report', 'oemedical.nutritional', '', '')
