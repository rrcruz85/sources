# -*- encoding: utf-8 -*-
import os
import openerp
import random
import string
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import pooler, tools
from openerp.report.interface import report_rml
from PIL import Image
from openerp.tools.translate import _

def randomString(stringLength=10):
  """Generate a random string of fixed length """
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(stringLength))

class odontogram(report_rml):
    
    def create(self, cr, uid, ids, datas, context):
        odontology_exam_obj = pooler.get_pool(cr.dbname).get('oemedical.odontology.exam')
        company_obj = pooler.get_pool(cr.dbname).get('res.company')
        
        company_ids_list = company_obj.search(cr, uid, [], context=context)
        company = company_obj.browse(cr, uid, company_ids_list[0], context) if len(company_ids_list) > 0 else False
        
        for odontology_exam in odontology_exam_obj.browse(cr, uid, ids, context):
            first_name = tools.ustr(odontology_exam.appointment_id.patient_id.first_name.split(" ")[0])
            second_name = tools.ustr(odontology_exam.appointment_id.patient_id.first_name.split(" ")[1]) if len(odontology_exam.appointment_id.patient_id.first_name.split(" ")) > 1 else ""
            
            rml = """<document filename="OdontogramReport.pdf">
                        <template pageSize="(595.0,842.0)" title="Odontogram Report" author="EasysDev" allowSplitting="20">
                            <pageTemplate id="page1">
                                <pageGraphics>
                                <place x="57.5" y="765.0" width="459.0" height="77.0">
                                    <blockTable colWidths="415.0,8.0,5.0,4.0,18.0,9.0" rowHeights="30.0,20.0,2.0,15.0,10.0" style="Table1">
                                      <tr>
                                        <td>
                                          <para style="P1">
                                            <font color="white"></font>
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
                                            <font face="Helvetica-Bold"></font>
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
                              <blockSpan start="0,1" stop="32,1"/>
                              <blockSpan start="0,2" stop="32,2"/>
                              <blockSpan start="0,3" stop="32,3"/>
                              <blockSpan start="0,4" stop="32,4"/>
                              <blockSpan start="0,5" stop="32,5"/>
                              
                              <blockBackground colorName="#F0A9C4" start="0,0" stop="32,0"/> 
                              
                              <!--                              
                              <blockBackground colorName="#CAE7D4" start="0,2" stop="32,2"/>
                              -->

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
                                <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.4"/>
                                <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,0" thickness="0.4"/>
                                <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="0,0" thickness="0.4"/>
                                <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="0,0" thickness="0.4"/>
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
                            <paraStyle name="P200_2" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="CENTER"/>
                            <paraStyle name="P200_LEFT" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="LEFT"/>
                            
                            <paraStyle name="P220" fontName="Helvetica" fontSize="6.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P220_BOLD" fontName="Helvetica-Bold" fontSize="6.0" leading="8" alignment="LEFT"/>
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
           
            rml += """<story>    
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
                                        <font color="black">""" + (tools.ustr(odontology_exam.appointment_id.patient_id.first_name) if odontology_exam.appointment_id.patient_id.first_name else "")[0:22]  + """</font>
                                      </para>
                                    </td>
                                    
                                    <td>
                                      <para style="P20_COURIER_CENTER">
                                        <font color="black">""" + ((tools.ustr(odontology_exam.appointment_id.patient_id.last_name) if odontology_exam.appointment_id.patient_id.last_name else "") + " " + (tools.ustr(odontology_exam.appointment_id.patient_id.slastname) if odontology_exam.appointment_id.patient_id.slastname else ""))[0:22] + """</font>
                                      </para>
                                    </td>
                                    
                                    <td>
                                      <para style="P20_COURIER_CENTER">
                                        <font color="black">""" + ("X" if odontology_exam.appointment_id.patient_id.sex and odontology_exam.appointment_id.patient_id.sex == "m" else "") + """</font>
                                      </para>
                                    </td>
                                    
                                    <td>
                                      <para style="P20_COURIER_CENTER">
                                        <font color="black">""" + ("X" if odontology_exam.appointment_id.patient_id.sex and odontology_exam.appointment_id.patient_id.sex == "f" else "") + """</font>
                                      </para>
                                    </td>
                                    
                                    <td>
                                      <para style="P20_COURIER_CENTER"><font color="black">1</font></para>
                                    </td>
                                    
                                    <td>
                                      <para style="P20_COURIER_CENTER">
                                        <font color="black">""" + (tools.ustr(odontology_exam.appointment_id.patient_id.identification_code) if odontology_exam.appointment_id.patient_id.identification_code else "") + """</font>
                                      </para>
                                    </td>
                                  </tr>
                                </blockTable>"""
               
            years = self._get_year(odontology_exam.appointment_id.patient_id)
            a = True if odontology_exam.appointment_id.is_planned and years == 0 else False
            b = True if years >= 1 and years <= 4 else False
            c = True if odontology_exam.appointment_id.is_planned and years >= 5 and years <= 9 else False
            d = True if years >= 5 and years <= 14 and not odontology_exam.appointment_id.is_planned else False
            e = True if years >= 10 and years <= 14 and odontology_exam.appointment_id.is_planned else False
            f = True if years >= 15 and years <= 19 else False
            g = True if years >= 20 else False
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="52.0,10.0,52.0,10.0,72.0,10.0,52.0,10.0,50.0,10.0,55.0,10.0,62.0,10.0,52.0,10.0" rowHeights="15.0" style="Table0">
                                <tr>
                                    <td><para style="P14_LEFT">""" + tools.ustr("MENOR DE 1 AÑO") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if a else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("1-4 AÑOS") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if b else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("5-9 AÑOS PROGRAMADO") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if c else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("5-14 AÑOS NO PROGRAMADO") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if d else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("10-14 AÑOS PROGRAMADO") + """</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if e else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("15-19 AÑOS") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if f else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("MAYOR DE 20 AÑOS") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if g else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("EMBARAZADA") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.is_pregnant else "") + """</para></td>
                                </tr>
                            </blockTable>"""
            
            letters_per_row = 123            
            
            rowHeights = '12.0'
            if odontology_exam.appointment_id.motive:
                strMDC = odontology_exam.appointment_id.motive.replace('\n',' ')
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
                                
                                <tr><td><para style="P20_COURIER">""" + (tools.ustr(odontology_exam.appointment_id.motive) if odontology_exam.appointment_id.motive else "") + """</para></td><td></td></tr>
                            </blockTable>"""
           
            info_diagnosis = ""
            if odontology_exam.appointment_id.info_diagnosis:
                word_list = self._get_list_words(odontology_exam.appointment_id.info_diagnosis, letters_per_row * 4)
                info_diagnosis = word_list[0] if len(word_list) >= 1 else ''
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="170.0,357.0" rowHeights="12.0,36.0" style="Table3">
                                <tr>
                                    <td><para style="P20">2.  ENFERMEDAD O PROBLEMA ACTUAL</para></td>
                                    <td><para style="P14_RIGHT">""" + tools.ustr("SINTOMAS: CRONOLOGIA, LOCALIZACIÓN, CARACTERÍSTICAS, INTENSIDAD, CAUSA APARENTE, SÍNTOMAS ASOCIADOS, EVOLUCIÓN, ESTADO ACTUAL.") + """</para></td>
                                </tr>
                                <tr><td><para style="P20_COURIER">""" + tools.ustr(info_diagnosis) + """</para></td><td></td></tr>
                            </blockTable>"""
            
            others_antecedents = ""
            if odontology_exam.appointment_id.others_antecedents and odontology_exam.appointment_id.other:
                word_list = self._get_list_words(odontology_exam.appointment_id.others_antecedents, letters_per_row * 2)
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
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.antibotic_allergic else "") + """</para></td>
                                    <td><para style="P14_LEFT">2. ALERGIA ANESTESIA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.anesthesia_allergic else "") + """</para></td>
                                    <td><para style="P14_LEFT">3. HEMORRAGIAS</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.hemorrhage else "") + """</para></td>
                                    <td><para style="P14_LEFT">4. VIH/SIDA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.vih_sida else "") + """</para></td>
                                    <td><para style="P14_LEFT">5. TUBERCULOSIS</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.tuberculosis else "") + """</para></td>
                                    <td><para style="P14_LEFT">6. ASMA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.asma else "") + """</para></td>
                                    <td><para style="P14_LEFT">7. DIABETES</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.diabetes else "") + """</para></td>
                                    <td><para style="P14_LEFT">8. HIPERTENSION</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.hipertension else "") + """</para></td>
                                    <td><para style="P14_LEFT">9. ENF. CARDIACA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.enf_car else "") + """</para></td>
                                    <td><para style="P14_LEFT">10. OTRO</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.appointment_id.patient_id.other else "") + """</para></td>
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
                                    <td><para style="P144_CENTER">""" + (odontology_exam.appointment_id.pat_info if odontology_exam.appointment_id.pat_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("FRECUENCIA CARDIACA min") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(odontology_exam.appointment_id.ppm_info) if odontology_exam.appointment_id.ppm_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("FRECUENCIA RESPIRAT. min") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(odontology_exam.appointment_id.ppr_info) if odontology_exam.appointment_id.ppr_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("TEMPERATURA BUCAL °C") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(odontology_exam.appointment_id.tem_info) if odontology_exam.appointment_id.tem_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("TEMPERATURA AXILAR °C") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(odontology_exam.appointment_id.tem2_info) if odontology_exam.appointment_id.tem2_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("PESO Kg") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(odontology_exam.appointment_id.pes_info) if odontology_exam.appointment_id.pes_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("TALLA m") + """</para></td>
                                    <td><para style="P144_CENTER">""" + (str(odontology_exam.appointment_id.size_info) if odontology_exam.appointment_id.size_info else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("NO APLICA") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.not_apply else "") + """</para></td>
                                </tr>
                            </blockTable>"""
            
            stomatognathic_system_observation = ""
            if odontology_exam.stomatognathic_system_observation:
                word_list = self._get_list_words(odontology_exam.stomatognathic_system_observation, letters_per_row * 4 - 17)
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
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.libs else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("2. MEJILLAS") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.cheeks else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("3. MAXILAR SUPERIOR") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.top_max else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("4. MAXILAR INFERIOR") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.bottom_max else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("5. LENGUA") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.tongle else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("6. PALADAR") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.taste else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("7. PISO") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.floor else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("8. CARRILLOS") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.jowls else "") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P14_LEFT">""" + tools.ustr("9. GLANDULAS SALIVALES") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.sal_glands else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("10. ORO FARINGE") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.pharynx else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("11. ATM") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.atm else "") + """</para></td>
                                    <td><para style="P14_LEFT">""" + tools.ustr("12. GANGLIOS") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.lymph else "") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                <tr>
                                    <td><para style="P20_COURIER">""" + tools.ustr(stomatognathic_system_observation) + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            png_odontogram_img = ""            
            path = openerp.modules.get_module_path('oemedical_odontology_exam')            
            path += '/static/src/img/tmp'
            path = os.path.normpath(path)
            _png_odontogram_img = os.path.join(path, 'empty.png')

            if odontology_exam.odontogram_img:              
              png_odontogram_img = os.path.join(path, randomString() + '.png')
              _png_odontogram_img = os.path.join(path, randomString() + '.png')

              with open(png_odontogram_img, "wb") as fh:
                fh.write(odontology_exam.odontogram_img.decode('base64'))

              fill_color = 'white'
              image = Image.open(png_odontogram_img)
              if image.mode in ('RGBA', 'LA'):
                background = Image.new(image.mode[:-1], image.size, fill_color)
                background.paste(image, image.split()[-1])
                image = background
              image.save(_png_odontogram_img, 'png', quality = 98)
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="19.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,51.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,5.0,23.0,19.0" rowHeights="12.0, 180.0, 12.0, 12.0, 24.0, 12.0" style="Table7">
                                <tr>
                                    <td><para style="P20">""" + tools.ustr("6.  ODONTOGRAMA") + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><image file='""" + _png_odontogram_img + """' x="3" y="1" width="500" height="178" preserveAspectRatio="no"/> 
                                    </td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                               
                                <tr>
                                    <td><para style="P200">SIMBOLOGIA DEL ODONTOGRAMA</para></td>
                                    <td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>

                                <tr>
                                    <td></td>
                                    <td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>

                                <tr>
                                    <td>
                                         <blockTable colWidths="45.0,20.0,2.0,50.0,20.0,2.0,60.0,20.0,2.0,60.0,20.0,2.0,60.0,28.0,2.0,55.0,20.0" rowHeights="12.0,12.0" style="Table9">
                                            <tr>
                                                <td><para style="P220">Caries</para></td>
                                                <td><para style="P220_BOLD">O</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Restaurac.</para></td>
                                                <td><para style="P220_BOLD">/</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Retos radic.</para></td>
                                                <td><para style="P220_BOLD">F</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Corona</para></td>
                                                <td><para style="P220_BOLD">C</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">""" + tools.ustr("Prótesis remov.") + """</para></td>
                                                <td><para style="P220_BOLD">W</para></td>
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
                                                <td><para style="P220_BOLD">*</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">""" + tools.ustr("Extracción") + """</para></td>
                                                <td><para style="P220_BOLD">X</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Ausente</para></td>
                                                <td><para style="P220_BOLD">A</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">Trat. endodon.</para></td>
                                                <td><para style="P220_BOLD">I</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">""" + tools.ustr("Prótesis fija") + """</para></td>
                                                <td><para style="P220_BOLD">0-0</para></td>
                                                <td><para style="P220"></para></td>
                                                <td><para style="P220">""" + tools.ustr("Calza") + """</para></td>
                                                <td><para style="P220_BOLD">K</para></td>
                                            </tr>
                                        </blockTable>
                                    </td>
                                    <td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>

                                <tr>
                                    <td><para style="P200">""" + tools.ustr("Usar color ROJO para Patología actual, AZUL para tratamientos odontológicos realizados") + """</para></td>
                                    <td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td>
                                </tr>
                                
                              </blockTable>
                            """
             
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
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.periodontale_illness == 'leve' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">ANGLE I</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.malocclusion == 'angle1' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">LEVE</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.fluorosis == 'leve' else "") + """</para></td>
                                    
                                    <td></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.carieDC) if odontology_exam.carieDC else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.carieDP) if odontology_exam.carieDP else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.carieDO) if odontology_exam.carieDO else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.totalCarieD) if odontology_exam.totalCarieD else "") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">16</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._16 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">17</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._17 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">55</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._55 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_1_placa) if odontology_exam.section_1_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_1_calculo) if odontology_exam.section_1_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_1_gingivitis) if odontology_exam.section_1_gingivitis else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">MODERADA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.periodontale_illness == 'moderada' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">ANGLE II</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.malocclusion == 'angle2' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">MODERADA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.fluorosis == 'moderada' else "") + """</para></td>
                                    
                                    <td><para style="PP20_CENTER">d</para></td>
                                    
                                    <td><para style="P220_CENTER">c</para></td>
                                    <td><para style="P220_CENTER">e</para></td>
                                    <td><para style="P220_CENTER">o</para></td>
                                    <td><para style="P220_CENTER">TOTAL</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">11</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._11 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">21</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._21 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">51</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._51 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_2_placa) if odontology_exam.section_2_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_2_calculo) if odontology_exam.section_2_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_2_gingivitis) if odontology_exam.section_2_gingivitis else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">SEVERA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.periodontale_illness == 'severa' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">ANGLE III</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.malocclusion == 'angle3' else "") + """</para></td>
                                    
                                    <td><para style="P221_CENTER">SEVERA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.fluorosis == 'severa' else "") + """</para></td>
                                    
                                    <td></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.carie_dc) if odontology_exam.carie_dc else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.carie_de) if odontology_exam.carie_de else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.carie_do) if odontology_exam.carie_do else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.totalCarie_d) if odontology_exam.totalCarie_d else "") + """</para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">26</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._26 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">27</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._27 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">65</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._65 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_3_placa) if odontology_exam.section_3_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_3_calculo) if odontology_exam.section_3_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_3_gingivitis) if odontology_exam.section_3_gingivitis else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">36</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._36 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">37</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._37 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">75</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._75 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_4_placa) if odontology_exam.section_4_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_4_calculo) if odontology_exam.section_4_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_4_gingivitis) if odontology_exam.section_4_gingivitis else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">31</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._31 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">41</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._41 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">71</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._71 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_5_placa) if odontology_exam.section_5_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_5_calculo) if odontology_exam.section_5_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_5_gingivitis) if odontology_exam.section_5_gingivitis else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P222_CENTER">46</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._46 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">47</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._47 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">85</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam._85 else "") + """</para></td>
                                    
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_6_placa) if odontology_exam.section_6_placa else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_6_calculo) if odontology_exam.section_6_calculo else "") + """</para></td>
                                    <td><para style="P222_CENTER">""" + (str(odontology_exam.section_6_gingivitis) if odontology_exam.section_6_gingivitis else "") + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P220_CENTER_BOLD">TOTALES</para></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                    
                                    <td><para style="P220_CENTER_BOLD">""" + str(odontology_exam.totalPlate) + """</para></td>
                                    <td><para style="P220_CENTER_BOLD">""" + str(odontology_exam.totalStone) + """</para></td>
                                    <td><para style="P220_CENTER_BOLD">""" + str(odontology_exam.totalGengivitis) + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      </section>"""
            rml += """      <pageBreak></pageBreak>"""            
           
            other_observation = ""
            if odontology_exam.other_observation:
                word_list = self._get_list_words(odontology_exam.other_observation, letters_per_row * 2)
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
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.biometric else "") + """</para></td>
                                    
                                    <td><para style="P14_LEFT">""" + tools.ustr("2. QUIMICA SANGUINEA") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.blood_chemistry else "") + """</para></td>
                                    
                                    <td><para style="P14_LEFT">""" + tools.ustr("3. RAYOS-X") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.x_rays else "") + """</para></td>
                                    
                                    <td><para style="P14_LEFT">""" + tools.ustr("4. OTRO") + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ("X" if odontology_exam.other else "") + """</para></td>
                                    <td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P20_COURIER">""" + tools.ustr(other_observation or '') + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                            </blockTable>"""
            
            diag_cant = 0
            diagnostics_list = []
            if odontology_exam.diagnosis_ids:
                for diag in odontology_exam.diagnosis_ids:
                    diagnostics_list.append((diag.name if diag.name else '', diag.code if diag.code else '', "X" if diag.presuntive else "", "X" if diag.definitive else "", "X" if diag.foment else ""))
                    diag_cant = diag_cant + 1
            
            while diag_cant < 4:
                diagnostics_list.append(('', '', '', '', ''))
                diag_cant = diag_cant + 1
            
            word_list = []
            if odontology_exam.diagnosis_observation:
                word_list = self._get_list_words(odontology_exam.diagnosis_observation, 68)
            
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
            if odontology_exam.appointment_id.treatment_ids:
                for tr in odontology_exam.appointment_id.treatment_ids:
                  concentration = ''
                  presentation = ''
                  via = ''
                  dosis = ''
                  frequency = ''
                  days = ''
                  if tr.medicament_ids:
                    concentration = tr.medicament_ids[0].medicament_id.concentracion
                    presentation = tr.medicament_ids[0].medicament_id.presentation
                    via = tr.medicament_ids[0].via
                    dosis = tr.medicament_ids[0].dosis
                    frequency = tr.medicament_ids[0].frequency
                    days = tr.medicament_ids[0].days
                  lista_tratamientos.append((tr.treatment_id.name, concentration, presentation,via,dosis,frequency,days))
                  cant = cant + 1
            
            while cant < 4:
                lista_tratamientos.append(('', '', '', '', '', '', ''))
                cant = cant + 1
            
            word_list = []
            if odontology_exam.appointment_id.treatment_ids and odontology_exam.appointment_id.treatment_ids[0].observations:
                word_list = self._get_list_words(odontology_exam.appointment_id.treatment_ids[0].observations, 68)
            
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
                                    <td><para style="P14_CENTER">""" + ("X" if odontology_exam.interconsult else "") + """</para></td>
                                    
                                    <td><para style="P55P">PROCEDIMIENTO</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if odontology_exam.procedure else "") + """</para></td>
                                    
                                    <td><para style="P55P">INTERNACION</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if odontology_exam.internation else "") + """</para></td>
                                    
                                    <td><para style="P55P">CONSULTA EXTERNA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if odontology_exam.extern_consult else "") + """</para></td>
                                    
                                    <td><para style="P55P">DIAS DE INCAPACIDAD</para></td>
                                    <td><para style="P14_LEFT">""" + (str(odontology_exam.incapacity_days) if odontology_exam.incapacity_days else "") + """</para></td>
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
                                    <td><para style="P14_CENTER">""" + ("X" if odontology_exam.fluor_topification else "") + """</para></td>
                                    
                                    <td><para style="P55P">SELLANTES</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if odontology_exam.sealment else "") + """</para></td>
                                    
                                    <td><para style="P55P">REFERENCIA</para></td>
                                    <td><para style="P14_CENTER">""" + ("X" if odontology_exam.reference else "") + """</para></td>
                                    
                                    <td><para style="P55P">SERVICIO</para></td>
                                    <td><para style="P144_LEFT_COURIER">""" + (odontology_exam.service[0:14] if odontology_exam.service else "") + """</para></td>
                                    
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
            
            app_date = odontology_exam.appointment_id.next_appointment_date if odontology_exam.appointment_id.next_appointment_date else ''
            hour = 0
            minute = 0
            if odontology_exam.appointment_id.next_appointment_hour:
              hour = int(odontology_exam.appointment_id.next_appointment_hour)
              minute = int(round(odontology_exam.appointment_id.next_appointment_hour - hour, 2) * 60)
              app_date += str(hour) + ':' + str(minute)

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
                                    <td><para style="P220_CENTER">""" + (app_date or '') + """</para></td>
                                    
                                    <td></td><td></td>
                                    <td><para style="P220">ODONTOLOGO</para></td>
                                    <td><para style="P220_CENTER">""" + (tools.ustr(odontology_exam.appointment_id.doctor_id.physician_id.first_name)) + """</para></td>
                                    <td><para style="P220_CENTER">""" + (odontology_exam.appointment_id.doctor_id.doctor_id if odontology_exam.appointment_id.doctor_id.doctor_id else '') + """</para></td>
                                    
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
            if odontology_exam.evolution_ids:
                for evo in odontology_exam.evolution_ids:
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
                
            rml += """ </blockTable>"""
            rml += """ </story>"""
            rml += """</document>"""

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        
        #Removing temporary file
        if png_odontogram_img:
          os.remove(png_odontogram_img)
        if _png_odontogram_img and odontology_exam.odontogram_img:
          os.remove(_png_odontogram_img)
        odontology_exam_obj.write(cr, uid, ids, {'odontogram_img': None})
        
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

odontogram('report.odontogram_report', 'oemedical.odontology.exam', '', '')
