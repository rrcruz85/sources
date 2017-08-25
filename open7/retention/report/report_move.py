# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

import time
from openerp.report import report_sxw
from openerp.osv import osv
import openerp.pooler

class move(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(move, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_analytic_lines': self.get_analytic_lines,
        })

    def get_analytic_lines(self, obj_id, data):
        print obj_id, data
        move = self.pool.get('account.move').browse(self.cr, self.uid, obj_id)
        lines = []
        for line in move.line_id:
            for al in line.analytic_lines:
                if al.amount == 0:
                    continue
                line_data = {'acc_name': al.account_id.name,
                             'code': al.account_id.code,
                             'general_account': al.general_account_id.code,
                             'amount': abs(al.amount),
                             'name': al.name}
                lines.append(line_data)
        return lines
   
report_sxw.report_sxw('report.account.move','account.move','addons/retention/report/report_move.rml',parser=move)

