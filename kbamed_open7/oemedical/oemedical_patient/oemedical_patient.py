# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields
from dateutil.relativedelta import relativedelta
from datetime import datetime
import re

class OeMedicalPatient(osv.osv):

    _inherits = {
        'res.partner': 'partner_id',
    }

    _name = 'oemedical.patient'

    def _current_user_is_patient(self, cr, uid, ids, field_name, arg, context=None):
        return {}.fromkeys(ids, self.pool.get('res.users').has_group(cr, uid, 'oemedical.patient_group'))

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Related Partner', required=True, domain=[('is_doctor', '=', True)],
                                      ondelete='cascade', help='Partner-related data of the patient'),
        'blood_type': fields.selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O'), ], string='Blood Type'),
        'rh': fields.selection([('+', '+'), ('-', '-')], string='Rh'),
        'general_info': fields.text(string='General Information', help='General information about the patient'),
        'primary_care_doctor': fields.many2one('oemedical.physician', 'Primary Care Doctor', help='Current primary care / family doctor'),
        'childbearing_age': fields.boolean('Potential for Childbearing'),        
        'evaluations': fields.one2many('oemedical.patient.evaluation', 'patient_id', string='Evaluations'),        
        'critical_info': fields.text(string='Important disease, allergy or procedures information',
                                     help='Write any important information on the patient\'s disease, surgeries, allergies, ...'),
        'app_info': fields.text(string='Antecedentes Patológicos Personales',
                                help='Enfermedades y padecimientos que haya tenido el paciente, ...'),
        'cardiopatia': fields.boolean(string='Cardiopatía'),
        'diabetes': fields.boolean(string='Diabetes'),
        'enf_car': fields.boolean(string='Enfermedad Cardiovascular'),
        'hipertension': fields.boolean(string='Hipertensión'),
        'cancer': fields.boolean(string='Cancer'),
        'tuberculosis': fields.boolean(string='Tuberculosis'),
        'enf_men': fields.boolean(string='Enfermedad Mental'),
        'enf_inf': fields.boolean(string='Enfermedad Infecciosa'),
        'mal_for': fields.boolean(string='Mal Formación'),
        'antibotic_allergic' : fields.boolean(string='Alergia a antibioticos'),
        'anesthesia_allergic' : fields.boolean(string='Alergia a anestesia'),
        'hemorrhage' : fields.boolean(string='Hemorragia'),
        'vih_sida' : fields.boolean(string='VIH/SIDA'),        
        'asma' : fields.boolean(string='Asma'),
        'other': fields.boolean(string='Otra'),
        'others_antecedents': fields.text(string='Descripción de otros antescedentes'),
 
        'apf_info': fields.text(string='Antecedentes Patológicos Familiares'),
        'diseases': fields.one2many('oemedical.patient.disease', 'patient_id', string='Diseases',
                                    help='Mark if the patient has died'),        
        'vaccinations': fields.one2many('oemedical.vaccination', 'patient_id', 'Vaccinations'),
        'marital_status': fields.selection([('s', 'Single'), ('m', 'Married'),('w', 'Widowed'),('d', 'Divorced'),
                                            ('x', 'Separated'),('z', 'law marriage')], string='Marital Status', sort=False),
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
        'referido_por': fields.many2one('res.partner', string='Refererido Por'),        
        'membresia': fields.selection([('a', 'Anual'), ('s', 'Semestral'), ('t', 'Trimestral'), ('m', 'Mensual')],
                                      'Tipo de membresia :'),
        'fec_ime': fields.date(string='Fecha de inicio de membresia :'),
        'fec_fme': fields.date(string='Fecha de finalización de membresía :'),
        'loc_nac': fields.char(string='Lugar de Nacimiento :', size=70),
        
        # Emergency contact
        'emergency_person': fields.char('Full Names', size=200),
        'emergency_phone': fields.char('Phone', size=64),
        'emergency_mobile': fields.char('Mobile', size=200),

        'nationality_id': fields.many2one('res.country', string='Nationality'),
        'current_user_is_patient': fields.function(_current_user_is_patient, type='boolean', string='Current User Is Patient'),
    }

    _defaults = {
        'ref': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'),
    }

    def _check_mobile_contact_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.emergency_mobile and not re.match(r'^[0-9]{9,10}$', obj.emergency_mobile):
                return False
        return True

    def _check_contact_phone_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.emergency_phone and not re.match(r'^[0-9]{7,9}$', obj.emergency_phone):
                return False
        return True

    def _check_age(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):            
            birthdate = datetime.strptime(str(obj.birthdate), '%Y-%m-%d')
            delta = relativedelta(datetime.now(), birthdate)
            if delta.years == 0 and delta.months == 0:
                return False
        return True
    
    def _check_emergency_fullname(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.emergency_person and not re.match(r'^[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]+\D*([a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]\D*)*$', obj.emergency_person):
                return False
        return True

    _constraints = [
        (_check_mobile_contact_number, 'El número móvil de la persona de contacto esta incorrecto', ['emergency_mobile']),
        (_check_contact_phone_number, 'El número de teléfono de la persona de contacto esta incorrecto', ['emergency_phone']),
        (_check_age, 'La edad del paciente no puede ser cero', ['age']),
        (_check_emergency_fullname, 'Los nombres y apellidos de la persona de contacto estan incorrectos', ['emergency_person'])
    ]

    def onchange_name(self, cr, uid, ids, first_name, last_name, slastname, context=None):
        if first_name == False:
            first_name = ''
        if last_name == False:
            last_name = ''
        if slastname == False:
            slastname = ''
        res = {
            'value': {
                'name': first_name + ' ' + last_name + ' ' + slastname
            }
        }
        return res

    def onchange_dob(self, cr, uid, ids, birthdate, context=None):
        res = {}
        if birthdate:
            delta = relativedelta(datetime.now(), datetime.strptime(str(birthdate), '%Y-%m-%d'))
            res['value'] = {
                'age': delta.years
            }
        return res

    def create(self, cr, uid, vals, context=None):
        vals['is_patient'] = True
        vals['is_person'] = True
        vals['is_company'] = False   
        return super(OeMedicalPatient, self).create(cr, uid, vals, context=context)        
    
    def unlink(self, cr, uid, ids, context=None):
        partners = [r.partner_id.id for r in self.browse(cr,uid, ids)]
        self.pool.get('res.partner').write(cr, uid, partners, {'active': False})
        return super(OeMedicalPatient, self).unlink(cr, uid, ids, context=context)

OeMedicalPatient()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
