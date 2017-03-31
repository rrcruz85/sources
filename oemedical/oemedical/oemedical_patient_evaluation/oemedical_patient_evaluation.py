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
from openerp.osv.fields import boolean

class OeMedicalPatientEvaluation(osv.Model):
    _name='oemedical.patient.evaluation'
#    _rec_name='identification_code'

    def _get_patient(self, cr, uid, context):
        run_pool = self.pool.get('oemedical.patient')
        run_data = {}
        if context and context.get('active_id', False):
            run_data = run_pool.read(cr, uid, context['active_id'], ['patient_id'])
            patient_id = run_data.get('id', False)
            if patient_id:
                return patient_id
        return False
    
    def button_print_official_report(self, cr, uid, ids, context=None):
        return {
            'type'        : 'ir.actions.report.xml',
            'res_model'   : 'oemedical.patient.evaluation',
            'report_name' : 'oemedical_patient_evaluation_report',
            'report_type' : 'pdf',
        }
    
    _columns={
              'patient_id':fields.many2one('oemedical.patient', 'Patient', required=True),
              'information_source': fields.char(size=256, string='Source',
                                                help="Source of" "Information, eg : Self, relative, friend ..."),
              'tem_info': fields.float('Temperatura', digits=(12,3)),
              'pat_info': fields.char(size=256, string='Presión arterial'),
              'ppm_info': fields.integer('Frecuencia cardiaca'),
              'est_info': fields.float('Estatura del paciente (cm)', digits=(12,3)),
              'pes_info': fields.float('Peso del paciente (Kg)', digits=(12,3)),
              'fqr_info': fields.char(string='Frecuencia respiratoria', size=256),
              'info_diagnosis': fields.text(string='Enfermedad Actual'),
              'evaluation_type': fields.selection([
                                                   ('a', 'Ambulatory'),
                                                   ('e', 'Emergency'),
                                                   ('i', 'Inpatient'),
                                                   ('pa', 'Pre-arranged appointment'),
                                                   ('pc', 'Periodic control'),
                                                   ('p', 'Phone call'),
                                                   ('t', 'Telemedicine'),
                                                   ], string='Type'),
              'actions': fields.one2many('oemedical.directions',
                                         'evaluation_id', string='Procedures',
                                         help='Procedures / Actions to take'),
              'present_illness': fields.text(string='Present Illness'),
              'evaluation_date': fields.date(string='Date',
                                                 help='Enter or select the date / ID of the appointment related to'\
                                                 ' this evaluation',
                                                 readonly=True, size=256),
              'user_id': fields.many2one('res.users', string='Last Changed by',
                                         readonly=True),
              'doctor': fields.many2one('oemedical.physician', string='Doctor'),
              'next_evaluation': fields.many2one('oemedical.appointment',
                                                 string='Next Appointment',),
              'specialty': fields.many2one('oemedical.specialty',
                                           string='Specialty',),
              'derived_to': fields.many2one('oemedical.specialty',
                                            string='Interconsulta Hacia ',
                                            help='Physician to whom escalate / derive the case'),
              
              'diagnosis': fields.many2many('oemedical.pathology', 'oemedical_evaluation_diagnosis_rel', 'evaluation_id', 'diagnosis_id', 'Presumptive diagnosis'),
              'definitive_diagnosis': fields.many2many('oemedical.pathology', 'oemedical_evaluation_definitivediagnosis_rel', 'evaluation_id', 'definitivediagnosis_id', 'Definitive diagnosis'),
              
              'notes_complaint': fields.text(string='Complaint details'),
              'mdc_info': fields.char(size=256, string='Motivo de Consulta'),
              'eac_info': fields.text(string='Enfermedad actual'),
              'ena_info': fields.text(string='Examen Físico'),
              'revision_organos':fields.text(string='Revisión de Organos y Sistemas'),
              'rxl_complaint': fields.text(string='Laboratorio y Rayos X'),
              'osat': fields.integer(string='Oxygen Saturation',
                                     help='Oxygen Saturation(arterial).'),
              'evl_info': fields.text(string='Evolución'),
              'dag_info': fields.text(string='Diagnostico'),
              'trt_info': fields.text(string='Tratamiento seguido'),
              'directions': fields.text(string='Tratamiento'),
              
              'org_scp': fields.boolean(string='Organos de los Sentidos / CP'),
              'org_ssp': fields.boolean(string='Organos de los Sentidos / SP'),
              'res_cp': fields.boolean(string='Respiratorio / CP'),
              'res_sp': fields.boolean(string='Respiratorio / SP'),
              'car_vcp': fields.boolean(string='Cardio Vascular / CP'),
              'car_vsp': fields.boolean(string='Cardio Vascular / SP'),
              'dig_cp': fields.boolean(string='Digestivo / CP'),
              'dig_sp': fields.boolean(string='Digestivo / SP'),
              'gen_cp': fields.boolean(string='Genital / CP'),
              'gen_sp': fields.boolean(string='Genital / SP'),
              'uri_cp': fields.boolean(string='Urinario / CP'),
              'uri_sp': fields.boolean(string='Urinario / SP'),
              'mus_ecp': fields.boolean(string='Musculo Esquelético / CP'),
              'mus_esp': fields.boolean(string='Musculo Esquelético / SP'),
              'end_cp': fields.boolean(string='Endócrino / CP'),
              'end_sp': fields.boolean(string='Endócrino / SP'),
              'hmo_lcp': fields.boolean(string='Hemo Linfático / CP'),
              'hmo_lsp': fields.boolean(string='Hemo Linfático / SP'),
              'nrv_cp': fields.boolean(string='Nervioso / CP'),
              'nrv_sp': fields.boolean(string='Nervioso / SP'),
              'des_eva': fields.text(string='Descripción'),
              'cab_cp': fields.boolean(string='Cabeza / CP'),
              'cab_sp': fields.boolean(string='Cabeza / SP'),
              'cue_cp': fields.boolean(string='Cuello / CP'),
              'cue_sp': fields.boolean(string='Cuello / SP'),
              'trx_vcp': fields.boolean(string='Torax / CP'),
              'trx_vsp': fields.boolean(string='Torax / SP'),
              'abd_cp': fields.boolean(string='Abdomen / CP'),
              'abd_sp': fields.boolean(string='Abdomen / SP'),
              'pel_cp': fields.boolean(string='Pelvis / CP'),
              'pel_sp': fields.boolean(string='Pelvis / SP'),
              'ext_cp': fields.boolean(string='Extremidades / CP'),
              'ext_sp': fields.boolean(string='Extremidades / SP'),
              'des_erg': fields.text(string='Descripción'),
              
              'evolution_ids': fields.one2many('oemedical.patient.evolution',
                                         'evaluation_id', string='Evoluciones',),
              }
    
    _defaults = {
              'evaluation_date': time.strftime('%Y-%m-%d'),
              'patient_id': _get_patient,
              }
    
    def _diagnosis_constraint(self, cr, uid, ids):
        for evaluation in self.browse(cr, uid, ids):
            if len(evaluation.diagnosis) + len(evaluation.definitive_diagnosis) > 4: return False
            return True
    
    def _diagnosis_constraint_mdc_info(self, cr, uid, ids):
        for evaluation in self.browse(cr, uid, ids):
            if evaluation.mdc_info and (evaluation.mdc_info.count('\n') > 0 or len(evaluation.mdc_info) > 116):
                return False
        return True
    
    def _diagnosis_constraint_eac_info(self, cr, uid, ids):
        for evaluation in self.browse(cr, uid, ids):
            if evaluation.eac_info:
                strs = evaluation.eac_info.split('\n')
                if len(strs) > 7:
                    return False
                if len(strs) >= 1:
                    for s in strs:
                        if len(s) > 116:
                            return False
                else:
                    if len(strs) > 116:
                        return False                
        return True
    
    def _diagnosis_constraint_directions(self, cr, uid, ids):
        for evaluation in self.browse(cr, uid, ids):
            if evaluation.directions:
                strs = evaluation.directions.split('\n')
                if len(strs) > 6:
                    return False
                if len(strs) >= 1:
                    for s in strs:
                        if len(s) > 116:
                            return False
                else:
                    if len(strs) > 116:
                        return False                
        return True
    
    _constraints = [(_diagnosis_constraint, _('You can not specified more than four diagnosis!'), ['diagnosis', 'definitive_diagnosis']),
                    #(_diagnosis_constraint_mdc_info, _("El campo MOTIVO DE CONSULTA no puede contener saltos de linea ni mas de 116 caracteres."), []),
                    #(_diagnosis_constraint_eac_info, _("El campo ENFERMEDAD O PROBLEMA ACTUAL no puede contener mas de 7 lineas ni mas de 116 caracteres por linea."), []),
                    #(_diagnosis_constraint_directions, _("El campo TRATAMIENTO no puede contener mas de 6 lineas ni mas de 116 caracteres por linea."), []),
                    ]

OeMedicalPatientEvaluation()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
