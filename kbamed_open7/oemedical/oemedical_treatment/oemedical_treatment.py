# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class OeMedicalTreatment(osv.Model):
    _name = 'oemedical.treatment'

    _columns = {
        'name': fields.char(size=512, required=True, string='Name'),
        'cost': fields.float(string='Cost', required=True),
        'description': fields.text(string='Description'),
    }

    def _check_cost(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.cost <= 0:
                return False
        return True

    _constraints = [
        (_check_cost, 'El costo no puede ser menor o igual a cero.', []),
    ]

OeMedicalTreatment()

class OeMedicalAppointmentTreatment(osv.Model):
    _name = 'oemedical.appointment.treatment'
    _rec_name = 'treatment_id'

    def _get_appointment_data(self, cr, uid, ids, name, args, context):
        res = {}.fromkeys(ids, {'treatment_date': False, 'doctor_id': False})        
        for obj in self.browse(cr,uid,ids):
            res[obj.id]['treatment_date'] =  obj.appointment_id.appointment_time
            res[obj.id]['doctor_id'] = obj.appointment_id.doctor_id.id
        return res

    _columns = {
     'appointment_id'   : fields.many2one('oemedical.appointment', 'Appointment', required=True),
     'treatment_id'     : fields.many2one('oemedical.treatment', 'Treatment', required=True),
     'cost'             : fields.float(string='Cost'),   
     'treatment_date'   : fields.function(_get_appointment_data, string='DateTime', type='datetime', multi = "_val"),
     'doctor_id'        : fields.function(_get_appointment_data, string='Doctor', type='many2one', relation = "oemedical.physician", multi = "_val"),
     'medicament_ids'   : fields.one2many('oemedical.appointment.treatment.medicament', 'appointment_treatment_id', 'Medicamentos'),
     'observations'     : fields.text('Observations'), 
    }

    _defaults = {
        'appointment_id': lambda self, cr, uid, context: context.get('appointment_id', False) or False,
    }

    def onchange_appointment(self, cr, uid, ids, appointment_id, context = None):
        res = {'value': {}}    
        if appointment_id:
            obj = self.pool.get('oemedical.appointment').browse(cr, uid, appointment_id)
            res['value']['treatment_date'] = obj.appointment_time
            res['value']['doctor_id'] = obj.doctor_id.id
        return res
    
    def onchange_treatment(self, cr, uid, ids, treatment_id, context = None):
        res = {'value': {}}    
        if treatment_id:
            obj = self.pool.get('oemedical.treatment').browse(cr, uid, treatment_id)
            res['value']['cost'] = obj.cost
        return res

    def _check_cost(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.cost <= 0:
                return False
        return True

    _constraints = [
        (_check_cost, 'El costo no puede ser menor o igual a cero.', []),
    ]

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
     'appointment_treatment_id'     : fields.many2one('oemedical.appointment.treatment', 'Treatment', required=True),
     'medicament_id'                : fields.many2one('oemedical.medicament', 'Medicamento', required=True),  
     'concentration'                : fields.function(_get_concentration_presentation, string='Concentration', type='text', multi = "_val"),
     'presentation'                 : fields.function(_get_concentration_presentation, string='Presentation', type='text', multi = "_val"),
     'via'                          : fields.char(size=256, string='Via'),
     'dosis'                        : fields.char(size=256, string='Dosis'),
     'frequency'                    : fields.char(size=256, string='Frecuencia'),        
     'days'                         : fields.char(size=256, string='Dias')
    }

    def onchange_medicament(self, cr, uid, ids, medicament_id, context = None):
        res = {'value': {}}    
        if medicament_id:
            obj = self.pool.get('oemedical.medicament').browse(cr,uid,medicament_id)
            res['value']['concentration'] =  obj.concentration
            res['value']['presentation'] = obj.presentation
        return res
    
    _defaults = {
        'appointment_treatment_id': lambda self, cr, uid, context: context.get('treatment_id', False) or False,
    }

OeMedicalAppointmentTreatmentMedicament()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
