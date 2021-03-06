# -*- coding: utf-8 -*-
from osv import osv
from osv import fields

class OeMedicalSpecialty(osv.Model):
    _name = 'oemedical.specialty'

    _columns = {
        'code': fields.char(size=25, string='Code'),
        'name': fields.char(size=256, string='Name', required=True),
        'description': fields.text(string='Description'),
        'parent_id': fields.many2one('oemedical.specialty', 'Parent Specialty'),
        'parent_name': fields.related('parent_id', 'name', type='char', readonly=True, string='Parent Specialty'),
        'child_ids': fields.one2many('oemedical.specialty', 'parent_id', 'Child Specialties'),  
        'cost': fields.float(string='Appointment Cost'),
    }

    _defaults = {
        'cost': 40
    }

    def _check_cost(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.cost <= 0:
                return False
        return True

    _sql_constraints = [       
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]

    _constraints = [
        (osv.osv._check_recursion, 'Error! You can not create recursive specialties.', ['parent_id']),
        (_check_cost, 'El costo de la consulta de esta especialidad no puede ser menor o igual a cero.', [])
    ]

OeMedicalSpecialty()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
