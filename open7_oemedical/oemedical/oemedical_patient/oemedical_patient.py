# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from dateutil.relativedelta import relativedelta
from datetime import datetime
import re

def _check_cedula(identificador):
    try:
        ident=int(identificador)
    except ValueError:
        raise osv.except_osv(('Aviso !'), 'La cedula no puede contener caracteres')

    if len(identificador) == 13 and not identificador[10:13] == '001':
        return False
    elif len(identificador) < 10:
        return False
    
    coef = [2,1,2,1,2,1,2,1,2]
    cedula = identificador[:9]
    suma = 0
    for c in cedula:
        val = int(c) * coef.pop()
        suma += val > 9 and val-9 or val
    result = 10 - ((suma % 10)!=0 and suma%10 or 10)
    if result == int(identificador[9:10]):
        return True
    else:
        return False
 
def _check_ruc(ced_ruc, position):
    ruc = ced_ruc
    if not len(ruc) == 13:
        return False
    if position == 'SECTOR PUBLICO':
        coef = [3,2,7,6,5,4,3,2,0,0]
        coef.reverse()
        verificador = int(ruc[8:9])
    else:
        if int(ruc[2:3]) < 6:
            return _check_cedula(ced_ruc) 
        if ruc[2:3] == '9':
            coef = [4,3,2,7,6,5,4,3,2,0]
            coef.reverse()
            verificador = int(ruc[9:10])
        elif ruc[2:3] == '6':
            coef = [3,2,7,6,5,4,3,2,0,0]
            coef.reverse()
            verificador = int(ruc[9:10])
        else:
            raise osv.except_osv('Error', 'Cambie el tipo de persona')
    suma = 0
    for c in ruc[:10]:
        suma += int(c) * coef.pop()
        result = 11 - (suma>0 and suma % 11 or 11)
    if result == verificador:
        return True
    else:
        return False
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
    
    def onchange_dob(self, cr, uid, ids, dob, context=None):
        res = {}
        age = 0
        if dob:
            delta = relativedelta(datetime.now(), datetime.strptime(str(dob), '%Y-%m-%d'))
            res['value'] = {
                'age' : delta.years
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
    
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Related Partner', required=True,
                                      ondelete='cascade', help='Partner-related data of the patient'),
        'first_name': fields.char(size=256, string='Name', required=True),
        'last_name': fields.char(size=256, string='Last Name', required=True),
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
        'telefono': fields.char('Teléfono familiar / Contacto', size=64),
        'celular': fields.char('Celular familiar / Contacto', size=64),

        'ced_ruc': fields.char('Nro. Identificación', size=15, required=False, readonly=False),
        'tipo_persona': fields.char('Tipo Persona', size=15, required=False, readonly=False),
        'type_ced_ruc': fields.selection(
            [('ruc', 'Ruc'), ('cedula', 'Cédula'), ('pasaporte', 'Pasaporte')],
            string='Tipo identificación', select=True, readonly=False),
    }

    def _get_default_country(self, cr, uid, context=None):
        result = self.pool.get('res.country').search(cr, uid, [('code', '=', 'EC')])
        return result and result[0] or False
    
    def _get_default_state(self, cr, uid, context=None):
        result = self.pool.get('res.country').search(cr, uid, [('code', '=', 'EC')])
        if result and result[0]:
             res = self.pool.get('res.country.state').search(cr, uid, [('country_id', '=', result[0]),('code', '=', 'PIC')])
             return res and res[0] or False
        return False

    _defaults = {
        'ref': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'),
        'tipo_persona': '6',
        'type_ced_ruc': 'cedula',
        'is_patient'  : True,
        'city'        : 'Quito',
        'country_id'  : _get_default_country,
        'state_id'    : _get_default_state
    }

    def _check_ced_ruc(self, cr, uid, ids, context=None):
        partners = self.browse(cr, uid, ids)
        for partner in partners:             
            if partner.type_ced_ruc == 'pasaporte':
                return True
            if partner.ced_ruc == '9999999999999':
                return True             
            if partner.type_ced_ruc == 'ruc' and partner.tipo_persona == '9':
                return _check_ruc(partner.ced_ruc, partner.property_account_position.name)
            else:
                if partner.ced_ruc[:2] == '51':
                    return True
                else:
                    return _check_cedula(partner.ced_ruc)
        return True

    def _check_full_name(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if not re.match(r'^[a-zA-Z]+\D*[a-zA-Z]*$', obj.first_name):
                return False
        return True

    def _check_last_name(self, cr, uid, ids, context=None):    
        for obj in self.browse(cr, uid, ids, context=context):
            if not re.match(r'^[a-zA-Z]+$', obj.last_name):
                return False
        return True

    def _check_slast_name(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if not re.match(r'^[a-zA-Z]+$', obj.slastname):
                return False
        return True
    
    def _check_mobile_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if not re.match(r'^[0-9]{9,10}$', obj.mobile):
                return False
        return True

    def _check_mobile_contact_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.celular and not re.match(r'^[0-9]{9,10}$', obj.celular):
                return False
        return True

    def _check_phone_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.phone and not re.match(r'^[0-9]{7,9}$', obj.phone):
                return False
        return True
    
    def _check_contact_phone_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.telefono and not re.match(r'^[0-9]{7,9}$', obj.telefono):
                return False
        return True
    
    def _check_email(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', obj.email):
                return False
        return True

    def _check_age(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):            
            dob = datetime.strptime(str(obj.dob), '%Y-%m-%d')
            delta = relativedelta(datetime.now(), dob)
            if delta.years == 0 and delta.months == 0:
                return False
        return True
    
    _constraints = [
        (_check_ced_ruc, 'La cédula o el ruc esta incorrecto', ['ced_ruc']),
        (_check_full_name, 'El nombre esta incorrecto', ['first_name']),
        (_check_last_name, 'El primer apellido esta incorrecto', ['last_name']),
        (_check_slast_name, 'El segundo apellido esta incorrecto', ['slastname']),
        (_check_mobile_number, 'El número móvil esta incorrecto', ['mobile']),
        (_check_mobile_contact_number, 'El número móvil de la persona de contacto esta incorrecto', ['celular']),
        (_check_phone_number, 'El número de teléfono esta incorrecto', ['phone']),
        (_check_contact_phone_number, 'El número de teléfono de la persona de contacto esta incorrecto', ['telefono']),
        (_check_email, 'El correo electrónico esta incorrecto', ['email']),
        (_check_age, 'La edad del paciente no puede ser cero', ['age'])
    ]
    
    def create(self, cr, uid, vals, context=None):
        #sequence = unicode (self.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'))
        #vals['identification_code'] = sequence
        return super(OeMedicalPatient, self).create(cr, uid, vals, context=context)
    
OeMedicalPatient()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
