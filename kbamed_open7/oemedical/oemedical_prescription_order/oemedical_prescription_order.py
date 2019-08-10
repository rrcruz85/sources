# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from openerp import netsvc
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

class OeMedicalPrescriptionOrder(osv.Model):
    _name='oemedical.prescription.order'

    _columns={
        'patient_id': fields.many2one('oemedical.patient', string='Patient', required=True),        
        'notes': fields.text(string='Prescription Notes'),
        'prescription_line': fields.one2many('oemedical.prescription.line', 'name', string='Prescription line',),
        'pharmacy': fields.many2one('res.partner', string='Pharmacy', domain =[('is_pharmacy', '=', True)]),
        'prescription_date': fields.datetime(string='Prescription Date'),
        'prescription_warning_ack': fields.boolean( string='Prescription verified'),
        'physician_id': fields.many2one('oemedical.physician', string='Prescribing Doctor',  required=True),
        'name': fields.char(size=256, string='Prescription ID', required=True, help='Type in the ID of this prescription'),
        'indications': fields.text(string='Doctor indications'),
        'diagnosis': fields.char(size=120, string='Diagnóstico'),
        'next_date': fields.date(string='Próx. Cita'),
    }
    
    _defaults={
        'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid,'oemedical.prescription.order'),
	    'prescription_date':lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    def print_prescription(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        #self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'oemedical.prescription.order',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'oemedical.prescription.print.webkit',
            'datas': datas,
            'nodestroy' : True
        }

#    def print_prescription(self, cr, uid, ids, context=None):
        '''
        '''
#        assert len(ids) == 1, 'This option should only be used for a single id at a time'
#        wf_service = netsvc.LocalService("workflow")
#        wf_service.trg_validate(uid, 'oemedical.prescription.order', ids[0], 'prescription_sent', cr)
#        datas = {
#                 'model': 'oemedical.prescription.order',
#                 'ids': ids,
#                 'form': self.read(cr, uid, ids[0], context=context),
#        }
#        return {'type': 'ir.actions.report.xml', 'report_name': 'prescription.order', 'datas': datas, 'nodestroy': True}


OeMedicalPrescriptionOrder()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
