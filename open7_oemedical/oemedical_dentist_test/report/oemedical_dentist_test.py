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
import openerp

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import pooler, tools
from openerp.report.interface import report_rml

from openerp.tools.translate import _

class oemedical_dentist_test_report(report_rml):
    def create(self, cr, uid, ids, datas, context):
        dentist_test_obj = pooler.get_pool(cr.dbname).get('oemedical.dentist.test')
        company_obj = pooler.get_pool(cr.dbname).get('res.company')
        
        company_ids_list = company_obj.search(cr, uid, [], context=context)
        company = company_obj.browse(cr, uid, company_ids_list[0], context) if len(company_ids_list) > 0 else False
        
        for dentist_test in dentist_test_obj.browse(cr, uid, ids, context):
            first_name = tools.ustr(dentist_test.patient_id.first_name.split(" ")[0])
            second_name = tools.ustr(dentist_test.patient_id.first_name.split(" ")[1]) if len(dentist_test.patient_id.first_name.split(" ")) > 1 else ""
            
            rml = """<document filename="test.pdf">
                        <template pageSize="(595.0,842.0)" title=" """ + _("Odonthology Tests") + """ " author="Reynaldo Rodriguez Cruz" allowSplitting="20">
                            <pageTemplate id="page1">
                                <pageGraphics>
                                <place x="57.5" y="765.0" width="459.0" height="77.0">
                                    <blockTable colWidths="415.0,8.0,5.0,4.0,18.0,9.0" rowHeights="30.0,20.0,2.0,15.0,10.0" style="Table1">
                                      <tr>
                                        <td>
                                          <para style="P1">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P2">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P2">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P2">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P3"> </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P3">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                      </tr>
                                      
                                      <tr>
                                        <td vAlign="bottom" bottomPadding="5">
                                          <para style="P10">
                                            <font face="Helvetica-Bold">""" + tools.ustr("") + """</font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P12">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P4"> </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P4">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P11">
                                            <font face="Helvetica"></font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P8">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                      </tr>
                                      
                                      <tr>
                                        <td>
                                          <para style="P5"></para>
                                        </td>
                                        
                                        <td>
                                          <para style="P5"></para>
                                        </td>
                                        
                                        <td>
                                          <para style="P5"></para>
                                        </td>
                                        
                                        <td>
                                          <para style="P5"></para>
                                        </td>
                                        
                                        <td>
                                          <para style="P5"></para>
                                        </td>
                                        
                                        <td>
                                          <para style="P5"></para>
                                        </td>
                                      </tr>
                                      
                                      <tr>
                                        <td>
                                          <para style="P13">Sistema Nacional de Salud</para>
                                        </td>
                                        
                                        <td>
                                          <para style="P13">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P3"> </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P3">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P3"> </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P3">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                      </tr>
                                      
                                      <tr>
                                        <td>
                                          <para style="P2">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P2">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P2">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P2">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P3"> </para>
                                        </td>
                                        
                                        <td>
                                          <para style="P3">
                                            <font color="white"> </font>
                                          </para>
                                        </td>
                                      </tr>
                                    </blockTable>
                                </place>
                                
                                <place x="57.5" y="5.0" width="470.0" height="40.0">
                                    <blockTable colWidths="235.0,235.0" style="Table11">
                                        <tr>
                                            <td><para style="P26">SNS-MSP / HCU-form.014 / 2007</para></td>
                                            <td><para style="P27">ODONTOLOGIA</para></td>
                                        </tr>
                                    </blockTable>
                                </place>
                                </pageGraphics>
                                
                                <frame id="first" x1="57.0" y1="55.0" width="498" height="700"/>
                            </pageTemplate>
                        </template>"""
            
            rml += """
                        <stylesheet>
                            <blockTableStyle id="Table0">
                              <blockValign value="MIDDLE"/>
                              <blockAlignment value="LEFT"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              
                              <blockBackground colorName="#CAE7D4" start="0,0" stop="0,0"/>
                              <blockBackground colorName="#CAE7D4" start="2,0" stop="2,0"/>
                              <blockBackground colorName="#CAE7D4" start="4,0" stop="4,0"/>
                              <blockBackground colorName="#CAE7D4" start="6,0" stop="6,0"/>
                              <blockBackground colorName="#CAE7D4" start="8,0" stop="8,0"/>
                              <blockBackground colorName="#CAE7D4" start="10,0" stop="10,0"/>
                              <blockBackground colorName="#CAE7D4" start="12,0" stop="12,0"/>
                              <blockBackground colorName="#CAE7D4" start="14,0" stop="14,0"/>
                              
                              <blockBackground colorName="#F9F1AD" start="1,0" stop="1,0"/>
                              <blockBackground colorName="#F9F1AD" start="3,0" stop="3,0"/>
                              <blockBackground colorName="#F9F1AD" start="5,0" stop="5,0"/>
                              <blockBackground colorName="#F9F1AD" start="7,0" stop="7,0"/>
                              <blockBackground colorName="#F9F1AD" start="9,0" stop="9,0"/>
                              <blockBackground colorName="#F9F1AD" start="11,0" stop="11,0"/>
                              <blockBackground colorName="#F9F1AD" start="13,0" stop="13,0"/>
                              <blockBackground colorName="#F9F1AD" start="15,0" stop="15,0"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table1">
                              <blockAlignment value="LEFT"/>
                              <blockValign value="TOP"/>
                              
                              <blockSpan start="1,0" stop="1,4"/>
                              <blockSpan start="0,2" stop="1,2"/>
                              
                              <blockBackground colorName="#C0C0C2" start="4,0" stop="4,3"/>
                              <blockBackground colorName="#D1D3D4" start="2,0" stop="2,4"/>
                              <blockBackground colorName="#EBECEC" start="0,2" stop="1,2"/>
                              <blockBackground colorName="#EBECEC" start="3,2" stop="5,2"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table2">
                              <blockAlignment value="CENTER"/>
                              <blockValign value="MIDDLE"/>
                              
                              <blockSpan start="0,0" stop="0,1"/>
                              <blockSpan start="1,0" stop="1,1"/>
                              <blockSpan start="2,0" stop="2,1"/>
                              <blockSpan start="5,0" stop="5,1"/>
                              <blockSpan start="6,0" stop="6,1"/>
                              <blockSpan start="3,0" stop="4,0"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="1,0" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,0" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="1,0" stop="1,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="1,-1" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="2,0" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="2,0" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="2,0" stop="2,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="2,-1" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="3,0" stop="3,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="3,0" stop="3,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="3,0" stop="3,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="3,-1" stop="3,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="4,0" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="4,0" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="4,0" stop="4,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="4,-1" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="5,0" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="5,0" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="5,0" stop="5,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="5,-1" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="0,1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="1,1" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,1" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="1,1" stop="1,1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="1,-1" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,2" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,2" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,2" stop="0,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="1,2" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,2" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="1,2" stop="1,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="1,-1" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="2,2" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="2,2" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="2,2" stop="2,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="2,-1" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="3,2" stop="3,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="3,2" stop="3,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="3,2" stop="3,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="3,-1" stop="3,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="4,2" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="4,2" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="4,2" stop="4,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="4,-1" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="5,2" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="5,2" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="5,2" stop="5,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="5,-1" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="6,2" stop="6,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="6,2" stop="6,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="6,2" stop="6,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="6,-1" stop="6,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="3,0" stop="3,1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="4,0" stop="4,1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="6,0" stop="6,1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="6,0" stop="6,1" thickness="0.1"/>
                              
                              <blockBackground colorName="#CAE7D4" start="0,0" stop="6,0"/>
                              <blockBackground colorName="#CAE7D4" start="0,1" stop="6,1"/>
                              <blockBackground colorName="#F9F1AD" start="3,2" stop="4,2"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table3">
                              <blockValign value="MIDDLE"/>
                              <blockAlignment value="LEFT"/>
                              <blockSpan start="0,1" stop="1,1"/>
                              <blockValign value="TOP" start="0,1" stop="1,1"/>
                              <blockBackground colorName="#F0A9C4" start="0,0" stop="1,0"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="1,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="1,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,0" stop="1,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="1,1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,0" stop="1,-1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="1,-1" stop="1,-1" thickness="0.1"/>
                              
                              <blockSpan start="0,2" stop="1,2"/>
                              <blockSpan start="0,3" stop="1,3"/>
                              <blockSpan start="0,4" stop="1,4"/>
                              <blockSpan start="0,5" stop="1,5"/>
                              <blockSpan start="0,6" stop="1,6"/>
                              <blockSpan start="0,7" stop="1,7"/>
                              <blockSpan start="0,8" stop="1,8"/>
                              <blockSpan start="0,9" stop="1,9"/>
                              
                              <blockSpan start="0,10" stop="1,10"/>
                              <blockSpan start="0,11" stop="1,11"/>
                              <blockSpan start="0,12" stop="1,12"/>
                              <blockSpan start="0,13" stop="1,13"/>
                              <blockSpan start="0,14" stop="1,14"/>
                              <blockSpan start="0,15" stop="1,15"/>
                              <blockSpan start="0,16" stop="1,16"/>
                              <blockSpan start="0,17" stop="1,17"/>
                              <blockSpan start="0,18" stop="1,18"/>
                              <blockSpan start="0,19" stop="1,19"/>
                              
                              <blockSpan start="0,20" stop="1,20"/>
                              <blockSpan start="0,21" stop="1,21"/>
                              <blockSpan start="0,22" stop="1,22"/>
                              <blockSpan start="0,23" stop="1,23"/>
                              <blockSpan start="0,24" stop="1,24"/>
                              <blockSpan start="0,25" stop="1,25"/>
                              <blockSpan start="0,26" stop="1,26"/>
                              <blockSpan start="0,27" stop="1,27"/>
                              <blockSpan start="0,28" stop="1,28"/>
                              <blockSpan start="0,29" stop="1,29"/>
                              
                              <blockSpan start="0,30" stop="1,30"/>
                              <blockSpan start="0,31" stop="1,31"/>
                              <blockSpan start="0,32" stop="1,32"/>
                              <blockSpan start="0,33" stop="1,33"/>
                              <blockSpan start="0,34" stop="1,34"/>
                              <blockSpan start="0,35" stop="1,35"/>
                              <blockSpan start="0,36" stop="1,36"/>
                              <blockSpan start="0,37" stop="1,37"/>
                              <blockSpan start="0,38" stop="1,38"/>
                              <blockSpan start="0,39" stop="1,39"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table4">
                              <blockValign value="MIDDLE"/>
                              <blockAlignment value="LEFT"/>
                              <blockSpan start="0,0" stop="19,0"/>
                              <blockSpan start="0,2" stop="19,2"/>
                              <blockSpan start="0,3" stop="19,3"/>
                              <blockSpan start="0,4" stop="19,4"/>
                              <blockSpan start="0,5" stop="19,5"/>
                              <blockSpan start="0,6" stop="19,6"/>
                              <blockSpan start="0,7" stop="19,7"/>
                              <blockSpan start="0,8" stop="19,8"/>
                              <blockSpan start="0,9" stop="19,9"/>
                              <blockSpan start="0,10" stop="19,10"/>
                              <blockSpan start="0,11" stop="19,11"/>
                              <blockSpan start="0,12" stop="19,12"/>
                              <blockBackground colorName="#F0A9C4" start="0,0" stop="19,0"/>
                              
                              <blockBackground colorName="#CAE7D4" start="0,1" stop="0,1"/>
                              <blockBackground colorName="#CAE7D4" start="2,1" stop="2,1"/>
                              <blockBackground colorName="#CAE7D4" start="4,1" stop="4,1"/>
                              <blockBackground colorName="#CAE7D4" start="6,1" stop="6,1"/>
                              <blockBackground colorName="#CAE7D4" start="8,1" stop="8,1"/>
                              <blockBackground colorName="#CAE7D4" start="10,1" stop="10,1"/>
                              <blockBackground colorName="#CAE7D4" start="12,1" stop="12,1"/>
                              <blockBackground colorName="#CAE7D4" start="14,1" stop="14,1"/>
                              <blockBackground colorName="#CAE7D4" start="16,1" stop="16,1"/>
                              <blockBackground colorName="#CAE7D4" start="18,1" stop="18,1"/>
                              
                              <blockBackground colorName="#F9F1AD" start="1,1" stop="1,1"/>
                              <blockBackground colorName="#F9F1AD" start="3,1" stop="3,1"/>
                              <blockBackground colorName="#F9F1AD" start="5,1" stop="5,1"/>
                              <blockBackground colorName="#F9F1AD" start="7,1" stop="7,1"/>
                              <blockBackground colorName="#F9F1AD" start="9,1" stop="9,1"/>
                              <blockBackground colorName="#F9F1AD" start="11,1" stop="11,1"/>
                              <blockBackground colorName="#F9F1AD" start="13,1" stop="13,1"/>
                              <blockBackground colorName="#F9F1AD" start="15,1" stop="15,1"/>
                              <blockBackground colorName="#F9F1AD" start="17,1" stop="17,1"/>
                              <blockBackground colorName="#F9F1AD" start="19,1" stop="19,1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="19,0" stop="19,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="19,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="19,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="19,1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="19,1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="19,1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="19,1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,2" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="19,2" stop="19,-1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,2" stop="19,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,2" stop="19,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table5">
                              <blockValign value="MIDDLE"/>
                              <blockAlignment value="LEFT"/>
                              <blockSpan start="0,0" stop="15,0"/>
                              <blockBackground colorName="#F0A9C4" start="0,0" stop="15,0"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="15,0" stop="15,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="15,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="15,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="15,1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="15,1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="15,1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="15,1" thickness="0.1"/>
                              
                              <blockBackground colorName="#CAE7D4" start="0,1" stop="0,1"/>
                              <blockBackground colorName="#CAE7D4" start="2,1" stop="2,1"/>
                              <blockBackground colorName="#CAE7D4" start="4,1" stop="4,1"/>
                              <blockBackground colorName="#CAE7D4" start="6,1" stop="6,1"/>
                              <blockBackground colorName="#CAE7D4" start="8,1" stop="8,1"/>
                              <blockBackground colorName="#CAE7D4" start="10,1" stop="10,1"/>
                              <blockBackground colorName="#CAE7D4" start="12,1" stop="12,1"/>
                              <blockBackground colorName="#CAE7D4" start="14,1" stop="14,1"/>
                              <blockBackground colorName="#F9F1AD" start="15,1" stop="15,1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table6">
                              <blockValign value="MIDDLE"/>
                              <blockAlignment value="LEFT"/>
                              
                              <blockSpan start="0,0" stop="6,0"/>
                              <blockSpan start="8,2" stop="15,2"/>
                              <blockSpan start="7,0" stop="15,0"/>
                              
                              <blockSpan start="0,3" stop="15,3"/>
                              <blockSpan start="0,4" stop="15,4"/>
                              <blockSpan start="0,5" stop="15,5"/>
                              <blockSpan start="0,6" stop="15,6"/>
                              <blockSpan start="0,7" stop="15,7"/>
                              <blockSpan start="0,8" stop="15,8"/>
                              <blockSpan start="0,9" stop="15,9"/>
                              <blockSpan start="0,10" stop="15,10"/>
                              <blockSpan start="0,11" stop="15,11"/>
                              <blockSpan start="0,12" stop="15,12"/>
                              <blockSpan start="0,13" stop="15,13"/>
                              <blockSpan start="0,14" stop="15,14"/>
                              <blockSpan start="0,15" stop="15,15"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="15,0" stop="15,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="15,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="15,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="15,2" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="15,2" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="15,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="15,2" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,3" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="15,3" stop="15,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,3" stop="15,-1" thickness="0.1"/>
                              
                              <blockBackground colorName="#F0A9C4" start="0,0" stop="15,0"/>
                              
                              <blockBackground colorName="#CAE7D4" start="0,1" stop="0,2"/>
                              <blockBackground colorName="#CAE7D4" start="2,1" stop="2,2"/>
                              <blockBackground colorName="#CAE7D4" start="4,1" stop="4,2"/>
                              <blockBackground colorName="#CAE7D4" start="6,1" stop="6,2"/>
                              <blockBackground colorName="#CAE7D4" start="8,1" stop="8,1"/>
                              <blockBackground colorName="#CAE7D4" start="10,1" stop="10,1"/>
                              <blockBackground colorName="#CAE7D4" start="12,1" stop="12,1"/>
                              <blockBackground colorName="#CAE7D4" start="14,1" stop="14,1"/>
                              
                              <blockBackground colorName="#F9F1AD" start="1,1" stop="1,2"/>
                              <blockBackground colorName="#F9F1AD" start="3,1" stop="3,2"/>
                              <blockBackground colorName="#F9F1AD" start="5,1" stop="5,2"/>
                              <blockBackground colorName="#F9F1AD" start="7,1" stop="7,2"/>
                              <blockBackground colorName="#F9F1AD" start="9,1" stop="9,1"/>
                              <blockBackground colorName="#F9F1AD" start="11,1" stop="11,1"/>
                              <blockBackground colorName="#F9F1AD" start="13,1" stop="13,1"/>
                              <blockBackground colorName="#F9F1AD" start="15,1" stop="15,1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table7">
                              <blockValign value="BOTTOM"/>
                              <blockAlignment value="CENTER"/>
                              
                              <blockSpan start="0,0" stop="32,0"/>
                              <blockBackground colorName="#F0A9C4" start="0,0" stop="32,0"/>
                              <blockBackground colorName="#CAE7D4" start="0,1" stop="32,-1"/>
                              
                              <blockSpan start="3,5" stop="30,5"/>
                              <blockSpan start="1,10" stop="10,10"/>
                              <blockSpan start="1,11" stop="31,12"/>
                              <blockSpan start="1,13" stop="31,13"/>
                              
                              <blockSpan start="1,4" stop="31,4"/>
                              <blockSpan start="1,9" stop="31,9"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="32,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="32,0" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="32,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="32,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="32,0" stop="32,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,-1" stop="32,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table8">
                              <blockValign value="MIDDLE"/>
                              <blockAlignment value="CENTER"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="checkBox">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="CENTER"/>
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table9">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="LEFT"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table10">
                                <blockValign value="MIDDLE"/>
                                <blockAlignment value="LEFT"/>
                                
                                <blockSpan start="0,0" stop="14,0"/>
                                <blockSpan start="15,0" stop="19,0"/>
                                
                                <blockSpan start="0,1" stop="5,1"/>
                                <blockSpan start="0,2" stop="5,2"/>
                                <blockSpan start="0,9" stop="5,9"/>
                                
                                <blockSpan start="9,1" stop="10,1"/>
                                <blockSpan start="9,5" stop="19,5"/>
                                
                                <blockSpan start="11,1" stop="12,1"/>
                                <blockSpan start="13,1" stop="14,1"/>
                                <blockSpan start="15,1" stop="15,2"/>
                                <blockSpan start="15,3" stop="15,4"/>
                                
                                <blockSpan start="9,6" stop="11,6"/>
                                <blockSpan start="9,7" stop="11,7"/>
                                <blockSpan start="9,8" stop="11,8"/>
                                <blockSpan start="9,9" stop="11,9"/>
                                
                                <blockSpan start="12,6" stop="15,6"/>
                                <blockSpan start="12,7" stop="15,7"/>
                                <blockSpan start="12,8" stop="15,8"/>
                                <blockSpan start="12,9" stop="15,9"/>
                                
                                <blockSpan start="16,6" stop="19,6"/>
                                <blockSpan start="16,7" stop="19,7"/>
                                <blockSpan start="16,8" stop="19,8"/>
                                <blockSpan start="16,9" stop="19,9"/>
                                
                                <blockBackground colorName="#F0A9C4" start="0,0" stop="19,0"/>
                                <blockBackground colorName="#CAE7D4" start="0,1" stop="19,-1"/>
                                <blockBackground colorName="#F0A9C4" start="9,5" stop="19,5"/>
                                
                                <blockBackground colorName="#F9F1AD" start="1,3" stop="1,8"/>
                                <blockBackground colorName="#F9F1AD" start="3,3" stop="3,8"/>
                                <blockBackground colorName="#F9F1AD" start="5,3" stop="5,8"/>
                                
                                <blockBackground colorName="#F9F1AD" start="10,2" stop="10,4"/>
                                <blockBackground colorName="#F9F1AD" start="12,2" stop="12,4"/>
                                <blockBackground colorName="#F9F1AD" start="14,2" stop="14,4"/>
                                
                                <blockBackground colorName="#FFFFFF" start="6,3" stop="8,9"/>
                                <blockBackground colorName="#FFFFFF" start="16,2" stop="19,2"/>
                                <blockBackground colorName="#FFFFFF" start="16,4" stop="19,4"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="19,0" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="19,0" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="19,0" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="19,0" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="15,1" stop="19,4" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="15,1" stop="19,4" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="15,1" stop="19,4" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="15,1" stop="19,4" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="0,2" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="6,1" stop="14,1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,2" stop="5,2" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="5,2" stop="5,2" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,3" stop="8,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,3" stop="8,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,3" stop="8,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,3" stop="8,-1" thickness="0.1"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="6,2" stop="8,2" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="7,5" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="7,5" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="7,5" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="7,5" stop="-1,-1" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="10,2" stop="10,4" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="10,2" stop="10,4" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="10,2" stop="10,4" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="10,2" stop="10,4" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="12,2" stop="12,4" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="12,2" stop="12,4" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="12,2" stop="12,4" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="12,2" stop="12,4" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="14,2" stop="14,4" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="14,2" stop="14,4" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="14,2" stop="14,4" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="14,2" stop="14,4" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table11">
                              <blockValign value="TOP"/>
                              <blockLeftPadding value="0"/>
                              <blockRightPadding value="0"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table12">
                              <blockAlignment value="LEFT"/>
                              <blockValign value="TOP"/>
          
                              <blockSpan start="0,2" stop="2,2"/>
          
                              <blockBackground colorName="#EBECEC" start="0,2" stop="2,2"/>
                              <blockBackground colorName="#EBECEC" start="4,2" stop="6,2"/>
                              <blockBackground colorName="#C0C0C2" start="1,0" stop="1,1"/>
                              <blockBackground colorName="#C0C0C2" start="1,3" stop="1,3"/>
                              <blockBackground colorName="#D1D3D4" start="3,0" stop="3,4"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table13">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="MIDDLE"/>
                                
                                <blockSpan start="0,0" stop="7,0"/>
                                <blockSpan start="0,2" stop="8,2"/>
                                <blockSpan start="0,3" stop="8,3"/>
                                <blockSpan start="0,4" stop="8,4"/>
                                <blockSpan start="0,5" stop="8,5"/>
                                <blockSpan start="0,6" stop="8,6"/>
                                <blockSpan start="0,7" stop="8,7"/>
                                <blockSpan start="0,8" stop="8,8"/>
                                <blockSpan start="0,9" stop="8,9"/>
                                <blockSpan start="0,10" stop="8,10"/>
                                <blockSpan start="0,11" stop="8,11"/>
                                <blockSpan start="0,12" stop="8,12"/>
                                
                                <blockBackground colorName="#F0A9C4" start="0,0" stop="8,0"/>
                                
                                <blockBackground colorName="#CAE7D4" start="0,1" stop="0,1"/>
                                <blockBackground colorName="#CAE7D4" start="2,1" stop="2,1"/>
                                <blockBackground colorName="#CAE7D4" start="4,1" stop="4,1"/>
                                <blockBackground colorName="#CAE7D4" start="6,1" stop="6,1"/>
                                
                                <blockBackground colorName="#F9F1AD" start="1,1" stop="1,1"/>
                                <blockBackground colorName="#F9F1AD" start="3,1" stop="3,1"/>
                                <blockBackground colorName="#F9F1AD" start="5,1" stop="5,1"/>
                                <blockBackground colorName="#F9F1AD" start="7,1" stop="7,1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table14">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="MIDDLE"/>
                                
                                <blockSpan start="0,0" stop="5,0"/>
                                <blockBackground colorName="#F0A9C4" start="0,0" stop="6,0"/>
                                <blockBackground colorName="#CAE7D4" start="0,1" stop="5,1"/>
                                <blockBackground colorName="#CAE7D4" start="0,2" stop="0,6"/>
                                <blockBackground colorName="#F9F1AD" start="3,2" stop="5,6"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="1,2" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="1,2" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="1,2" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="1,2" stop="-1,-1" thickness="0.1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="6,0" stop="6,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="6,0" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="6,0" thickness="0.1"/>
                                
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="5,1" stop="5,1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,5" stop="0,5" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="0,1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table15">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="MIDDLE"/>
                                
                                <blockSpan start="0,0" stop="7,0"/>
                                <blockSpan start="8,0" stop="17,0"/>
                                <blockSpan start="15,2" stop="17,2"/>
                                
                                <blockSpan start="8,3" stop="17,3"/>
                                <blockSpan start="8,4" stop="17,4"/>
                                <blockSpan start="8,5" stop="17,5"/>
                                
                                <blockBackground colorName="#F0A9C4" start="0,0" stop="17,0"/>
                                <blockBackground colorName="#CAE7D4" start="0,1" stop="7,1"/>
                                <blockBackground colorName="#CAE7D4" start="8,1" stop="8,2"/>
                                
                                <blockBackground colorName="#CAE7D4" start="10,1" stop="10,2"/>
                                <blockBackground colorName="#CAE7D4" start="12,1" stop="12,2"/>
                                <blockBackground colorName="#CAE7D4" start="14,1" stop="14,2"/>
                                <blockBackground colorName="#CAE7D4" start="16,1" stop="16,1"/>
                                
                                <blockBackground colorName="#F9F1AD" start="9,1" stop="9,2"/>
                                <blockBackground colorName="#F9F1AD" start="11,1" stop="11,2"/>
                                <blockBackground colorName="#F9F1AD" start="13,1" stop="13,2"/>
                                <blockBackground colorName="#F9F1AD" start="15,1" stop="15,1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table16">
                                <blockAlignment value="LEFT"/>
                                <blockValign value="MIDDLE"/>
                                
                                <blockBackground colorName="#CAE7D4" start="0,1" stop="0,1"/>
                                <blockBackground colorName="#CAE7D4" start="2,1" stop="2,1"/>
                                <blockBackground colorName="#CAE7D4" start="4,1" stop="4,1"/>
                                <blockBackground colorName="#CAE7D4" start="7,1" stop="7,1"/>
                                
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="-1,-1" thickness="0.1"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="-1,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <initialize>
                                <paraStyle name="all" alignment="justify"/>
                            </initialize>
                            
                            <paraStyle name="P1" fontName="Helvetica-Bold" fontSize="7.0" leading="9" spaceBefore="0.0" spaceAfter="0.0" alignment="CENTER"/>
                            <paraStyle name="P2" fontName="Helvetica" fontSize="5.0" leading="5" spaceBefore="0.0" spaceAfter="0.0" alignment="CENTER"/>
                            <paraStyle name="P2_LEFT" fontName="Helvetica" fontSize="5.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P3" fontName="Helvetica" fontSize="6.0" leading="8" spaceBefore="0.0" spaceAfter="0.0" alignment="CENTER"/>
                            <paraStyle name="P3_left_bold" fontName="Helvetica-Bold" fontSize="6.0" leading="8" spaceBefore="0.0" spaceAfter="0.0" alignment="LEFT"/>
                            <paraStyle name="P3_LEFT" alignment="LEFT"/>
                            
                            <paraStyle name="P13" fontName="Helvetica-Bold" fontSize="9.0" leading="11" alignment="RIGHT" spaceBefore="0.0" spaceAfter="0.0" textColor="#a0a2a5"/>
                            <paraStyle name="P14_RIGHT" fontName="Helvetica" fontSize="5.0" leading="5" alignment="RIGHT"/>
                            <paraStyle name="P14_LEFT" fontName="Helvetica" fontSize="4.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P14_CENTER" fontName="Helvetica" fontSize="5.0" leading="15" alignment="CENTER"/>
                            
                            <paraStyle name="P144_LEFT" fontName="Helvetica" fontSize="5.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P144_LEFT_COURIER" fontName="Courier" fontSize="6.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P144_CENTER" fontName="Helvetica" fontSize="5.0" leading="5" alignment="CENTER"/>
                            
                            <paraStyle name="P15" fontName="Helvetica" fontSize="6.0" leading="5" alignment="CENTER"/>
                            
                            <paraStyle name="P16" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="CENTER"/>
                            <paraStyle name="P18" fontName="Helvetica" fontSize="8.0" leading="10" alignment="CENTER"/>
                            <paraStyle name="P19" fontName="Helvetica" fontSize="7.0" leading="7" alignment="CENTER"/>
                            
                            <paraStyle name="P20" fontName="Helvetica" fontSize="7.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P20_CENTER" fontName="Helvetica" fontSize="7.0" leading="8" alignment="CENTER"/>
                            <paraStyle name="PP20_CENTER" fontName="Helvetica-Bold" fontSize="7.0" leading="15" alignment="CENTER"/>
                            
                            <paraStyle name="P20_COURIER" fontName="Courier" fontSize="7.0" leading="8" alignment="JUSTIFY"/>
                            <paraStyle name="P20_COURIER_CENTER" fontName="Courier" fontSize="7.0" leading="8" alignment="CENTER"/>
                            
                            <paraStyle name="P200" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="CENTER"/>
                            <paraStyle name="P200_LEFT" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="LEFT"/>
                            
                            <paraStyle name="P220" fontName="Helvetica" fontSize="6.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P220_CENTER" fontName="Helvetica" fontSize="5.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P2220_CENTER" fontName="Helvetica" fontSize="5.0" leading="50" alignment="CENTER"/>
                            <paraStyle name="P220_CENTER_BOLD" fontName="Helvetica-Bold" fontSize="5.0" leading="5" alignment="CENTER"/>
                            
                            <paraStyle name="P221_CENTER" fontName="Helvetica" fontSize="4.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P2211_CENTER" fontName="Helvetica" fontSize="4.0" leading="0" alignment="CENTER"/>
                            <paraStyle name="P222_CENTER" fontName="Helvetica" fontSize="4.0" leading="4" alignment="CENTER"/>
                            
                            <paraStyle name="P26" fontName="Helvetica-Bold" fontSize="9.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P27" fontName="Helvetica-Bold" fontSize="14.0" leading="5" alignment="CENTER"/>
                            
                            <paraStyle name="P22" fontName="Helvetica" fontSize="5.0" leading="5" spaceBefore="0.0" spaceAfter="0.0" alignment="LEFT"/>
                            <paraStyle name="P2222" fontName="Helvetica" fontSize="5.0" leading="15" alignment="LEFT"/>
                            
                            <paraStyle name="P26" fontName="Helvetica-Bold" fontSize="9.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P27" fontName="Helvetica-Bold" fontSize="10.0" leading="5" alignment="RIGHT"/>
                            
                            <paraStyle name="P55" fontName="Helvetica" fontSize="5.0" leading="13" alignment="CENTER"/>
                            <paraStyle name="P55P" fontName="Helvetica" fontSize="4.0" leading="5" alignment="CENTER"/>
                        </stylesheet>"""
                        
            rml += """  <story>"""
            
            rml += """      
                            <section>
                            <blockTable colWidths="296.0,110.0,163.0" style="">
                                <tr><td></td><td></td><td></td></tr>
                            </blockTable>
                            
                            <blockTable colWidths="105.0,114.0,114.0,19.0,19.0,61.0,95.0" rowHeights="8.0,8.0,12.0" style="Table2">
                              <tr>
                                <td><para style="P18">ESTABLECIMIENTO</para></td>
                                <td><para style="P18">NOMBRE</para></td>
                                <td><para style="P18">APELLIDO</para></td>
                                <td><para style="P16">SEXO</para></td>
                                <td><para style="P16"></para></td>
                                <td><para style="P19">NUMERO DE HOJA</para></td>
                                <td><para style="P18">HISTORIA CLINICA</para></td>
                              </tr>
                              
                              <tr>
                                <td>zxc</td>
                                <td>zxc</td>
                                <td>zxc</td>
                                <td><para style="P16">M</para></td>
                                <td><para style="P16">F</para></td>
                                <td>zxc</td>
                                <td>zxc</td>
                              </tr>
                              
                              <tr>
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + (tools.ustr(company.name) if company else "")[0:18]  + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + (tools.ustr(dentist_test.patient_id.first_name) if dentist_test.patient_id.first_name else "")[0:22]  + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + ((tools.ustr(dentist_test.patient_id.last_name) if dentist_test.patient_id.last_name else "") + " " + (tools.ustr(dentist_test.patient_id.slastname) if dentist_test.patient_id.slastname else ""))[0:22] + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + ("X" if dentist_test.patient_id.sex and dentist_test.patient_id.sex == "m" else "") + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + ("X" if dentist_test.patient_id.sex and dentist_test.patient_id.sex == "f" else "") + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER"><font color="black">1</font></para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + (tools.ustr(dentist_test.patient_id.identification_code) if dentist_test.patient_id and dentist_test.patient_id.identification_code else '') + """</font>
                                  </para>
                                </td>
                              </tr>
                            </blockTable>"""
            
            years = self._get_year(dentist_test.patient_id)
            a = True if dentist_test.is_planned and years == 0 else False
            b = True if years >= 1 and years <= 4 else False
            c = True if dentist_test.is_planned and years >= 5 and years <= 9 else False
            d = True if years >= 5 and years <= 14 and not dentist_test.is_planned else False
            e = True if years >= 10 and years <= 14 and dentist_test.is_planned else False
            f = True if years >= 15 and years <= 19 else False
            g = True if years >= 20 else False
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="52.0,10.0,52.0,10.0,72.0,10.0,52.0,10.0,50.0,10.0,55.0,10.0,62.0,10.0,52.0,10.0" rowHeights="15.0" style="Table0">
                                <tr>
                                    <td><para style="P14_LEFT">""" + tools.ustr("MENOR DE 1 AÑO") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if a else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("1-4 AÑOS") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if b else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("5-9 AÑOS PROGRAMADO") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if c else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("5-14 AÑOS NO PROGRAMADO") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if d else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("10-14 AÑOS PROGRAMADO") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if e else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("15-19 AÑOS") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if f else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("MAYOR DE 20 AÑOS") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if g else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("EMBARAZADA") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.patient_id.is_pregnant else "") + """</para></td>
                                </tr>
                            </blockTable>"""
            
            letters_per_row = 123
            
            
            rowHeights = '12.0'
            if dentist_test.mdc_info:
                strMDC = dentist_test.mdc_info.replace('\n',' ')
                if len(strMDC) > 123:
                    filaAlto = 1 
                    tmp = len(strMDC)/123            
                    filaAlto = tmp + 1 if len(strMDC) % 123 != 0 else tmp
                    rowHeights += ',' + str(12.0 * filaAlto)                     
                else:
                    rowHeights += ',12.0'                          
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="140.0,387.0" rowHeights=" """ + str(rowHeights) + """ " style="Table3">
                                <tr>
                                    <td><para style="P20">1.  MOTIVO DE CONSULTA</para></td>
                                    <td><para style="P14_RIGHT">ANOTAR LA CAUSA DEL PROBLEMA EN LA VERSION DEL INFORMANTE</para></td>
                                </tr>
                                
                                <tr><td><para style="P20_COURIER">""" + (tools.ustr(dentist_test.mdc_info) if dentist_test.mdc_info else '') + """</para></td><td></td></tr>
                            </blockTable>"""
            '''
            mdc_info = ''
            if dentist_test.mdc_info:
                word_list = self._get_list_words(dentist_test.mdc_info, letters_per_row)
                mdc_info = word_list[0]
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="140.0,387.0" rowHeights="12.0,12.0" style="Table3">
                                <tr>
                                    <td><para style="P20">1.  MOTIVO DE CONSULTA</para></td>
                                    <td><para style="P14_RIGHT">ANOTAR LA CAUSA DEL PROBLEMA EN LA VERSION DEL INFORMANTE</para></td>
                                </tr>
                                <tr>
                                    <td><para style="P20_COURIER">""" + tools.ustr(mdc_info) + """</para></td><td></td>
                                </tr>
                            </blockTable>"""
            '''
            info_diagnosis = ''
            if dentist_test.info_diagnosis:
                word_list = self._get_list_words(dentist_test.info_diagnosis, letters_per_row * 4)
                info_diagnosis = word_list[0] if len(word_list) >= 1 else ''
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="170.0,357.0" rowHeights="12.0,36.0" style="Table3">
                                <tr>
                                    <td><para style="P20">2.  ENFERMEDAD O PROBLEMA ACTUAL</para></td>
                                    <td><para style="P14_RIGHT">""" + tools.ustr("SINTOMAS: CRONOLOGIA, LOCALIZACIÓN, CARACTERÍSTICAS, INTENSIDAD, CAUSA APARENTE, SÍNTOMAS ASOCIADOS, EVOLUCIÓN, ESTADO ACTUAL.") + """</para></td>
                                </tr>
                                <tr><td><para style="P20_COURIER">""" + tools.ustr(info_diagnosis) + """</para></td><td></td></tr>
                            </blockTable>"""
            
            others_antecedents = ''
            if dentist_test.others_antecedents and dentist_test.others:
                word_list = self._get_list_words(dentist_test.others_antecedents, letters_per_row * 2)
                others_antecedents = word_list[0] if len(word_list) >= 1 else ''
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="40.0,11.0,40.0,11.0,50.0,11.0,35.0,11.0,50.0,11.0,32.0,11.0,40.0,11.0,50.0,11.0,40.0,11.0,40.0,11.0" rowHeights="12.0,12.0,24.0" style="Table4">
                                <tr>
                                    <td><para style="P20">3.  ANTECEDENTES PERSONALES Y FAMILIARES</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P14_LEFT">1. ALERGIA ANTIBIOTICO</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.antibotic_allergic else "") + """</para></td>
                                    <td><para style="P14_LEFT">2. ALERGIA ANESTESIA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.anesthesia_allergic else "") + """</para></td>
                                    <td><para style="P14_LEFT">3. HEMORRAGIAS</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.hemorrhage else "") + """</para></td>
                                    <td><para style="P14_LEFT">4. VIH/SIDA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.vih_sida else "") + """</para></td>
                                    <td><para style="P14_LEFT">5. TUBERCULOSIS</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.tuberculosis else "") + """</para></td>
                                    <td><para style="P14_LEFT">6. ASMA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.asma else "") + """</para></td>
                                    <td><para style="P14_LEFT">7. DIABETES</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.diabetes else "") + """</para></td>
                                    <td><para style="P14_LEFT">8. HIPERTENSION</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.hipertension else "") + """</para></td>
                                    <td><para style="P14_LEFT">9. ENF. CARDIACA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.enf_cardiaca else "") + """</para></td>
                                    <td><para style="P14_LEFT">10. OTRO</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.others else "") + """</para></td>
                                </tr>
                                <tr>
                                    <td><para style="P20_COURIER">""" + tools.ustr(others_antecedents) + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="32.0,35.0,45.0,30.0,45.0,30.0,45.0,30.0,45.0,30.0,23.0,30.0,25.0,30.0,40.0,12.0" rowHeights="12.0,12.0" style="Table5">
                                <tr>
                                    <td><para style="P20">4.  SIGNOS VITALES Y MEDICIONES</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P14_LEFT">""" + tools.ustr("PRESIÓN ARTERIAL") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (dentist_test.pat_info if dentist_test.pat_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("FRECUENCIA CARDIACA min") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(dentist_test.ppm_info) if dentist_test.ppm_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("FRECUENCIA RESPIRAT. min") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(dentist_test.ppr_info) if dentist_test.ppr_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("TEMPERATURA BUCAL °C") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(dentist_test.tem_info) if dentist_test.tem_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("TEMPERATURA AXILAR °C") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(dentist_test.tem2_info) if dentist_test.tem2_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("PESO Kg") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(dentist_test.pes_info) if dentist_test.pes_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("TALLA m") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(dentist_test.size_info) if dentist_test.size_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("NO APLICA") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.not_apply else "") + """</para></td>
                                </tr>
                            </blockTable>"""
            
            stomatognathic_system_observation = ''
            if dentist_test.stomatognathic_system_observation:
                word_list = self._get_list_words(dentist_test.stomatognathic_system_observation, letters_per_row * 4 - 17)
                stomatognathic_system_observation = word_list[0] if len(word_list) >= 1 else ''
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="50,11.0,60,11.0,50,11.0,50,11.0,56,11.0,61,11.0,61,11.0,51,11.0" rowHeights="12.0,12.0,12.0,36.0" style="Table6">
                                <tr>
                                    <td><para style="P20">""" + tools.ustr("5.  EXAMEN DEL SISTEMA ESTOMATOGNÁTICO") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td><para style="P14_RIGHT">""" + tools.ustr("DESCRIBIR LA PATOLOGIA DE LA REGION AFECTADA ANOTANDO EL NUMERO") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P14_LEFT">""" + tools.ustr("1. LABIOS") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.libs else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("2. MEJILLAS") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.cheeks else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("3. MAXILAR SUPERIOR") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.top_max else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("4. MAXILAR INFERIOR") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.bottom_max else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("5. LENGUA") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.tongle else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("6. PALADAR") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.taste else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("7. PISO") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.floor else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("8. CARRILLOS") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.jowls else "") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P14_LEFT">""" + tools.ustr("9. GLANDULAS SALIVALES") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.sal_glands else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("10. ORO FARINGE") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.pharynx else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("11. ATM") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.atm else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("12. GANGLIOS") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.lymph else "") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                <tr>
                                    <td><para style="P20_COURIER">""" + tools.ustr(stomatognathic_system_observation) + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            path = openerp.modules.get_module_path('oemedical_dentist_test')
            path += '/static/src/img/'
            path = os.path.normpath(path)
            
            c_path = os.path.join(path, 'cuadro_print.png')
            o_path = os.path.join(path, 'circulo_print.png')
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="19.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,51.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,19.0" rowHeights="12.0,12.0,7.0,25.0,10.0,92.0,10.0,7.0,25.0,10.0,10.0,12.0,12.0,12.0" style="Table7">
                                <tr>
                                    <td><para style="P20">""" + tools.ustr("6.  ODONTOGRAMA") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P200"></para></td>"""
            
            x = 18
            for y in range(8):
                rml += """          <td><para style="P200">""" + str(x) + """</para></td>
                                    <td><para style="P200"></para></td>"""
                x = x - 1
                                  
            x = 21
            for y in range(8):
                rml += """          <td><para style="P200">""" + str(x) + """</para></td>
                                    <td><para style="P200"></para></td>"""
                x = x + 1
            
            rml += """          </tr>
                                
                                <tr>
                                    <td></td>"""
            
            x = 18
            for y in range(16):
                if x == 10: x = 21
                
                rml += """          <td>
                                        <illustration width="25" height="23" borderStrokeWidth="1" borderStrokeColor="black">
                                            <setFont name="Helvetica-Bold" size="7"/>
                                            <image file="file:""" + c_path + """ " x="0" y="0" width="25" height="23"/>"""
                
                current_piece = self._get_current_piece(dentist_test, x)
                show_others_symbols = True
                
                current_piece_zone_one_symbol = self._get_zone_symbol(current_piece, 'zone_one')
                current_piece_zone_one_color = self._get_zone_color(current_piece, 'zone_one')
                
                current_piece_zone_two_symbol = self._get_zone_symbol(current_piece, 'zone_two')
                current_piece_zone_two_color = self._get_zone_color(current_piece, 'zone_two')
                
                current_piece_zone_three_symbol = self._get_zone_symbol(current_piece, 'zone_three')
                current_piece_zone_three_color = self._get_zone_color(current_piece, 'zone_three')
                
                current_piece_zone_four_symbol = self._get_zone_symbol(current_piece, 'zone_four')
                current_piece_zone_four_color = self._get_zone_color(current_piece, 'zone_four')
                
                current_piece_zone_five_symbol = self._get_zone_symbol(current_piece, 'zone_five')
                current_piece_zone_five_color = self._get_zone_color(current_piece, 'zone_five')
                
                if x == 11: next_piece = self._get_current_piece(dentist_test, 21)
                elif x >= 21: next_piece = self._get_current_piece(dentist_test, x+1)
                else: next_piece = self._get_current_piece(dentist_test, x-1)
                
                if x == 21: before_piece = self._get_current_piece(dentist_test, 11)
                elif x > 21: before_piece = self._get_current_piece(dentist_test, x-1)
                else: before_piece = self._get_current_piece(dentist_test, x+1)
                
                if x == 16:
                    pass
                
                if (self._has_symbol_0_0(current_piece)):
                        show_others_symbols = False
                        rml += """          <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                0.0 8.0 23.0 8.0
                                                0.0 15.0 23.0 15.0
                                            </lines>"""
                
                # Piece extraction...
                if self._has_symbol_x(current_piece):
                    show_others_symbols = False
                    rml += """              <lineMode width="2" cap="round"/>"""
                    if self._has_symbol_x(current_piece) == 'red': rml += """<stroke color="red"/>"""
                    if self._has_symbol_x(current_piece) == 'blue': rml += """<stroke color="blue"/>"""
                    rml += """              <lines>-1.0 24.0 26.0 -1.0 -1.0 -1.0 26.0 24.0</lines>"""
                
                # Total prosthesis...
                elif current_piece and current_piece.total_prosthesis:
                    show_others_symbols = False
                    rml += """              <stroke color="blue"/>
                                            <lineMode width="2" cap="round"/>
                                            <lines>
                                                -1.0 -1.0 -1.0 24.0
                                                -1.0 24.0 24.0 24.0
                                                24.0 24.0 24.0 -1.0
                                                -1.0 -1.0 24.0 -1.0
                                            </lines>"""
                    
                    if self._has_symbol_0_0(next_piece):
                        if x == 11:
                            rml += """      <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                24.0 8.0 80.0 8.0
                                                24.0 15.0 80.0 15.0
                                            </lines>"""
                        else:
                            rml += """      <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                24.0 8.0 28.0 8.0
                                                24.0 15.0 28.0 15.0
                                            </lines>"""
                
                # In place prosthesis...
                elif self._has_symbol_0_0(current_piece) and (self._has_symbol_0_0(next_piece) or (next_piece and next_piece.total_prosthesis)):
                    show_others_symbols = False
                    rml += """              <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                24.0 8.0 28.0 8.0
                                                24.0 15.0 28.0 15.0
                                            </lines>"""
                    
                    if (self._has_symbol_0_0(before_piece) or (before_piece and before_piece.total_prosthesis)):
                        show_others_symbols = False
                        rml += """          <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                0.0 8.0 23.0 8.0
                                                0.0 15.0 23.0 15.0
                                            </lines>"""
                    
                    if x == 11:
                        rml += """          <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                24.0 8.0 80.0 8.0
                                                24.0 15.0 80.0 15.0
                                            </lines>"""
                
                # Removible prosthesis...
                elif self._has_symbol_w(current_piece):
                    show_others_symbols = False
                
                # Symbol C and I...
                elif self._has_symbol_i(current_piece) and self._has_symbol_c(current_piece):
                    show_others_symbols = False
                
                # Symbol I...
                elif self._has_symbol_i(current_piece) and not self._has_symbol_c(current_piece):
                    show_others_symbols = False
                    rml += """              <setFont name="Liberation Serif" size="32"/>"""
                    if self._has_symbol_i(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    if self._has_symbol_i(current_piece) == 'red': rml += """<fill color="red"/>"""
                    rml += """              <drawCentredString x="11.5" y="1.0">I</drawCentredString>"""
                
                # Symbol C...
                elif self._has_symbol_c(current_piece) and not self._has_symbol_i(current_piece):
                    show_others_symbols = False
                    rml += """              <setFont name="Liberation Serif" size="32"/>"""
                    if self._has_symbol_c(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    if self._has_symbol_c(current_piece) == 'red': rml += """<fill color="red"/>"""
                    rml += """              <drawCentredString x="10.5" y="1.0">C</drawCentredString>"""
                
                
                if show_others_symbols:
                    # Zone 1 ##############################################
                    if current_piece_zone_one_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_one_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>3.0 21.5 21.0 21.5</lines>"""
                        rml += """          <lines>3.5 21.0 21.0 21.0</lines>"""
                        rml += """          <lines>4.5 20.0 20.0 20.0</lines>"""
                        rml += """          <lines>5.5 19.0 19.0 19.0</lines>"""
                        rml += """          <lines>6.5 18.0 18.0 18.0</lines>"""
                        rml += """          <lines>7.5 17.0 17.0 17.0</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_one_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>6.5 19.0 18.0 19.0</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="17">""" + (current_piece_zone_one_symbol if current_piece_zone_one_symbol else '') + """</drawString>"""
                    
                    # Zone 2 ##############################################
                    if current_piece_zone_two_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_two_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>1.5 3.5 1.5 20.0</lines>"""
                        rml += """          <lines>2.0 4.0 2.0 19.5</lines>"""
                        rml += """          <lines>3.0 5.0 3.0 18.5</lines>"""
                        rml += """          <lines>4.0 6.0 4.0 17.5</lines>"""
                        rml += """          <lines>5.0 7.0 5.0 16.5</lines>"""
                        rml += """          <lines>5.5 8.0 5.5 15.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_two_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>3.0 7.0 3.0 16.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="2" y="9">""" + (current_piece_zone_two_symbol if current_piece_zone_two_symbol else '' ) + """</drawString>"""
                    
                    # Zone 3 ##############################################
                    if current_piece_zone_three_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_three_symbol == 'K':
                        rml += """          <lineMode width="7.5" cap="square"/>"""
                        rml += """          <lines>11.0 11.7 13.5 11.7</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_three_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>11.0 11.7 13.5 11.7</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="9">""" + (current_piece_zone_three_symbol if current_piece_zone_three_symbol else '') + """</drawString>"""
                
                    # Zone 4 ##############################################
                    if current_piece_zone_four_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_four_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>22.0 3.0 22.0 20.0</lines>"""
                        rml += """          <lines>21.5 3.5 21.5 19.5</lines>"""
                        rml += """          <lines>20.5 4.5 20.5 18.5</lines>"""
                        rml += """          <lines>19.5 5.5 19.5 17.5</lines>"""
                        rml += """          <lines>18.5 6.5 18.5 16.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_four_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>20.5 6.5 20.5 16.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="18" y="9">""" + (current_piece_zone_four_symbol if current_piece_zone_four_symbol else '') + """</drawString>"""
                    
                    # Zone 5 ##############################################
                    if current_piece_zone_five_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_five_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>7.5 6.0 17.0 6.0</lines>"""
                        rml += """          <lines>6.5 5.0 18.0 5.0</lines>"""
                        rml += """          <lines>5.5 4.0 19.0 4.0</lines>"""
                        rml += """          <lines>4.5 3.0 20.0 3.0</lines>"""
                        rml += """          <lines>3.5 2.0 21.0 2.0</lines>"""
                        rml += """          <lines>3.0 1.5 21.0 1.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_five_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>6.5 4.0 18.0 4.0</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="1">""" + (current_piece_zone_five_symbol if current_piece_zone_five_symbol else '') + """</drawString>"""
                
                rml += """              </illustration>
                                    </td>
                                    <td></td>"""
                
                if x >= 21: x = x + 1
                else: x = x - 1
            
            rml += """          </tr>
                                <tr>
                                    <td></td>
                                    <td>
                                        <illustration width="489" height="10" borderStrokeWidth="1" borderStrokeColor="black">"""
            
            if self._has_symbol_w(dentist_test.piece18) and self._has_symbol_w(dentist_test.piece17):
                rml += """                  <lines>
                                                13.0 8.0 25.0 3.0
                                                25.0 3.0 37.0 8.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece17) and self._has_symbol_w(dentist_test.piece16):
                rml += """                  <lines>
                                                41.0 8.0 53.0 3.0
                                                53.0 3.0 65.0 8.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece16) and self._has_symbol_w(dentist_test.piece15):
                rml += """                  <lines>
                                                69.0 8.0 81.0 3.0
                                                81.0 3.0 93.0 8.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece15) and self._has_symbol_w(dentist_test.piece14):
                rml += """                  <lines>
                                                97.0 8.0 109.0 3.0
                                                109.0 3.0 121.0 8.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece14) and self._has_symbol_w(dentist_test.piece13):
                rml += """                  <lines>
                                                125.0 8.0 137.0 3.0
                                                137.0 3.0 149.0 8.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece13) and self._has_symbol_w(dentist_test.piece12):
                rml += """                  <lines>
                                                153.0 8.0 165.0 3.0
                                                165.0 3.0 177.0 8.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece12) and self._has_symbol_w(dentist_test.piece11):
                rml += """                  <lines>
                                                181.0 8.0 193.0 3.0
                                                193.0 3.0 205.0 8.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece11) and self._has_symbol_w(dentist_test.piece21):
                rml += """                  <lines>
                                                209.0 5.0 245.5 0.0
                                                245.5 0.0 278.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece21) and self._has_symbol_w(dentist_test.piece22):
                rml += """                  <lines>
                                                282.0 5.0 294.5 0.0
                                                294.5 0.0 306.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece22) and self._has_symbol_w(dentist_test.piece23):
                rml += """                  <lines>
                                                310.0 5.0 322.5 0.0
                                                322.5 0.0 334.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece23) and self._has_symbol_w(dentist_test.piece24):
                rml += """                  <lines>
                                                338.0 5.0 350.5 0.0
                                                350.5 0.0 362.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece24) and self._has_symbol_w(dentist_test.piece25):
                rml += """                  <lines>
                                                366.0 5.0 378.5 0.0
                                                378.5 0.0 390.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece25) and self._has_symbol_w(dentist_test.piece26):
                rml += """                  <lines>
                                                394.0 5.0 406.5 0.0
                                                406.5 0.0 418.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece26) and self._has_symbol_w(dentist_test.piece27):
                rml += """                  <lines>
                                                422.0 5.0 434.5 0.0
                                                434.5 0.0 446.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece27) and self._has_symbol_w(dentist_test.piece28):
                rml += """                  <lines>
                                                450.0 5.0 462.5 0.0
                                                462.5 0.0 474.0 5.0
                                            </lines>"""
            
            if self._has_symbol_c(dentist_test.piece18) and self._has_symbol_i(dentist_test.piece18):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="0.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece18) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece18) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="6.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="10.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece18) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece18) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="14.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece17) and self._has_symbol_i(dentist_test.piece17):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="28.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece17) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece17) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="34.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="38.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece17) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece17) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="42.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece16) and self._has_symbol_i(dentist_test.piece16):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="56.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece16) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece16) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="62.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="66.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece16) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece16) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="70.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece15) and self._has_symbol_i(dentist_test.piece15):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="84.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece15) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece15) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="90.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="94.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece15) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece15) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="98.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece14) and self._has_symbol_i(dentist_test.piece14):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="112.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece14) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece14) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="118.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="122.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece14) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece14) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="126.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece13) and self._has_symbol_i(dentist_test.piece13):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="140.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece13) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece13) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="146.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="150.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece13) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece13) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="154.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece12) and self._has_symbol_i(dentist_test.piece12):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="168.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece12) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece12) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="174.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="178.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece12) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece12) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="182.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece11) and self._has_symbol_i(dentist_test.piece11):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="196.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece11) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece11) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="202.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="206.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece11) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece11) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="210.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece21) and self._has_symbol_i(dentist_test.piece21):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="270.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece21) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece21) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="276.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="280.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece21) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece21) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="284.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece22) and self._has_symbol_i(dentist_test.piece22):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="298.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece22) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece22) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="304.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="308.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece22) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece22) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="312.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece23) and self._has_symbol_i(dentist_test.piece23):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="326.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece23) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece23) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="332.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="336.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece23) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece23) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="340.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece24) and self._has_symbol_i(dentist_test.piece24):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="354.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece24) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece24) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="360.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="364.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece24) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece24) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="368.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece25) and self._has_symbol_i(dentist_test.piece25):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="382.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece25) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece25) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="388.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="394.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece25) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece25) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="398.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece26) and self._has_symbol_i(dentist_test.piece26):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="410.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece26) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece26) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="416.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="420.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece26) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece26) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="424.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece27) and self._has_symbol_i(dentist_test.piece27):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="438.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece27) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece27) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="444.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="448.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece27) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece27) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="452.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece28) and self._has_symbol_i(dentist_test.piece28):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="466.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece28) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece28) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="472.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="476.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece28) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece28) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="480.5" y="2.0">I</drawCentredString>"""
            
            rml += """                  </illustration>
                                    </td>
                                    
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td>
                                    
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td></td><td></td><td></td>
                                    <td>
                                        <blockTable colWidths="5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,145.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0" rowHeights="8.0,25.0,12.0,8.0,25.0,12.0" style="Table8">
                                            <tr>
                                                <td></td>
                                                <td><para style="P200">55</para></td>
                                                <td></td>
                                                <td><para style="P200">54</para></td>
                                                <td></td>
                                                <td><para style="P200">53</para></td>
                                                <td></td>
                                                <td><para style="P200">52</para></td>
                                                <td></td>
                                                <td><para style="P200">51</para></td>
                                                
                                                <td></td>
                                                
                                                <td><para style="P200">61</para></td>
                                                <td></td>
                                                <td><para style="P200">62</para></td>
                                                <td></td>
                                                <td><para style="P200">63</para></td>
                                                <td></td>
                                                <td><para style="P200">64</para></td>
                                                <td></td>
                                                <td><para style="P200">65</para></td>
                                                <td></td>
                                            </tr>
                                            
                                            <tr>
                                                <td></td>"""
            
            x = 55
            for y in range(10):
                if x == 50: x = 61
                
                rml += """                      <td>
                                                    <illustration width="25" height="23" borderStrokeWidth="1" borderStrokeColor="black">
                                                        <setFont name="Helvetica-Bold" size="7"/>
                                                        <image file="file:""" + o_path + """ " x="0" y="0" width="25" height="23"/>"""
                
                current_piece = self._get_current_piece(dentist_test, x)
                show_others_symbols = True
                
                current_piece_zone_one_symbol = self._get_zone_symbol(current_piece, 'zone_one')
                current_piece_zone_one_color = self._get_zone_color(current_piece, 'zone_one')
                
                current_piece_zone_two_symbol = self._get_zone_symbol(current_piece, 'zone_two')
                current_piece_zone_two_color = self._get_zone_color(current_piece, 'zone_two')
                
                current_piece_zone_three_symbol = self._get_zone_symbol(current_piece, 'zone_three')
                current_piece_zone_three_color = self._get_zone_color(current_piece, 'zone_three')
                
                current_piece_zone_four_symbol = self._get_zone_symbol(current_piece, 'zone_four')
                current_piece_zone_four_color = self._get_zone_color(current_piece, 'zone_four')
                
                current_piece_zone_five_symbol = self._get_zone_symbol(current_piece, 'zone_five')
                current_piece_zone_five_color = self._get_zone_color(current_piece, 'zone_five')
                
                if x == 51: next_piece = self._get_current_piece(dentist_test, 61)
                elif x >= 61: next_piece = self._get_current_piece(dentist_test, x+1)
                else: next_piece = self._get_current_piece(dentist_test, x-1)
                
                if x == 61: before_piece = self._get_current_piece(dentist_test, 51)
                elif x > 61: before_piece = self._get_current_piece(dentist_test, x-1)
                else: before_piece = self._get_current_piece(dentist_test, x+1)
                
                # Piece extraction...
                if self._has_symbol_x(current_piece):
                    show_others_symbols = False
                    rml += """                          <lineMode width="2" cap="round"/>"""
                    if self._has_symbol_x(current_piece) == 'red': rml += """<stroke color="red"/>"""
                    if self._has_symbol_x(current_piece) == 'blue': rml += """<stroke color="blue"/>"""
                    rml += """                          <lines>1.0 22.0 24.0 1.0 1.0 1.0 24.0 22.0</lines>"""
                
                # Symbol C and I...
                elif self._has_symbol_i(current_piece) and self._has_symbol_c(current_piece):
                    show_others_symbols = False
                
                # Symbol I...
                elif self._has_symbol_i(current_piece) and not self._has_symbol_c(current_piece):
                    show_others_symbols = False
                    rml += """                          <setFont name="Liberation Serif" size="32"/>"""
                    if self._has_symbol_i(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    if self._has_symbol_i(current_piece) == 'red': rml += """<fill color="red"/>"""
                    rml += """                          <drawCentredString x="13.0" y="1.0">I</drawCentredString>"""
                
                # Symbol C...
                elif self._has_symbol_c(current_piece) and not self._has_symbol_i(current_piece):
                    show_others_symbols = False
                    rml += """                          <setFont name="Liberation Serif" size="32"/>"""
                    if self._has_symbol_c(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    if self._has_symbol_c(current_piece) == 'red': rml += """<fill color="red"/>"""
                    rml += """                          <drawCentredString x="11.5" y="1.0">C</drawCentredString>"""
                
                if show_others_symbols:
                    # Zone 1 ##############################################
                    if current_piece_zone_one_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_one_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>7.5 21.0 17.0 21.0</lines>"""
                        rml += """          <lines>4.5 20.0 20.0 20.0</lines>"""
                        rml += """          <lines>5.5 19.0 19.0 19.0</lines>"""
                        rml += """          <lines>6.5 18.0 18.0 18.0</lines>"""
                        rml += """          <lines>7.5 17.0 17.0 17.0</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_one_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>6.0 18.5 18.0 18.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="17">""" + (current_piece_zone_one_symbol if current_piece_zone_one_symbol else '') + """</drawString>"""
                    
                    # Zone 2 ##############################################
                    if current_piece_zone_two_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_two_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>2.0 8.0 2.0 15.5</lines>"""
                        rml += """          <lines>3.0 5.0 3.0 18.5</lines>"""
                        rml += """          <lines>4.0 6.0 4.0 17.5</lines>"""
                        rml += """          <lines>5.0 7.0 5.0 16.5</lines>"""
                        rml += """          <lines>5.5 8.0 5.5 15.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_two_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>4.0 6.5 4.0 16.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="2" y="9">""" + (current_piece_zone_two_symbol if current_piece_zone_two_symbol else '' ) + """</drawString>"""
                    
                    # Zone 3 ##############################################
                    if current_piece_zone_three_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_three_symbol == 'K':
                        rml += """          <lineMode width="7.5" cap="square"/>"""
                        rml += """          <lines>12.0 11.7 13.5 11.7</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_three_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <circle x="13.0" y="11.5" radius="3.5" fill="yes" stroke="no"/>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="9">""" + (current_piece_zone_three_symbol if current_piece_zone_three_symbol else '') + """</drawString>"""
                    
                    # Zone 4 ##############################################
                    if current_piece_zone_four_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_four_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>23.0 7.5 23.0 16.0</lines>"""
                        rml += """          <lines>22.5 6.5 22.5 16.5</lines>"""
                        rml += """          <lines>22.0 6.5 22.0 16.5</lines>"""
                        rml += """          <lines>20.5 4.5 20.5 18.5</lines>"""
                        rml += """          <lines>19.5 5.5 19.5 17.5</lines>"""
                        rml += """          <lines>18.5 6.5 18.5 16.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_four_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>21.0 6.5 21.0 16.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="18" y="9">""" + (current_piece_zone_four_symbol if current_piece_zone_four_symbol else '') + """</drawString>"""
                    
                    # Zone 5 ##############################################
                    if current_piece_zone_five_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_five_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>7.5 6.0 17.0 6.0</lines>"""
                        rml += """          <lines>6.5 5.0 18.0 5.0</lines>"""
                        rml += """          <lines>5.5 4.0 19.0 4.0</lines>"""
                        rml += """          <lines>5.5 3.0 19.5 3.0</lines>"""
                        rml += """          <lines>7.5 2.0 17.0 2.0</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_five_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>6.0 4.5 18.0 4.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="1">""" + (current_piece_zone_five_symbol if current_piece_zone_five_symbol else '') + """</drawString>"""
                
                rml += """                          </illustration>
                                                </td>
                                                <td></td>"""
            
                if x >= 61: x = x + 1
                else: x = x - 1
            
            rml += """                      </tr>"""
                                            
            rml += """                      <tr>"""
            
            x = 55
            for y in range(10):
                if x == 50: x = 61
                current_piece = self._get_current_piece(dentist_test, x)
            
                rml += """                      <td></td>
                                                <td>"""
                
                if self._has_symbol_c(current_piece) and self._has_symbol_i(current_piece):
                    rml += """                      <illustration width="25" height="10" borderStrokeWidth="1" borderStrokeColor="black">
                                                        <stroke color="black"/>
                                                        <setFont name="Helvetica" size="6"/>
                                                        <rect x="2.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                    
                    if self._has_symbol_c(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    else: rml += """                    <fill color="red"/>"""
                    
                    rml += """                          <drawCentredString x="8.5" y="2.0">C</drawCentredString>"""
                    rml += """                          <fill color="black"/>"""
                    rml += """                          <drawCentredString x="12.5" y="2.0">/</drawCentredString>"""
                    
                    if self._has_symbol_i(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    else: rml += """                    <fill color="red"/>"""
                    rml += """                          <drawCentredString x="16.5" y="2.0">I</drawCentredString>"""
                    rml += """                      </illustration>"""
                
                rml += """                      </td>"""
                
                if x >= 61: x = x + 1
                else: x = x - 1
            
            rml += """                      </tr>"""
                                            
            rml += """                      <tr>
                                                <td></td>
                                                <td><para style="P200">85</para></td>
                                                <td></td>
                                                <td><para style="P200">84</para></td>
                                                <td></td>
                                                <td><para style="P200">83</para></td>
                                                <td></td>
                                                <td><para style="P200">82</para></td>
                                                <td></td>
                                                <td><para style="P200">81</para></td>
                                                
                                                <td></td>
                                                
                                                <td><para style="P200">71</para></td>
                                                <td></td>
                                                <td><para style="P200">72</para></td>
                                                <td></td>
                                                <td><para style="P200">73</para></td>
                                                <td></td>
                                                <td><para style="P200">74</para></td>
                                                <td></td>
                                                <td><para style="P200">75</para></td>
                                                <td></td>
                                            </tr>
                                            
                                            <tr>
                                                <td></td>"""
            
            x = 85
            for y in range(10):
                if x == 80: x = 71
                
                rml += """                      <td>
                                                    <illustration width="25" height="23" borderStrokeWidth="1" borderStrokeColor="black">
                                                        <setFont name="Helvetica-Bold" size="7"/>
                                                        <image file="file:""" + o_path + """ " x="0" y="0" width="25" height="23"/>"""
                
                current_piece = self._get_current_piece(dentist_test, x)
                show_others_symbols = True
                
                current_piece_zone_one_symbol = self._get_zone_symbol(current_piece, 'zone_one')
                current_piece_zone_one_color = self._get_zone_color(current_piece, 'zone_one')
                
                current_piece_zone_two_symbol = self._get_zone_symbol(current_piece, 'zone_two')
                current_piece_zone_two_color = self._get_zone_color(current_piece, 'zone_two')
                
                current_piece_zone_three_symbol = self._get_zone_symbol(current_piece, 'zone_three')
                current_piece_zone_three_color = self._get_zone_color(current_piece, 'zone_three')
                
                current_piece_zone_four_symbol = self._get_zone_symbol(current_piece, 'zone_four')
                current_piece_zone_four_color = self._get_zone_color(current_piece, 'zone_four')
                
                current_piece_zone_five_symbol = self._get_zone_symbol(current_piece, 'zone_five')
                current_piece_zone_five_color = self._get_zone_color(current_piece, 'zone_five')
                
                if x == 81: next_piece = self._get_current_piece(dentist_test, 71)
                elif x > 81: next_piece = self._get_current_piece(dentist_test, x-1)
                else: next_piece = self._get_current_piece(dentist_test, x+1)
                
                if x == 71: before_piece = self._get_current_piece(dentist_test, 81)
                elif x >= 81: before_piece = self._get_current_piece(dentist_test, x+1)
                else: before_piece = self._get_current_piece(dentist_test, x-1)
                
                # Piece extraction...
                if self._has_symbol_x(current_piece):
                    show_others_symbols = False
                    rml += """                          <lineMode width="2" cap="round"/>"""
                    if self._has_symbol_x(current_piece) == 'red': rml += """<stroke color="red"/>"""
                    if self._has_symbol_x(current_piece) == 'blue': rml += """<stroke color="blue"/>"""
                    rml += """                          <lines>1.0 22.0 24.0 1.0 1.0 1.0 24.0 22.0</lines>"""
                
                # Symbol C and I...
                elif self._has_symbol_i(current_piece) and self._has_symbol_c(current_piece):
                    show_others_symbols = False
                
                # Symbol I...
                elif self._has_symbol_i(current_piece) and not self._has_symbol_c(current_piece):
                    show_others_symbols = False
                    rml += """                          <setFont name="Liberation Serif" size="32"/>"""
                    if self._has_symbol_i(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    if self._has_symbol_i(current_piece) == 'red': rml += """<fill color="red"/>"""
                    rml += """                          <drawCentredString x="13.0" y="1.0">I</drawCentredString>"""
                
                # Symbol C...
                elif self._has_symbol_c(current_piece) and not self._has_symbol_i(current_piece):
                    show_others_symbols = False
                    rml += """                          <setFont name="Liberation Serif" size="32"/>"""
                    if self._has_symbol_c(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    if self._has_symbol_c(current_piece) == 'red': rml += """<fill color="red"/>"""
                    rml += """                          <drawCentredString x="11.5" y="1.0">C</drawCentredString>"""
                
                if show_others_symbols:
                    # Zone 1 ##############################################
                    if current_piece_zone_one_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_one_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>7.5 21.0 17.0 21.0</lines>"""
                        rml += """          <lines>4.5 20.0 20.0 20.0</lines>"""
                        rml += """          <lines>5.5 19.0 19.0 19.0</lines>"""
                        rml += """          <lines>6.5 18.0 18.0 18.0</lines>"""
                        rml += """          <lines>7.5 17.0 17.0 17.0</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_one_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>6.0 18.5 18.0 18.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="17">""" + (current_piece_zone_one_symbol if current_piece_zone_one_symbol else '') + """</drawString>"""
                    
                    # Zone 2 ##############################################
                    if current_piece_zone_two_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_two_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>2.0 8.0 2.0 15.5</lines>"""
                        rml += """          <lines>3.0 5.0 3.0 18.5</lines>"""
                        rml += """          <lines>4.0 6.0 4.0 17.5</lines>"""
                        rml += """          <lines>5.0 7.0 5.0 16.5</lines>"""
                        rml += """          <lines>5.5 8.0 5.5 15.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_two_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>4.0 6.5 4.0 16.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="2" y="9">""" + (current_piece_zone_two_symbol if current_piece_zone_two_symbol else '' ) + """</drawString>"""
                    
                    # Zone 3 ##############################################
                    if current_piece_zone_three_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_three_symbol == 'K':
                        rml += """          <lineMode width="7.5" cap="square"/>"""
                        rml += """          <lines>12.0 11.7 13.5 11.7</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_three_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <circle x="13.0" y="11.5" radius="3.5" fill="yes" stroke="no"/>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="9">""" + (current_piece_zone_three_symbol if current_piece_zone_three_symbol else '') + """</drawString>"""
                    
                    # Zone 4 ##############################################
                    if current_piece_zone_four_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_four_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>23.0 7.5 23.0 16.0</lines>"""
                        rml += """          <lines>22.5 6.5 22.5 16.5</lines>"""
                        rml += """          <lines>22.0 6.5 22.0 16.5</lines>"""
                        rml += """          <lines>20.5 4.5 20.5 18.5</lines>"""
                        rml += """          <lines>19.5 5.5 19.5 17.5</lines>"""
                        rml += """          <lines>18.5 6.5 18.5 16.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_four_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>21.0 6.5 21.0 16.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="18" y="9">""" + (current_piece_zone_four_symbol if current_piece_zone_four_symbol else '') + """</drawString>"""
                    
                    # Zone 5 ##############################################
                    if current_piece_zone_five_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_five_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>7.5 6.0 17.0 6.0</lines>"""
                        rml += """          <lines>6.5 5.0 18.0 5.0</lines>"""
                        rml += """          <lines>5.5 4.0 19.0 4.0</lines>"""
                        rml += """          <lines>5.5 3.0 19.5 3.0</lines>"""
                        rml += """          <lines>7.5 2.0 17.0 2.0</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_five_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>6.0 4.5 18.0 4.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="1">""" + (current_piece_zone_five_symbol if current_piece_zone_five_symbol else '') + """</drawString>"""
                
                rml += """                          </illustration>
                                                </td>
                                                <td></td>"""
            
                if x >= 81: x = x - 1
                else: x = x + 1
            
            rml += """                      </tr>"""
            
            rml += """                      <tr>"""
            
            x = 85
            for y in range(10):
                if x == 80: x = 71
                current_piece = self._get_current_piece(dentist_test, x)
            
                rml += """                      <td></td>
                                                <td>"""
                
                if self._has_symbol_c(current_piece) and self._has_symbol_i(current_piece):
                    rml += """                      <illustration width="25" height="10" borderStrokeWidth="1" borderStrokeColor="black">
                                                        <stroke color="black"/>
                                                        <setFont name="Helvetica" size="6"/>
                                                        <rect x="2.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                    
                    if self._has_symbol_c(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    else: rml += """                    <fill color="red"/>"""
                    
                    rml += """                          <drawCentredString x="8.5" y="2.0">C</drawCentredString>"""
                    rml += """                          <fill color="black"/>"""
                    rml += """                          <drawCentredString x="12.5" y="2.0">/</drawCentredString>"""
                    
                    if self._has_symbol_i(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    else: rml += """                    <fill color="red"/>"""
                    rml += """                          <drawCentredString x="16.5" y="2.0">I</drawCentredString>"""
                    rml += """                      </illustration>"""
                
                rml += """                      </td>"""
                
                if x >= 81: x = x - 1
                else: x = x + 1
            
            rml += """                      </tr>"""
                                        
            rml += """                  </blockTable>
                                    </td>
                                    
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">48</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">47</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">46</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">45</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">44</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">43</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">42</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">41</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">31</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">32</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">33</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">34</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">35</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">36</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">37</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200">38</para></td>
                                    <td><para style="P200"></para></td>
                                </tr>
                                
                                <tr>
                                    <td></td>"""
            
            x = 48
            for y in range(16):
                if x == 40: x = 31
                
                if x == 41:
                    pass
                
                rml += """          <td>
                                        <illustration width="25" height="23" borderStrokeWidth="1" borderStrokeColor="black">
                                            <setFont name="Helvetica-Bold" size="7"/>
                                            <image file="file:""" + c_path + """ " x="0" y="0" width="25" height="23"/>"""
                
                current_piece = self._get_current_piece(dentist_test, x)
                show_others_symbols = True
                
                current_piece_zone_one_symbol = self._get_zone_symbol(current_piece, 'zone_one')
                current_piece_zone_one_color = self._get_zone_color(current_piece, 'zone_one')
                
                current_piece_zone_two_symbol = self._get_zone_symbol(current_piece, 'zone_two')
                current_piece_zone_two_color = self._get_zone_color(current_piece, 'zone_two')
                
                current_piece_zone_three_symbol = self._get_zone_symbol(current_piece, 'zone_three')
                current_piece_zone_three_color = self._get_zone_color(current_piece, 'zone_three')
                
                current_piece_zone_four_symbol = self._get_zone_symbol(current_piece, 'zone_four')
                current_piece_zone_four_color = self._get_zone_color(current_piece, 'zone_four')
                
                current_piece_zone_five_symbol = self._get_zone_symbol(current_piece, 'zone_five')
                current_piece_zone_five_color = self._get_zone_color(current_piece, 'zone_five')
                
                if x == 41: next_piece = self._get_current_piece(dentist_test, 31)
                elif x > 41: next_piece = self._get_current_piece(dentist_test, x-1)
                else: next_piece = self._get_current_piece(dentist_test, x+1)
                
                if x == 31: before_piece = self._get_current_piece(dentist_test, 41)
                elif x > 31: before_piece = self._get_current_piece(dentist_test, x+1)
                else: before_piece = self._get_current_piece(dentist_test, x-1)
                
                if (self._has_symbol_0_0(current_piece)):
                    show_others_symbols = False
                    rml += """          <stroke color="blue"/>
                                        <lineMode width="2" cap="square"/>
                                        <lines>
                                            0.0 8.0 23.0 8.0
                                            0.0 15.0 23.0 15.0
                                        </lines>"""
                
                # Piece extraction...
                if self._has_symbol_x(current_piece):
                    show_others_symbols = False
                    rml += """              <lineMode width="2" cap="round"/>"""
                    if self._has_symbol_x(current_piece) == 'red': rml += """<stroke color="red"/>"""
                    if self._has_symbol_x(current_piece) == 'blue': rml += """<stroke color="blue"/>"""
                    rml += """              <lines>-1.0 24.0 26.0 -1.0 -1.0 -1.0 26.0 24.0</lines>"""
                
                # Total prosthesis...
                elif current_piece and current_piece.total_prosthesis:
                    show_others_symbols = False
                    rml += """              <stroke color="blue"/>
                                            <lineMode width="2" cap="round"/>
                                            <lines>
                                                -1.0 -1.0 -1.0 24.0
                                                -1.0 24.0 24.0 24.0
                                                24.0 24.0 24.0 -1.0
                                                -1.0 -1.0 24.0 -1.0
                                            </lines>"""
                    
                    if self._has_symbol_0_0(next_piece):
                        if x == 41:
                            rml += """      <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                24.0 8.0 80.0 8.0
                                                24.0 15.0 80.0 15.0
                                            </lines>"""
                        else:
                            rml += """      <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                24.0 8.0 28.0 8.0
                                                24.0 15.0 28.0 15.0
                                            </lines>"""
                
                # In place prosthesis...
                elif self._has_symbol_0_0(current_piece) and (self._has_symbol_0_0(next_piece) or (next_piece and next_piece.total_prosthesis)):
                    show_others_symbols = False
                    rml += """              <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                24.0 8.0 28.0 8.0
                                                24.0 15.0 28.0 15.0
                                            </lines>"""
                    
                    if (self._has_symbol_0_0(before_piece) or (before_piece and before_piece.total_prosthesis)):
                        show_others_symbols = False
                        rml += """          <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                0.0 8.0 23.0 8.0
                                                0.0 15.0 23.0 15.0
                                            </lines>"""
                    
                    if x == 41:
                        rml += """          <stroke color="blue"/>
                                            <lineMode width="2" cap="square"/>
                                            <lines>
                                                24.0 8.0 80.0 8.0
                                                24.0 15.0 80.0 15.0
                                            </lines>"""
                
                # Removible prosthesis...
                elif self._has_symbol_w(current_piece):
                    show_others_symbols = False
                
                # Symbol C and I...
                elif self._has_symbol_i(current_piece) and self._has_symbol_c(current_piece):
                    show_others_symbols = False
                
                # Symbol I...
                elif self._has_symbol_i(current_piece) and not self._has_symbol_c(current_piece):
                    show_others_symbols = False
                    rml += """              <setFont name="Liberation Serif" size="32"/>"""
                    if self._has_symbol_i(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    if self._has_symbol_i(current_piece) == 'red': rml += """<fill color="red"/>"""
                    rml += """              <drawCentredString x="11.5" y="1.0">I</drawCentredString>"""
                
                # Symbol C...
                elif self._has_symbol_c(current_piece) and not self._has_symbol_i(current_piece):
                    show_others_symbols = False
                    rml += """              <setFont name="Liberation Serif" size="32"/>"""
                    if self._has_symbol_c(current_piece) == 'blue': rml += """<fill color="blue"/>"""
                    if self._has_symbol_c(current_piece) == 'red': rml += """<fill color="red"/>"""
                    rml += """              <drawCentredString x="10.5" y="1.0">C</drawCentredString>"""
                
                
                if show_others_symbols:
                    # Zone 1 ##############################################
                    if current_piece_zone_one_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_one_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>3.0 21.5 21.0 21.5</lines>"""
                        rml += """          <lines>3.5 21.0 21.0 21.0</lines>"""
                        rml += """          <lines>4.5 20.0 20.0 20.0</lines>"""
                        rml += """          <lines>5.5 19.0 19.0 19.0</lines>"""
                        rml += """          <lines>6.5 18.0 18.0 18.0</lines>"""
                        rml += """          <lines>7.5 17.0 17.0 17.0</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_one_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>6.5 19.0 18.0 19.0</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="17">""" + (current_piece_zone_one_symbol if current_piece_zone_one_symbol else '') + """</drawString>"""
                    
                    # Zone 2 ##############################################
                    if current_piece_zone_two_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_two_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>1.5 3.5 1.5 20.0</lines>"""
                        rml += """          <lines>2.0 4.0 2.0 19.5</lines>"""
                        rml += """          <lines>3.0 5.0 3.0 18.5</lines>"""
                        rml += """          <lines>4.0 6.0 4.0 17.5</lines>"""
                        rml += """          <lines>5.0 7.0 5.0 16.5</lines>"""
                        rml += """          <lines>5.5 8.0 5.5 15.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_two_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>3.0 7.0 3.0 16.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="2" y="9">""" + (current_piece_zone_two_symbol if current_piece_zone_two_symbol else '' ) + """</drawString>"""
                    
                    # Zone 3 ##############################################
                    if current_piece_zone_three_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_three_symbol == 'K':
                        rml += """          <lineMode width="7.5" cap="square"/>"""
                        rml += """          <lines>11.0 11.7 13.5 11.7</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_three_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>11.0 11.7 13.5 11.7</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="9">""" + (current_piece_zone_three_symbol if current_piece_zone_three_symbol else '') + """</drawString>"""
                
                    # Zone 4 ##############################################
                    if current_piece_zone_four_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_four_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>22.0 3.0 22.0 20.0</lines>"""
                        rml += """          <lines>21.5 3.5 21.5 19.5</lines>"""
                        rml += """          <lines>20.5 4.5 20.5 18.5</lines>"""
                        rml += """          <lines>19.5 5.5 19.5 17.5</lines>"""
                        rml += """          <lines>18.5 6.5 18.5 16.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_four_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>20.5 6.5 20.5 16.5</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="18" y="9">""" + (current_piece_zone_four_symbol if current_piece_zone_four_symbol else '') + """</drawString>"""
                    
                    # Zone 5 ##############################################
                    if current_piece_zone_five_color  == 'red':
                        rml += """          <stroke color="red"/>"""
                        rml += """          <fill color="red"/>"""
                    else: 
                        rml += """          <stroke color="blue"/>"""
                        rml += """          <fill color="blue"/>"""
                    
                    # Symbol K...
                    if current_piece_zone_five_symbol == 'K':
                        rml += """          <lineMode width="2" cap="round"/>"""
                        rml += """          <lines>7.5 6.0 17.0 6.0</lines>"""
                        rml += """          <lines>6.5 5.0 18.0 5.0</lines>"""
                        rml += """          <lines>5.5 4.0 19.0 4.0</lines>"""
                        rml += """          <lines>4.5 3.0 20.0 3.0</lines>"""
                        rml += """          <lines>3.5 2.0 21.0 2.0</lines>"""
                        rml += """          <lines>3.0 1.5 21.0 1.5</lines>"""
                    
                    # Symbol O...
                    elif current_piece_zone_five_symbol == 'O':
                        rml += """          <lineMode width="4" cap="square"/>"""
                        rml += """          <lines>6.5 4.0 18.0 4.0</lines>"""
                    
                    # Another symbol...
                    else: rml += """        <drawString x="10" y="1">""" + (current_piece_zone_five_symbol if current_piece_zone_five_symbol else '') + """</drawString>"""
                
                rml += """              </illustration>
                                    </td>
                                    <td></td>"""
                
                if x >= 41: x = x - 1
                else: x = x + 1
            
            rml += """          </tr>
                                
                                <tr>"""
            
            rml += """
                                    <td></td>
                                    <td>
                                        <illustration width="489" height="10" borderStrokeWidth="1" borderStrokeColor="black">"""
            
            if self._has_symbol_w(dentist_test.piece48) and self._has_symbol_w(dentist_test.piece47):
                rml += """                  <lines>
                                                13.0 5.0 25.0 0.0
                                                25.0 0.0 37.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece47) and self._has_symbol_w(dentist_test.piece46):
                rml += """                  <lines>
                                                41.0 5.0 53.0 0.0
                                                53.0 0.0 65.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece46) and self._has_symbol_w(dentist_test.piece45):
                rml += """                  <lines>
                                                69.0 5.0 81.0 0.0
                                                81.0 0.0 93.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece45) and self._has_symbol_w(dentist_test.piece44):
                rml += """                  <lines>
                                                97.0 5.0 109.0 0.0
                                                109.0 0.0 121.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece44) and self._has_symbol_w(dentist_test.piece43):
                rml += """                  <lines>
                                                125.0 5.0 137.0 0.0
                                                137.0 0.0 149.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece43) and self._has_symbol_w(dentist_test.piece42):
                rml += """                  <lines>
                                                153.0 5.0 165.0 0.0
                                                165.0 0.0 177.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece42) and self._has_symbol_w(dentist_test.piece41):
                rml += """                  <lines>
                                                181.0 5.0 193.0 0.0
                                                193.0 0.0 205.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece41) and self._has_symbol_w(dentist_test.piece31):
                rml += """                  <lines>
                                                209.0 5.0 245.5 0.0
                                                245.5 0.0 278.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece31) and self._has_symbol_w(dentist_test.piece32):
                rml += """                  <lines>
                                                282.0 5.0 294.5 0.0
                                                294.5 0.0 306.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece32) and self._has_symbol_w(dentist_test.piece33):
                rml += """                  <lines>
                                                310.0 5.0 322.5 0.0
                                                322.5 0.0 334.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece33) and self._has_symbol_w(dentist_test.piece34):
                rml += """                  <lines>
                                                338.0 5.0 350.5 0.0
                                                350.5 0.0 362.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece34) and self._has_symbol_w(dentist_test.piece35):
                rml += """                  <lines>
                                                366.0 5.0 378.5 0.0
                                                378.5 0.0 390.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece35) and self._has_symbol_w(dentist_test.piece36):
                rml += """                  <lines>
                                                394.0 5.0 406.5 0.0
                                                406.5 0.0 418.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece36) and self._has_symbol_w(dentist_test.piece37):
                rml += """                  <lines>
                                                422.0 5.0 434.5 0.0
                                                434.5 0.0 446.0 5.0
                                            </lines>"""
            
            if self._has_symbol_w(dentist_test.piece37) and self._has_symbol_w(dentist_test.piece38):
                rml += """                  <lines>
                                                450.0 5.0 462.5 0.0
                                                462.5 0.0 474.0 5.0
                                            </lines>"""
            
            if self._has_symbol_c(dentist_test.piece48) and self._has_symbol_i(dentist_test.piece48):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="0.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece48) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece48) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="6.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="10.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece48) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece48) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="14.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece47) and self._has_symbol_i(dentist_test.piece47):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="28.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece47) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece47) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="34.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="38.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece47) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece47) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="42.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece46) and self._has_symbol_i(dentist_test.piece46):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="56.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece46) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece46) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="62.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="66.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece46) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece46) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="70.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece45) and self._has_symbol_i(dentist_test.piece45):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="84.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece45) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece45) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="90.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="94.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece45) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece45) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="98.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece44) and self._has_symbol_i(dentist_test.piece44):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="112.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece44) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece44) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="118.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="122.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece44) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece44) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="126.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece43) and self._has_symbol_i(dentist_test.piece43):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="140.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece43) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece43) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="146.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="150.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece43) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece43) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="154.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece42) and self._has_symbol_i(dentist_test.piece42):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="168.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece42) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece42) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="174.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="178.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece42) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece42) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="182.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece41) and self._has_symbol_i(dentist_test.piece41):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="196.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece41) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece41) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="202.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="206.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece41) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece41) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="210.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece31) and self._has_symbol_i(dentist_test.piece31):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="270.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece31) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece31) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="276.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="280.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece31) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece31) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="284.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece32) and self._has_symbol_i(dentist_test.piece32):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="298.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece32) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece32) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="304.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="308.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece32) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece32) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="312.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece33) and self._has_symbol_i(dentist_test.piece33):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="326.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece33) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece33) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="332.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="336.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece33) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece33) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="340.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece34) and self._has_symbol_i(dentist_test.piece34):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="354.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece34) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece34) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="360.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="364.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece34) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece34) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="368.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece35) and self._has_symbol_i(dentist_test.piece35):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="382.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece35) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece35) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="388.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="394.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece35) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece35) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="398.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece36) and self._has_symbol_i(dentist_test.piece36):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="410.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece36) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece36) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="416.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="420.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece36) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece36) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="424.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece37) and self._has_symbol_i(dentist_test.piece37):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="438.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece37) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece37) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="444.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="448.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece37) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece37) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="452.5" y="2.0">I</drawCentredString>"""
            
            if self._has_symbol_c(dentist_test.piece38) and self._has_symbol_i(dentist_test.piece38):
                rml += """
                                            <stroke color="black"/>
                                            <setFont name="Helvetica" size="6"/>
                                            <rect x="466.0" y="0.0" width="22" height="8" fill="no" stroke="yes"/>"""
                
                if self._has_symbol_c(dentist_test.piece38) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_c(dentist_test.piece38) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="472.5" y="2.0">C</drawCentredString>"""
                
                rml += """                  <fill color="black"/>"""
                rml += """                  <drawCentredString x="476.5" y="2.0">/</drawCentredString>"""
                
                if self._has_symbol_i(dentist_test.piece38) == 'blue':
                    rml += """              <fill color="blue"/>"""
                if self._has_symbol_i(dentist_test.piece38) == 'red':
                    rml += """              <fill color="red"/>"""
                
                rml += """                  <drawCentredString x="480.5" y="2.0">I</drawCentredString>"""
            
            rml += """                  </illustration>
                                    </td>
                                    
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td>
                                    
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td></td>
                                    <td><para style="P200_LEFT">SIMBOLOGIA DEL ODONTOGRAMA</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td></td>
                                    <td>
                                        <blockTable colWidths="45.0,20.0,2.0,50.0,20.0,2.0,60.0,20.0,2.0,60.0,20.0,2.0,60.0,28.0,2.0,55.0,20.0" rowHeights="12.0,12.0" style="Table9">
                                            <tr>
                                                <td><para style="P220">Caries</para></td>
                                                <td><para style="P220">O</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Restaurac.</para></td>
                                                <td><para style="P220">/</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Retos radic.</para></td>
                                                <td><para style="P220">F</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Corona</para></td>
                                                <td><para style="P220">C</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">""" + tools.ustr("Prótesis remov.") + """</para></td>
                                                <td><para style="P220">w</para></td>
                                                <td></td>
                                                <td><para style="P220">""" + tools.ustr("Prótesis total") + """</para></td>
                                                <td>
                                                    <blockTable colWidths="6.0" rowHeights="6.0" style="checkBox">
                                                        <tr><td><para style="P2222"></para></td></tr>
                                                    </blockTable>
                                                </td>
                                            </tr>
                                            
                                            <tr>
                                                <td><para style="P220">Sellante</para></td>
                                                <td><para style="P220">*</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">""" + tools.ustr("Estracción") + """</para></td>
                                                <td><para style="P220">X</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Ausente</para></td>
                                                <td><para style="P220">A</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Trat. endodon.</para></td>
                                                <td><para style="P220">I</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">""" + tools.ustr("Prótesis fija.") + """</para></td>
                                                <td><para style="P220">0-0</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">""" + tools.ustr("Calza") + """</para></td>
                                                <td><para style="P220">K</para></td>
                                            </tr>
                                        </blockTable>
                                    </td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td></td>
                                    <td><para style="P200_LEFT">""" + tools.ustr("Usar color ROJO para Patología actual AZUL para tratamientos odontológicos realizados") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="20.0,12.0,20.0,12.0,20.0,12.0,53.0,53.0,53.0,53.0,11.0,40.0,11.0,40.0,11.0,15.0,20.0,20.0,20.0,31.0" rowHeights="12.0,12.0,12.0,12.0,12.0,12.0,12.0,12.0,12.0,12.0" style="Table10">
                                <tr>
                                    <td><para style="P20">7.  INDICADORES DE SALUD BUCAL</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td>
                                    <td><para style="P220_CENTER">CARIES</para></td>
                                    <td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P220_CENTER">HIGIENE ORAL SIMPLIFICADA</para></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                    
                                    <td><para style="P2211_CENTER">PLACA</para></td>
                                    <td><para style="P2211_CENTER">CALCULO</para></td>
                                    <td><para style="P2211_CENTER">GINGIVITIS</para></td>
                                    
                                    <td><para style="P220_CENTER">ENF. PERIODONTAL</para></td>
                                    <td></td>
                                    
                                    <td><para style="P220_CENTER">MALOCLUSION</para></td>
                                    <td></td>
                                    
                                    <td><para style="P220_CENTER">FLUOROSIS</para></td>
                                    <td></td>
                                    
                                    <td><para style="PP20_CENTER">D</para></td>
                                    
                                    <td><para style="P220_CENTER">C</para></td>
                                    <td><para style="P220_CENTER">P</para></td>
                                    <td><para style="P220_CENTER">O</para></td>
                                    <td><para style="P220_CENTER">TOTAL</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P220_CENTER">PIEZAS</para></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                    
                                    <td><para style="P222_CENTER">0 - 1 - 2 - 3 - 9</para></td>
                                    <td><para style="P222_CENTER">0 - 1 - 2 - 3</para></td>
                                    <td><para style="P222_CENTER">0 - 1</para></td>
                                    
                                    <td><para style="P221_CENTER">LEVE</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.periodontale_illness == 'leve' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">ANGLE I</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.malocclusion == 'angle1' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">LEVE</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.fluorosis == 'leve' else "") + """</para></td>
                                    
                                    <td></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.carieDC) if dentist_test.carieDC else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.carieDP) if dentist_test.carieDP else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.carieDO) if dentist_test.carieDO else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.totalCarieD) if dentist_test.totalCarieD else "") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">16</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._16 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">17</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._17 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">55</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._55 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_1_placa) if dentist_test.section_1_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_1_calculo) if dentist_test.section_1_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_1_gingivitis) if dentist_test.section_1_gingivitis else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">MODERADA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.periodontale_illness == 'moderada' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">ANGLE II</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.malocclusion == 'angle2' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">MODERADA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.fluorosis == 'moderada' else "") + """</para></td>
                                    
                                    <td><para style="PP20_CENTER">d</para></td>
                                    
                                    <td><para style="P220_CENTER">c</para></td>
                                    <td><para style="P220_CENTER">e</para></td>
                                    <td><para style="P220_CENTER">o</para></td>
                                    <td><para style="P220_CENTER">TOTAL</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">11</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._11 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">21</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._21 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">51</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._51 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_2_placa) if dentist_test.section_2_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_2_calculo) if dentist_test.section_2_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_2_gingivitis) if dentist_test.section_2_gingivitis else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">SEVERA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.periodontale_illness == 'severa' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">ANGLE III</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.malocclusion == 'angle3' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">SEVERA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.fluorosis == 'severa' else "") + """</para></td>
                                    
                                    <td></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.carie_dc) if dentist_test.carie_dc else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.carie_de) if dentist_test.carie_de else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.carie_do) if dentist_test.carie_do else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.totalCarie_d) if dentist_test.totalCarie_d else "") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">26</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._26 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">27</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._27 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">65</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._65 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_3_placa) if dentist_test.section_3_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_3_calculo) if dentist_test.section_3_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_3_gingivitis) if dentist_test.section_3_gingivitis else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">36</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._36 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">37</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._37 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">75</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._75 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_4_placa) if dentist_test.section_4_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_4_calculo) if dentist_test.section_4_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_4_gingivitis) if dentist_test.section_4_gingivitis else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">31</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._31 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">41</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._41 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">71</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._71 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_5_placa) if dentist_test.section_5_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_5_calculo) if dentist_test.section_5_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_5_gingivitis) if dentist_test.section_5_gingivitis else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">46</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._46 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">47</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._47 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">85</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test._85 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_6_placa) if dentist_test.section_6_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_6_calculo) if dentist_test.section_6_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(dentist_test.section_6_gingivitis) if dentist_test.section_6_gingivitis else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P220_CENTER_BOLD">TOTALES</para></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                    
                                    <td><para style="P220_CENTER_BOLD">""" + str(dentist_test.totalPlate) + """</para></td>
                                    <td><para style="P220_CENTER_BOLD">""" + str(dentist_test.totalStone) + """</para></td>
                                    <td><para style="P220_CENTER_BOLD">""" + str(dentist_test.totalGengivitis) + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      </section>"""
            rml += """      <pageBreak></pageBreak>"""
            
            other_observation = ''
            if dentist_test.other_observation:
                word_list = self._get_list_words(dentist_test.other_observation, letters_per_row * 2)
                other_observation = word_list[0] if len(word_list) >= 1 else ''
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="40.0,11.0,60.0,11.0,35.0,11.0,30.0,11.0,319.0" rowHeights="12.0,12.0,24.0" style="Table13">
                                <tr>
                                    <td><para style="P20">""" + tools.ustr("9.  PLAN DIAGNOSTICO") + """</para></td>
                                    <td></td><td></td>
                                    <td></td><td></td><td></td>
                                    <td></td><td></td>
                                    <td><para style="P14_RIGHT">""" + tools.ustr("DESCRIBIR ABAJO ANOTANDO EL NUMERO, SI APLICA") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P14_LEFT">""" + tools.ustr("1. BIOMETRIA") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.biometric else "") + """</para></td>
                                    
                                    <td><para style="P14_LEFT">""" + tools.ustr("2. QUIMICA SANGUINEA") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.blood_chemistry else "") + """</para></td>
                                    
                                    <td><para style="P14_LEFT">""" + tools.ustr("3. RAYOS-X") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.x_rays else "") + """</para></td>
                                    
                                    <td><para style="P14_LEFT">""" + tools.ustr("4. OTRO") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.other else "") + """</para></td>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P20_COURIER">""" + tools.ustr(other_observation) + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            diag_cant = 0
            diagnostics_list = []
            if dentist_test.diagnosis_ids:
                for diag in dentist_test.diagnosis_ids:
                    diagnostics_list.append((diag.name if diag.name else '', diag.code if diag.code else '', "X" if diag.presuntive else "", "X" if diag.definitive else "", "X" if diag.foment else ""))
                    diag_cant = diag_cant + 1
            
            while diag_cant < 4:
                diagnostics_list.append(('', '', '', '', ''))
                diag_cant = diag_cant + 1
            
            word_list = []
            if dentist_test.mdc_info:
                word_list = self._get_list_words(dentist_test.diagnosis_observation, 68)
            
            d = {
                1: word_list[0] if len(word_list) >= 1 else '',
                2: word_list[1] if len(word_list) >= 2 else '',
                3: word_list[2] if len(word_list) >= 3 else '',
                4: word_list[3] if len(word_list) >= 4 else '',
                5: word_list[4] if len(word_list) >= 5 else '',
            }
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="20.0,150.0,30.0,25.0,25.0,25.0,254.0" rowHeights="12.0,15.0,12.0,12.0,12.0,12.0" style="Table14">
                                <tr>
                                    <td><para style="P20">""" + tools.ustr("10.  DIAGNOSTICOS") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                    <td><para style="P14_RIGHT">""" + tools.ustr("DESCRIBIR ABAJO") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td></td>
                                    <td><para style="P221_CENTER">CIE= CLASIFICACION INTERNACIONAL DE ENFERMEDADES PRE= PRESUNTIVO DEF= DEFINITIVO FOM= FOMENTO</para></td>
                                    <td><para style="P22">CIE</para></td>
                                    <td><para style="P22">PRE</para></td>
                                    <td><para style="P22">DEF</para></td>
                                    <td><para style="P22">FOM</para></td>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">1</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[0][0][0:38]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[0][1][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[0][2]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[0][3]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[0][4]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(d[1]) + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">2</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[1][0][0:38]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[1][1][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[1][2]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[1][3]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[1][4]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(d[2]) + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">3</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[2][0][0:38]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[2][1][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[2][2]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[2][3]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[2][4]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(d[3]) + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">4</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[3][0][0:38]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[3][1][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[3][2]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[3][3]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(diagnostics_list[3][4]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(d[4]) + """</para></td>
                                </tr>
                            </blockTable>"""
            
            cant = 0
            lista_tratamientos = []
            if dentist_test.treatment_ids:
                for tr in dentist_test.treatment_ids:
                    lista_tratamientos.append((tr.name if tr.name else '', tr.concentration if tr.concentration else '', tr.presentation if tr.presentation else '', tr.via if tr.via else '', tr.dosis if tr.dosis else '', tr.frequency if tr.frequency else '', tr.days if tr.days else ''))
                    cant = cant + 1
            
            while cant < 4:
                lista_tratamientos.append(('', '', '', '', '', '', ''))
                cant = cant + 1
            
            word_list = []
            if dentist_test.mdc_info:
                word_list = self._get_list_words(dentist_test.treatment_observation, 68)
            
            d = {
                1: word_list[0] if len(word_list) >= 1 else '',
                2: word_list[1] if len(word_list) >= 2 else '',
                3: word_list[2] if len(word_list) >= 3 else '',
            }
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="19.0,80.0,33.0,33.0,23.0,28.0,31.0,24.0,38.0,10.0,35.0,10.0,40.0,10.0,40.0,10.0,45.0,20.0" rowHeights="12.0,15.0,12.0,12.0,12.0,12.0" style="Table15">
                                <tr>
                                    <td><para style="P20">""" + tools.ustr("11.  PLAN DE TRATAMIENTO") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td><para style="P14_RIGHT">""" + tools.ustr("DESCRIBIR ABAJO LA CAUSA Y DETALLES DE LA ACTIVIDAD SENALADA") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">""" + tools.ustr("N°") + """</para></td>
                                    <td><para style="P55P">""" + tools.ustr("MEDICAMENTO GENÉRICO") + """</para></td>
                                    <td><para style="P55P">""" + tools.ustr("CONCENTRACION") + """</para></td>
                                    <td><para style="P55P">""" + tools.ustr("PRESENTACION") + """</para></td>
                                    
                                    <td><para style="P55P">VIA</para></td>
                                    <td><para style="P55P">DOSIS</para></td>
                                    <td><para style="P55P">FRECUENCIA</para></td>
                                    
                                    <td><para style="P55P">""" + tools.ustr("DIAS") + """</para></td>
                                    <td><para style="P55P">""" + tools.ustr("INTER CONSULTA") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.interconsult else "") + """</para></td>
                                    
                                    <td><para style="P55P">PROCEDIMIENTO</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.procedure else "") + """</para></td>
                                    
                                    <td><para style="P55P">INTERNACION</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.internation else "") + """</para></td>
                                    
                                    <td><para style="P55P">CONSULTA EXTERNA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.extern_consult else "") + """</para></td>
                                    
                                    <td><para style="P55P">DIAS DE INCAPACIDAD</para></td>
                                    <td><para style="P14_LEFT">""" + (str(dentist_test.incapacity_days) if dentist_test.incapacity_days else "") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">1</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[0][0][0:18]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[0][1][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[0][2][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[0][3][0:3]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[0][4][0:4]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[0][5][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[0][6][0:3]) + """</para></td>
                                    
                                    <td><para style="P55P">TOPICACION FLUOR</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.fluor_topification else "") + """</para></td>
                                    
                                    <td><para style="P55P">SELLANTES</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.sealment else "") + """</para></td>
                                    
                                    <td><para style="P55P">REFERENCIA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if dentist_test.reference else "") + """</para></td>
                                    
                                    <td><para style="P55P">SERVICIO</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + (dentist_test.service[0:14] if dentist_test.service else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">2</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[1][0][0:18]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[1][1][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[1][2][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[1][3][0:3]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[1][4][0:4]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[1][5][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[1][6][0:3]) + """</para></td>
                                    
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(d[1]) + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">3</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[2][0][0:18]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[2][1][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[2][2][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[2][3][0:3]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[2][4][0:4]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[2][5][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[2][6][0:3]) + """</para></td>
                                    
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(d[2]) + """</para></td>
                                    <td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P55P">4</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[3][0][0:18]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[3][1][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[3][2][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[3][3][0:3]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[3][4][0:4]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[3][5][0:5]) + """</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(lista_tratamientos[3][6][0:3]) + """</para></td>
                                    
                                    <td><para style="P144_LEFT_COURIER">""" + tools.ustr(d[3]) + """</para></td>
                                    <td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="49.0,70.0,30.0,30.0,80.0,120.0,50.0,50.0,50.0" rowHeights="10.0,12.0" style="Table16">
                                <tr>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td><para style="P220_CENTER_BOLD">CODIGO</para></td>
                                    <td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P220_CENTER">FECHA PROX. SESION</para></td>
                                    <td><para style="P220_CENTER">""" + (dentist_test.next_appointment_date if dentist_test.next_appointment_date else '') + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td><para style="P220">ODONTOLOGO</para></td>
                                    <td><para style="P220_CENTER">""" + (tools.ustr(dentist_test.doctor.physician_id.name) if dentist_test.doctor and dentist_test.doctor.physician_id and dentist_test.doctor.physician_id.name else '') + """</para></td>
                                    <td><para style="P220_CENTER">""" + (dentist_test.doctor.doctor_id if dentist_test.doctor and dentist_test.doctor.doctor_id else '') + """</para></td>
                                    
                                    <td><para style="P220">FIRMA</para></td>
                                    <td></td>
                                </tr>
                            </blockTable>"""
            
            max_rows_table12 = 36
            rowHeights = '12.0'
            
            for x in xrange(max_rows_table12):
                rowHeights += ',12.0'
            
            rml += """
                            <spacer length="0.2cm"/>
                            <blockTable colWidths="170.0,359.0" rowHeights=" """ + rowHeights + """ " style="Table3">
                                <tr>
                                    <td><para style="P20">12. NOTAS DE EVOLUCION</para></td>
                                    <td><para style="P14_RIGHT">""" + tools.ustr("ANOTAR: NUMERO DE SESION, FECHA, ANAMNESIS, EXAMEN DENTAL, RESULTADO DE EXAMENES, ANALISIS, DIAGNOSTICO, PLAN DE TRATAMIENTO, FIRMAS") + """</para></td>
                                </tr>"""
            
            cant = 0
            if dentist_test.evolution_ids:
                for evo in dentist_test.evolution_ids:
                    texto = (evo.evolution_date if evo.evolution_date else "")
                    texto += (", " + evo.name if evo.name else "")
                    texto += ", " + evo.observation if evo.observation else ""
                                        
                    word_list = self._get_list_words(texto, letters_per_row)
                    for part_text in word_list:
                        if cant < max_rows_table12:
                            cant = cant + 1
                            rml += """
                                    <tr><td><para style="P20_COURIER">""" + tools.ustr(part_text) + """</para></td><td></td></tr>"""
            
            while cant < max_rows_table12:
                cant = cant + 1
                rml += """      <tr><td><para style="P20_COURIER"></para></td><td></td></tr>"""
                
            rml += """      </blockTable>"""
            
            rml += """ </story>
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
    
    def _get_current_piece(self, object, number):
        field = 'piece' + str(number)
        return getattr(object, field, False)
    
    def _get_zone_symbol(self, piece, zone='zone_one'):
        field = zone + '_symbol'
        return getattr(piece, field, False)
    
    def _get_zone_color(self, piece, zone='zone_one'):
        field = zone + '_color'
        return getattr(piece, field, False)
    
    def _has_symbol_w(self, piece):
        if piece:
            if piece.zone_one_symbol == 'w' or piece.zone_two_symbol == 'w' or piece.zone_three_symbol == 'w' or piece.zone_four_symbol == 'w' or piece.zone_five_symbol == 'w': return True
        return False
    
    def _has_symbol_x(self, piece):
        if piece:
            if piece.zone_one_symbol == 'X': return piece.zone_one_color
            if piece.zone_two_symbol == 'X': return piece.zone_two_color
            if piece.zone_three_symbol == 'X': return piece.zone_three_color
            if piece.zone_four_symbol == 'X': return piece.zone_four_color
            if piece.zone_five_symbol == 'X': return piece.zone_five_color
        return False
    
    def _has_symbol_0_0(self, piece):
        if piece:
            if piece.zone_one_symbol == '0-0' or piece.zone_two_symbol == '0-0' or piece.zone_three_symbol == '0-0' or piece.zone_four_symbol == '0-0' or piece.zone_five_symbol == '0-0': return True
        return False
    
    def _has_symbol_i(self, piece):
        if piece:
            if piece.zone_one_symbol == 'I': return piece.zone_one_color
            if piece.zone_two_symbol == 'I': return piece.zone_two_color
            if piece.zone_three_symbol == 'I': return piece.zone_three_color
            if piece.zone_four_symbol == 'I': return piece.zone_four_color
            if piece.zone_five_symbol == 'I': return piece.zone_five_color
        return False
    
    def _has_symbol_c(self, piece):
        if piece:
            if piece.zone_one_symbol == 'C': return piece.zone_one_color
            if piece.zone_two_symbol == 'C': return piece.zone_two_color
            if piece.zone_three_symbol == 'C': return piece.zone_three_color
            if piece.zone_four_symbol == 'C': return piece.zone_four_color
            if piece.zone_five_symbol == 'C': return piece.zone_five_color
        return False
oemedical_dentist_test_report('report.oemedical_dentist_test_report', 'oemedical.dentist.test', '', '')