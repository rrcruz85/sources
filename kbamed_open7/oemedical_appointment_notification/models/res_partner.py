# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class ResPartner(osv.osv):
    _inherit = 'res.partner'

    def _compute_is_patient(self, cr, uid, ids, name, args, context=None):
        res = dict.fromkeys(ids, False)
        patients_ids = self.pool.get('oemedical.patient').search(cr, uid, [('partner_id', 'in', ids)], context=context)
        patients = self.pool.get('oemedical.patient').browse(cr, uid, patients_ids, context)

        for patient in patients:
            res[patient.partner_id.id] = True
        return res

    _columns = {
        'is_patient': fields.function(_compute_is_patient, string="Is patient?", type='boolean', store=True)
    }
