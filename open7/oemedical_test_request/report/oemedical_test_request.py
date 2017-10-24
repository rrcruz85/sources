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

import os
import time
import string
import openerp

from openerp import pooler, tools
from openerp.report import report_sxw
from openerp.report.interface import report_rml

from openerp.tools import to_xml
from openerp.tools.translate import _

from dateutil.relativedelta import relativedelta
from datetime import datetime

class oemedical_test_request_report(report_rml):
    def create(self, cr, uid, ids, datas, context):
        test_request_obj = pooler.get_pool(cr.dbname).get('oemedical.test.request')
        company_obj = pooler.get_pool(cr.dbname).get('res.company')
        
        company_ids_list = company_obj.search(cr, uid, [], context=context)
        company = company_obj.browse(cr, uid, company_ids_list[0], context) if len(company_ids_list) > 0 else False
        
        for test_request in test_request_obj.browse(cr, uid, ids, context):
            first_name = tools.ustr(test_request.patient_id.first_name.split(" ")[0])
            second_name = tools.ustr(test_request.patient_id.first_name.split(" ")[1]) if len(test_request.patient_id.first_name.split(" ")) > 1 else ""
            rml = """<document filename="test.pdf">
                        <template pageSize="(595.0,842.0)" title=" """ + _("Laboratory Tests") + """ " author="Reynaldo Rodriguez Cruz" allowSplitting="20">
                            <pageTemplate id="page1">
                                <frame id="first" x1="50.0" y1="500.0" width="498" height="300"/>
                                
                                <frame id="column1" x1="40.0" y1="50.0" width="120" height="580"/>
                                <frame id="column2" x1="165.0" y1="50.0" width="120" height="580"/>
                                <frame id="column3" x1="290.0" y1="50.0" width="120" height="580"/>
                                <frame id="column4" x1="415.0" y1="50.0" width="120" height="580"/>
                            </pageTemplate>
                            
                            <pageTemplate id="page2">
                                <frame id="first" x1="40.0" y1="50.0" width="115" height="750"/>
                                <frame id="column2" x1="160.0" y1="50.0" width="115" height="750"/>
                                <frame id="column3" x1="290.0" y1="50.0" width="115" height="750"/>
                                <frame id="column4" x1="410.0" y1="50.0" width="115" height="750"/>
                            </pageTemplate>
                        </template>"""
            
            rml += """
                        <stylesheet>
                            <blockTableStyle id="Table1">
                                <blockAlignment value="CENTER"/>
                                <blockValign value="MIDDLE"/>
                                
                                <blockSpan start="0,0" stop="1,0"/>
                                <blockSpan start="2,0" stop="3,0"/>
                                
                                <blockSpan start="0,1" stop="1,2"/>
                                <blockSpan start="2,1" stop="3,2"/>
                                <blockSpan start="4,1" stop="4,2"/>
                                
                                <blockSpan start="8,0" stop="8,1"/>
                                <blockSpan start="1,3" stop="2,3"/>
                                <blockSpan start="1,4" stop="2,4"/>
                                <blockSpan start="4,3" stop="6,3"/>
                                
                                <blockSpan start="5,0" stop="7,0"/>
                                <blockSpan start="4,4" stop="6,4"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="gray" start="0,0" stop="0,-1" thickness="1"/>
                                <lineStyle kind="LINEAFTER" colorName="gray" start="8,0" stop="8,-1" thickness="1"/>
                                <lineStyle kind="LINEABOVE" colorName="gray" start="0,0" stop="8,0" thickness="1"/>
                                <lineStyle kind="LINEBELOW" colorName="gray" start="0,-1" stop="8,-1" thickness="1"/>
                                
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="7,0" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="7,0" stop="7,0" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="7,1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="7,1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="7,1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="7,1" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,2" stop="7,2" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,2" stop="7,2" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,2" stop="7,2" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,2" stop="7,2" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,3" stop="8,3" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,3" stop="8,3" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,4" stop="8,4" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,4" stop="8,4" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,4" stop="8,4" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,4" stop="8,4" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table2">
                                <blockAlignment value="CENTER"/>
                                <blockValign value="MIDDLE"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="gray" start="0,0" stop="0,-1" thickness="1"/>
                                <lineStyle kind="LINEAFTER" colorName="gray" start="9,0" stop="9,-1" thickness="1"/>
                                <lineStyle kind="LINEABOVE" colorName="gray" start="0,0" stop="9,0" thickness="1"/>
                                <lineStyle kind="LINEBELOW" colorName="gray" start="0,-1" stop="9,-1" thickness="1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="-1,1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="-1,1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="-1,1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="-1,1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table3">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>
                                <blockBackground colorName="#000000" start="0,3" stop="0,3"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="miniTable">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>
                                <blockSpan start="0,0" stop="1,0"/>
                                <blockBackground colorName="gray" start="0,0" stop="1,0"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="checkBox">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <initialize>
                                <paraStyle name="all" alignment="justify"/>
                            </initialize>
                            
                            <paraStyle name="P1" fontName="Helvetica-Bold" fontSize="7.0" leading="9" spaceBefore="0.0" spaceAfter="0.0" alignment="CENTER"/>
                            <paraStyle name="P2" fontName="Helvetica" fontSize="5.0" leading="5" spaceBefore="0.0" spaceAfter="0.0" alignment="CENTER"/>
                            <paraStyle name="P2_LEFT" fontName="Helvetica" fontSize="5.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P3" fontName="Helvetica" fontSize="5.0" leading="5" spaceBefore="0.0" spaceAfter="0.0" alignment="CENTER"/>
                            <paraStyle name="P3_left_bold" fontName="Helvetica-Bold" fontSize="6.0" leading="8" spaceBefore="0.0" spaceAfter="0.0" alignment="LEFT"/>
                            <paraStyle name="P3_LEFT" alignment="LEFT"/>

                            <paraStyle name="P26" fontName="Helvetica-Bold" fontSize="9.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P27" fontName="Helvetica-Bold" fontSize="14.0" leading="5" alignment="CENTER"/>
                            
                            <paraStyle name="P22" fontName="Helvetica" fontSize="5.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P2222" fontName="Helvetica" fontSize="5.0" leading="15" alignment="LEFT"/>
                       
						</stylesheet>"""
                        
            rml += """  <story>"""
            
            rml += """
                            <section>
                            <blockTable colWidths="100.0,30.0,50.0,100.0,50.0,45.0,35.0,40.0,90.0" rowHeights="12.0,12.0,12.0,12.0,15.0" style="Table1">
                                <tr>
                                    <td><para style="P1">""" + tools.ustr("INSTITUCIÓN DEL SISTEMA") + """</para></td>
                                    <td></td>
                                    <td><para style="P1">UNIDAD OPERATIVA</para></td>
                                    <td></td>
                                    <td><para style="P1">COD. UO</para></td>
                                    <td><para style="P1">""" + tools.ustr("COD. LOCALIZACIÓN") + """</para></td>
                                    <td></td>
                                    <td></td>
                                    <td><para style="P1">""" + tools.ustr("NÚMERO DE HISTORIA CLÍNICA") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td>""" + (tools.ustr(company.name) if company else "") + """</td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td><para style="P2">PARROQUIA</para></td>
                                    <td><para style="P2">""" + tools.ustr("CANTÓN") + """</para></td>
                                    <td><para style="P2">PROVINCIA</para></td>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td><para style="P2_LEFT">""" + (tools.ustr(test_request.patient_id.partner_id.state_id.name) if test_request.patient_id.partner_id and test_request.patient_id.partner_id.state_id else '' ) + """</para></td>
                                    <td>""" + (tools.ustr(test_request.patient_id.identification_code) if test_request.patient_id and test_request.patient_id.identification_code else '') + """</td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P3">APELLIDO PATERNO</para></td>
                                    <td><para style="P3">APELLIDO MATERNO</para></td>
                                    <td></td>
                                    <td><para style="P3">PRIMER NOMBRE</para></td>
                                    <td><para style="P3">SEGUNDO NOMBRE</para></td>
                                    <td></td>
                                    <td></td>
                                    <td><para style="P3">EDAD</para></td>
                                    <td><para style="P3">""" + tools.ustr("CÉDULA DE CIUDADANÍA") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td>""" + (tools.ustr(test_request.patient_id.last_name) if test_request.patient_id and test_request.patient_id.last_name else '') + """</td>
                                    <td>""" + (tools.ustr(test_request.patient_id.slastname) if test_request.patient_id and test_request.patient_id.slastname else '') + """</td>
                                    <td></td>
                                    <td>""" + first_name + """</td>
                                    <td>""" + second_name + """</td>
                                    <td></td>
                                    <td></td>
                                    <td>""" + self._get_age(test_request.patient_id) + """</td>
                                    <td></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <spacer length="0.2cm"/>"""
            
            rml += """      <blockTable colWidths="210.0,40.0,35.0,35.0,40.0,15.0,40.0,15.0,40.0,70.0" rowHeights="12.0,15.0" style="Table2">
                                <tr>
                                    <td><para style="P3_left_bold">""" + tools.ustr("MÉDICO SOLICITANTE") + """</para></td>
                                    <td><para style="P3">SERVICIO</para></td>
                                    <td><para style="P3">SALA</para></td>
                                    <td><para style="P3">CAMA</para></td>
                                    <td></td>
                                    <td></td>
                                    <td><para style="P3">PRIORIDAD</para></td>
                                    <td></td>
                                    <td></td>
                                    <td><para style="P3">FECHA DE TOMA</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P3_LEFT">""" + (tools.ustr(test_request.doctor.name) if test_request.doctor and test_request.doctor.name else '') + """</para></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td><para style="P3">URGENTE</para></td>
                                    <td></td>
                                    <td><para style="P3">RUTINA</para></td>
                                    <td></td>
                                    <td><para style="P3">CONTROL</para></td>
                                    <td>""" + ((test_request.test_date.split('-')[2] + '/' + test_request.test_date.split('-')[1] + '/' + test_request.test_date.split('-')[0]) if test_request.test_date else '') + """</td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <spacer length="0.2cm"/>"""
            
            rml += """      
                            <blockTable colWidths="540.0" rowHeights="20.0, 15.0, 15.0, 2.0" style="Table3">
                                <tr>
                                    <td><para style="P27">""" + tools.ustr("SOLICITUD DE EXÁMENES LABORATORIO") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P26">FOR/001 (MAN/ATPA/TEC-LAB/001)</para></td>
                                </tr>
                                
                                <tr>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td></td>
                                </tr>
                            </blockTable>
                            </section>"""
            
            rml += """      <spacer length="0.1cm"/>"""
            rml += """      <nextFrame/>"""
            
            test_list_obj = pooler.get_pool(cr.dbname).get('oemedical.test.list')
            test_list_ids_list = test_list_obj.search(cr, uid, [], context=context)
            oemedical_test_list_list = test_list_obj.browse(cr, uid, test_list_ids_list, context)
            
            rml += """      <section>"""
            rml += """      <setNextTemplate name="page2"/>"""
            
            if test_request.type_hema_ids:
                xtype = 'HEMATOLOGIA'
                selected_items = [ test.id for test in test_request.type_hema_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_coag_ids:
                xtype = 'COAGULACION'
                selected_items = [ test.id for test in test_request.type_coag_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_qmsa_ids:
                xtype = 'QUIMICA SANGUINEA'
                selected_items = [ test.id for test in test_request.type_qmsa_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_prlp_ids:
                xtype = 'PERFIL LIPIDICO'
                selected_items = [ test.id for test in test_request.type_prlp_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                    
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_prep_ids:
                xtype = 'PERFIL HEPATICO'
                selected_items = [ test.id for test in test_request.type_prep_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else "") + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_enzi_ids:
                xtype = 'PRUEBAS ENZIMATICAS'
                selected_items = [ test.id for test in test_request.type_enzi_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_sero_ids:
                xtype = 'SEROLOGIA'
                selected_items = [ test.id for test in test_request.type_sero_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_horm_ids:
                xtype = 'PRUEBAS HORMONALES'
                selected_items = [ test.id for test in test_request.type_horm_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_onco_ids:
                xtype = 'MARCADORES ONCOLOGICOS'
                selected_items = [ test.id for test in test_request.type_onco_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_elec_ids:
                xtype = 'ELECTROLITOS'
                selected_items = [ test.id for test in test_request.type_elec_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_para_ids:
                xtype = 'ANTICUERPOS VIRALES Y PARASITOSIS'
                selected_items = [ test.id for test in test_request.type_para_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_inmu_ids:
                xtype = 'AUTOINMUNIDAD'
                selected_items = [ test.id for test in test_request.type_inmu_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_diag_ids:
                xtype = 'INMUNO DIAGNOSTICO'
                selected_items = [ test.id for test in test_request.type_diag_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_tera_ids:
                xtype = 'DROGAS TERAPEUTICAS'
                selected_items = [ test.id for test in test_request.type_tera_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_orin_ids:
                xtype = 'ORINA'
                selected_items = [ test.id for test in test_request.type_orin_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_ores_ids:
                xtype = 'PRUEBAS ESPECIALES EN ORINA'
                selected_items = [ test.id for test in test_request.type_ores_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_hece_ids:
                xtype = 'HECES Y MALA ABSORCION'
                selected_items = [ test.id for test in test_request.type_hece_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_bact_ids:
                xtype = 'BACTERIOLOGIA'
                selected_items = [ test.id for test in test_request.type_bact_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_pato_ids:
                xtype = 'PATOLOGIA'
                selected_items = [ test.id for test in test_request.type_pato_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            if test_request.type_other_ids:
                xtype = 'OTROS'
                selected_items = [ test.id for test in test_request.type_other_ids ]
                test_list = self.get_list_by_type(xtype, oemedical_test_list_list, selected_items)
                
                rowHeights = '10.0'
                for test in test_list:
                    rowHeights += ',10.0'
                
                rml += """      <blockTable colWidths="8.0,100.0" rowHeights=" """ + rowHeights + """ " style="miniTable">"""
                rml += """          <tr>
                                        <td><para style="P3_left_bold">""" + xtype + """</para></td>
                                        <td></td>
                                    </tr>"""
                
                for test in test_list:
                    rml += """      <tr>
                                        <td>
                                            <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                <tr><td><para style="P2222">""" + ('X' if test[0] else '') + """</para></td></tr>
                                            </blockTable>
                                        </td>
                                        <td><para style="P22">""" + tools.ustr(test[1]) + """</para></td>
                                    </tr>"""
                
                rml += """      </blockTable>"""
                rml += """      <spacer length="0.1cm"/>"""
            
            rml += """ </section></story></document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        
        return (pdf, report_type)
    
    def get_list_by_type(self, xtype, element_list, selected_items):
        res = []
        for element in element_list:
            if element.type == xtype and element.id in selected_items:
                res.append((True, element.name))
        return res
    
    def _get_age(self, record):
        now = datetime.now()
        dob = datetime.strptime(str(record.dob), '%Y-%m-%d')
        delta = relativedelta(now, dob)        
        return str(delta.years)
    
oemedical_test_request_report('report.oemedical_test_request_report', 'oemedical.test.request', '', '')