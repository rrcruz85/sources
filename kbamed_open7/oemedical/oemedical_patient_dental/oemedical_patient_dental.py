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
#from osv import osv
#from osv import fields

import time
from openerp.osv import fields, osv, orm
from time import strftime

class OeMedicalPatientDental(osv.Model):
    _name='oemedical.patient.dental'
    
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

    def _check_eva(self, cr, uid, ids, context=None):
        for eva in self.browse(cr, uid, ids, context):
            if eva.eva_value >= 1 and eva.eva_value <= 10: 
                return True
        return False
    
    def _date_to_str(self, cr, uid, ids, field_name, arg, context=None):
        '''From a date 2015-09-30 return a dictionary with 20150930'''
        res = {}
        for date in self.browse(cr, uid, ids, context=context):
            date_split = date.physio_date.split("-")
            date_str = date_split[0] + date_split[1] + date_split[2]
            #date_str += date.physio_date.strftime("%d")
            res[ids[0]] = date_str
        return res

        
    _columns={
              'patient_id':fields.many2one('oemedical.patient', 'Patient', required=True),
              'doctor': fields.many2one('oemedical.physician', string='Doctor'),
              'date_str': fields.function(_date_to_str, store=True, string='DateStr', type='char', size=8),
              'eva_value': fields.integer('Valor EVA', size=2),
              'dental_date': fields.date(string='Date', readonly=True),
              'labios': fields.boolean('Labios'),
              'mejillas': fields.boolean('Mejillas'),
              'max_superior': fields.boolean('Maxilar Superior'),
              'max_inferior': fields.boolean('Maxilar Inferior'),
              'lengua': fields.boolean('Lengua'),
              'paladar': fields.boolean('Paladar'),
              'piso': fields.boolean('Piso'),
              'carrillos': fields.boolean('Carrillos'),
              'glan_salivales': fields.boolean('Glandulas Salivales'),
              'oro_faringe': fields.boolean('Oro Faringe'),
              'atm': fields.boolean('ATM'),
              'ganglios': fields.boolean('Ganglios'),
              'detalle': fields.text('Detalle'), 
            }
    
    _defaults = {
              'dental_date': time.strftime('%Y-%m-%d'),
              'patient_id': _get_patient,
              #'doctor': _get_doctor,
              }
    
    _constraints = [
        (_check_eva, 'El valor EVA solo puede ser un entero entre 1 y 10', ['eva_value']),
    ]
    
OeMedicalPatientDental()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
