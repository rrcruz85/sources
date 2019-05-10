# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from dateutil.relativedelta import relativedelta
from datetime import datetime
import re
from ..oemedical_patient import oemedical_patient

class OeMedicalPhysician(osv.Model):
    _name = 'oemedical.physician'

    _inherits={
        'res.partner': 'physician_id'
    }

    def _get_primary_specialty(self, cr, uid, ids, name, args, context=None):
        res = {}
        for specialty in self.browse(cr, uid, ids, context=context):
            res[specialty.id] = {
                'specialty_id': False,
                'specialty_year_experience': 0
            }             
            for l in specialty.specialty_ids:
                if l.is_primary:
                    res[specialty.id]['specialty_id'] =  l.specialty_id.id
                    date_end = datetime.strptime(str(l.date_end), '%Y-%m-%d')
                    delta = relativedelta(datetime.now(), date_end)
                    res[specialty.id]['specialty_year_experience'] = delta.years
        return res 

    def _get_age(self, cr, uid, ids, field_name, arg, context=None):
        res = {}         
        now = datetime.now()
        for record in self.browse(cr, uid, ids, context=context):
            if (record.dob):
                dob = datetime.strptime(str(record.dob), '%Y-%m-%d')
                delta = relativedelta(now, dob)
                years_months_days = delta.years
            else:
                years_months_days = 0
            res[record.id] = years_months_days
        return res    

    def _get_specialty_ids(self, cr, uid, ids, context=None):
        result = set()
        for line in self.pool.get('oemedical.physician.specialty').browse(cr, uid, ids, context=context):
            result.add(line.physician_id.id)
        return list(result)

    _columns = {
        'physician_id': fields.many2one('res.partner', string='Health Professional',required=True , help='Physician', 
            ondelete='cascade', domain=[('is_doctor', '=', True)]),
        'first_name': fields.char(size=256, string='First Name', required=True),
        'last_name': fields.char(size=256, string='Last Name', required=True),
        'slastname': fields.char(size=256, string='Second LastName', required=True),       
        'specialty_ids': fields.one2many('oemedical.physician.specialty', 'physician_id', string='Specialties'),
        'nationality_id': fields.many2one('res.country', string='Nationality'),
        'specialty_id': fields.function(_get_primary_specialty,  type='many2one', relation="oemedical.specialty", string='Specialty', multi="specialty",
                store={
                        'oemedical.physician': (lambda self, cr, uid, ids, c={}: ids, ['specialty_ids'], 10),
                        'oemedical.physician.specialty': (_get_specialty_ids, ['is_primary'], 10),
                }),
        'specialty_year_experience': fields.function(_get_primary_specialty, type='integer', string='Specialty Years of Experience', multi="specialty",
            store={
                        'oemedical.physician': (lambda self, cr, uid, ids, c={}: ids, ['specialty_ids'], 10),
                        'oemedical.physician.specialty': (_get_specialty_ids, ['is_primary', 'date_start', 'date_end'], 10),
                }),
        'info': fields.text(string='Extra info'),

        'ced_ruc': fields.char('Nro. Identificación', size=15, help='Formatos correctos:\nCédula: 10 dígitos\nRuc: 13 dígitos (debe terminar en 001)\nPasaporte: Sólo letras o dígitos'),
        'tipo_persona': fields.char('Tipo Persona', size=15),
        'type_ced_ruc': fields.selection([('ruc', 'Ruc'), ('cedula', 'Cédula'), ('pasaporte', 'Pasaporte')],
            string='Tipo identificación', select=True, readonly=False),
        'sex': fields.selection([('m', 'Male'), ('f', 'Female'), ], string='Gender', required=True),
        'dob': fields.date(string='BirthDate'),
        'age': fields.function(_get_age, type='integer', string='Age', 
            store={
                'oemedical.physician': (lambda self, cr, uid, ids, c={}: ids, ['dob'], 10),                         
            }),
        'is_currently_working': fields.boolean(string='Is Currently Working'),
        'work_institution_id': fields.many2one('res.partner', string='Work Institution', domain=['|',('is_institution', '=', True),('is_work', '=', True)], help='Institution where she/he works' ),
        'work_since_date': fields.date(string='Work Date'),

        'graduated_institution_id': fields.many2one('res.partner', string='Graduated Institution', domain=['|',('is_institution', '=', True), ('is_school', '=', True)], help='Institution where she/he gratuated' ),
        'graduated_title': fields.char(string='Graduated Title', size = 256),
        'graduated_date': fields.date(string='Graduated Date'),
        'academic_degree_id': fields.many2one('res.partner.category', string='Academic Degree'),
        
        'doctor_id': fields.char(string='Medical Record Id', size = 32, help="The id of the doctor registered in the MS, Cenescyt or Equivalent"),
        'registered_institution_id': fields.many2one('res.partner', string='Registered Institution', domain=['|',('is_institution', '=', True), ('is_school', '=', True)], help='Institution where she/he registered her/his title as a doctor' ),
        'registered_date': fields.date(string='Registration Date', help="Date on which the doctor was registered"),
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
        'tipo_persona': '6',
        'type_ced_ruc': 'cedula',        
        'city'        : 'Quito',
        'country_id'  : _get_default_country,
        'state_id'    : _get_default_state
    }

    def _check_ced_ruc(self, cr, uid, ids, context=None):
        partners = self.browse(cr, uid, ids)
        for partner in partners:             
            if partner.type_ced_ruc == 'pasaporte':
                return re.match(r'^[a-zA-Z0-9]+$', partner.ced_ruc)
            if partner.ced_ruc == '9999999999999':
                return True             
            if partner.type_ced_ruc == 'ruc' and partner.tipo_persona == '9':
                return oemedical_patient._check_ruc(partner.ced_ruc, partner.property_account_position.name)
            else:
                if partner.ced_ruc[:2] == '51':
                    return True
                else:
                    return oemedical_patient._check_cedula(partner.ced_ruc)
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

    def _check_phone_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.phone and not re.match(r'^[0-9]{7,9}$', obj.phone):
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
        (_check_ced_ruc, 'El número de cédula, ruc o pasaporte esta incorrecto', ['ced_ruc']),
        (_check_full_name, 'El nombre esta incorrecto', ['first_name']),
        (_check_last_name, 'El primer apellido esta incorrecto', ['last_name']),
        (_check_slast_name, 'El segundo apellido esta incorrecto', ['slastname']),
        (_check_mobile_number, 'El número móvil esta incorrecto', ['mobile']),
        (_check_phone_number, 'El número de teléfono esta incorrecto', ['phone']),
        (_check_email, 'El correo electrónico esta incorrecto', ['email']),
        (_check_age, 'La edad del paciente no puede ser cero', ['age']),
    ]    

    def onchange_name(self, cr, uid, ids, first_name, last_name, slastname, context=None):
        if first_name == False:
            first_name = ''
        if last_name == False:
            last_name = ''
        if slastname == False:
            slastname = ''
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

    def create(self, cr, uid, vals, context=None):             
        vals['is_doctor'] = True
        vals['is_company'] = False
        return super(OeMedicalPhysician, self).create(cr, uid, vals, context=context)
    
    def unlink(self, cr, uid, ids, context=None):
        partners = [r.physician_id.id for r in self.browse(cr,uid, ids)]
        self.pool.get('res.partner').write(cr, uid, partners, {'active': False});
        result = super(OeMedicalPhysician, self).unlink(cr, uid, ids, context=context)  

OeMedicalPhysician()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
