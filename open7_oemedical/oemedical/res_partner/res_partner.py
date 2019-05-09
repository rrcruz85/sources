# -*- coding: utf-8 -*-
from osv import osv
from osv import fields

class ResPartner(osv.Model):
    _inherit = 'res.partner'
    
    _columns = {
                'is_insurance_company': fields.boolean(string='Insurance Company',
                                                       help='Check if the party is an Insurance Company'),
                'relationship': fields.char(size=256, string='Relationship'),
                'insurance_company_type': fields.selection([
                                                            ('state', 'State'),
                                                            ('labour_union', 'Labour Union / Syndical'),
                                                            ('private', 'Private'), ],
                                                           string='Insurance Type',select=True),
                'is_institution': fields.boolean(string='Institution', help='Check if the party is a Medical Center'),
                'relative_id': fields.many2one('res.partner', string='Contact', ),
                'is_doctor': fields.boolean(string='Health Prof', help='Check if the party is a health professional'),
                'is_patient': fields.boolean(string='Patient', help='Check if the party is a patient'),
                'alias': fields.char(size=256, string='Alias', help='Common name that the Party is reffered'),
                'internal_user': fields.many2one('res.users', string='Internal User',
                                                 help='In GNU Health is the user (doctor, nurse) that logins.When the'\
                                                 ' party is a doctor or a health professional, it will be the user'\
                                                 ' that maps the doctor\'s party name. It must be present.'),
                'activation_date': fields.date(string='Activation date', help='Date of activation of the party'),
                'lastname': fields.char(size=256, string='Last Name', help='Last Name'),
                'is_work': fields.boolean(string='Work'),
                'is_person': fields.boolean(string='Person', help='Check if the party is a person.'),
                'is_school': fields.boolean(string='School'),
                'is_pharmacy': fields.boolean(string='Pharmacy', help='Check if the party is a Pharmacy'),
                'ref': fields.char(size=256, string='SSN', help='Patient Social Security Number or equivalent'),               
    }

ResPartner()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
