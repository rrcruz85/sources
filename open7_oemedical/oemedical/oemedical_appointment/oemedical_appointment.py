# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.tools.translate import _
from openerp.tools import misc
import pytz


class OeMedicalAppointment(osv.Model):
    _name = 'oemedical.appointment'
    _rec_name = 'patient_id'

    def _get_appointment_time(self, cr, uid, ids, field_name, arg, context=None):
        res = {} 
        for record in self.browse(cr, uid, ids, context=context):
            hour = int(record.start_time)
            min = int(round(record.start_time - hour, 2) * 60)
            res[record.id] = datetime.strptime(str(record.start_date) + ' ' + str(hour) + '-' + str(min), '%Y-%m-%d %H-%M')
        return res    

    
    _columns = {
        'patient_id': fields.many2one('oemedical.patient', string='Patient', required=True, select=True),
        'specialty_id': fields.many2one('oemedical.specialty', string='Specialty',required=True),
        'type': fields.selection([('c', 'Control Normal'),('cp', 'Control Periodico'),('u', 'Urgencia')], string='Type', required=True),
        'appointment_time': fields.function(_get_appointment_time, type='datetime', string='Appointment DateTime', 
            store={
                'oemedical.appointment': (lambda self, cr, uid, ids, c={}: ids, ['start_date','start_time'], 10),                         
        }),
        'start_date': fields.date(string='Date',required=True),
        'start_time': fields.float(string='Time',required=True),
        'doctor_id': fields.many2one('oemedical.physician',  string='Doctor', required=True), 
        'end_date': fields.datetime(string='End DateTime'),        
        'stimated_duration': fields.integer('Stimated Duration'),                
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
            hour = int(obj.start_time)
            min = int(round(obj.start_time - hour, 2) * 60)
            start_time = datetime.strptime(str(obj.start_date) + ' ' + str(hour) + '-' + str(min), '%Y-%m-%d %H-%M')
            if obj.end_date:
                end_date = datetime.strptime(str(obj.end_date), '%Y-%m-%d %H-%M')
                if start_time > end_date:
                    return False              
        return True
    
    def _check_start_time(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):          
            if obj.start_time > 24 or obj.start_time < 0:
                return False              
        return True

    _constraints = [    
        (_check_start_time, 'La hora de inicio esta incorrecta', []),   
        (_check_date_start_end, 'La fecha y hora de inicio no puede ser posterior a la fecha final', []),        
    ]

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

        val_history = {}
        ait_obj = self.pool.get('oemedical.appointment.history')

        self.write(cr, uid, ids, {'state':'done'} ,context=context)

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
