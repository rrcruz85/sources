# -*- coding: utf-8 -*-
from osv import osv
from osv import fields

class ResPartner(osv.Model):
    _inherit = 'res.partner'
    
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
        'type_ced_ruc': fields.selection(
            [('ruc', 'Ruc'), ('cedula', 'Cédula'), ('pasaporte', 'Pasaporte')],
            string='Tipo identificación', select=True, readonly=False),
    }

    def _get_default_tipo_persona(self, cr, uid, context=None):
        return '6' if context and 'default_is_person' in context and context['default_is_person'] else '9'


    _defaults = {
        'tipo_persona':  _get_default_tipo_persona,
        'type_ced_ruc': 'cedula'
    }

ResPartner()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
