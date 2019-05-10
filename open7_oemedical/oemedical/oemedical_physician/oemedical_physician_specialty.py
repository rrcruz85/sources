# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from datetime import datetime

class OeMedicalPhysicianSpecialty(osv.Model):
    _name = 'oemedical.physician.specialty'
    _rec_name = 'specialty_id'

    _columns = {
        'physician_id': fields.many2one('oemedical.physician', string='Health Professional',required=True),
        'specialty_id': fields.many2one('oemedical.specialty', string='Specialty',required=True),
        'institution_id': fields.many2one('res.partner', string='Institution',required=True, domain=['|',('is_institution', '=', True),('is_school', '=', True)]),         
        'date_start': fields.date(string='Date Start',required=True),     
        'date_end': fields.date(string='Date End',required=True),       
        'is_primary': fields.boolean(string='Is Primary'), 
        'is_currently_performed': fields.boolean(string='Is Currently Performed'),  
        'degree': fields.selection([('0','General'),('1','1er'),('2','2do'),('3','3er'),('4','4to')], string='Degree'),
        'other_degree': fields.char(string='Other Degrees or Distintions', size = 256),
        'extra_info': fields.text(string='Other Information'),                 
    } 

    _sql_constraints = [       
        ('specialty_uniq', 'UNIQUE(physician_id,specialty_id)', 'Specialty must be unique!'),
    ]

    def _check_dates(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context):            
            date_start = datetime.strptime(str(obj.date_start), '%Y-%m-%d')
            date_end = datetime.strptime(str(obj.date_end), '%Y-%m-%d')            
            if date_start >= date_end:
                return False
        return True

    def _check_date_end(self, cr, uid, ids, context=None):        
        for obj in self.browse(cr, uid, ids, context=context): 
            date_end = datetime.strptime(str(obj.date_end), '%Y-%m-%d')            
            if date_end >= datetime.now():
                return False
        return True

    _constraints = [
        (_check_dates, 'El fecha de inicio no puede ser superior a la fecha final', []),
        (_check_date_end, 'La fecha final no puede ser posterior a la fecha actual', []),
    ]

OeMedicalPhysicianSpecialty()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
