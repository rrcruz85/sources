# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
import re
from dateutil.relativedelta import relativedelta
from datetime import datetime

def _check_cedula(identificador, cedula):
    try:
        ident=int(identificador)
    except ValueError:
        raise osv.except_osv(('Aviso !'), 'La cedula no puede contener caracteres')

    if cedula and len(identificador) != 10:
        return False

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
    result = 10 - ((suma % 10) != 0 and suma%10 or 10)
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
            return _check_cedula(ced_ruc, False)
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

class ResPartner(osv.Model):
    _inherit = 'res.partner'

    def _get_age(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        age = 0
        now = datetime.now()
        for record in self.browse(cr, uid, ids, context=context):
            if (record.is_person or record.is_patient or record.is_doctor) and record.birthdate:
                birthdate = datetime.strptime(str(record.birthdate), '%Y-%m-%d')
                delta = relativedelta(now, birthdate)
                years_months_days = delta.years  # + 'y ' \ + str(delta.months) + 'm ' \ + str(delta.days) + 'd' + deceased
            else:
                years_months_days = 0

            # Return the age in format y m d when the caller is the field name
            if field_name == 'age':
                age = years_months_days

            res[record.id] = age
        return res
    
    _columns = {
        'relationship': fields.char(size=256, string='Relationship'),
        'insurance_company_type': fields.selection([('state', 'State'),
                                                    ('labour_union','Labour Union / Syndical'),
                                                    ('private', 'Private')], string='Insurance Type', select=True),        
        'relative_id': fields.many2one('res.partner', string='Contact'),       
        'alias': fields.char(size=256, string='Alias', help='Common name that the Party is reffered'),
        'internal_user': fields.many2one('res.users', string='Internal User',
                                         help='In GNU Health is the user (doctor, nurse) that logins.When the'
                                         ' party is a doctor or a health professional, it will be the user'
                                         ' that maps the doctor\'s party name. It must be present.'),
        'activation_date': fields.date(string='Activation date', help='Date of activation of the party'),

        'is_insurance_company': fields.boolean(string='Insurance Company', help='Check if the party is an Insurance Company'),
        'is_institution': fields.boolean(string='Institution', help='Check if the party is a Medical Center'),
        'is_doctor': fields.boolean(string='Health Prof', help='Check if the party is a health professional'),
        'is_patient': fields.boolean(string='Patient', help='Check if the party is a patient'),
        'is_work': fields.boolean(string='Work'),
        'is_person': fields.boolean(string='Person', help='Check if the party is a person.'),
        'is_school': fields.boolean(string='School'),
        'is_pharmacy': fields.boolean(string='Pharmacy', help='Check if the party is a Pharmacy'),

        'first_name': fields.char(size=256, string='Name', required=True),
        'last_name': fields.char(size=256, string='Last Name', required=True),
        'slastname': fields.char(size=256, string='Second Last Name'),
        'ced_ruc': fields.char('Nro. Identificación', size=15, help='Formatos correctos:\nCédula: 10 dígitos\nRuc: 13 dígitos (debe terminar en 001)\nPasaporte: Sólo letras o dígitos'),
        'tipo_persona': fields.char('Tipo Persona', size=15),
        'type_ced_ruc': fields.selection([('ruc', 'Ruc'), ('cedula', 'Cédula'), ('pasaporte', 'Pasaporte')],
            string='Tipo identificación', select=True, readonly=False),
        'mobile_operator': fields.selection([('claro', 'Claro'), ('cnt', 'CNT'), ('movistar', 'Movistar')],
            string='Operadora'),
        'sex': fields.selection([('m', 'Male'), ('f', 'Female'), ], string='Gender', required=True),
        'birthdate': fields.date(string='Birthdate'),
        'age': fields.function(_get_age, type='integer', string='Age',
                               store={
                                   'res.partner': (lambda self, cr, uid, ids, c={}: ids, ['birthdate'], 10),
                               }),
    }

    def _get_default_tipo_persona(self, cr, uid, context=None):
        return '6' if context and 'default_is_person' in context and context['default_is_person'] else '9'

    def _get_default_country(self, cr, uid, context=None):
        result = self.pool.get('res.country').search(cr, uid, [('code', '=', 'EC')])
        return result and result[0] or False

    def _get_default_state(self, cr, uid, context=None):
        result = self.pool.get('res.country').search(cr, uid, [('code', '=', 'EC')])
        if result and result[0]:
            res = self.pool.get('res.country.state').search(cr, uid,[('country_id', '=', result[0]), ('code', '=', 'PIC')])
            return res and res[0] or False
        return False

    _defaults = {
        'tipo_persona':  _get_default_tipo_persona,
        'type_ced_ruc': 'cedula',
        'mobile_operator': 'claro',
        'city': 'Quito',
        'country_id': _get_default_country,
        'state_id': _get_default_state,
        'tz': 'America/Guayaquil'
    }

    def _check_ced_ruc(self, cr, uid, ids, context=None):
        partners = self.browse(cr, uid, ids)
        for partner in partners: 
            if partner.is_doctor or partner.is_patient or partner.is_person:            
                if partner.type_ced_ruc == 'pasaporte':
                    return re.match(r'^[a-zA-Z0-9]+$', partner.ced_ruc)
                if partner.ced_ruc == '9999999999999':
                    return True             
                if partner.type_ced_ruc == 'ruc' and partner.tipo_persona == '9':
                    return _check_ruc(partner.ced_ruc, partner.property_account_position.name)
                else:
                    if partner.ced_ruc[:2] == '51':
                        return True
                    else:
                        return _check_cedula(partner.ced_ruc, partner.type_ced_ruc == 'cedula')
        return True

    def _check_first_name(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if (obj.is_doctor or obj.is_patient or obj.is_person) and obj.first_name and not re.match(r'^[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]+\D*[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]*$', obj.first_name):
                return False
        return True

    def _check_last_name(self, cr, uid, ids, context=None):    
        for obj in self.browse(cr, uid, ids, context=context):
            if (obj.is_doctor or obj.is_patient or obj.is_person) and obj.last_name and not re.match(r'^[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]+$', obj.last_name):
                return False
        return True

    def _check_slast_name(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if (obj.is_doctor or obj.is_patient or obj.is_person) and obj.slastname and not re.match(r'^[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]+$', obj.slastname):
                return False
        return True
    
    def _check_mobile_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.mobile and not re.match(r'^[0-9]{9,10}$', obj.mobile):
                return False
        return True

    def _check_phone_number(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.phone and not re.match(r'^[0-9]{7,9}$', obj.phone):
                return False
        return True

    def _check_email(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.email and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', obj.email):
                return False
        return True

    _constraints = [
        (_check_ced_ruc, 'El número de cédula, ruc o pasaporte esta incorrecto', ['ced_ruc']),
        (_check_first_name, 'El nombre esta incorrecto', ['first_name']),
        (_check_last_name, 'El primer apellido esta incorrecto', ['last_name']),
        (_check_slast_name, 'El segundo apellido esta incorrecto', ['slastname']),
        (_check_mobile_number, 'El número móvil esta incorrecto', ['mobile']),
        (_check_email, 'El correo electrónico esta incorrecto', ['email']),
   ]

ResPartner()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
