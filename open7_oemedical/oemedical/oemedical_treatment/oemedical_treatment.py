# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import tools

class OeMedicalTreatment(osv.Model):
    _name = 'oemedical.treatment'

    _columns = {
        'name'   : fields.char(size=512, string='Name'),      
    }

OeMedicalTreatment()

class OeMedicalAppointmentTreatment(osv.Model):
    _name = 'oemedical.appointment.treatment'
    _rec_name = 'treatment_id'

    _columns = {
     'treatment_id'     : fields.many2one('oemedical.treatment', 'Treatment', required=True),
     'appointment_id'   : fields.many2one('oemedical.appointment', 'Appointment', required=True),
     'medicament_ids'   : fields.one2many('oemedical.appointment.treatment.medicament', 'treatment_id', 'Medicamentos'),
     'observations'     : fields.text('Observations'), 
    }

    _defaults = {
        'appointment_id': lambda self, cr, uid, context: context.get('appointment_id', False) or False,
    }

OeMedicalAppointmentTreatment()

class OeMedicalAppointmentTreatmentMedicament(osv.Model):
    _name = 'oemedical.appointment.treatment.medicament'
    _rec_name = 'medicament_id'

    def _get_concentration_presentation(self, cr, uid, ids, name, args, context):
        res = {}.fromkeys(ids, {'concentration': '', 'presentation': ''})        
        for obj in self.browse(cr,uid,ids):
            res[obj.id]['concentration'] =  obj.medicament_id.concentration
            res[obj.id]['presentation'] = obj.medicament_id.presentation
        return res

    _columns = {     
     'treatment_id'     : fields.many2one('oemedical.appointment.treatment', 'Treatment', required=True),
     'medicament_id'    : fields.many2one('oemedical.medicament', 'Medicamento', required=True),  
     'concentration'    : fields.function(_get_concentration_presentation, string='Concentration', type='text', multi = "_val"),
     'presentation'     : fields.function(_get_concentration_presentation, string='Presentation', type='text', multi = "_val"),
     'via'              : fields.char(size=256, string='Via'),
     'dosis'            : fields.char(size=256, string='Dosis'),
     'frequency'        : fields.char(size=256, string='Frecuencia'),        
     'days'             : fields.char(size=256, string='Dias')
    }

    def onchange_medicament(self, cr, uid, ids, medicament_id, context = None):
        res = {'value': {}}    
        if medicament_id:
            obj = self.pool.get('oemedical.medicament').browse(cr,uid,medicament_id)
            res['value']['concentration'] =  obj.concentration
            res['value']['presentation'] = obj.presentation
        return res
    
    _defaults = {
        'treatment_id': lambda self, cr, uid, context: context.get('treatment_id', False) or False,
    }

OeMedicalAppointmentTreatmentMedicament()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
