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
from osv import osv
from osv import fields
from dateutil.relativedelta import relativedelta
from datetime import datetime


class OeMedicalPatient(osv.osv):
    _inherits={
        'res.partner': 'partner_id',
    }

    _name='oemedical.patient'
    
    def onchange_name(self, cr, uid, ids, first_name, last_name, slastname, context=None):
        if first_name == False:
            first_name = ''
        if last_name == False:
            last_name = ''
        if slastname == False:
            slastname = ''
        
        #warning = {
        #    'title': 'Test',
        #    'message': 'Notification Message',
        #}    
        
        res = {
            'value':{
                'name' : first_name + ' ' + last_name + ' ' + slastname
            }             
        }
        return res
    
    def _get_age(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        age = 0
        now = datetime.now()
        for record in self.browse(cr, uid, ids, context=context):
            if (record.dob):
                dob = datetime.strptime(str(record.dob), '%Y-%m-%d')
                if record.deceased:
                    dod = datetime.strptime(record.dod, '%Y-%m-%d %H:%M:%S')
                    delta = relativedelta(dod, dob)
                    deceased = ' (deceased)'
                else:
                    delta = relativedelta(now, dob)
                    deceased = ''
                years_months_days = delta.years # + 'y ' \ + str(delta.months) + 'm ' \ + str(delta.days) + 'd' + deceased
            else:
                years_months_days = 0
                
            # Return the age in format y m d when the caller is the field name
            if field_name == 'age':
                age = years_months_days
            
            res[record.id] = age
        return res
    
    def get_imc1(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.epa_pac / (r.epa_tal * r.epa_tal)
           print "IMC", res
        return res

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Related Partner', required=True,
                                      ondelete='cascade', help='Partner-related data of the patient'),
        'first_name': fields.char(size=256, string='Name', required=True),
        'last_name': fields.char(size=256, string='Lastname', required=True),
        'slastname': fields.char(size=256, string='Second Lastname'),       
        'photo': fields.binary(string='Picture'),
        'sex': fields.selection([('m', 'Male'), ('f', 'Female'), ], string='Gender', required=True),
        'blood_type': fields.selection([
            ('A', 'A'),
            ('B', 'B'),
            ('AB', 'AB'),
            ('O', 'O'), ], string='Blood Type'),
        'rh': fields.selection([
            ('+', '+'),
            ('-', '-'), ], string='Rh'),
        'general_info': fields.text(string='General Information', help='General information about the patient'),
        'primary_care_doctor': fields.many2one('oemedical.physician', 'Primary Care Doctor',
                                               help='Current primary care / family doctor'),
        'childbearing_age': fields.boolean('Potential for Childbearing'),        
        'evaluations': fields.one2many('oemedical.patient.evaluation', 'patient_id', string='Evaluations', ),        
        'critical_info': fields.text(string='Important disease, allergy or procedures information',
                                     help='Write any important information on the patient\'s disease, surgeries, allergies, ...'),
        'app_info': fields.text(string='Antecedentes Patológicos Personales',
                                help='Enfermedades y padecimientos que haya tenido el paciente, ...'),
        'cardiopatia': fields.boolean(string='1. Cardiopatía'),
        'diabetes': fields.boolean(string='2. Diabetes'),
        'enf_car': fields.boolean(string='3. Enfermedad Cardiovascular'),
        'hipertension': fields.boolean(string='4. Hipertensión'),
        'cancer': fields.boolean(string='5. Cancer'),
        'tuberculosis': fields.boolean(string='6. Tuberculosis'),
        'enf_men': fields.boolean(string='7. Enfermedad Mental'),
        'enf_inf': fields.boolean(string='8. Enfermedad Infecciosa'),
        'mal_for': fields.boolean(string='9. Mal Formación'),
        'otra': fields.boolean(string='10. Otra'),
        'otr_des': fields.text(string='Descripción de otros antescedentes'),
        'apf_info': fields.text(string='Antecedentes Patológicos Familiares'),
        'diseases': fields.one2many('oemedical.patient.disease', 'patient_id', string='Diseases',
                                    help='Mark if the patient has died'),        
        'vaccinations': fields.one2many('oemedical.vaccination', 'patient_id', 'Vaccinations', ),
        'dob': fields.date(string='BirthDate'),
        'age': fields.function(_get_age, type='integer', string='Age'),
        'marital_status': fields.selection([('s', 'Single'), ('m', 'Married'),
                                            ('w', 'Widowed'),
                                            ('d', 'Divorced'),
                                            ('x', 'Separated'),
                                            ('z', 'law marriage'), ],
                                           string='Marital Status', sort=False),
        'dod': fields.datetime(string='Date of Death'),
        'current_insurance': fields.char(string='Aseguradora', size=256,
                                         help='Insurance information. You may choose from the different insurances belonging to the patient'),
        'corredor_seguros': fields.char(string='Corredor de Seguros', size=256),
        'cmp_pac': fields.char(string='Compañía', size=256),
        'cod': fields.many2one('oemedical.pathology', string='Cause of Death', ),
        'identification_code': fields.char(size=256, string='ID',
                                           help='Patient Identifier provided by the Health Center'),
        'deceased': fields.boolean(string='Deceased'),
        'occupation': fields.many2one('oemedical.occupation', string='Occupation'),
        'aqu_info': fields.text(string='Antecedentes Quirúrgicos'),
        'tipo': fields.selection([('a', 'A'), ('b', 'B'), ('c', 'C')], 'Tipo'),
        'referido_por': fields.char(string='Médico referente', size=60),
        'membresia': fields.selection([('a', 'Anual'), ('s', 'Semestral'), ('t', 'Trimestral'), ('m', 'Mensual')],
                                      'Tipo de membresia :'),
        'fec_ime': fields.date(string='Fecha de inicio de membresia :'),
        'fec_fme': fields.date(string='Fecha de finalización de membresía :'),
        'loc_nac': fields.char(string='Lugar de Nacimiento :', size=70),
        
        # Información de contacto
        'contacto': fields.char('Persona de contacto', size=200),
        'telefono': fields.char('Telefono familiar / Contacto', size=64),
        'celular': fields.char('Celular familiar / Contacto', size=64),

        'ced_ruc': fields.char('No. Identificacion', size=15, required=False, readonly=False),
        'tipo_persona': fields.char('Tipo Persona', size=15, required=False, readonly=False),
        'type_ced_ruc': fields.selection(
            [('ruc', 'Ruc'), ('cedula', 'Cedula'), ('pasaporte', 'Pasaporte')],
            string='Tipo identificacion', select=True, readonly=False),
    }

    _defaults = {
        'ref': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'),
        'tipo_persona': '6',
        'type_ced_ruc': 'cedula',
        'is_patient' : True,
    }
    
    def create(self, cr, uid, vals, context=None):
        #sequence = unicode (self.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'))
        #vals['identification_code'] = sequence
        return super(OeMedicalPatient, self).create(cr, uid, vals, context=context)
    
OeMedicalPatient()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
