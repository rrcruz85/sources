# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
import time
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools.translate import _
from openerp.tools import misc
import pytz

def get_datetime(pdate, float_time):
    hour = int(float_time)
    min = int(round(float_time - hour, 2) * 60)
    return datetime.strptime(str(pdate) + ' ' + str(hour) + '-' + str(min), '%Y-%m-%d %H-%M')

class OeMedicalAppointment(osv.Model):
    _name = 'oemedical.appointment'
    _rec_name = 'patient_id'

    def _get_appointment_time(self, cr, uid, ids, field_name, arg, context=None):
        res = {} 
        for record in self.browse(cr, uid, ids, context=context):
            start_time = get_datetime(record.start_date, record.start_time)
            res[record.id] = {
                'appointment_time' : start_time,
                'appointment_stimated_endtime': start_time + timedelta(minutes = record.stimated_duration)
            } 
        return res   
    
    _columns = {
        'patient_id': fields.many2one('oemedical.patient', string='Patient', required=True, select=True),
        'specialty_id': fields.many2one('oemedical.specialty', string='Specialty'),
        'type': fields.selection([('c', 'Control Normal'),('cp', 'Control Periodico'),('u', 'Urgencia')], string='Type', required=True),
        'appointment_time': fields.function(_get_appointment_time, type='datetime', string='Appointment DateTime', 
            store={
                'oemedical.appointment': (lambda self, cr, uid, ids, c={}: ids, ['start_date','start_time'], 10),                         
        }, multi='time'),
        'appointment_stimated_endtime': fields.function(_get_appointment_time, type='datetime', string='Stimated End Time', 
            store={
                'oemedical.appointment': (lambda self, cr, uid, ids, c={}: ids, ['start_date','start_time','stimated_duration'], 10),                         
        }, multi='time'),
        'start_date': fields.date(string='Date',required=True),
        'start_time': fields.float(string='Time',required=True),
        'doctor_id': fields.many2one('oemedical.physician',  string='Doctor', required=True), 
        'end_date': fields.datetime(string='End DateTime'),        
        'stimated_duration': fields.integer('Stimated Duration', help="Stimated Time in minutes [15-120] that the appointment last"),                
        'comments': fields.text(string='Comments'),       
        'state': fields.selection([('draft', 'Draft'),('confirm', 'Confirm'),
            ('waiting', 'Wating'),('in_consultation', 'In consultation'),
            ('done', 'Done'),('canceled', 'Canceled')], string='State'),
        'history_ids' : fields.one2many('oemedical.appointment.history','appointment_id','History lines', states={'start':[('readonly',True)]}),
    }
   
    _defaults = {         
        'stimated_duration': 30,
        'type': 'c',
        'state': 'draft',
        'start_date': time.strftime('%Y-%m-%d'),
        'start_time' : 8.5         
    }

    def _check_date_start_end(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.start_time > 24 or obj.start_time < 0:
                return False 
            start_time = get_datetime(obj.start_date, obj.start_time)
            if obj.end_date:
                end_date = datetime.strptime(str(obj.end_date), '%Y-%m-%d %H:%M:%S')
                if start_time > end_date:
                    return False              
        return True
    
    def _check_start_time(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):          
            if obj.start_time > 24 or obj.start_time < 0:
                return False              
        return True
    
    def _check_stimated_time(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):          
            if obj.stimated_duration < 15 or obj.stimated_duration > 120:
                return False              
        return True
    
    def _check_overlapped(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context): 
            date_start = get_datetime(obj.start_date, obj.start_time)  
            #date_end = date_start + timedelta(minutes = obj.stimated_duration)            
            records = self.search(cr,uid, [('id', '!=', obj.id ),('doctor_id', '=', obj.doctor_id.id),('appointment_time', '<=', str(date_start)),('appointment_stimated_endtime', '>', str(date_start))])
            if records:
                return False    
        return True

    _constraints = [    
        (_check_start_time, 'La hora de inicio esta incorrecta', []),   
        (_check_date_start_end, 'La fecha y hora de inicio no puede ser posterior a la fecha final', []),   
        (_check_overlapped, 'En la fecha y hora seleccionada el doctor ya tiene una cita, debe escoger otro horario', []),
        (_check_stimated_time, 'El tiempo estimado de la cita esta incorrecto, el rango correcto es [15-120]', []),        
    ]

    def onchange_patient_doctor(self, cr, uid, ids, patient_id, doctor_id, context=None):
        res = {}
        if patient_id and doctor_id: 
            recordIds = self.search(cr,uid, [('patient_id', '=', patient_id),('doctor_id', '=', doctor_id)], order = "appointment_stimated_endtime")
            if recordIds and recordIds[-1]: 
                end_datetime = datetime.strptime(self.browse(cr, uid, recordIds[-1]).appointment_stimated_endtime, '%Y-%m-%d %H:%M:%S')      
                end_datetime = end_datetime + timedelta(minutes = 5)
                hour = end_datetime.hour
                minutes = round(float(end_datetime.minute)/60, 2)              
                res['value'] = {'start_date': str(end_datetime.date()), 'start_time': hour + minutes}
        return res

    def onchange_specialty_id(self, cr, uid, ids, specialty_id, context=None):
        res = {}
        if specialty_id:
            res['value'] = {'doctor_id': False}
            res['domain'] = {'doctor_id': [('specialty_id', '=', specialty_id)]}
        return res

    def create(self, cr, uid, vals, context=None):
        val_history = {}
        val_history['user_id'] = uid
        val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        val_history['action'] = "Appointment Created"
        vals['history_ids'] = [(0, 0, val_history)] 
        
        hour = int(vals['start_time'])
        min = int(round(vals['start_time'] - hour, 2) * 60)

        start_date = datetime.strptime(str(vals['start_date']) + ' ' + str(hour) + '-' + str(min), '%Y-%m-%d %H-%M')
        if start_date < datetime.now():
            raise osv.except_osv(_('Error!'), _('The start datetime must be higher the current datetime'))
        return super(OeMedicalAppointment, self).create(cr, uid, vals, context=context)     

    def button_back(self, cr, uid, ids, context=None):

        val_history = {}
        ait_obj = self.pool.get('oemedical.appointment.history')

        for order in self.browse(cr, uid, ids, context=context):
            if order.state == 'confirm':
                self.write(cr, uid, ids, {'state':'draft'} ,context=context)
                val_history['action'] = "Changed to Draft"
            if order.state == 'waiting':
                val_history['action'] = "Changed to Confirm"
                self.write(cr, uid, ids, {'state':'confirm'} ,context=context)
            if order.state == 'in_consultation':
                val_history['action'] = "Changed to Waiting"
                self.write(cr, uid, ids, {'state':'waiting'} ,context=context)
            if order.state == 'done':
                val_history['action'] = "Changed to In Consultation"
                self.write(cr, uid, ids, {'state':'in_consultation'} ,context=context)
            if order.state == 'canceled':
                val_history['action'] = "Changed to Draft"
                self.write(cr, uid, ids, {'state':'draft'} ,context=context)

        val_history['appointment_id'] = ids[0]
        val_history['user_id'] = uid
        val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')

        ait_obj.create(cr, uid, val_history)

        return True

    def button_confirm(self, cr, uid, ids, context=None):

        val_history = {}
        ait_obj = self.pool.get('oemedical.appointment.history')

        self.write(cr, uid, ids, {'state':'confirm'} ,context=context)

        val_history['appointment_id'] = ids[0]
        val_history['user_id'] = uid
        val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        val_history['action'] = "Changed to Comfirm"
        ait_obj.create(cr, uid, val_history)

        return True

    def button_waiting(self, cr, uid, ids, context=None):

        val_history = {}
        ait_obj = self.pool.get('oemedical.appointment.history')

        self.write(cr, uid, ids, {'state':'waiting'} ,context=context)

        val_history['appointment_id'] = ids[0]
        val_history['user_id'] = uid
        val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        val_history['action'] = "Changed to Waiting"
        ait_obj.create(cr, uid, val_history)

        return True

    def button_in_consultation(self, cr, uid, ids, context=None):

        val_history = {}
        ait_obj = self.pool.get('oemedical.appointment.history')

        self.write(cr, uid, ids, {'state':'in_consultation'} ,context=context)

        val_history['appointment_id'] = ids[0]
        val_history['user_id'] = uid
        val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        val_history['action'] = "Changed to In Consultation"
        ait_obj.create(cr, uid, val_history)

        return True

    def button_done(self, cr, uid, ids, context=None):

        self.write(cr, uid, ids, {'state':'done', 'end_date': time.strftime('%Y-%m-%d %H:%M:%S')} ,context=context)

        ait_obj = self.pool.get('oemedical.appointment.history')
        val_history = {}
        val_history['appointment_id'] = ids[0]
        val_history['user_id'] = uid
        val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        val_history['action'] = "Changed to Done"
        ait_obj.create(cr, uid, val_history)

        return True

    def button_cancel(self, cr, uid, ids, context=None):

        val_history = {}
        ait_obj = self.pool.get('oemedical.appointment.history')

        self.write(cr, uid, ids, {'state':'canceled'} ,context=context)

        val_history['appointment_id'] = ids[0]
        val_history['user_id'] = uid
        val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        val_history['action'] = "Changed to Canceled"
        ait_obj.create(cr, uid, val_history)

        return True


OeMedicalAppointment()

class OeMedicalAppointmentHistory(osv.Model):
    _name = 'oemedical.appointment.history'

    _columns = {
        'appointment_id' :  fields.many2one('oemedical.appointment','History', ondelete='cascade'),
        'date': fields.datetime(string='Date and Time'),
        'user_id': fields.many2one('res.users', string='User'),
	    'action' : fields.text('Action'),
    }   

OeMedicalAppointmentHistory()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
