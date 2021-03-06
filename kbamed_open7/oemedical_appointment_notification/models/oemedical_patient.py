# -*- coding: utf-8 -*-

from openerp.osv import osv


class OeMedicalPatient(osv.osv):
    _inherit = 'oemedical.patient'
    
    def create(self, cr, uid, vals, context=None):
        res = super(OeMedicalPatient, self).create(cr, uid, vals, context=context)
        patient = self.browse(cr, uid, res, context)
        self.pool.get('res.partner').write(cr, uid, patient.partner_id.id, {'is_patient': True}, context=context)
        return res
    
OeMedicalPatient()