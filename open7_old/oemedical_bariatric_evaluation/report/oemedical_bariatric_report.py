# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
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

import os
import string
import openerp

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import pooler, tools
from openerp.report import report_sxw
from openerp.report.interface import report_rml

from openerp.tools import to_xml
from openerp.tools.translate import _

class oemedical_bariatric_report(report_rml):
    def create(self, cr, uid, ids, datas, context):
        bariatric_obj = pooler.get_pool(cr.dbname).get('oemedical.bariatric.evaluation')
        company_obj = pooler.get_pool(cr.dbname).get('res.company')
        company_ids_list = company_obj.search(cr, uid, [], context=context)
        company = company_obj.browse(cr, uid, company_ids_list[0], context) if len(company_ids_list) > 0 else False
        
        for bariatric in bariatric_obj.browse(cr, uid, ids, context):
            
            rml = """   <document filename="test.pdf">
                            <template pageSize="(595.0,842.0)" title=" """ + _("Bariatric Report") + """ " author="Reynaldo Rodriguez Cruz" allowSplitting="20">
                                <pageTemplate id="page1">
                                    <frame id="first" x1="47.0" y1="50.0" width="500" height="730"/>
                                </pageTemplate>
                            </template>"""
            
            rml += """
                            <stylesheet>
                                <blockTableStyle id="Table">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                
                                    <blockBackground colorName="#F7DCE9" start="0,0" stop="-1,0"/>
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table01">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table_12">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                  
                                    <blockBackground colorName="#E6FAE9" start="0,0" stop="-1,0"/>
                                </blockTableStyle> 
                                
                                <blockTableStyle id="Table_13">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                  
                                    <blockBackground colorName="#F7DCE9" start="0,0" stop="-1,0"/>
                                </blockTableStyle>                                                  
                                
                                <blockTableStyle id="Table_14">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                  
                                    <blockBackground colorName="#F7DCE9" start="0,0" stop="0,0"/>
                                    <blockBackground colorName="#F7DCE9" start="2,0" stop="2,0"/>
                                    <blockBackground colorName="#F7DCE9" start="4,0" stop="4,0"/>
                                    <blockBackground colorName="#F7DCE9" start="6,0" stop="6,0"/>
                                    
                                </blockTableStyle> 
                                
                                <blockTableStyle id="Table_141">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                  
                                    <blockBackground colorName="#E6FAE9" start="0,0" stop="0,0"/>
                                    <blockBackground colorName="#E6FAE9" start="2,0" stop="2,0"/>
                                    <blockBackground colorName="#E6FAE9" start="4,0" stop="4,0"/>
                                    <blockBackground colorName="#E6FAE9" start="6,0" stop="6,0"/>
                                    
                                </blockTableStyle>  
                                 
                                
                                <blockTableStyle id="Table_15">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                  
                                    <blockBackground colorName="#F7DCE9" start="0,0" stop="0,-1"/>
                                    
                                </blockTableStyle>                                                  
                                                                                
                                <blockTableStyle id="Table_16">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                  
                                    <blockBackground colorName="#E6FAE9" start="0,0" stop="0,0"/>
                                    <blockBackground colorName="#E6FAE9" start="4,0" stop="4,0"/>
                                    <blockBackground colorName="#FAF9C8" start="2,0" stop="3,0"/>
                                    <blockBackground colorName="#FAF9C8" start="6,0" stop="7,0"/>
                                    <blockBackground colorName="#EBEAE4" start="1,0" stop="1,0"/>
                                    <blockBackground colorName="#EBEAE4" start="5,0" stop="5,0"/>
                                
                                </blockTableStyle>                                                  
                                
                                
                                <blockTableStyle id="Table_1">
                                    <blockValign value="TOP" start="0,0" stop="0,0"/>
                                    <blockValign value="MIDDLE" start="1,0" stop="-1,-1"/>                                    
                                    <blockAlignment value="LEFT"/>
                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <blockSpan start="0,0" stop="0,-1"/>
                                    
                                    <blockBackground colorName="#F7DCE9" start="1,0" stop="1,0"/>
                                    <blockBackground colorName="#F7DCE9" start="1,2" stop="1,2"/>
                                    <blockBackground colorName="#F7DCE9" start="1,4" stop="1,4"/>
                                    <blockBackground colorName="#F7DCE9" start="1,6" stop="1,6"/>
                                    <blockBackground colorName="#F7DCE9" start="1,8" stop="1,8"/>
                                    
                                    <blockBackground colorName="#F7DCE9" start="2,0" stop="2,11"/>
                                    <blockBackground colorName="#F7DCE9" start="2,12" stop="8,12"/>
                                    <blockBackground colorName="#F7DCE9" start="2,14" stop="8,14"/>
                                    <blockBackground colorName="#F7DCE9" start="2,16" stop="8,16"/>
                                    
                                    <blockBackground colorName="#F7DCE9" start="4,0" stop="4,9"/>
                                    
                                    <blockBackground colorName="#F7DCE9" start="6,0" stop="8,0"/>
                                    <blockBackground colorName="#F7DCE9" start="6,2" stop="8,2"/>
                                    <blockBackground colorName="#F7DCE9" start="6,4" stop="8,4"/>
                                    <blockBackground colorName="#F7DCE9" start="6,6" stop="8,6"/>
                                    <blockBackground colorName="#F7DCE9" start="6,8" stop="8,8"/>
                                    <blockBackground colorName="#F7DCE9" start="6,10" stop="8,10"/>
                                    
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table_11">                                    
                                    <blockValign value="MIDDLE"/>                                    
                                    <blockAlignment value="LEFT"/>
                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#FAFAFA" start="0,0" stop="0,0" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="1,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <blockSpan start="0,0" stop="0,-1"/>
                                    
                                    <blockBackground colorName="#F7DCE9" start="2,0" stop="6,0"/>
                                    <blockBackground colorName="#F7DCE9" start="2,2" stop="5,2"/>
                                    <blockBackground colorName="#F7DCE9" start="2,4" stop="5,4"/>
                                    <blockBackground colorName="#F7DCE9" start="2,6" stop="5,6"/>
                                    <blockBackground colorName="#F7DCE9" start="2,8" stop="6,8"/>
                                    
                                    <blockBackground colorName="#FAF9C8" start="2,9" stop="-1,-1"/>
                                    
                                    
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table_112">                                    
                                    <blockValign value="MIDDLE"/>                                    
                                    <blockAlignment value="LEFT"/>
                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#FAFAFA" start="0,0" stop="0,0" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="1,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <blockBackground colorName="#FAF9C8" start="2,0" stop="-1,-1"/>
                                    <blockSpan start="0,0" stop="0,-1"/>
                                
                                </blockTableStyle>
                                
                                
                                <blockTableStyle id="Table1">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>
                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    
                                    <blockSpan start="2,0" stop="3,0"/>
                                    <blockSpan start="4,0" stop="5,0"/>
                                    
                                    <blockSpan start="2,1" stop="3,1"/>
                                    <blockSpan start="4,1" stop="5,1"/>
                                    
                                    <blockSpan start="0,2" stop="1,2"/>
                                    <blockSpan start="0,3" stop="1,3"/>
                                    
                                    <blockSpan start="3,2" stop="5,2"/>
                                    <blockSpan start="3,3" stop="5,3"/>
                                    
                                    <blockSpan start="6,2" stop="7,2"/>
                                    <blockSpan start="6,3" stop="7,3"/>
                                    
                                    <blockSpan start="3,4" stop="5,4"/>
                                    <blockSpan start="3,5" stop="5,5"/>
                                    
                                    <blockSpan start="6,4" stop="7,4"/>
                                    <blockSpan start="6,5" stop="7,5"/>
                                    
                                    <blockSpan start="2,6" stop="3,6"/>
                                    <blockSpan start="6,6" stop="7,6"/>
                                    
                                    <blockSpan start="2,7" stop="3,7"/>
                                    <blockSpan start="6,7" stop="7,7"/>
                                    
                                    <blockSpan start="0,8" stop="1,8"/>
                                    <blockSpan start="2,8" stop="3,8"/>
                                    <blockSpan start="4,8" stop="5,8"/>
                                    <blockSpan start="6,8" stop="7,8"/>
                                    
                                    <blockSpan start="0,9" stop="1,9"/>
                                    <blockSpan start="2,9" stop="3,9"/>
                                    <blockSpan start="4,9" stop="5,9"/>
                                    <blockSpan start="6,9" stop="7,9"/>
                                    
                                    <blockBackground colorName="#E6FAE9" start="0,0" stop="-1,0"/>
                                    
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table2">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table3">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>
                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    
                                    <blockBackground colorName="#F0A9C4" start="0,0" stop="-1,0"/>
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table4">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>
                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    
                                    <blockBackground colorName="#F0A9C4" start="0,0" stop="0,0"/>                                    
                                    <blockBackground colorName="#F7DCE9" start="0,1" stop="0,1"/> 
                                    <blockBackground colorName="#F7DCE9" start="0,3" stop="0,3"/>                                    
                                    
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table5">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>
                                    <blockSpan start="0,0" stop="0,1"/>
                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                
                                    <blockBackground colorName="#F7DCE9" start="0,0" stop="0,0"/>
                                    <blockBackground colorName="#F7DCE9" start="1,0" stop="1,0"/>
                                    <blockBackground colorName="#F7DCE9" start="3,0" stop="3,0"/>
                                    <blockBackground colorName="#F7DCE9" start="5,0" stop="5,0"/>
                                    <blockBackground colorName="#F7DCE9" start="7,0" stop="7,0"/>
                                    
                                    <blockBackground colorName="#F7DCE9" start="0,1" stop="0,1"/>
                                    <blockBackground colorName="#F7DCE9" start="1,1" stop="1,1"/>
                                    <blockBackground colorName="#F7DCE9" start="3,1" stop="3,1"/>
                                    <blockBackground colorName="#F7DCE9" start="5,1" stop="5,1"/>
                                    <blockBackground colorName="#F7DCE9" start="7,1" stop="7,1"/>
                               
                               
                                </blockTableStyle>
                                
                                <blockTableStyle id="Table6">
                                    <blockValign value="MIDDLE"/>
                                    <blockAlignment value="CENTER"/>
                                    <blockBackground colorName="#F0A9C4" start="0,0" stop="-1,0"/>
                                    
                                    <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                    <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                </blockTableStyle>
                                
                                <initialize>
                                    <paraStyle name="all" alignment="justify"/>
                                </initialize>
                                
                                <paraStyle name="P5_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="5.0" leading="8" alignment="CENTER"/>
                                
                                <paraStyle name="P6_BOLD" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="JUSTIFY"/>
                                <paraStyle name="P6_BOLD_CENTER" fontName="Helvetica-Bold" fontSize="5.5" leading="8" alignment="CENTER"/>
                                <paraStyle name="P6_BOLD_LEFT" fontName="Helvetica" fontSize="5.5" leading="8" alignment="LEFT" vAlign="TOP"/>
                                <paraStyle name="P6_LEFT" fontName="Helvetica" fontSize="5.5" leading="8" alignment="LEFT" vAlign="TOP"/>
                                <paraStyle name="P6_CENTER" fontName="Helvetica" fontSize="5.5" leading="8" alignment="CENTER" vAlign="TOP"/>
                                
                                <paraStyle name="P7_COURIER" fontName="Courier" fontSize="7.0" leading="8" alignment="JUSTIFY"/>
                                <paraStyle name="P7_COURIER_CENTER" fontName="Courier" fontSize="7.0" leading="8" alignment="CENTER"/>
                                
                                <paraStyle name="P8_COURIER" fontName="Courier" fontSize="8.0" leading="8" alignment="JUSTIFY"/>
                                <paraStyle name="P8_COURIER_LEFT" fontName="Courier" fontSize="8.0" leading="8" alignment="LEFT"/>
                                <paraStyle name="P8_COURIER_CENTER" fontName="Courier" fontSize="8.0" leading="8" alignment="CENTER"/>
                            </stylesheet>"""
            
            rml += """      <story>"""
            
            dob = bariatric.patient_id.dob if bariatric.patient_id.dob else ''
            if dob: 
                dob = dob.split('-')
                if len(dob) > 2:
                    dob = dob[2] + '/' + dob[1] + '/' + dob[0]
                    
            eva_date = bariatric.eva_date if bariatric.eva_date else ''
            if eva_date: 
                tmp = eva_date.split('-')
                if len(tmp) > 2:
                    eva_date = tmp[2] + '/' + tmp[1] + '/' + tmp[0]            
            
            marital_status = False
            if bariatric.patient_id.marital_status:
                if bariatric.patient_id.marital_status == 's': marital_status = _('Soltero(a)')
                if bariatric.patient_id.marital_status == 'm': marital_status = _('Casado(a)')
                if bariatric.patient_id.marital_status == 'w': marital_status = _('Viudo(a)')
                if bariatric.patient_id.marital_status == 'd': marital_status = _('Divorciado(a)')
                if bariatric.patient_id.marital_status == 'x': marital_status = _('Separado(a)')
                if bariatric.patient_id.marital_status == 'z': marital_status = _('Unión libre')
            
            first_name = ''
            second_name = ''
            
            if bariatric.patient_id.first_name:
                names = bariatric.patient_id.first_name.split(' ')
                if len(names) >= 1:
                    first_name = names[0]
                if len(names) >= 2:
                    second_name = names[1]                    
            
            first_lastname = ''
            second_lastname = ''
            
            if bariatric.patient_id.last_name:
                names = bariatric.patient_id.last_name.split(' ')
                if len(names) >= 1:
                    first_lastname = names[0]
                if len(names) >= 2:
                    second_lastname = names[1]                    
            
            
            rml += """      <blockTable colWidths="80.0,100.0,64.0,50.0,50.0,50.0,30.0,100.0" style="Table1">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('FECHA DE ATENCIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">ESTABLECIMIENTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">NOMBRES</para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER">APELLIDOS</para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER">SEXO</para></td>
                                    <td><para style="P6_BOLD_CENTER">CEDULA DE IDENTIDAD</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr(eva_date) + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(company.name) if company else "")  + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr(first_name) + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr(second_name) + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr(first_lastname)  + " " + (tools.ustr(bariatric.patient_id.slastname) if bariatric.patient_id.slastname else "") + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr(second_lastname) + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('M' if bariatric.patient_id.sex == 'm' else 'F') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (bariatric.patient_id.cedula if getattr(bariatric.patient_id, 'cedula', False) else '') + """</para></td>
                                </tr>
                            </blockTable>"""
                            
            rml += """      <blockTable colWidths="180.0,64.0,150.0,130.0" style="Table_12">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DIRECCIÓN DOMICILIARIA') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CIUDAD</para></td>
                                    <td><para style="P6_BOLD_CENTER">FECHA DE NACIMIENTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">EDAD</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.patient_id.street) if bariatric.patient_id.street else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.patient_id.city) if bariatric.patient_id.city else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (dob if dob else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + str(self._get_year(bariatric.patient_id)) + tools.ustr(' años') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.patient_id.phone and not bariatric.patient_id.mobile and not bariatric.patient_id.occupation and not bariatric.patient_id.email:
                rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,100.0,64.0,150.0,130.0" rowHeights=" """ + rowHeights + """ " style="Table_12">"""
            else: 
                rml += """      <blockTable colWidths="80.0,100.0,64.0,150.0,130.0" style="Table_12">"""
            
            rml += """      <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('TELEFONOS DOMICI.') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CELULAR</para></td>
                                    <td><para style="P6_BOLD_CENTER">CELULAR FAMILIAR</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('OCUPACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CORREO</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.patient_id.phone) if bariatric.patient_id.phone else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.patient_id.mobile) if bariatric.patient_id.mobile else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr('') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.patient_id.occupation.name) if bariatric.patient_id.occupation else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.patient_id.email) if bariatric.patient_id.email else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not marital_status and not bariatric.patient_id.cmp_pac:
                rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,100.0,64.0,50.0,50.0,50.0,65.0,65.0" rowHeights=" """ + rowHeights + """ " style="Table_12">"""
            else: 
                rml += """      <blockTable colWidths="80.0,100.0,64.0,50.0,50.0,50.0,65.0,65.0" style="Table_12">"""
            
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('ESTADO CIVIL') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">EMPRESA</para></td>
                                    <td><para style="P6_BOLD_CENTER">DIR. EMPRESA</para></td>
                                    <td><para style="P6_BOLD_CENTER">TELEFONOS</para></td>
                                    <td><para style="P6_BOLD_CENTER">EXT</para></td>
                                    <td><para style="P6_BOLD_CENTER">CIUDAD</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DIRECCIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">INGRESOS</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(marital_status) if marital_status else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.patient_id.cmp_pac) if bariatric.patient_id.cmp_pac else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER"></para></td>
                                    <td><para style="P7_COURIER_CENTER"></para></td>
                                    <td><para style="P7_COURIER_CENTER"></para></td>
                                    <td><para style="P7_COURIER_CENTER"></para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr('') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER"></para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = '15.0,15.0'
            
            rml += """      <blockTable colWidths="180.0,114.0,100.0,130.0" rowHeights=" """ + rowHeights + """ " style="Table_12"> 
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('REFERENCIA') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('LUGAR DE NACIMIENTO') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('LUGAR DE RESIDENCIA') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('OTROS') + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr(' ') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr('') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr('') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + tools.ustr('') + """</para></td>
                                </tr>
                            </blockTable>"""
                                
            letters_per_row = 106
            word_list = []
            
            rowHeights = '15.0'
            if bariatric.mot_cta:
                strMDC = bariatric.mot_cta.replace('\n',' ')
                if len(strMDC) > 106:
                    filaAlto = 1 
                    tmp = len(strMDC)/106            
                    filaAlto = tmp + 1 if len(strMDC) % 106 != 0 else tmp
                    rowHeights += ',' + str(15.0 * filaAlto)                     
                else:
                    rowHeights += ',15.0'
            else:
                rowHeights += ',15.0'
            
            rml += """  <blockTable colWidths="524.0" rowHeights=" """ + rowHeights + """ " style="Table3">"""
            
            rml += """     <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('1. MOTIVO DE CONSULTA') + """</para></td></tr>
                           <tr><td><para style="P8_COURIER_LEFT">""" + (tools.ustr(bariatric.mot_cta) if bariatric.mot_cta else '' ) + """</para></td></tr>
                        </blockTable>"""            
            
            rowHeights = '15.0,15.0'
            if bariatric.ant_qur:
                strMDC = bariatric.ant_qur.replace('\n',' ')
                if len(strMDC) > 106:
                    filaAlto = 1 
                    tmp = len(strMDC)/106            
                    filaAlto = tmp + 1 if len(strMDC) % 106 != 0 else tmp
                    rowHeights += ',' + str(15.0 * filaAlto)                     
                else:
                    rowHeights += ',15.0'
            else:
                rowHeights += ',15.0'            
            rowHeights += ',15.0'    
            
            rml += """      <blockTable colWidths="524.0" rowHeights=" """ + rowHeights + """ " style="Table4">"""
            
            rml += """          <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('2. ANTECEDENTES PERSONALES') + """</para></td></tr>
                                <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('QUIRÚRGICOS') + """</para></td></tr>
                                <tr><td><para style="P8_COURIER_LEFT">""" + (tools.ustr(bariatric.ant_qur) if bariatric.ant_qur else '' ) + """</para></td></tr>
                                <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('GINECOLÓGICOS') + """</para></td></tr>
                            </blockTable>"""            
            
            fum_date = False
            if bariatric.ang_fum:
                temp = bariatric.ang_fum.split('-')
                if len(temp) >= 3:
                    fum_date = temp[2] + '/' + temp[1] + '/' + temp[0]
            
            rowHeights = ''
            if not bariatric.ang_g and not bariatric.ang_p and not bariatric.ang_c and not bariatric.ang_a and not bariatric.ang_hv and not fum_date and not bariatric.ang_ant:
                rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,100.0,64.0,50.0,50.0,50.0,130.0" rowHeights=" """ + rowHeights + """ " style="Table_13">"""
            else: 
                rml += """      <blockTable colWidths="80.0,100.0,64.0,50.0,50.0,50.0,130.0" style="Table_13">"""
            
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">G:</para></td>
                                    <td><para style="P6_BOLD_CENTER">P:</para></td>
                                    <td><para style="P6_BOLD_CENTER">C:</para></td>
                                    <td><para style="P6_BOLD_CENTER">A:</para></td>
                                    <td><para style="P6_BOLD_CENTER">HV:</para></td>
                                    <td><para style="P6_BOLD_CENTER">FUM:</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('ANTICONCEPCIÓN:') + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + (str(bariatric.ang_g) if bariatric.ang_g else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.ang_p) if bariatric.ang_p else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.ang_c) if bariatric.ang_c else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.ang_a) if bariatric.ang_a else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.ang_hv) if bariatric.ang_hv else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (fum_date if fum_date else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.ang_ant) if bariatric.ang_ant else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="524.0" style="Table_13">
                                <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('CLINICOS') + """</para></td></tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">HTA SI:</para></td>
                                    <td><para style="P6_BOLD_CENTER">HTA NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('MEDICACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_hta and not bariatric.anc_hdr and not bariatric.anc_hto and not bariatric.anc_hmd and not bariatric.anc_hdc:
                rowHeights = '15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" rowHeights=" """ + rowHeights + """ " style="Table01">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table01">"""
            
            rml += """          <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_hta == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_hta == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_hdr) if bariatric.anc_hdr else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_hto) if bariatric.anc_hto else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_hmd) if bariatric.anc_hmd else '') + """</para></td>
                                    <td><para style="P8_COURIER">""" + (tools.ustr(bariatric.anc_hdc) if bariatric.anc_hdc else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">DM SI:</para></td>
                                    <td><para style="P6_BOLD_CENTER">DM NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('MEDICACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_dm and not bariatric.anc_ddr and not bariatric.anc_dto and not bariatric.anc_dmd and not bariatric.anc_ddc:
                rowHeights = '15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" rowHeights=" """ + rowHeights + """ " style="Table01">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table01">"""
            
            rml += """          <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_dm == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_dm == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_ddr) if bariatric.anc_ddr else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_dto) if bariatric.anc_dto else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_dmd) if bariatric.anc_dmd else '') + """</para></td>
                                    <td><para style="P8_COURIER">""" + (tools.ustr(bariatric.anc_ddc) if bariatric.anc_ddc else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">DLP SI:</para></td>
                                    <td><para style="P6_BOLD_CENTER">DLP NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('MEDICACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_dlp and not bariatric.anc_ldr and not bariatric.anc_lto and not bariatric.anc_lmd and not bariatric.anc_ldc:
                rowHeights = '15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" rowHeights=" """ + rowHeights + """ " style="Table01">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table01">"""
            
            rml += """          <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_dlp == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_dlp == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_ldr) if bariatric.anc_ldr else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_lto) if bariatric.anc_lto else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_lmd) if bariatric.anc_lmd else '') + """</para></td>
                                    <td><para style="P8_COURIER">""" + (tools.ustr(bariatric.anc_ldc) if bariatric.anc_ldc else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">APNEA SI:</para></td>
                                    <td><para style="P6_BOLD_CENTER">APNEA NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('MEDICACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_apn and not bariatric.anc_adr and not bariatric.anc_ato and not bariatric.anc_amd and not bariatric.anc_adc:
                rowHeights  = '15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" rowHeights=" """ + rowHeights + """ " style="Table01">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table01">"""
            
            rml += """          <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_apn == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_apn == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_adr) if bariatric.anc_adr else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_ato) if bariatric.anc_ato else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_amd) if bariatric.anc_amd else '') + """</para></td>
                                    <td><para style="P8_COURIER">""" + (tools.ustr(bariatric.anc_adc) if bariatric.anc_adc else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">OSTEOARTRITIS SI:</para></td>
                                    <td><para style="P6_BOLD_CENTER">OSTEOARTRITIS NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('MEDICACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_ost and not bariatric.anc_odr and not bariatric.anc_oto and not bariatric.anc_omd and not bariatric.anc_odc:
                rowHeights = rowHeights = '15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" rowHeights=" """ + rowHeights + """ " style="Table01">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table01">"""
            
            rml += """          <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_ost == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_ost == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_odr) if bariatric.anc_odr else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_oto) if bariatric.anc_oto else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_omd) if bariatric.anc_omd else '') + """</para></td>
                                    <td><para style="P8_COURIER">""" + (tools.ustr(bariatric.anc_odc) if bariatric.anc_odc else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">SOP SI:</para></td>
                                    <td><para style="P6_BOLD_CENTER">SOP NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('MEDICACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_sop and not bariatric.anc_sdr and not bariatric.anc_sto and not bariatric.anc_smd and not bariatric.anc_sdc:
                rowHeights = '15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" rowHeights=" """ + rowHeights + """ " style="Table01">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table01">"""
            
            rml += """          <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_sop == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_sop == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_sdr) if bariatric.anc_sdr else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_sto) if bariatric.anc_sto else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_smd) if bariatric.anc_smd else '') + """</para></td>
                                    <td><para style="P8_COURIER">""" + (tools.ustr(bariatric.anc_sdc) if bariatric.anc_sdc else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">OTROS SI:</para></td>
                                    <td><para style="P6_BOLD_CENTER">OTROS NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('MEDICACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_otr and not bariatric.anc_rdr and not bariatric.anc_rto and not bariatric.anc_rmd and not bariatric.anc_rdc:
                rowHeights = '15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" rowHeights=" """ + rowHeights + """ " style="Table01">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table01">"""
            
            rml += """          <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_otr == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_otr == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_rdr) if bariatric.anc_rdr else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_rto) if bariatric.anc_rto else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_rmd) if bariatric.anc_rmd else '') + """</para></td>
                                    <td><para style="P8_COURIER">""" + (tools.ustr(bariatric.anc_rdc) if bariatric.anc_rdc else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">OTROS SI:</para></td>
                                    <td><para style="P6_BOLD_CENTER">OTROS NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('MEDICACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,80.0,64.0,50.0,70.0,180.0" rowHeights = "15.0" style="Table01">"""
            
            rml += """          <tr>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER"></para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_tab and not bariatric.anc_alc and not bariatric.anc_drg and not bariatric.anc_tad:
                rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,64.0,50.0,56.0,130.0" rowHeights=" """ + rowHeights + """ " style="Table_13">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,64.0,50.0,56.0,130.0" style="Table_13">"""
            
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">TABACO SI</para></td>
                                    <td><para style="P6_BOLD_CENTER">TABACO NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">ALCOHOL SI</para></td>
                                    <td><para style="P6_BOLD_CENTER">ALCOHOL NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">DROGAS SI</para></td>
                                    <td><para style="P6_BOLD_CENTER">DROGAS NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">COMENTARIOS</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_tab == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_tab == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_alc == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_alc == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_drg == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_drg == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_tad) if bariatric.anc_tad else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="80.0,50.0,44.0,81.0,50.0,44.0,81.0,50.0,44.0" rowHeights="15.0,15.0,15.0" style="Table_13">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">MEDICAMENTOS</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                    <td><para style="P6_BOLD_CENTER">TIEMPO</para></td>
                                    <td><para style="P6_BOLD_CENTER">MEDICAMENTOS</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                    <td><para style="P6_BOLD_CENTER">TIEMPO</para></td>
                                    <td><para style="P6_BOLD_CENTER">MEDICAMENTOS</para></td>
                                    <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                    <td><para style="P6_BOLD_CENTER">TIEMPO</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                    <td><para style="P8_COURIER_CENTER"></para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anc_tab and not bariatric.anc_alc and not bariatric.anc_drg and not bariatric.anc_tad:
                rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="80.0,80.0,64.0,64.0,50.0,56.0,130.0" rowHeights=" """ + rowHeights + """ " style="Table">"""
            else: 
                rml += """      <blockTable colWidths="80.0,80.0,64.0,64.0,50.0,56.0,130.0" style="Table_13">"""
            
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">TABACO SI</para></td>
                                    <td><para style="P6_BOLD_CENTER">TABACO NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">ALCOHOL SI</para></td>
                                    <td><para style="P6_BOLD_CENTER">ALCOHOL NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">DROGAS SI</para></td>
                                    <td><para style="P6_BOLD_CENTER">DROGAS NO</para></td>
                                    <td><para style="P6_BOLD_CENTER">COMENTARIOS</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_tab == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_tab == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_alc == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_alc == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_drg == 's' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + ('X' if bariatric.anc_drg == 'n' else '') + """</para></td>
                                    <td><para style="P8_COURIER_CENTER">""" + (tools.ustr(bariatric.anc_tad) if bariatric.anc_tad else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="524.0" style="Table3">
                                <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('3. ANTECEDENTES FAMILIARES') + """</para></td></tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.anf_pdr and not bariatric.anf_mdr and not bariatric.anf_hrm and not bariatric.anf_hij and not bariatric.anf_abp and not bariatric.anf_aap and not bariatric.anf_abm and not bariatric.anf_aam and not bariatric.anf_otr:
                rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="58.2,58.2,58.2,58.2,58.2,58.2,58.2,58.2,58.4" rowHeights=" """ + rowHeights + """ " style="Table_13">"""
            else: 
                rml += """      <blockTable colWidths="58.2,58.2,58.2,58.2,58.2,58.2,58.2,58.2,58.4" style="Table_13">"""
            
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">PADRE</para></td>
                                    <td><para style="P6_BOLD_CENTER">MADRE</para></td>
                                    <td><para style="P6_BOLD_CENTER">HERMANOS</para></td>
                                    <td><para style="P6_BOLD_CENTER">HIJOS</para></td>
                                    <td><para style="P6_BOLD_CENTER">ABUELO P</para></td>
                                    <td><para style="P6_BOLD_CENTER">ABUELA P</para></td>
                                    <td><para style="P6_BOLD_CENTER">ABUELO M</para></td>
                                    <td><para style="P6_BOLD_CENTER">ABUELA M</para></td>
                                    <td><para style="P6_BOLD_CENTER">OTROS</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_pdr) if bariatric.anf_pdr else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_mdr) if bariatric.anf_mdr else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_hrm) if bariatric.anf_hrm else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_hij) if bariatric.anf_hij else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_abp) if bariatric.anf_abp else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_aap) if bariatric.anf_aap else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_abm) if bariatric.anf_abm else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_aam) if bariatric.anf_aam else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.anf_otr) if bariatric.anf_otr else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="524.0" style="Table3">
                                <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('4. ENFERMEDAD O PROBLEMA ACTUAL') + """</para></td></tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table_14">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">APARECIMIENTO</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_apa) if bariatric.epa_apa else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">LUGAR</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_lug) if bariatric.epa_lug else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">INTENSIDAD</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_int) if bariatric.epa_int else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('ACOMPAÑANTE') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_aco) if bariatric.epa_aco else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = '15.0'
            if bariatric.epa_rea:
                strMDC = bariatric.epa_rea.replace('\n',' ')
                if len(strMDC) > 106:
                    filaAlto = 1 
                    tmp = len(strMDC)/106            
                    filaAlto = tmp + 1 if len(strMDC) % 106 != 0 else tmp
                    rowHeights = str(15.0 * filaAlto)                     
            
            rml += """      <blockTable colWidths="70.5,453.5" rowHeights=" """  + rowHeights + """ " style="Table_15">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('RELACIÓN A:') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.epa_rea) if bariatric.epa_rea else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table_14">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">DIETA</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('Si' if bariatric.epa_die and bariatric.epa_die == 's'  else 'No') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CUAL</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_cdi) if bariatric.epa_cdi else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_ddi) if bariatric.epa_ddi else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">RESULTADO</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_dre) if bariatric.epa_dre else '') + """</para></td>
                                </tr>
                            </blockTable>
                            <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table_14">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">EJERCICIO</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('Si' if bariatric.epa_eje and bariatric.epa_eje == 's'  else 'No') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CUAL</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_cej) if bariatric.epa_cej else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_dej) if bariatric.epa_dej else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">RESULTADO</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_rej) if bariatric.epa_rej else '') + """</para></td>
                                </tr>
                            </blockTable>
                            <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table_14">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">MEDICAMENTOS</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('Si' if bariatric.epa_med and bariatric.epa_med == 's'  else 'No') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CUAL</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_cme) if bariatric.epa_cme else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_dme) if bariatric.epa_dme else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">RESULTADO</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_rme) if bariatric.epa_rme else '') + """</para></td>
                                </tr>
                            </blockTable>
                            <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table_14">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">NUTRICIONISTA</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('Si' if bariatric.epa_med and bariatric.epa_med == 's'  else 'No') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CUAL</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_cnu) if bariatric.epa_cnu else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('DURACIÓN') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_dnu) if bariatric.epa_dnu else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">RESULTADO</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_rnu) if bariatric.epa_rnu else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table5">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('ALIMENTACIÓN') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">FRECUENCIA</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_afr) if bariatric.epa_afr else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">SAL</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + ('X' if bariatric.epa_sal else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">DULCE</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + ('X' if bariatric.epa_dul else '') + """</para></td>
                                    <td><para style="P6_BOLD">PICADORA """ + ('X' if bariatric.epa_pic else '') + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER">ATRACONES</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + ('X' if bariatric.epa_atr else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">ANSIEDAD</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + ('X' if bariatric.epa_ans else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">VOMITOS</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + ('X' if bariatric.epa_vom else '') + """</para></td>
                                    <td><para style="P6_BOLD">OTROS """ + ('X' if bariatric.epa_otr else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table_14">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('PESO MÁXIMO') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pmx) if bariatric.epa_pmx else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('PESO MÍNIMO') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pmn) if bariatric.epa_pmn else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">PESO ACTUAL</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pac) if bariatric.epa_pac else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">PESO IDEAL</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pid) if bariatric.epa_pid else '') + """</para></td>
                                </tr>
                            </blockTable>
                            <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table_14">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">EXCESO DE PESO</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pex) if bariatric.epa_pex else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">QUIERE QX</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('Si' if bariatric.epa_qqx and bariatric.epa_qqx == 's'  else 'No') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CUAL</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_cqx) if bariatric.epa_cqx else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">CUANDO</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (tools.ustr(bariatric.epa_qcu) if bariatric.epa_qcu else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            
            word_list = []
            if bariatric.ros_des: word_list = self._get_list_words(bariatric.ros_des, 102)
            
            rowHeights = ''
            if len(word_list) == 0: rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="524.0" rowHeights=" """ + rowHeights + """ " style="Table3">"""
            else: rml += """      <blockTable colWidths="524.0" style="Table3">"""
            
            rml += """          <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('5. REVISIÓN ACTUAL DE ORGANOS Y SISTEMAS') + """</para></td></tr>
                                <tr><td><para style="P8_COURIER_LEFT">""" + (tools.ustr(word_list[0]) if len(word_list) >= 1 else ' ' ) + """</para></td></tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="524.0" style="Table3">
                                <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('6. SIGNOS VITALES') + """</para></td></tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" style="Table_15">
                                <tr>
                                    <td><para style="P5_BOLD_CENTER">""" + tools.ustr('FECHA') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr(datetime.now().strftime('%d/%m/%Y')) + """</para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P5_BOLD_CENTER">""" + tools.ustr('PRESION ARTERIAL') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(bariatric.pat_info) if bariatric.pat_info else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P5_BOLD_CENTER">""" + tools.ustr('PULSO X min') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(bariatric.ppm_info) if bariatric.ppm_info else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P5_BOLD_CENTER">""" + tools.ustr('TEMPERATURA °C') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(bariatric.tem_info) if bariatric.tem_info else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="524.0" style="Table3">
                                <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('7. EXAMEN FISICO') + """</para></td></tr>
                            </blockTable>"""
            
            rowHeights = '15.0,15.0'
            rml += """      <blockTable colWidths="70.5,65.5,60.5,65.5,65.5,65.5,65.5,65.5" rowHeights=" """ + rowHeights + """ " style="Table">"""
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">PESO LIBRAS</para></td>
                                    <td><para style="P6_BOLD_CENTER">PESO KG</para></td>
                                    <td><para style="P6_BOLD_CENTER">TALLA</para></td>
                                    <td><para style="P6_BOLD_CENTER">IMC</para></td>
                                    <td><para style="P6_BOLD_CENTER">PESO IDEAL</para></td>
                                    <td><para style="P6_BOLD_CENTER">EXCESO DE PESO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('50% PEP') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + tools.ustr('ÉXITO') + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_plb) if bariatric.epa_plb else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pac) if bariatric.epa_pac else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_tal) if bariatric.epa_tal else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_imc) if bariatric.epa_imc else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pid) if bariatric.epa_pid else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pex) if bariatric.epa_pex else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_pep) if bariatric.epa_pep else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.epa_exi) if bariatric.epa_exi else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = ''
            if not bariatric.cir_cin and not bariatric.cir_cad and not bariatric.eva_pil and not bariatric.eva_cab and not bariatric.eva_tir and not bariatric.eva_pul and not bariatric.eva_car and not bariatric.eva_abd and not bariatric.eva_gen:
                rowHeights = '15.0,15.0'
            else: 
                rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="61.2,58.2,58.2,58.2,58.2,58.2,58.2,58.2,55.4" rowHeights=" """ + rowHeights + """ " style="Table">"""
            else: rml += """      <blockTable colWidths="61.2,58.2,58.2,58.2,58.2,58.2,58.2,58.2,55.4" style="Table">"""
            
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">CIRC. CINTURA</para></td>
                                    <td><para style="P6_BOLD_CENTER">CIRC. CADERA</para></td>
                                    <td><para style="P6_BOLD_CENTER">PIEL</para></td>
                                    <td><para style="P6_BOLD_CENTER">CABEZA - CUELLO</para></td>
                                    <td><para style="P6_BOLD_CENTER">TIROIDES</para></td>
                                    <td><para style="P6_BOLD_CENTER">PULMONAR</para></td>
                                    <td><para style="P6_BOLD_CENTER">CARDIACO</para></td>
                                    <td><para style="P6_BOLD_CENTER">ABDOMINALES</para></td>
                                    <td><para style="P6_BOLD_CENTER">GENITALES</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.cir_cin) if bariatric.cir_cin else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + (str(bariatric.cir_cad) if bariatric.cir_cad else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_pil) if bariatric.eva_pil else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_cab) if bariatric.eva_cab else '') + ' ' + (tools.ustr(bariatric.eva_cue) if bariatric.eva_cue else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_tir) if bariatric.eva_tir else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_pul) if bariatric.eva_pul else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_car) if bariatric.eva_car else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_abd) if bariatric.eva_abd else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_gen) if bariatric.eva_gen else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            if bariatric:
                if not bariatric.eva_ext and not bariatric.eva_ene and not bariatric.eva_otr:
                    rowHeights = '15.0,15.0'
            else: 
                rowHeights = '15.0,15.0'
            
            if not rowHeights == '':
                rml += """      <blockTable colWidths="61.2,58.2,404.6" rowHeights=" """ + rowHeights + """ " style="Table">"""
            else: 
                rml += """      <blockTable colWidths="61.2,58.2,404.6" style="Table">"""
            
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">EXTREMIDADES</para></td>
                                    <td><para style="P6_BOLD_CENTER">ENE</para></td>
                                    <td><para style="P6_BOLD_CENTER">OTROS</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_ext) if bariatric.eva_ext else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_ene) if bariatric.eva_ene else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + (tools.ustr(bariatric.eva_otr) if bariatric.eva_otr else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            diagnosisList = []
            for diagnosis in bariatric.diag_bariatric:
                if len(diagnosisList) < 6:
                    diagnosisList.append((tools.ustr(diagnosis.name), 'pre', tools.ustr(diagnosis.code)))
            
            for diagnosis in bariatric.diag_bariatric_def:
                if len(diagnosisList) < 6:
                    diagnosisList.append((tools.ustr(diagnosis.name), 'def', tools.ustr(diagnosis.code)))
            
            
            if len(diagnosisList) < 6:
                while len(diagnosisList) < 6:
                    diagnosisList.append(('', '', ''))
            
            rml += """      <blockTable colWidths="182.0,30.0,25.0,25.0,182.0,30.0,25.0,25.0" style="Table6">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">8. DIAGNOSTICOS</para></td>
                                    <td><para style="P6_BOLD_CENTER">CIE</para></td>
                                    <td><para style="P6_BOLD_CENTER">PRE</para></td>
                                    <td><para style="P6_BOLD_CENTER">DEF</para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                    <td><para style="P6_BOLD_CENTER">CIE</para></td>
                                    <td><para style="P6_BOLD_CENTER">PRE</para></td>
                                    <td><para style="P6_BOLD_CENTER">DEF</para></td>
                                </tr>
                            </blockTable>"""
            
            filaAlto1 = 1      
            if len(diagnosisList[0][0]) > 30:
                tmp1 = len(diagnosisList[0][0])/30            
                filaAlto1 = tmp1 + 1 if len(diagnosisList[0][0]) % 30 != 0 else tmp1
            
            filaAlto2 = 1     
            if len(diagnosisList[1][0]) > 30:
                tmp2 = len(diagnosisList[1][0])/30            
                filaAlto2 = tmp2 + 1 if len(diagnosisList[1][0]) % 30 != 0 else tmp2
              
            maxVal = max([filaAlto1,filaAlto2])
            
            rowHeights = str(15.0 * maxVal)
            
            rml += """      <blockTable colWidths="182.0,30.0,25.0,25.0,182.0,30.0,25.0,25.0" rowHeights=" """ + rowHeights + """ " style="Table_16">"""
            
            rml += """          <tr>
                                    <td><para style="P7_COURIER">""" + diagnosisList[0][0] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + diagnosisList[0][2][0:3] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[0][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[0][1] == 'def' else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + diagnosisList[1][0] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + diagnosisList[1][2][0:3] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[1][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[1][1] == 'def' else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            
            filaAlto1 = 1      
            if len(diagnosisList[2][0]) > 30:
                tmp1 = len(diagnosisList[2][0])/30            
                filaAlto1 = tmp1 + 1 if len(diagnosisList[2][0]) % 30 != 0 else tmp1
            
            filaAlto2 = 1     
            if len(diagnosisList[3][0]) > 30:
                tmp2 = len(diagnosisList[3][0])/30            
                filaAlto2 = tmp2 + 1 if len(diagnosisList[3][0]) % 30 != 0 else tmp2
              
            maxVal = max([filaAlto1,filaAlto2])
            
            rowHeights = str(15.0 * maxVal)
            
            rml += """      <blockTable colWidths="182.0,30.0,25.0,25.0,182.0,30.0,25.0,25.0" rowHeights=" """ + rowHeights + """ " style="Table_16">"""
            rml += """          <tr>
                                    <td><para style="P7_COURIER">""" + diagnosisList[2][0] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + diagnosisList[2][2][0:3] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[2][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[2][1] == 'def' else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + diagnosisList[3][0] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + diagnosisList[3][2][0:3] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[3][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[3][1] == 'def' else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            filaAlto1 = 1      
            if len(diagnosisList[4][0]) > 30:
                tmp1 = len(diagnosisList[4][0])/30            
                filaAlto1 = tmp1 + 1 if len(diagnosisList[4][0]) % 30 != 0 else tmp1
            
            filaAlto2 = 1     
            if len(diagnosisList[5][0]) > 30:
                tmp2 = len(diagnosisList[5][0])/30            
                filaAlto2 = tmp2 + 1 if len(diagnosisList[5][0]) % 30 != 0 else tmp2
              
            maxVal = max([filaAlto1,filaAlto2])
            
            rowHeights = str(15.0 * maxVal)
            
            rml += """      <blockTable colWidths="182.0,30.0,25.0,25.0,182.0,30.0,25.0,25.0" rowHeights=" """ + rowHeights + """ " style="Table_16">"""
            rml += """          <tr>
                                    <td><para style="P7_COURIER">""" + diagnosisList[4][0] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + diagnosisList[4][2][0:3] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[4][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[4][1] == 'def' else '') + """</para></td>
                                    <td><para style="P7_COURIER">""" + diagnosisList[5][0] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + diagnosisList[5][2][0:3] + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[5][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P7_COURIER_CENTER">""" + ('X' if diagnosisList[5][1] == 'def' else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            
            rml += """      <blockTable colWidths="524.0" style="Table3">
                                <tr><td><para style="P6_BOLD_CENTER">""" + tools.ustr('9. PLANES') + """</para></td></tr>
                            </blockTable>"""
           

            rml += """      <blockTable colWidths="83.0,83.0,83.0,83.0,83.0,109.0" style="Table">"""
            rml += """          <tr>
                                    <td><para style="P6_BOLD_CENTER">EXAMENES</para></td>
                                    <td><para style="P6_BOLD_CENTER">EVALUACIONES</para></td>
                                    <td><para style="P6_BOLD_CENTER">CIRUGIA</para></td>
                                    <td><para style="P6_BOLD_CENTER">FECHA DE QX</para></td>
                                    <td><para style="P6_BOLD_CENTER">COSTO</para></td>
                                    <td><para style="P6_BOLD_CENTER">FINANCIAMIENTO</para></td>                                    
                                </tr>
                            </blockTable>"""
            
            filaAlto1 = 1      
            if bariatric.exams and len(bariatric.exams) > 40:
        	   tmp1 = len(bariatric.exams)/40            
        	   filaAlto1 = tmp1 + 1 if len(bariatric.exams) % 40 != 0 else tmp1
        		
            filaAlto2 = 1      
            if bariatric.evalucs and len(bariatric.evalucs) > 40:
        	   tmp2 = len(bariatric.evalucs)/40            
        	   filaAlto2 = tmp2 + 1 if len(bariatric.evalucs) % 40 != 0 else tmp2
            
            filaAlto3 = 1     
            if bariatric.cirugia and len(bariatric.cirugia) > 40:
        	   tmp3 = len(bariatric.cirugia)/40            
        	   filaAlto3 = tmp3 + 1 if len(bariatric.cirugia) % 40 != 0 else tmp3
		    
            filaAlto4 = 1     
            if bariatric.fianc and len(bariatric.fianc) > 50:
               tmp4 = len(bariatric.fianc)/50            
               filaAlto4 = tmp4 + 1 if len(bariatric.fianc) % 50 != 0 else tmp4
              
            maxVal = max([filaAlto1,filaAlto2,filaAlto3,filaAlto4])         
            
            rowHeights = str(15.0 * maxVal)
            
            fecha_qx = False
            if bariatric.fechaqx:
                temp = bariatric.fechaqx.split('-')
                if len(temp) >= 3:
                    fecha_qx = temp[2] + '/' + temp[1] + '/' + temp[0]
            
            rml += """      <blockTable colWidths="83.0,83.0,83.0,83.0,83.0,109.0" rowHeights=" """ + rowHeights + """ " style="Table01">"""
            rml += """          <tr>
                                    <td><para style="P6_LEFT">""" + (tools.ustr(bariatric.exams) if bariatric.exams else '') + """</para></td>
                                    <td><para style="P6_LEFT">""" + (tools.ustr(bariatric.evalucs) if bariatric.evalucs else '') + """</para></td>
                                    <td><para style="P6_LEFT">""" + (tools.ustr(bariatric.cirugia) if bariatric.cirugia else '') + """</para></td>
                                    <td><para style="P6_CENTER">""" + (tools.ustr(fecha_qx) if fecha_qx else '') + """</para></td>
                                    <td><para style="P6_CENTER">""" + (tools.ustr(round(bariatric.costo,2)) if bariatric.costo else '') + """</para></td>
                                    <td><para style="P6_LEFT">""" + (tools.ustr(bariatric.fianc) if bariatric.fianc else '') + """</para></td>                                    
                                </tr>
                            </blockTable>""" 
            
            fecha_control = False
            if bariatric.fecha_control:
                temp = bariatric.fecha_control.split('-')
                if len(temp) >= 3:
                    fecha_control = temp[2] + '/' + temp[1] + '/' + temp[0]
            
            
            rml += """      <blockTable colWidths="65.5,65.5,65.5,65.5,65.5,65.5,65.5,65.5" style="Table_141">
                                <tr>
                                    <td><para style="P6_BOLD_CENTER">FECHA PARA CONTROL</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(fecha_control) if fecha_control else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">HORA FIN</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(bariatric.hora_fin) if bariatric.hora_fin else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">MEDICO</para></td>
                                    <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(bariatric.doctor.physician_id.name) if bariatric.doctor and bariatric.doctor.physician_id else '') + """</para></td>
                                    <td><para style="P6_BOLD_CENTER">FIRMA</para></td>
                                    <td><para style="P6_BOLD_CENTER"></para></td>
                                </tr>
                            </blockTable>"""
            
            cant = 0
            for evolution in bariatric.evolution_ids:
                cant = cant + 1
                
                evo_date = False
                if evolution.evo_date:
                    temp = evolution.evo_date.split('-')
                    if len(temp) >= 3:
                        evo_date = temp[2] + '/' + temp[1] + '/' + temp[0]            
                
                cir_date = False
                if evolution.cir_date:
                    temp = evolution.cir_date.split('-')
                    if len(temp) >= 3:
                        cir_date = temp[2] + '/' + temp[1] + '/' + temp[0]            
                    
                cir_tmp = False
                if evolution.cir_tmp:
                    temp = evolution.cir_tmp.split(' ')
                    if len(temp) >= 2:
                        temp = temp.split(':')
                        if len(temp) >= 3:                        
                            cir_tmp = temp[0] + ':' + temp[1] + ':' + temp[2] 
                
                rml += """      <pageBreak/> 
                                <spacer length="1.0cm"/>
                                <blockTable colWidths="51.0,65.4,121.4,121.4,164.8" style="Table3">
                                    <tr>
                                        <td><para style="P5_BOLD_CENTER">""" + tools.ustr('FECHA \nDIA/MES/AÑO') + """</para></td>
                                        <td><para style="P5_BOLD_CENTER">HORA</para></td>
                                        <td><para style="P5_BOLD_CENTER">EVOLUCION FIRMAR AL PIE DE CADA NOTA DE EVOLUCION</para></td>
                                        <td><para style="P5_BOLD_CENTER">PRESCRIPCIONES FIRMAR AL PIE DE CADA CONJUNTO DE PRESCRIPCIONES</para></td>
                                        <td><para style="P5_BOLD_CENTER">EXAMENES CONTROL</para></td>
                                    </tr>
                                </blockTable>"""
                
                rowHeights = "15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0"
                
                rml += """   <blockTable colWidths="51.0,65.4,63.2,58.2,63.2,58.2,55.2,55.2,54.4" rowHeights=" """ + rowHeights + """ " style="Table_1">
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evo_date) if evo_date else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + tools.ustr('FECHA DE CIRUGÍA') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">DIETA</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_die) if evolution.evo_die else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">OMEPRAZOL</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_1) if evolution.evo_pres_1 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">LEUCOS</para></td>
                                        <td><para style="P6_BOLD_CENTER">HB</para></td>
                                        <td><para style="P6_BOLD_CENTER">HCTO</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(cir_date) if cir_date else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">LIQUIDOS</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_liq) if evolution.evo_liq else '') + """ </para></td>
                                        <td><para style="P6_BOLD_CENTER">NEUROBION</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_2) if evolution.evo_pres_2 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_1) if evolution.evo_exam_ctl_1 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_2) if evolution.evo_exam_ctl_2 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_3) if evolution.evo_exam_ctl_3 else '') + """</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + tools.ustr('TIEMPO DE CIRUGÍA') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">EJERCICIO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_eje) if evolution.evo_eje else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">HIERRO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_3) if evolution.evo_pres_3 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">TGO</para></td>
                                        <td><para style="P6_BOLD_CENTER">TGP</para></td>
                                        <td><para style="P6_BOLD_CENTER">BIL D</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(cir_tmp) if cir_tmp else '00:00') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">DEPOSICION</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_dep) if evolution.evo_dep else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">CALCIO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_4) if evolution.evo_pres_4 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_4) if evolution.evo_exam_ctl_4 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_5) if evolution.evo_exam_ctl_5 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_6) if evolution.evo_exam_ctl_6 else '') + """</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + tools.ustr('PESO INICIO') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">VOMITO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_vom) if evolution.evo_vom else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">SUPLEMENTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_5) if evolution.evo_pres_5 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">GGT</para></td>
                                        <td><para style="P6_BOLD_CENTER">PROT</para></td>
                                        <td><para style="P6_BOLD_CENTER">ALBUMINA</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evaluation_id.epa_pac) if evolution.evaluation_id.epa_pac else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">MEDICAMENTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_med) if evolution.evo_med else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">PROTEINA</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_6) if evolution.evo_pres_6 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_7) if evolution.evo_exam_ctl_7 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_8) if evolution.evo_exam_ctl_8 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_9) if evolution.evo_exam_ctl_9 else '') + """</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + tools.ustr('IMC INICIO') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">PESO HOY</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_peso_hoy) if evolution.evo_peso_hoy else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">EJERCICIO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_7) if evolution.evo_pres_7 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">COLESTEROL</para></td>
                                        <td><para style="P6_BOLD_CENTER">TG</para></td>
                                        <td><para style="P6_BOLD_CENTER">HDL</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evaluation_id.epa_imc) if evolution.evaluation_id.epa_imc else '') +"""</para></td>
                                        <td><para style="P6_BOLD_CENTER">IMC HOY</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_imc_hoy) if evolution.evo_imc_hoy else '') +"""</para></td>
                                        <td><para style="P6_BOLD_CENTER">EXAMENES</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_exam) if evolution.evo_pres_exam else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_10) if evolution.evo_exam_ctl_10 else '') +"""</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_11) if evolution.evo_exam_ctl_11 else '') +"""</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_12) if evolution.evo_exam_ctl_12 else '') +"""</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + tools.ustr('TIPO DE CIRUGÍA') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">PESO PERDIDO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pes_perd) if evolution.evo_pes_perd else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">NUTRICIONISTA</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_nutri) if evolution.evo_pres_nutri else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">LDL</para></td>
                                        <td><para style="P6_BOLD_CENTER">VLDL</para></td>
                                        <td><para style="P6_BOLD_CENTER">GLUCOSA</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.cir_tip) if evolution.cir_tip else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">IMC PERDIDO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_imc_perd) if evolution.evo_imc_perd else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">PSICOLOGA</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_pres_psico) if evolution.evo_pres_psico else '') +"""</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_13) if evolution.evo_exam_ctl_13 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_14) if evolution.evo_exam_ctl_14 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_15) if evolution.evo_exam_ctl_15 else '') + """</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">EXCESO DE PESO</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exceso_pes) if evolution.evo_exceso_pes else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">CREATININA</para></td>
                                        <td><para style="P6_BOLD_CENTER">AC, UR</para></td>
                                        <td><para style="P6_BOLD_CENTER">BUN</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + tools.ustr('%PEP') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_perc_pep) if evolution.evo_perc_pep else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_16) if evolution.evo_exam_ctl_16 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_17) if evolution.evo_exam_ctl_17 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_18) if evolution.evo_exam_ctl_18 else '') + """</para></td>
                                    </tr>
                                    
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">HTA SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">HTA NO</para></td>
                                        <td><para style="P6_BOLD_CENTER">MEDICAMENTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                        <td><para style="P6_BOLD_CENTER">HG GLIC</para></td>
                                        <td><para style="P6_BOLD_CENTER">T3</para></td>
                                        <td><para style="P6_BOLD_CENTER">T4</para></td>
                                    </tr>                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if  evolution.evo_hta and evolution.evo_hta == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if  evolution.evo_hta and evolution.evo_hta == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_hmd) if evolution.evo_hmd else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_hdc) if evolution.evo_hdc else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_19) if evolution.evo_exam_ctl_19 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_20) if evolution.evo_exam_ctl_20 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_21) if evolution.evo_exam_ctl_21 else '') + """</para></td>
                                    </tr>
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">DM SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">DM NO</para></td>
                                        <td><para style="P6_BOLD_CENTER">MEDICAMENTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                        <td><para style="P6_BOLD_CENTER">TSH</para></td>
                                        <td><para style="P6_BOLD_CENTER">NA</para></td>
                                        <td><para style="P6_BOLD_CENTER">K</para></td>
                                    </tr>
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_dm and evolution.evo_dm == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_dm and evolution.evo_dm == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_dmd) if evolution.evo_dmd else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_ddc) if evolution.evo_ddc else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_22) if evolution.evo_exam_ctl_22 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_23) if evolution.evo_exam_ctl_23 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_24) if evolution.evo_exam_ctl_24 else '') + """</para></td>
                                    </tr>
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">DLP SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">DLP NO</para></td>
                                        <td><para style="P6_BOLD_CENTER">MEDICAMENTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                        <td><para style="P6_BOLD_CENTER">CALCIO</para></td>
                                        <td><para style="P6_BOLD_CENTER">CA ION</para></td>
                                        <td><para style="P6_BOLD_CENTER">P</para></td>
                                    </tr>
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_dlp and evolution.evo_dlp == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_dlp and evolution.evo_dlp == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_lmd) if evolution.evo_lmd else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_ldc) if evolution.evo_ldc else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_25) if evolution.evo_exam_ctl_25 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_26) if evolution.evo_exam_ctl_26 else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_27) if evolution.evo_exam_ctl_27 else '') + """</para></td>
                                    </tr>
                                    
                                </blockTable>"""
                
                rowHeights = '15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0'

                filaAlto1 = 1      
                if evolution.evo_compli_cual and len(evolution.evo_compli_cual) > 30:
        		    tmp1 = len(evolution.evo_compli_cual)/30            
        		    filaAlto1 = tmp1 + 1 if len(evolution.evo_compli_cual) % 30 != 0 else tmp1
        		
                filaAlto2 = 1      
                if evolution.evo_compli_tto and len(evolution.evo_compli_tto) > 20:
        		    tmp2 = len(evolution.evo_compli_tto)/20            
        		    filaAlto2 = tmp2 + 1 if len(evolution.evo_compli_tto) % 20 != 0 else tmp2
            
                filaAlto3 = 1     
                if evolution.evo_coment and len(evolution.evo_coment) > 70:
        		    tmp3 = len(evolution.evo_coment)/70            
        		    filaAlto3 = tmp3 + 1 if len(evolution.evo_coment) % 70 != 0 else tmp3
		      
                maxVal = max([filaAlto1,filaAlto2,filaAlto3])         
            
                rowHeights += ',' + str(15.0 * maxVal)
                
                rml += """    <blockTable colWidths="51.0,65.4,63.2,58.2,63.2,58.2,164.8" rowHeights=" """ + rowHeights + """ " style="Table_11">"""
                rml += """         <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">APNEA SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">APNEA NO</para></td>
                                        <td><para style="P6_BOLD_CENTER">MEDICAMENTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                        <td><para style="P6_BOLD_CENTER">OTROS</para></td>
                                   </tr>
                                   <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_apn and evolution.evo_apn == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_apn and evolution.evo_apn == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_amd) if evolution.evo_amd else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_adc) if evolution.evo_adc else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_exam_ctl_28) if evolution.evo_exam_ctl_28 else '') + """</para></td>
                                    </tr>                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">OSTEO SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">OSTEO NO</para></td>
                                        <td><para style="P6_BOLD_CENTER">MEDICAMENTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                    </tr>                                                                        
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_ost and evolution.evo_ost == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_ost and evolution.evo_ost == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_omd) if evolution.evo_omd else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_odc) if evolution.evo_odc else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                    </tr>                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">SOP SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">SOP NO</para></td>
                                        <td><para style="P6_BOLD_CENTER">MEDICAMENTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">DOSIS</para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_sop and evolution.evo_sop == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_sop and evolution.evo_sop == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_smd) if evolution.evo_smd else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + (tools.ustr(evolution.evo_sdc) if evolution.evo_sdc else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">HG SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">HG NO</para></td>
                                        <td><para style="P6_BOLD_CENTER">COLE SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">COLE NO</para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_hg and evolution.evo_hg == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_hg and evolution.evo_hg == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_cole and evolution.evo_cole == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_cole and evolution.evo_cole == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">COMPLIC SI</para></td>
                                        <td><para style="P6_BOLD_CENTER">COMPLIC NO</para></td>
                                        <td><para style="P6_BOLD_CENTER">CUAL</para></td>
                                        <td><para style="P6_BOLD_CENTER">TTO</para></td>
                                        <td><para style="P6_BOLD_CENTER">COMENTARIOS</para></td>
                                    </tr>
                                    
                                    <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_compli and evolution.evo_compli == 's' else '') + """</para></td>
                                        <td><para style="P6_BOLD_CENTER">""" + ('X' if evolution.evo_compli and evolution.evo_compli == 'n' else '') + """</para></td>
                                        <td><para style="P6_BOLD_LEFT">""" + (tools.ustr(evolution.evo_compli_cual) if evolution.evo_compli_cual else '') + """</para></td>
                                        <td><para style="P6_BOLD_LEFT">""" + (tools.ustr(evolution.evo_compli_tto) if evolution.evo_compli_tto else '') + """</para></td>
                                        <td><para style="P6_BOLD_LEFT">""" + (tools.ustr(evolution.evo_coment) if evolution.evo_coment else '') + """</para></td>
                                    </tr>
                             </blockTable> """

                
                  
                rowHeights = ''                
                valTmp = maxVal
                while(7 - valTmp > 0):
                    rowHeights += '15.0,'                
                    valTmp += 1
                rowHeights = rowHeights[0:-1]
                
                   
                rml += """<blockTable colWidths="51.0,65.4,63.2,58.2,63.2,58.2,164.8" rowHeights=" """ + rowHeights + """ " style="Table_112"> """
                
                while(7 - maxVal > 0):
                    rml += """     <tr>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                        <td><para style="P6_BOLD_CENTER"></para></td>
                                    </tr> """
                
                    maxVal += 1
                                   
                rml += """</blockTable>"""                
                
                rml += """  <condPageBreak height="100"/>"""
                                    
            rml += """      </story>
                        </document>"""
            
            
        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        return (pdf, report_type)
    
    def _get_year(self, record):
        if (record.dob):
            now = datetime.now()
            dob = datetime.strptime(str(record.dob), '%Y-%m-%d')
            delta = relativedelta(now, dob)
            return delta.years
        return ''   
    
    def _get_list_words(self, data, size):
        text = ''
        if data:
            text = data.replace('\n', ' ')
            text = text.split(' ')
        word_list = []
        temp = ''
        
        for x in xrange(len(text)):
            if len(temp) + len(text[x]) + 1 <= size:
                temp += text[x] + ' '
            else:
                word_list.append(temp)
                temp = ''
            
            if x == len(text): word_list.append(text[x])
        return word_list
    
oemedical_bariatric_report('report.oemedical_bariatric_report', 'oemedical.patient', '', '')
            
