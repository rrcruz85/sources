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
from openerp.tools.translate import _

class OeMedicalPatientEvolution(osv.Model):
    _name='oemedical.patient.evolution'
     
    def _get_doctor(self, cr, uid, context):
        run_pool = self.pool.get('res.users')
        run_data = {}
        run_data = run_pool.read(cr, uid, uid, context)
        user_id = run_data.get('id', False)
        if user_id:
            return user_id
        return False
        
    _columns={              
			    'patient_id':fields.many2one('oemedical.patient', 'Patient', required=False),
			    'evaluation_id':fields.many2one('oemedical.patient.evaluation', 'Evaluación', required=False),
				'evolution_date': fields.datetime(string='Date and time', help='Enter or select the date and related to this evaluation', readonly=True),
				'doctor': fields.many2one('oemedical.physician', string='Doctor'),
				'diagnosis': fields.many2one('oemedical.pathology', string='Presumptive Diagnosis'),
				'directions': fields.text(string='Tratamiento'),
				'evl_info': fields.text(string='Evolución'),
				'medicamentos': fields.text(string='Medicamentos'),
              }
    
    _defaults = {
               'evolution_date': time.strftime('%Y-%m-%d %H:%M:%S'),
               'doctor': _get_doctor,
			   'evaluation_id': lambda self, cr, uid, context: context.get('evaluation_id', False),
              }
    
    #def _evolution_constraint_evl_info(self, cr, uid, ids):
    #    for evolution in self.browse(cr, uid, ids):
    #        if evolution.evl_info and (evolution.evl_info.count('\n') > 0 or len(evolution.evl_info) > 45):
    #            return False
    #    return True
    
    def _evolution_constraint_directions(self, cr, uid, ids):
        for evolution in self.browse(cr, uid, ids):
            if evolution.directions and (evolution.directions.count('\n') > 0 or len(evolution.directions) > 58):
                return False
        return True
    
    _constraints = [#(_evolution_constraint_evl_info, _("El campo EVOLUCION no puede contener mas de 1 linea ni más de 29 caracteres."), []),
                    #(_evolution_constraint_directions, _("El campo TRATAMIENTO no puede contener mas de 1 linea ni más de 29 caracteres por linea."), []),
                   ]
    
OeMedicalPatientEvolution()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
