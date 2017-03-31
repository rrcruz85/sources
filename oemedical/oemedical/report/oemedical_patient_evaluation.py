# -*- enócoding: utf-8 -*-
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

from openerp import pooler, tools
from openerp.report.interface import report_rml
from openerp.tools.translate import _

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

class oemedical_patient_evaluation_report(report_rml):
    def create(self, cr, uid, ids, datas, context):
        evaluation_obj = pooler.get_pool(cr.dbname).get('oemedical.patient.evaluation')
        company_obj = pooler.get_pool(cr.dbname).get('res.company')
        
        company_ids_list = company_obj.search(cr, uid, [], context=context)
        company = company_obj.browse(cr, uid, company_ids_list[0], context) if len(company_ids_list) > 0 else False
        
        for evaluation in evaluation_obj.browse(cr, uid, ids, context):
            rml = """
                    <document filename="test.pdf">
                        <template pageSize="(595.0,842.0)" title=" """ + _("Official Report MSP") + """ " author="Reynaldo Rodriguez Cruz" allowSplitting="20">
                            <pageTemplate id="page1">
                                <frame id="first" x1="57.0" y1="55.0" width="498" height="805"/>
                                <frame id="third" x1="57.0" y1="5.0" width="498" height="70"/>
                            </pageTemplate>
                        </template>"""
            
            rml += """
                        <stylesheet>
                            <blockTableStyle id="Standard_Outline">
                              <blockAlignment value="LEFT"/>
                              <blockValign value="TOP"/>
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
                              <blockValign value="MIDDLE"/>
                              <blockAlignment value="CENTER"/>
                              <blockBackground colorName="#D9FFD9" start="0,0" stop="-1,0"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table2X">
                              <blockValign value="MIDDLE"/>
                              <blockAlignment value="LEFT"/>
                              
                              <blockValign value="TOP" start="0,1" stop="0,1"/>
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="1,0"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="-1,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              
                              <blockSpan start="0,1" stop="1,1"/>
                              <blockSpan start="0,2" stop="1,2"/>
                              <blockSpan start="0,3" stop="1,3"/>
                              <blockSpan start="0,4" stop="1,4"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table3">
                              <blockAlignment value="LEFT"/>
                              <blockValign value="MIDDLE"/>
                              <blockValign value="TOP" start="0,1" stop="0,1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="1,0"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table3M">
                              <blockAlignment value="LEFT"/>
                              <blockValign value="MIDDLE"/>
                              <blockValign value="TOP" start="0,1" stop="0,1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="19,1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="19,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,2" stop="19,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,3" stop="19,-1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="19,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="19,0" stop="19,3" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="19,0" thickness="0.1"/>
                              
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="19,0"/>
                              <blockBackground colorName="#D9FFD9" start="0,1" stop="0,1"/>
                              <blockBackground colorName="#D9FFD9" start="2,1" stop="2,1"/>
                              <blockBackground colorName="#D9FFD9" start="4,1" stop="4,1"/>
                              <blockBackground colorName="#D9FFD9" start="6,1" stop="6,1"/>
                              <blockBackground colorName="#D9FFD9" start="8,1" stop="8,1"/>
                              <blockBackground colorName="#D9FFD9" start="10,1" stop="10,1"/>
                              <blockBackground colorName="#D9FFD9" start="12,1" stop="12,1"/>
                              <blockBackground colorName="#D9FFD9" start="14,1" stop="14,1"/>
                              <blockBackground colorName="#D9FFD9" start="16,1" stop="16,1"/>
                              <blockBackground colorName="#D9FFD9" start="18,1" stop="18,1"/>
                              
                              <blockBackground colorName="#FFFF9F" start="1,1" stop="1,1"/>
                              <blockBackground colorName="#FFFF9F" start="3,1" stop="3,1"/>
                              <blockBackground colorName="#FFFF9F" start="5,1" stop="5,1"/>
                              <blockBackground colorName="#FFFF9F" start="7,1" stop="7,1"/>
                              <blockBackground colorName="#FFFF9F" start="9,1" stop="9,1"/>
                              <blockBackground colorName="#FFFF9F" start="11,1" stop="11,1"/>
                              <blockBackground colorName="#FFFF9F" start="13,1" stop="13,1"/>
                              <blockBackground colorName="#FFFF9F" start="15,1" stop="15,1"/>
                              <blockBackground colorName="#FFFF9F" start="17,1" stop="17,1"/>
                              <blockBackground colorName="#FFFF9F" start="19,1" stop="19,1"/>
                              
                              <blockSpan start="0,0" stop="19,0"/>
                              <blockSpan start="0,2" stop="19,2"/>
                              <blockSpan start="0,3" stop="19,3"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table4">
                              <blockAlignment value="LEFT"/>
                              <blockValign value="MIDDLE"/>
                              
                              <blockSpan start="0,0" stop="4,0"/>
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="4,0"/>
                              <blockBackground colorName="#D9FFD9" start="0,1" stop="0,5"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="4,0" stop="4,0" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="4,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="4,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="4,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="4,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table5">
                              <blockAlignment value="CENTER"/>
                              <blockValign value="MIDDLE"/>
                              
                              <blockSpan start="0,0" stop="1,0"/>
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="9,0"/>
                              <blockBackground colorName="#CAE7D4" start="0,1" stop="0,2"/>
                              <blockBackground colorName="#CAE7D4" start="5,1" stop="5,2"/>
                              <blockBackground colorName="#F9F1AD" start="3,1" stop="4,1"/>
                              <blockBackground colorName="#F9F1AD" start="3,2" stop="4,2"/>
                              <blockBackground colorName="#F9F1AD" start="8,1" stop="9,1"/>
                              <blockBackground colorName="#F9F1AD" start="8,2" stop="9,2"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="9,0" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="9,1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,2" stop="9,2" thickness="0.1"/>
                              
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="9,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="9,1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,2" stop="9,2" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="9,0" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="9,1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,2" stop="9,2" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="9,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="9,1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,2" stop="9,2" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table5M">
                              <blockAlignment value="LEFT"/>
                              <blockAlignment value="LEFT" start="9,0" stop="14,0"/>
                              <blockValign value="MIDDLE"/>
                              <blockValign value="TOP" start="0,1" stop="0,1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,2" stop="14,3" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="14,0" stop="14,-1" thickness="0.1"/>
                              
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="14,0"/>
                              <blockBackground colorName="#D9FFD9" start="0,1" stop="14,1"/>
                              
                              <blockBackground colorName="#D9FFD9" start="0,2" stop="0,3"/>
                              <blockBackground colorName="#D9FFD9" start="3,2" stop="3,3"/>
                              <blockBackground colorName="#D9FFD9" start="6,2" stop="6,3"/>
                              <blockBackground colorName="#D9FFD9" start="9,2" stop="9,3"/>
                              <blockBackground colorName="#D9FFD9" start="12,2" stop="12,3"/>
                              
                              <blockBackground colorName="#FFFF9F" start="1,2" stop="2,3"/>
                              <blockBackground colorName="#FFFF9F" start="4,2" stop="5,3"/>
                              <blockBackground colorName="#FFFF9F" start="7,2" stop="8,3"/>
                              <blockBackground colorName="#FFFF9F" start="10,2" stop="11,3"/>
                              <blockBackground colorName="#FFFF9F" start="13,2" stop="14,3"/>
                              
                              <blockSpan start="0,0" stop="8,0"/>
                              <blockSpan start="9,0" stop="14,0"/>
                              <blockSpan start="0,4" stop="14,4"/>
                              <blockSpan start="0,5" stop="14,5"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table6">
                              <blockAlignment value="CENTER"/>
                              <blockValign value="MIDDLE"/>
                              <blockValign value="TOP" start="0,1" stop="0,1"/>
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="1,0"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="0,1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,0" stop="1,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,1" stop="1,1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="1,0" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="1,1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="1,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="1,1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,1" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="1,1" stop="1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="1,1" stop="1,-1" thickness="0.1"/>
                              
                              <blockSpan start="0,1" stop="1,1"/>
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
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table6_1">
                              <blockAlignment value="CENTER"/>
                              <blockValign value="MIDDLE"/>       
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="0,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table7M">
                              <blockAlignment value="LEFT"/>
                              <blockValign value="MIDDLE"/>
                              
                              <blockSpan start="0,0" stop="9,0"/>
                              <blockSpan start="10,0" stop="17,0"/>
                              
                              <blockSpan start="0,3" stop="17,3"/>
                              <blockSpan start="0,4" stop="17,4"/>
                              <blockSpan start="0,5" stop="17,5"/>
                              <blockSpan start="0,6" stop="17,6"/>
                              
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="17,0"/>
                              <blockBackground colorName="#D9FFD9" start="0,1" stop="-1,1"/>
                              
                              <blockBackground colorName="#D9FFD9" start="0,2" stop="0,2"/>
                              <blockBackground colorName="#D9FFD9" start="3,2" stop="3,2"/>
                              <blockBackground colorName="#D9FFD9" start="6,2" stop="6,2"/>
                              <blockBackground colorName="#D9FFD9" start="9,2" stop="9,2"/>
                              <blockBackground colorName="#D9FFD9" start="12,2" stop="12,2"/>
                              <blockBackground colorName="#D9FFD9" start="15,2" stop="15,2"/>
                              
                              <blockBackground colorName="#FFFF9F" start="1,2" stop="2,2"/>
                              <blockBackground colorName="#FFFF9F" start="4,2" stop="5,2"/>
                              <blockBackground colorName="#FFFF9F" start="7,2" stop="8,2"/>
                              <blockBackground colorName="#FFFF9F" start="10,2" stop="11,2"/>
                              <blockBackground colorName="#FFFF9F" start="13,2" stop="14,2"/>
                              <blockBackground colorName="#FFFF9F" start="16,2" stop="17,2"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="17,0" stop="17,0" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="17,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="17,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,2" stop="-1,2" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,2" stop="-1,2" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,2" stop="-1,2" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,2" stop="-1,2" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="0,1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="17,1" stop="17,1" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,2" stop="0,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,2" stop="-1,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,2" stop="17,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table7">
                              <blockAlignment value="CENTER"/>
                              <blockValign value="MIDDLE"/>
                              
                              <blockBackground colorName="#D9FFD9" start="0,1" stop="0,1"/>
                              <blockBackground colorName="#D9FFD9" start="2,1" stop="2,1"/>
                              <blockBackground colorName="#D9FFD9" start="4,1" stop="4,1"/>
                              <blockBackground colorName="#D9FFD9" start="7,1" stop="7,1"/>
                              <blockBackground colorName="#D9FFD9" start="9,1" stop="9,1"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="10,1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="10,1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="10,1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="10,1" thickness="0.1"/>
                            </blockTableStyle>
                    
                            <blockTableStyle id="Table8">
                              <blockValign value="TOP"/>
                              <blockLeftPadding value="0"/>
                              <blockRightPadding value="0"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table8M">
                              <blockAlignment value="CENTER"/>
                              <blockValign value="MIDDLE"/>
                              
                              <blockSpan start="0,0" stop="1,0"/>
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="9,0"/>
                              <blockBackground colorName="#D9FFD9" start="0,1" stop="0,2"/>
                              <blockBackground colorName="#D9FFD9" start="5,1" stop="5,2"/>
                              <blockBackground colorName="#FFFF9F" start="3,1" stop="4,1"/>
                              <blockBackground colorName="#FFFF9F" start="3,2" stop="4,2"/>
                              <blockBackground colorName="#FFFF9F" start="8,1" stop="9,1"/>
                              <blockBackground colorName="#FFFF9F" start="8,2" stop="9,2"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="9,0" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,1" stop="9,1" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,2" stop="9,2" thickness="0.1"/>
                              
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="9,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,1" stop="9,1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,2" stop="9,2" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="9,0" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,1" stop="9,1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,2" stop="9,2" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="9,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,1" stop="9,1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,2" stop="9,2" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table10">
                              <blockAlignment value="LEFT"/>
                              <blockValign value="TOP"/>
          
                              <blockSpan start="0,2" stop="2,2"/>
          
                              <blockBackground colorName="#EBECEC" start="0,2" stop="2,2"/>
                              <blockBackground colorName="#EBECEC" start="4,2" stop="6,2"/>
                              <blockBackground colorName="#C0C0C2" start="1,0" stop="1,1"/>
                              <blockBackground colorName="#C0C0C2" start="1,3" stop="1,3"/>
                              <blockBackground colorName="#D1D3D4" start="3,0" stop="3,4"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table10M">
                              <blockBackground colorName="#C6C6FF" start="0,0" stop="1,0"/>
                              <blockBackground colorName="#C6C6FF" start="3,0" stop="4,0"/>
                              <blockAlignment value="LEFT"/>
                              <blockValign value="TOP"/>
                              
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="0,0" thickness="0.1"/>
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="3,0" stop="3,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="1,0" stop="1,0" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="4,0" stop="4,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="1,0" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="3,0" stop="4,0" thickness="0.1"/>
                              
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="1,0" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="3,0" stop="4,0" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <blockTableStyle id="Table22">
                              <blockValign value="TOP" start="0,0" stop="-1,-1"/>
                              <blockAlignment value="LEFT" start="0,0" stop="-1,-1"/>
                              <blockValign value="MIDDLE" start="0,0" stop="-1,0"/>
                              
                              <blockBackground colorName="#D9FFD9" start="0,0" stop="2,0"/>
                              <blockBackground colorName="#D9FFD9" start="4,0" stop="5,0"/>
                                  
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="0,0" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="0,0" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="2,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="2,-1" thickness="0.1"/>
                                
                              <lineStyle kind="LINEBEFORE" colorName="#000000" start="4,0" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEAFTER" colorName="#000000" start="4,0" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEABOVE" colorName="#000000" start="4,0" stop="5,-1" thickness="0.1"/>
                              <lineStyle kind="LINEBELOW" colorName="#000000" start="4,0" stop="5,-1" thickness="0.1"/>
                            </blockTableStyle>
                            
                            <initialize>
                              <paraStyle name="all" alignment="justify"/>
                            </initialize>
                    
                            <paraStyle name="P1" fontName="Helvetica" fontSize="12.0" leading="15" spaceBefore="0.0" spaceAfter="0.0"/>
                            <paraStyle name="P2" fontName="Helvetica" fontSize="10.0" leading="13" spaceBefore="0.0" spaceAfter="0.0"/>
                            <paraStyle name="P3" fontName="Helvetica" spaceBefore="0.0" spaceAfter="0.0" textColor="#000000"/>
                            <paraStyle name="P4" fontName="Helvetica" alignment="RIGHT" spaceBefore="0.0" spaceAfter="0.0" textColor="#000000"/>
                            <paraStyle name="P5" fontName="Helvetica" fontSize="1.0" leading="2" spaceBefore="0.0" spaceAfter="0.0" textColor="#000000"/>
                            <paraStyle name="P6" fontName="Helvetica" fontSize="1.0" leading="2" alignment="RIGHT" spaceBefore="0.0" spaceAfter="0.0" textColor="#000000"/>
                            <paraStyle name="P7" fontName="Helvetica" spaceBefore="0.0" spaceAfter="0.0" textColor="#767171"/>
                            <paraStyle name="P8" fontName="Helvetica" alignment="RIGHT" spaceBefore="0.0" spaceAfter="0.0" textColor="#767171"/>
                            <paraStyle name="P9" fontName="Helvetica" fontSize="1.0" leading="2" spaceBefore="0.0" spaceAfter="0.0" textColor="#767171"/>
                            <paraStyle name="P10" fontName="Helvetica" alignment="RIGHT" spaceBefore="0.0" spaceAfter="0.0" textColor="#58595b"/>
                            <paraStyle name="P11" fontName="Helvetica" alignment="CENTER" spaceBefore="0.0" spaceAfter="0.0" textColor="#ffffff"/>
                            <paraStyle name="P12" fontName="Helvetica-Bold" alignment="RIGHT" spaceBefore="0.0" spaceAfter="0.0" textColor="#58595b"/>
                            <paraStyle name="P13" fontName="Helvetica-Bold" fontSize="9.0" leading="11" alignment="RIGHT" spaceBefore="0.0" spaceAfter="0.0" textColor="#a0a2a5"/>
                            <paraStyle name="Standard" fontName="Helvetica"/>
                            <paraStyle name="Normal" fontName="Helvetica"/>
                            <paraStyle name="Table Contents" fontName="Helvetica"/>
                            
                            <paraStyle name="P6_CENTER" fontName="Helvetica" fontSize="6.0" leading="8" alignment="CENTER"/>
                            
                            <paraStyle name="P15" fontName="Helvetica" fontSize="7.0" leading="7" alignment="CENTER"/>
                            <paraStyle name="P15_2" fontName="Helvetica" fontSize="6.0" leading="7" alignment="CENTER"/>
                            
                            <paraStyle name="P116" fontName="Helvetica-Bold" fontSize="6.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P16" fontName="Helvetica-Bold" fontSize="7.0" leading="10" alignment="CENTER"/>
                            
                            <paraStyle name="P166" fontName="Helvetica-Bold" fontSize="7.0" leading="15" alignment="CENTER"/>
                            <paraStyle name="P166M" fontName="Helvetica-Bold" fontSize="6.0" leading="0" alignment="CENTER" spaceBefore="0.0cm"/>
                            <paraStyle name="P166F" fontName="Helvetica-Bold" fontSize="6.0" leading="0" alignment="CENTER"/>
                            
                            <paraStyle name="P18" fontName="Helvetica" fontSize="8.0" leading="10" alignment="CENTER"/>
                            <paraStyle name="P19" fontName="Helvetica" fontSize="7.0" leading="7" alignment="CENTER"/>
                            
                            <paraStyle name="P20" fontName="Helvetica" fontSize="7.0" leading="8" alignment="LEFT"/>
                            <paraStyle name="P20_COURIER" fontName="Courier" fontSize="7.0" leading="8" alignment="JUSTIFY"/>
                            <paraStyle name="P20_COURIER_CENTER" fontName="Courier" fontSize="7.0" leading="8" alignment="CENTER"/>
                            <paraStyle name="P20_COURIER_CENTERX" fontName="Courier" fontSize="7.0" leading="16" alignment="CENTER"/>
                            <paraStyle name="P20_COURIER_CENTER1" fontName="Courier" fontSize="7.0" leading="1" alignment="CENTER"/>
                            <paraStyle name="P20_COURIER_LEFT" fontName="Courier" fontSize="7.0" leading="15" alignment="LEFT"/>
                            <paraStyle name="P20_COURIER_JUSTIFY" fontName="Courier" fontSize="7.0" leading="8" alignment="JUSTIFY"/>
                            <paraStyle name="P20_COURIER_CENTRE" fontName="Courier" fontSize="7.0" leading="8" alignment="CENTRE"/>
                            
                            <paraStyle name="P2000" fontName="Helvetica" fontSize="7.0" leading="16" alignment="LEFT"/>
                            <paraStyle name="P21" fontName="Helvetica" fontSize="7.0" leading="8" alignment="CENTER"/>
                            <paraStyle name="P22" fontName="Helvetica-Bold" fontSize="5.0" leading="5" alignment="CENTER"/>
                            
                            <paraStyle name="P25" fontName="Helvetica" fontSize="8.0" leading="10" alignment="RIGHT"/>
                            <paraStyle name="P23" fontName="Helvetica-Bold" fontSize="4.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P2323" fontName="Helvetica-Bold" fontSize="4.0" leading="5" alignment="CENTER"/>
                            <paraStyle name="P23_LEFT" fontName="Helvetica-Bold" fontSize="4.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P23_RIGHT" fontName="Helvetica-Bold" fontSize="4.0" leading="5" alignment="RIGHT"/>
                            
                            <paraStyle name="P26" fontName="Helvetica-Bold" fontSize="9.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P27" fontName="Helvetica-Bold" fontSize="10.0" leading="5" alignment="RIGHT"/>
                            <paraStyle name="P100" fontName="Helvetica" alignment="LEFT" spaceBefore="0.0" spaceAfter="0.0" textColor="#58595b"/>
                            <paraStyle name="P188" fontName="Helvetica-Bold" fontSize="5.0" leading="7" alignment="CENTER"/>
                            <paraStyle name="P199" fontName="Helvetica" fontSize="5.0" leading="7" alignment="CENTER"/>
                            <paraStyle name="P26" fontName="Helvetica-Bold" fontSize="7.0" leading="5" alignment="LEFT"/>
                            <paraStyle name="P277" fontName="Helvetica-Bold" fontSize="11.0" leading="5" alignment="RIGHT"/>
                            
                            <paraStyle name="P200" fontName="Helvetica-Bold" fontSize="7.0" leading="10" alignment="CENTER"/>
                            <paraStyle name="P200_LEFT" fontName="Helvetica-Bold" fontSize="7.0" leading="10" alignment="LEFT"/>
                            <paraStyle name="P00_COURIER_CENTER" fontName="Courier" fontSize="6.0" leading="15" alignment="CENTER"/>
                            <images/>
                        </stylesheet>
                        
                        <story>"""
            
            rml += """
                            <section>
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
                            </section>"""
                
            rml += """      
                            <section>
                            <blockTable colWidths="296.0,110.0,163.0" style="">
                                <tr><td></td><td></td><td></td></tr>
                            </blockTable>
                            
                            <blockTable colWidths="105.0,112.0,107.0,39.0,42.0,95.0" rowHeights="8.0,12.0" style="Table2">
                              <tr>
                                <td><para style="P6_CENTER">ESTABLECIMIENTO</para></td>
                                <td><para style="P6_CENTER">NOMBRE</para></td>
                                <td><para style="P6_CENTER">APELLIDO</para></td>
                                <td><para style="P6_CENTER">SEXO</para></td>
                                <td><para style="P6_CENTER">EDAD</para></td>
                                <td><para style="P6_CENTER">HISTORIA CLINICA</para></td>
                              </tr>
                              
                              <tr>
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + (tools.ustr(company.name) if company and company.name else "")[0:18] + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + (tools.ustr(evaluation.patient_id.first_name)[0:17] if evaluation.patient_id.first_name else "") + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + tools.ustr((evaluation.patient_id.last_name if evaluation.patient_id.last_name else "") + " " + (evaluation.patient_id.slastname if evaluation.patient_id.slastname else ""))[0:20]  + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + evaluation.patient_id.sex.upper() + """</font>
                                  </para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER"><font color="black">""" + str(self._get_year(evaluation.patient_id) or '') + """</font></para>
                                </td>
                                
                                <td>
                                  <para style="P20_COURIER_CENTER">
                                    <font color="black">""" + (tools.ustr(evaluation.patient_id.identification_code) if evaluation.patient_id.identification_code else "") + """</font>
                                  </para>
                                </td>
                              </tr>
                            </blockTable>"""
            
            tRows = 36
            mdc_info = self._get_list_words(evaluation.mdc_info, 110)[0]
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="500" rowHeights="12.0" style="Table3">
                                <tr><td><para style="P20">1.  MOTIVO DE CONSULTA</para></td></tr>
                                <tr><td><para style="P20_COURIER">""" + (tools.ustr(mdc_info)) + """</para></td></tr>
                            </blockTable>"""
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="330.0,170.0" rowHeights="12.0,12.0,12.0,12.0,12.0" style="Table2X">
                                <tr>
                                    <td><para style="P20">2.  ANTECEDENTES PERSONALES</para></td>
                                    <td><para style="P23">""" + tools.ustr('DATOS CLÍNICO - QUIRURGICOS RELEVANTES Y GINECO OBSTÉTRICOS') + """</para></td>
                                </tr>"""
            
            app_info = self._get_list_words(evaluation.patient_id.app_info, 110)
            
            if len(app_info) > 0:
                rml += """      <tr>
                                    <td><para style="P20_COURIER">""" + (tools.ustr(app_info[0]) if len(app_info) > 0 else '') + """</para></td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td><para style="P20_COURIER">""" + (tools.ustr(app_info[1]) if len(app_info) > 1 else '') + """</para></td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td><para style="P20_COURIER">""" + (tools.ustr(app_info[2]) if len(app_info) > 2 else '') + """</para></td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td><para style="P20_COURIER">""" + (tools.ustr(app_info[3]) if len(app_info) > 3 else '') + """</para></td>
                                    <td></td>
                                </tr>"""
            else:
                rml += """      <tr><td><para style="P20_COURIER"></para></td><td></td></tr>"""
                rml += """      <tr><td><para style="P20_COURIER"></para></td><td></td></tr>"""
                rml += """      <tr><td><para style="P20_COURIER"></para></td><td></td></tr>"""
                rml += """      <tr><td><para style="P20_COURIER"></para></td><td></td></tr>"""
            
            rml += """      </blockTable>"""
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="45.0,10.0,40.0,10.0,40.0,10.0,50.0,10.0,38.0,10.0,50.0,10.0,30.0,10.0,34.0,10.0,45.0,10.0,28.0,10.0" rowHeights="12.0,12.0,12.0,12.0" style="Table3M">
                                <tr>
                                    <td><para style="P20">3.  ANTECEDENTES FAMILIARES</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>"""
            
            rml += """
                                <tr>
                                    <td><para style="P23">""" + tools.ustr('1. Cardiopatía') + """</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_cardiopatia else '') + """</para></td>
                                    <td><para style="P23">2. Diabetes</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_diabetes else '') + """</para></td>
                                    <td><para style="P23">3. Enf. C. Vascular</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_enf_c_vascular else '') + """</para></td>
                                    <td><para style="P23">""" + tools.ustr('4. Hipertersión') + """</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_hipertension else '') + """</para></td>
                                    <td><para style="P23">""" + tools.ustr('5. Cáncer') + """</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_cancer else '') + """</para></td>
                                    <td><para style="P23">""" + tools.ustr('6. Tuberculosis') + """</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_tuberculosis else '') + """</para></td>
                                    <td><para style="P23">7. Enf. Mental</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_enf_mental else '') + """</para></td>
                                    <td><para style="P23">8. Enf. Infecciosa</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_enf_infecciosa else '') + """</para></td>
                                    <td><para style="P23">""" + tools.ustr('9. Malformación') + """</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_mal_formacion else '') + """</para></td>
                                    <td><para style="P23">10. Otro</para></td>
                                    <td><para style="P00_COURIER_CENTER">""" + ('X' if evaluation.patient_id.has_otros else '') + """</para></td>
                                </tr>"""
            
            apf_info = self._get_list_words(evaluation.patient_id.apf_info, 110)
            
            if len(apf_info) > 0:
                rml += """      <tr><td><para style="P20_COURIER">""" + (tools.ustr(apf_info[0]) if len(apf_info) > 0 else '') + """</para></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"""
                rml += """      <tr><td><para style="P20_COURIER">""" + (tools.ustr(apf_info[1]) if len(apf_info) > 1 else '') + """</para></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"""
            else:
                rml += """      <tr>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>"""
                rml += """      <tr>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>"""
            
            rml += """      </blockTable>"""
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="500.0" rowHeights="12.0,12.0,12.0,12.0,12.0,12.0,12.0" style="Table3">
                                <tr><td><para style="P20">4.  ENFERMEDAD O PROBLEMA ACTUAL</para></td></tr>"""
            
            eac_info = self._get_list_words(evaluation.eac_info, 110)
            
            if len(eac_info) > 0:
                for i in range(6):
                    rml += """  <tr><td><para style="P20_COURIER">""" + (tools.ustr(eac_info[i]) if len(eac_info) > i else '') + """</para></td></tr>"""
            else:
                for i in range(6):
                    rml += """  <tr><td><para style="P20_COURIER"></para></td></tr>"""
            
            rml += """      </blockTable>"""
            
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="60.0,20.0,20.0,60.0,20.0,20.0,60.0,20.0,20.0,60.0,20.0,20.0,60.0,20.0,20.0" rowHeights="12.0,8.0,12.0,12.0,12.0,12.0" style="Table5M">
                                <tr>
                                    <td><para style="P20">5.  REVISION ACTUAL DE ORGANOS Y SISTEMAS</para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td>
                                        <para style="P23_LEFT">
                                            """ + tools.ustr('CP = Con evidencia de patología: marcar "x" y describir abajo anotando el número y letra.') + tools.ustr(' SP = Sin evidencia de patología: marcar "x" y no describir.') + """
                                        </para>
                                    </td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                </tr>
                                <tr>
                                    <td><para style="P20"></para></td>
                                    <td><para style="P2323">CP</para></td>
                                    <td><para style="P2323">SP</para></td>
                                    <td><para style="P23_LEFT"></para></td>
                                    <td><para style="P2323">CP</para></td>
                                    <td><para style="P2323">SP</para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P2323">CP</para></td>
                                    <td><para style="P2323">SP</para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P2323">CP</para></td>
                                    <td><para style="P2323">SP</para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P2323">CP</para></td>
                                    <td><para style="P2323">SP</para></td>
                                </tr>
                                <tr>
                                    <td><para style="P23_LEFT">""" + tools.ustr('1. ÓRGANOS DE LOS SENTIDOS') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.org_scp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.org_ssp else '') + """</para></td>
                                    <td><para style="P23_LEFT">""" + tools.ustr('3. CARDIO VASCULAR') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.car_vcp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.car_vsp else '') + """</para></td>
                                    <td><para style="P23_LEFT">""" + tools.ustr('5. GENITAL') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.gen_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.gen_sp else '') + """</para></td>
                                    <td><para style="P23_LEFT">""" + tools.ustr('7. MÚSCULO ESQUELÉTICO') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.mus_ecp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.mus_esp else '') + """</para></td>
                                    <td><para style="P23_LEFT">""" + tools.ustr('9. HEMO LINFÁTICO') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.hmo_lcp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.hmo_lsp else '') + """</para></td>
                                </tr>
                                <tr>
                                    <td><para style="P23_LEFT">""" + tools.ustr('2. RESPIRATORIO') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.res_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.res_sp else '') + """</para></td>
                                    <td><para style="P23_LEFT">""" + tools.ustr('4. DIGESTIVO') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.dig_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.dig_sp else '') + """</para></td>
                                    <td><para style="P23_LEFT">""" + tools.ustr('6. URINARIO') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.uri_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.uri_sp else '') + """</para></td>
                                    <td><para style="P23_LEFT">""" + tools.ustr('8. ENDOCRINO') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.end_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.end_sp else '') + """</para></td>
                                    <td><para style="P23_LEFT">""" + tools.ustr('10. NERVIOSO') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.nrv_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.nrv_sp else '') + """</para></td>
                                </tr>"""
            
            revision_organos = self._get_list_words(evaluation.revision_organos, 110)
            
            if len(revision_organos) > 0:
                rml += """      <tr><td><para style="P20_COURIER">""" + (tools.ustr(revision_organos[0]) if len(revision_organos) > 0 else '') + """</para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td></tr>"""
                rml += """      <tr><td><para style="P20_COURIER">""" + (tools.ustr(revision_organos[1]) if len(revision_organos) > 1 else '') + """</para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td></tr>"""
            else:
                rml += """      <tr><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td></tr>
                                <tr><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td><td><para style="P20_COURIER"></para></td></tr>"""
            
            rml += """      </blockTable>"""
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="130.0,92.5,92.5,92.5,92.5" rowHeights="12.0,12.0,12.0,12.0,12.0,12.0" style="Table4">
                                <tr>
                                    <td><para style="P20">6.  SIGNOS VITALES Y ANTROPOMETRIA</para></td>
                                    <td>2</td><td>2</td><td>2</td><td>2</td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P23_LEFT">FECHA DE MEDICION</para></td>
                                    <td><para style="P15_2">""" + (evaluation.evaluation_date if evaluation.evaluation_date else '') + """</para></td>
                                    <td><para style="P15_2"></para></td><td><para style="P15_2"></para></td><td><para style="P15_2"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P23_LEFT">""" + tools.ustr('TEMPERATURA °C') + """</para></td>
                                    <td><para style="P15_2">""" + (str(evaluation.tem_info) if evaluation.tem_info else '') + """</para></td>
                                    <td><para style="P15_2"></para></td><td><para style="P15_2"></para></td><td><para style="P15_2"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P23_LEFT">PRESION ARTERIAL</para></td>
                                    <td><para style="P15_2">""" + (evaluation.pat_info if evaluation.pat_info else '') + """</para></td>
                                    <td><para style="P15_2"></para></td><td><para style="P15_2"></para></td><td><para style="P15_2"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P23_LEFT">PULSO min / FRECUENCIA RESPIRATORIA</para></td>
                                    <td><para style="P15_2">""" + (str(evaluation.ppm_info) if evaluation.ppm_info else '') + ' | ' + (str(evaluation.fqr_info) if evaluation.fqr_info else '') + """</para></td>
                                    <td><para style="P15_2"></para></td><td><para style="P15_2"></para></td><td><para style="P15_2"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P23_LEFT">PESO (Kg) / TALLA (cm)</para></td>
                                    <td><para style="P15_2">""" + (str(evaluation.pes_info) + ' Kg' if evaluation.pes_info else '') + ' | ' + (str(evaluation.est_info) + ' cm' if evaluation.est_info else '') + """</para></td>
                                    <td><para style="P15_2"></para></td><td><para style="P15_2"></para></td><td><para style="P15_2"></para></td>
                                </tr>
                            </blockTable>"""
           
            rml += """
                            <spacer length="0.1cm"/>
                            <blockTable colWidths="43.33,20.0,20.0,38.33,20.0,20.0,43.33,20.0,20.0,43.33,20.0,20.0,38.33,20.0,20.0,53.33,20.0,20.0" rowHeights="12.0,8.0,12.0,12.0,12.0,12.0,12.0" style="Table7M">
                                <tr>
                                    <td><para style="P20">""" + tools.ustr('7.  EXAMEN FÍSICO REGIONAL') + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td>
                                        <para style="P23_LEFT">
                                            """ + tools.ustr('CP = Con evidencia de patología: marcar "x" y describir anotando el número y letra.') + tools.ustr(' SP = Sin evidencia de patología: marcar "x" y no describir.') + """
                                        </para>
                                    </td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P20"></para></td>
                                    <td><para style="P23">CP</para></td>
                                    <td><para style="P23">SP</para></td>
                                    <td><para style="P23_LEFT"></para></td>
                                    <td><para style="P23">CP</para></td>
                                    <td><para style="P23">SP</para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P23">CP</para></td>
                                    <td><para style="P23">SP</para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P23">CP</para></td>
                                    <td><para style="P23">SP</para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P23">CP</para></td>
                                    <td><para style="P23">SP</para></td>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td><para style="P23">CP</para></td>
                                    <td><para style="P23">SP</para></td>
                                </tr>"""
            
            rml += """
                                <tr>
                                    <td><para style="P23">1. CABEZA</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.cab_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.cab_sp else '') + """</para></td>
                                    <td><para style="P23">2. CUELLO</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.cue_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.cue_sp else '') + """</para></td>
                                    <td><para style="P23">""" + tools.ustr('3. TÓRAX') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.trx_vcp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.trx_vsp else '') + """</para></td>
                                    <td><para style="P23">4. ABDOMEN</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.abd_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.abd_sp else '') + """</para></td>
                                    <td><para style="P23">5. PELVIS</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.pel_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.pel_sp else '') + """</para></td>
                                    <td><para style="P23">6. EXTREMIDADES</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.ext_cp else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if evaluation.ext_sp else '') + """</para></td>
                                </tr>"""
            
            ena_info = self._get_list_words(evaluation.ena_info, 110)
            
            if len(ena_info) > 0:
                for i in range(4):
                    rml += """  <tr>
                                    <td><para style="P20_COURIER">""" + (tools.ustr(ena_info[i]) if len(ena_info) > i else '') + """</para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>"""
            else:
                for i in range(4):
                    rml += """  <tr>
                                    <td><para style="P20_COURIER"></para></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                    <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                </tr>"""
            
            rml += """</blockTable>"""
            
            if tRows < 0:                
                rml += """<pageBreak/> <spacer length="1.0cm"/> """
                tRows = 36
            
            diagnosisList = []
            for diagnosis in evaluation.diagnosis:
                diagnosisList.append((tools.ustr(diagnosis.name), 'pre', tools.ustr(diagnosis.code)))
            
            for diagnosis in evaluation.definitive_diagnosis:
                diagnosisList.append((tools.ustr(diagnosis.name), 'def', tools.ustr(diagnosis.code)))
            
            if len(diagnosisList) < 4:
                while len(diagnosisList) < 4:
                    diagnosisList.append(('', '', ''))
            
            filaAlto1 = 1      
            if len(diagnosisList[0][0]) > 30:
                tmp1 = len(diagnosisList[0][0])/30            
                filaAlto1 = tmp1 + 1 if len(diagnosisList[0][0]) % 30 != 0 else tmp1
            
            filaAlto2 = 1     
            if len(diagnosisList[2][0]) > 30:
                tmp2 = len(diagnosisList[2][0])/30            
                filaAlto2 = tmp2 + 1 if len(diagnosisList[2][0]) % 30 != 0 else tmp2
              
            maxVal1 = max([filaAlto1,filaAlto2])
            if maxVal1 != 1:
                tRows -= maxVal1         
            filaAlto1 = 12.0 * maxVal1 if 12.0 * maxVal1 < 58.0 else 58.0
            
            filaAlto3 = 1      
            if len(diagnosisList[1][0]) > 30:
                tmp3 = len(diagnosisList[1][0])/30            
                filaAlto3 = tmp3 + 1 if len(diagnosisList[1][0]) % 30 != 0 else tmp3
            
            filaAlto4 = 1     
            if len(diagnosisList[3][0]) > 30:
                tmp4 = len(diagnosisList[3][0])/30            
                filaAlto4 = tmp4 + 1 if len(diagnosisList[3][0]) % 30 != 0 else tmp4
              
            maxVal2 = max([filaAlto3,filaAlto4])
            if maxVal1 != 1:
                tRows -= maxVal2          
            filaAlto3 = 12.0 * maxVal2 if 12.0 * maxVal2 < 58.0 else 58.0
              
            if tRows < 0:
                rml += """<pageBreak/> <spacer length="1.0cm"/> """
                tRows = 36
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="15.0,156.0,33.5,23.0,23.0,15.0,156.0,33.5,23.0,23.0" rowHeights="12.0,12.0,12.0" style="Table8M">
                                <tr>
                                    <td><para style="P20">8.  DIAGNOSTICOS</para></td>
                                    <td><para style="P20"> </para></td>
                                    <td><para style="P22">CIE</para></td>
                                    <td><para style="P22">PRE</para></td>
                                    <td><para style="P22">DEF</para></td>
                                    <td><para style="P20"> </para></td>
                                    <td><para style="P23_LEFT">PRE= PRESUNTIVO  DEF= DEFINITIVO</para></td>
                                    <td><para style="P22">CIE</para></td>
                                    <td><para style="P22">PRE</para></td>
                                    <td><para style="P22">DEF</para></td>
                                </tr>"""          
            
            rml += """
                                <tr>
                                    <td><para style="P20_COURIER_CENTERX">""" + str(1) + """</para></td>
                                    <td><para style="P20_COURIER">""" + tools.ustr(diagnosisList[0][0][0:31]) + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + diagnosisList[0][2][0:5] + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if diagnosisList[0][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if diagnosisList[0][1] == 'def' else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTERX">""" + str(3) + """</para></td>
                                    <td><para style="P20_COURIER">""" + tools.ustr(diagnosisList[2][0][0:31]) + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + diagnosisList[2][2][0:5] + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if diagnosisList[2][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if diagnosisList[2][1] == 'def' else '') + """</para></td>
                                </tr>                                
                                <tr>
                                    <td><para style="P20_COURIER_CENTERX">""" +str(2) + """</para></td>
                                    <td><para style="P20_COURIER">""" + tools.ustr(diagnosisList[1][0][0:31]) + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + diagnosisList[1][2][0:5] + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if diagnosisList[1][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if diagnosisList[1][1] == 'def' else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTERX">""" +str(4) + """</para></td>
                                    <td><para style="P20_COURIER">""" + tools.ustr(diagnosisList[3][0][0:31]) + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + diagnosisList[3][2][0:5] + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if diagnosisList[3][1] == 'pre' else '') + """</para></td>
                                    <td><para style="P20_COURIER_CENTER">""" + ('X' if diagnosisList[3][1] == 'def' else '') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rowHeights = '12.0'
            for i in range(13):
               rowHeights += ',12.0' 
            
            if tRows < 0:
                rml += """<pageBreak/> <spacer length="1.0cm"/> """
                tRows = 36                            
            
            rml += """      <spacer length="0.1cm"/>
                            <blockTable colWidths="265.0,235.0" rowHeights=" """ + rowHeights + """" style="Table6">
                                <tr>
                                    <td><para style="P20">9.  PLANES</para></td>
                                    <td><para style="P23_RIGHT">""" + tools.ustr('PLANES DE DIAGNOSTICO, TERAPÉUTICO Y EDUCACIONAL') + """</para></td>
                                </tr>"""
            
            directions = self._get_list_words(evaluation.directions, 110)
            
            if len(directions) > 0:
                for i in range(13):
                    rml += """  <tr><td><para style="P20_COURIER">""" + (tools.ustr(directions[i]) if len(directions) > i else '') + """</para></td></tr>"""
            else:
                for i in range(13):
                    rml += """  <tr><td><para style="P20_COURIER"></para></td></tr>"""
            
            rml += """      </blockTable>"""
            
            rml += """      </section>"""
            rml += """      <nextFrame/>"""
            
            
            rml += """      <blockTable colWidths="35.0,45.0,30.0,35.0,50.0,136.0,35.0,35.0,50.0,35.0,15.0" rowHeights="7.0,12.0" style="Table7">
                                <tr>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23">CODIGO</para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23"></para></td>
                                </tr>
                                
                                <tr>
                                    <td><para style="P23">FECHA</para></td>
                                    <td><para style="P23">""" + (tools.ustr(evaluation.evaluation_date) if evaluation.evaluation_date else '') + """</para></td>
                                    <td><para style="P23">HORA</para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23">NOMBRE DEL PROFESIONAL</para></td>
                                    <td><para style="P23">""" + (tools.ustr(evaluation.doctor.physician_id.name) if evaluation.doctor.physician_id else '') + """</para></td>
                                    <td><para style="P23">""" + (tools.ustr(evaluation.doctor.code) if evaluation.doctor and evaluation.doctor.code else '') + """</para></td>
                                    <td><para style="P23">FIRMA</para></td>
                                    <td><para style="P23"></para></td>
                                    <td><para style="P23">NUMERO DE HOJA</para></td>
                                    <td><para style="P23"></para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <blockTable colWidths="135.0,335.0" style="Table8">
                                <tr>
                                    <td><para style="P26">SNS-MSP / HCU-form.002 / 2007</para></td>
                                    <td><para style="P27">""" + tools.ustr('CONSULTA EXTERNA - ANAMNESIS Y EXAMEN FÍSICO') + """</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """      <pageBreak/>"""
                
            rml += """      <blockTable colWidths="9.0,18.0,3.0,5.0,8.0,415.0" rowHeights="35.0,20.0,2.0,15.0,10.0" style="Table10">
                              <tr>
                                  <td><para style="P3"><font color="white"> </font></para></td>
                                  <td><para style="P3"> </para></td>
                                  <td><para style="P2"><font color="white"> </font></para></td>
                                  <td><para style="P2"><font color="white"> </font></para></td>
                                  <td><para style="P2"><font color="white"> </font></para></td>
                                  <td><para style="P1"><font color="white"> </font></para></td>
                              </tr>
                              
                              <tr>
                                  <td><para style="P8"><font color="white"> </font></para></td>
                                  <td><para style="P11"><font face="Helvetica"></font></para></td>
                                  <td><para style="P4"><font color="white"> </font></para></td>
                                  <td><para style="P4"> </para></td>
                                  <td><para style="P12"><font color="white"> </font></para></td>
                                  <td vAlign="bottom" bottomPadding="5"><para style="P100"><font face="Helvetica-Bold">""" + tools.ustr("") + """</font></para></td>
                              </tr>
                              
                              <tr>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                              </tr>
                              
                              <tr>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
                                  <td><para style="P5"></para></td>
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
                            </blockTable>"""
            
            rml += """
                            <blockTable colWidths="296.0,110.0,163.0" style="">
                                <tr><td></td><td></td><td></td></tr>
                            </blockTable>"""
            
            rml += """
                            <blockTable colWidths="215.0,50.0,5.0,165.0,65.0" rowHeights="15.0" style="Table10M">
                                <tr>
                                    <td><para style="P200_LEFT">""" + tools.ustr('10. EVOLUCIÓN') + """</para></td>
                                    <td><para style="P23_RIGHT">FIRMAR AL PIE DE CADA NOTA</para></td>
                                    <td><para style="P200"></para></td>
                                    <td><para style="P200_LEFT">11. PRESCRIPCIONES</para></td>
                                    <td><para style="P23_RIGHT">""" + tools.ustr('FIRMAR AL PIE DE CADA PRESCRIPCIÓN') + """</para></td>
                                </tr>
                            </blockTable>
                            <spacer length="0.2cm"/>"""
            
            x = 0
            tRows = 54
            rowHeights = '15.0'
            
            len_col_3 = 36
            len_col_4 = 30
            len_col_5 = 13
            
            if getattr(evaluation, 'evolution_ids', False):
                for evolution in evaluation.evolution_ids:
                    rows_evl_info = len(evolution.evl_info) / len_col_3 + 1 if evolution.evl_info and len(evolution.evl_info) % len_col_3 > 0 else 0
                    rows_directions = len(evolution.directions) / len_col_4 + 1 if evolution.directions and len(evolution.directions) % len_col_4 > 0 else 0
                    rows_medicamentos = len(evolution.medicamentos) / len_col_5 + 1 if evolution.medicamentos and len(evolution.medicamentos) % len_col_5 > 0 else 0
                    rows = max([rows_evl_info, rows_directions, rows_medicamentos])
                    
                    if tRows - (x + rows) >= 0:
                        rowHeights += ',' + str(12.0*rows)
                        x = x + rows
            
            while x < tRows:
                rowHeights += ',12.0'
                x = x + 1
            
            rml += """      <blockTable colWidths="55.0,30.0,180.0,5.0,165.0,65.0" rowHeights=" """ + rowHeights + """ " style="Table22">
                                <tr>
                                    <td><para style="P199">""" + tools.ustr('FECHA (DIA/MES/AÑO)') + """</para></td>
                                    <td><para style="P199">HORA</para></td>
                                    <td><para style="P199">""" + tools.ustr('NOTAS DE EVOLUCIÓN') + """</para></td>
                                    <td></td>
                                    <td><para style="P199">""" + tools.ustr('FARMACOTERAPIA E INDICACIONES PARA ENFERMERÍA Y OTRO PERSONAL') + """</para></td>
                                    <td><para style="P199">""" + tools.ustr('ADMINISTR. FÁRMACOS Y OTROS') + """</para></td>
                                </tr>"""
            
            x = 0
            if getattr(evaluation, 'evolution_ids', False):
                for evolution in evaluation.evolution_ids:
                    rows_evl_info = len(evolution.evl_info) / len_col_3 + 1 if evolution.evl_info and len(evolution.evl_info) % len_col_3 > 0 else 0
                    rows_directions = len(evolution.directions) / len_col_4 + 1 if evolution.directions and len(evolution.directions) % len_col_4 > 0 else 0
                    rows_medicamentos = len(evolution.medicamentos) / len_col_5 + 1 if evolution.medicamentos and len(evolution.medicamentos) % len_col_5 > 0 else 0
                    rows = max([rows_evl_info, rows_directions, rows_medicamentos])
                    
                    if tRows - (x + rows) >= 0:
                        x = x + rows
                        
                        if evolution.evolution_date:
                            temp = evolution.evolution_date.split(' ')[0].split('-')
                            date = temp[2] + '/' + temp[1] + '/' + temp[0]
                            time = '00:00'
                            if len(evolution.evolution_date.split(' ')) > 1:
                                temp = evolution.evolution_date.split(' ')[1].split(':')
                                if len(temp) > 1:
                                    time = temp[0] + ':' + temp[1]
                        else:
                            date = ''
                            time = ''
                        
                        rml += """  <tr>
                                        <td><para style="P20_COURIER_CENTER">""" + date + """</para></td>
                                        <td><para style="P20_COURIER_CENTER">""" + time + """</para></td>
                                        <td><para style="P20_COURIER">""" + (tools.ustr(evolution.evl_info) if evolution.evl_info else '') + """</para></td>
                                        <td></td>
                                        <td><para style="P20_COURIER">""" + (tools.ustr(evolution.directions) if evolution.directions else '') + """</para></td>
                                        <td><para style="P20_COURIER">"""+ (tools.ustr(evolution.medicamentos) if evolution.medicamentos else '') + """</para></td>
                                    </tr>"""
            
            while x < tRows:
                x = x + 1
                rml += """      <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>"""
            
            rml += """      </blockTable>"""
            rml += """      <nextFrame/>"""
                            
            rml += """      <blockTable colWidths="296.0,110.0,163.0" style="">
                                <tr><td></td><td></td><td></td></tr>
                            </blockTable>
                            
                            <blockTable colWidths="135.0,335.0" style="Table8">
                                <tr>
                                    <td><para style="P26">SNS-MSP / HCU-form.002 / 2008</para></td>
                                    <td><para style="P27">CONSULTA EXTERNA - EVOLUCION Y PRESCRIPCIONES</para></td>
                                </tr>
                            </blockTable>"""
            
            rml += """  </story>
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
        if not data: return ['']
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
		
oemedical_patient_evaluation_report('report.oemedical_patient_evaluation_report', 'oemedical.patient.evaluation', '', '')