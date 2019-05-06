# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.techreceptives.com>)
#    Special Credit and Thanks to Thymbra Latinoamericana S.A.
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
#/#############################################################################

import time
from openerp.osv import fields, osv, orm
from time import strftime

class OeMedicalTestRequest(osv.Model):
    _name='oemedical.test.request'

    def physio_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        #self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'oemedical.patient.physio',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'oemedical.patient.physioprint.webkit',
            'datas': datas,
            'nodestroy' : True
        }

    def _get_patient(self, cr, uid, context):
        run_pool = self.pool.get('oemedical.patient')
        run_data = {}
        if context and context.get('active_id', False):
            run_data = run_pool.read(cr, uid, context['active_id'], ['patient_id'])
            patient_id = run_data.get('id', False)
            if patient_id:
                return patient_id
        return False
    
    def _get_doctor(self, cr, uid, context):
        run_pool = self.pool.get('res.users')
        run_data = {}
        run_data = run_pool.read(cr, uid, uid, context)
        user_id = run_data.get('id', False)
        if user_id:
            return user_id
        return False
       
    _columns={
              'patient_id':fields.many2one('oemedical.patient', 'Patient', required=True),
              'test_date': fields.date(string='Fecha', readonly=True),
              'doctor': fields.many2one('oemedical.physician', string='Doctor'),
              'state': fields.selection([('draft','Solictado'),('done','Finalizado')]),
              'type_hema_ids': fields.many2many('oemedical.test.list','test_hema_list','pat_id','list_id', string='Examen'),
              'type_coag_ids': fields.many2many('oemedical.test.list','test_coag_list','pat_id','list_id', string='Examen'),
              'type_qmsa_ids': fields.many2many('oemedical.test.list','test_qmsa_list','pat_id','list_id', string='Examen'),
              'type_prlp_ids': fields.many2many('oemedical.test.list','test_prlp_list','pat_id','list_id', string='Examen'),
              'type_prep_ids': fields.many2many('oemedical.test.list','test_prep_list','pat_id','list_id', string='Examen'),
              'type_enzi_ids': fields.many2many('oemedical.test.list','test_enzi_list','pat_id','list_id', string='Examen'),
              'type_sero_ids': fields.many2many('oemedical.test.list','test_sero_list','pat_id','list_id', string='Examen'),
              'type_horm_ids': fields.many2many('oemedical.test.list','test_horm_list','pat_id','list_id', string='Examen'),
              'type_onco_ids': fields.many2many('oemedical.test.list','test_onco_list','pat_id','list_id', string='Examen'),
              'type_elec_ids': fields.many2many('oemedical.test.list','test_elec_list','pat_id','list_id', string='Examen'),
              'type_para_ids': fields.many2many('oemedical.test.list','test_para_list','pat_id','list_id', string='Examen'),
              'type_inmu_ids': fields.many2many('oemedical.test.list','test_inmu_list','pat_id','list_id', string='Examen'),
              'type_diag_ids': fields.many2many('oemedical.test.list','test_diag_list','pat_id','list_id', string='Examen'),
              'type_tera_ids': fields.many2many('oemedical.test.list','test_tera_list','pat_id','list_id', string='Examen'),
              'type_orin_ids': fields.many2many('oemedical.test.list','test_orin_list','pat_id','list_id', string='Examen'),
              'type_ores_ids': fields.many2many('oemedical.test.list','test_ores_list','pat_id','list_id', string='Examen'),
              'type_hece_ids': fields.many2many('oemedical.test.list','test_hece_list','pat_id','list_id', string='Examen'),
              'type_bact_ids': fields.many2many('oemedical.test.list','test_bact_list','pat_id','list_id', string='Examen'),
              'type_pato_ids': fields.many2many('oemedical.test.list','test_pato_list','pat_id','list_id', string='Examen'),
              'type_other_ids': fields.many2many('oemedical.test.list','test_other_list','pat_id','list_id', string='Examen'),
              }
    
    _defaults = {
              'test_date': time.strftime('%Y-%m-%d'),
              'patient_id': _get_patient,
#              'doctor': _get_doctor,
              }
    
OeMedicalTestRequest()

class TestList(osv.osv):

    _name = 'oemedical.test.list'
    
    _columns = {
        'name': fields.char(string='Nombre', size=50),
        'type': fields.char(string='Tipo', size=50, readonly=True),
        }

    _defaults = {
       'type' : lambda self, cr, uid, context : context['type'] if context and 'type' in context else None,
    }

TestList()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
