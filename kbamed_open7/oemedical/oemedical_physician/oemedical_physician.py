# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from dateutil.relativedelta import relativedelta
from datetime import datetime
 
class OeMedicalPhysician(osv.Model):
    _name = 'oemedical.physician'

    _inherits = {
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

    def _get_specialty_ids(self, cr, uid, ids, context=None):
        result = set()
        for line in self.pool.get('oemedical.physician.specialty').browse(cr, uid, ids, context=context):
            result.add(line.physician_id.id)
        return list(result)

    def _current_user_is_patient(self, cr, uid, ids, field_name, arg, context=None):
        return {}.fromkeys(ids, self.pool.get('res.users').has_group(cr, uid, 'oemedical.patient_group'))

    _columns = {
        'physician_id': fields.many2one('res.partner', string='Health Professional',required=True , help='Physician', 
            ondelete='cascade', domain=[('is_doctor', '=', True)]),               
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

        'is_currently_working': fields.boolean(string='Is Currently Working'),
        'work_institution_id': fields.many2one('res.partner', string='Work Institution', domain=['|',('is_institution', '=', True),('is_work', '=', True)], help='Institution where she/he works' ),
        'work_since_date': fields.date(string='Work Date'),

        'graduated_institution_id': fields.many2one('res.partner', string='Graduated Institution', domain=['|',('is_institution', '=', True), ('is_school', '=', True)], help='Institution where she/he gratuated' ),
        'graduated_title': fields.char(string='Graduated Title', size = 256),
        'graduated_date': fields.date(string='Graduated Date'),
        'academic_degree_id': fields.many2one('res.partner.category', string='Academic Degree'),
        
        'registered_institution_id': fields.many2one('res.partner', string='Registered Institution', domain=['|',('is_institution', '=', True), ('is_school', '=', True)], help='Institution where she/he registered her/his title as a doctor' ),
        'registered_date': fields.date(string='Registration Date', help="Date on which the doctor was registered"),
        'current_user_is_patient': fields.function(_current_user_is_patient, type='boolean', string='Current User Is Patient'),
    }

    def _check_age(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):            
            dob = datetime.strptime(str(obj.dob), '%Y-%m-%d')
            delta = relativedelta(datetime.now(), dob)
            if delta.years == 0 and delta.months == 0:
                return False
        return True

    _constraints = [        
        (_check_age, 'La edad del doctor no puede ser cero', ['age']),
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

    def onchange_dob(self, cr, uid, ids, dob, context=None):
        res = {}
        if dob:
            delta = relativedelta(datetime.now(), datetime.strptime(str(dob), '%Y-%m-%d'))
            res['value'] = {
                'age': delta.years
            }
        return res   

    def create(self, cr, uid, vals, context=None):             
        vals['is_doctor'] = True
        vals['is_person'] = True
        vals['is_patient'] = False
        vals['is_company'] = False
        return super(OeMedicalPhysician, self).create(cr, uid, vals, context=context)
    
    def unlink(self, cr, uid, ids, context=None):
        partners = [r.physician_id.id for r in self.browse(cr,uid, ids)]
        self.pool.get('res.partner').write(cr, uid, partners, {'active': False})
        return super(OeMedicalPhysician, self).unlink(cr, uid, ids, context=context)

OeMedicalPhysician()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
