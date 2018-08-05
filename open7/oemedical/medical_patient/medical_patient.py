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


class OeMedicalPatient(osv.Model):
    _name = 'oemedical.patient'
    
    def _get_name(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = record.patient_id.name
        return res
    
    def onchange_name(self, cr, uid, ids, first_name, last_name, slastname, context=None):
        if first_name == False:
            first_name = ''
        if last_name == False:
            last_name = ''
        if slastname == False:
            slastname = ''
            
        res = {}
        res = {'value': {
                         'name' : first_name + ' ' + last_name + ' ' + slastname
                         }
               }
        return res
    
    def _get_age(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        age = ''
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
                years_months_days = str(delta.years) + 'y ' \
                + str(delta.months) + 'm ' \
                + str(delta.days) + 'd' + deceased
            else:
                years_months_days = 'No DoB !'
                
            # Return the age in format y m d when the caller is the field name
            if field_name == 'age':
                age = years_months_days
            
            res[record.id] = age
        return res
    
    _columns={
              'patient_id': fields.many2one('res.partner', string='Patient',required=True , help='Patient' ,domain=[('category_id', '=', 'Patient')]),
              'name': fields.function(_get_name, type='char', string='Patient Name', help="", multi=False),
              'family': fields.many2one('oemedical.family', string='Family', help='Family Code'),
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
              'medications': fields.one2many('oemedical.patient.medication', 'patient_id', string='Medications',),
              'evaluations': fields.one2many('oemedical.patient.evaluation', 'patient_id', string='Evaluations',),
              'critical_info': fields.text( string='Important disease, allergy or procedures information',
                                            help='Write any important information on the patient\'s disease, surgeries, allergies, ...'),
              'diseases': fields.one2many('oemedical.patient.disease', 'patient_id', string='Diseases', help='Mark if the patient has died'),
              'ethnic_group': fields.many2one('oemedical.ethnicity', string='Ethnic group',),
              'ssn': fields.char(size=256, string='CC', readonly=True),
              'vaccinations': fields.one2many('oemedical.vaccination', 'patient_id', 'Vaccinations',),
              'dob': fields.date(string='DoB'),
              'age': fields.function(_get_age, type='char', string='Age',
                                     help="It shows the age of the patient in years(y), months(m) and days(d).\nIf the patient has died, the age shown is the age at time of death, the age corresponding to the date on the death certificate. It will show also \"deceased\" on the field", multi=False),
              'marital_status': fields.selection([('s', 'Single'), ('m', 'Married'),
                                                  ('w', 'Widowed'),
                                                  ('d', 'Divorced'),
                                                  ('x', 'Separated'),
                                                  ('z', 'law marriage'),],
                                                 string='Marital Status', sort=False),
              'dod': fields.datetime(string='Date of Death'),
              'current_insurance': fields.many2one('oemedical.insurance', string='Insurance',
                                                   help='Insurance information. You may choose from the different insurances belonging to the patient'),
              'cod': fields.many2one('oemedical.pathology', string='Cause of Death',),
              'identification_code': fields.char(size=256, string='ID', help='Patient Identifier provided by the Health Center'),
              'deceased': fields.boolean(string='Deceased'),
              'street': fields.char('Street', size=128),
              'street2': fields.char('Street2', size=128),
              'zip': fields.char('Zip', change_default=True, size=24),
              'city': fields.char('City', size=128),
              'state_id': fields.many2one("res.country.state", 'State'),
              'country_id': fields.many2one('res.country', 'Country'),
              'email': fields.char('Email', size=240),
              'phone': fields.char('Phone', size=64),
              'fax': fields.char('Fax', size=64),
              'mobile': fields.char('Mobile', size=64),
              }
    
    _defaults={
               'identification_code': lambda obj, cr, uid, context:obj.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'),
               'photo': lambda self, cr, uid, ctx={}: self.pool.get('res.partner')._get_default_image(cr, uid, False, ctx, colorize=True),
               'ssn': lambda self, cr, uid, ctx={}: self.pool.get('res.partner')._get_ced_ruc(cr, uid, False),
               }
    
    def create(self, cr, uid, vals, context=None):
        sequence = unicode (self.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'))
        vals['identification_code'] = sequence
        return super(OeMedicalPatient, self).create(cr, uid, vals, context=context)
    
OeMedicalPatient()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
