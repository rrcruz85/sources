# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import time
from datetime import datetime, timedelta
from openerp.tools.translate import _

def get_datetime(pdate, float_time):
    hour = int(float_time)
    minute = int(round(float_time - hour, 2) * 60)
    return datetime.strptime(str(pdate) + ' ' + str(hour) + '-' + str(minute), '%Y-%m-%d %H-%M')

def send_email_notification(self, cr, uid, template_name, appointment_ids, context = None):
    try:
        template = self.pool.get('ir.model.data').get_object(cr, uid, 'oemedical', template_name)
        if template:
            appointments = self.pool.get('oemedical.appointment').browse(cr, uid, appointment_ids)
            for appointment in appointments:
                if appointment.patient_id.partner_id.email:
                    self.pool.get('email.template').send_mail(cr, uid, template.id, appointment.id, True, context=context)
    except ValueError as e:
        print e
        pass

class OeMedicalAppointment(osv.Model):
    _name = 'oemedical.appointment'
    _rec_name = 'patient_id'
    _order = "appointment_time desc"

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for exam in self.browse(cr, uid, ids, context=context):
            patient_name = exam.patient_id.first_name + ' ' + exam.patient_id.last_name
            formatted_hours = get_datetime(exam.start_date, exam.start_time).strftime("%Y-%m-%d %H:%M")
            res.append((exam.id, patient_name + '(' +  exam.patient_id.ced_ruc + ') / (' + formatted_hours + ') / (' + exam.specialty_id.name + ')'))
        return res
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}   
        if 'search_odonto_appointment' in context and context['search_odonto_appointment']:
            odonto_specialty = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', '001')  
            args.append('|')  
            args.append(['specialty_id', '=', odonto_specialty[1]])  
            args.append(['specialty_id', 'child_of', odonto_specialty[1]])   
        return super(OeMedicalAppointment, self).search(cr, uid, args, offset, limit,
                order, context=context, count=count)
    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=80):
        if not args:
            args = []  
        if 'search_odonto_appointment' in context and context['search_odonto_appointment']:
            odonto_specialty = self.pool.get('ir.model.data').get_object_reference(cr, user, 'oemedical', '001')  
            args.append('|')  
            args.append(['specialty_id', '=', odonto_specialty[1]])  
            args.append(['specialty_id', 'child_of', odonto_specialty[1]])
            del context['search_odonto_appointment']
        ids = self.search(cr, user, args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)
    
    def _get_appointment_time(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            start_time = get_datetime(record.start_date, record.start_time)            
            res[record.id] = {
                'appointment_time': start_time,
                'appointment_stimated_endtime': start_time + timedelta(minutes=record.stimated_duration)
            } 
        return res   
    
    _columns = {
        'patient_id'            : fields.many2one('oemedical.patient', string='Patient', required=True, select=True),
        'specialty_id'          : fields.many2one('oemedical.specialty', string='Specialty'),
        'type'                  : fields.selection([('c', 'Control Normal'), ('1c', 'Primer Control'), ('2c', 'Segundo Control'), ('cp', 'Control Periodico'), ('u', 'Urgencia')], string='Type', required=True),
        'appointment_time'      : fields.function(_get_appointment_time, type='datetime', string='Appointment DateTime', 
            store={
                'oemedical.appointment': (lambda self, cr, uid, ids, c={}: ids, ['start_date','start_time'], 10),                         
            }, multi='time'),
        'appointment_stimated_endtime': fields.function(_get_appointment_time, type='datetime', string='Stimated End Time', 
            store={
                'oemedical.appointment': (lambda self, cr, uid, ids, c={}: ids, ['start_date','start_time','stimated_duration'], 10),                         
            }, multi='time'),
        'start_date'            : fields.date(string='Date', required=True),
        'start_time'            : fields.float(string='Time', required=True),
        'doctor_id'             : fields.many2one('oemedical.physician',  string='Doctor', required=True), 
        'end_date'              : fields.datetime(string='End DateTime'),        
        'stimated_duration'     : fields.integer('Stimated Duration', help="Stimated Time in minutes [15-120] that the appointment last"),                
        'motive'                : fields.text(string='Motive'),
        'comments'              : fields.text(string='Comments'),
        'state'                 : fields.selection([('draft', 'Draft'),('confirm', 'Confirm'),('waiting', 'Wating'),('in_consultation', 'In consultation'),
                                                    ('done', 'Done'),('canceled', 'Canceled')], string='State'),
        'history_ids'           : fields.one2many('oemedical.appointment.history','appointment_id','History lines', states={'start':[('readonly',True)]}),
        'is_planned'            : fields.boolean('Cita programada?'),
        'next_appointment_date' : fields.date(string='Fecha Proxima Cita'), 
        'next_appointment_hour' : fields.float(string='Hora Proxima Cita'),
        'info_diagnosis'        : fields.text(string='Enfermedad Actual'),
        'linked_appointment_id' : fields.many2one('oemedical.appointment', string='Appointment'),
        'treatment_ids'         : fields.one2many('oemedical.appointment.treatment','appointment_id','Tratamientos'),
        
        # Signos vitales y mediciones...
        'pat_info'  : fields.char(size=256, string='Presion arterial'),
        'ppm_info'  : fields.integer('Frecuencia cardiaca'),
        'ppr_info'  : fields.integer('Frecuencia respiratoria'),
        'tem_info'  : fields.float('Temperatura bucal', digits=(2,2)),
        'tem2_info' : fields.float('Temperatura axilar', digits=(2,2)),
        'pes_info'  : fields.float('Peso (Kg)', digits=(3,2)),
        'size_info' : fields.float('Talla (m)', digits=(3,2)), 

        'cardiopatia': fields.related('patient_id', 'cardiopatia', type='boolean', string='Cardiopatía'),  
        'diabetes': fields.related('patient_id', 'diabetes', type='boolean', string='Diabetes'),
        'enf_car': fields.related('patient_id', 'enf_car', type='boolean', string='Enfermedad Cardiovascular'),
        'hipertension': fields.related('patient_id', 'hipertension', type='boolean', string='Hipertensión'),
        'cancer': fields.related('patient_id', 'cancer', type='boolean', string='Cancer'),
        'tuberculosis': fields.related('patient_id', 'tuberculosis', type='boolean', string='Tuberculosis'),
        'enf_men': fields.related('patient_id', 'enf_men', type='boolean', string='Enfermedad Mental'),
        'enf_inf': fields.related('patient_id', 'enf_inf', type='boolean', string='Enfermedad Infecciosa'),
        'mal_for': fields.related('patient_id', 'mal_for', type='boolean', string='Mal Formación'),
        'antibotic_allergic': fields.related('patient_id', 'antibotic_allergic', type='boolean', string='Alergia a antibioticos'),
        'anesthesia_allergic': fields.related('patient_id', 'anesthesia_allergic', type='boolean',string='Alergia a anestesia'),
        'hemorrhage': fields.related('patient_id', 'hemorrhage', type='boolean', string='Hemorragia'),
        'vih_sida': fields.related('patient_id', 'vih_sida', type='boolean', string='VIH/SIDA'),
        'asma': fields.related('patient_id', 'asma', type='boolean', string='Asma'),
        'other': fields.related('patient_id', 'other', type='boolean', string='Otra'),
        'others_antecedents': fields.related('patient_id', 'others_antecedents', type='text', string='Descripción de otros antescedentes'),        
    }
    
    def _get_default_specialty(self, cr, uid, context = None):
        if context and 'odonto_specialty' in context and context['odonto_specialty']:
            odonto_specialty = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', '001')
            return odonto_specialty[1]
        else:
            doctor_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'doctor_group')
            user = self.pool.get('res.users').browse(cr, uid, uid)
            for g in user.groups_id:
                if g.id == doctor_group[1]:
                    doctor = self.pool.get('oemedical.physician').search(cr, uid, [('physician_id.user_id', '=', uid)])
                    if doctor:
                        specialty = self.pool.get('oemedical.physician').browse(cr, uid, doctor[0]).specialty_id
                        if specialty:
                            return specialty.id
        return False

    def _get_default_patient(self, cr, uid, context = None):
        patient_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'patient_group')
        user = self.pool.get('res.users').browse(cr, uid, uid)
        for g in user.groups_id:
            if g.id == patient_group[1]:
                patient = self.pool.get('oemedical.patient').search(cr, uid, [('partner_id.user_id', '=', uid)])
                return patient[0] if patient else False
        return False

    def _get_default_doctor(self, cr, uid, context = None):
        doctor_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'doctor_group')
        user = self.pool.get('res.users').browse(cr, uid, uid)
        for g in user.groups_id:
            if g.id == doctor_group[1]:
                doctor = self.pool.get('oemedical.physician').search(cr, uid, [('physician_id.user_id', '=', uid)])
                return doctor[0] if doctor else False
        return False
   
    _defaults = {         
        'stimated_duration': 30,
        'type': 'c',
        'state': 'draft',
        'start_date': time.strftime('%Y-%m-%d'),
        'start_time': 8.5,
        'specialty_id': _get_default_specialty,
        'patient_id': _get_default_patient,
        'doctor_id': _get_default_doctor
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
            records = self.search(cr, uid, [('id', '!=', obj.id), ('state', '!=', 'canceled'), ('doctor_id', '=', obj.doctor_id.id), ('appointment_time', '<=', str(date_start)),('appointment_stimated_endtime', '>', str(date_start))])
            if records:
                return False    
        return True

    def _check_next_date_appointment(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.next_appointment_date and obj.next_appointment_hour:
                records = self.search(cr, uid, [('id', '!=', obj.id), ('state', '!=', 'canceled'), ('is_planned', '=', False), ('doctor_id', '=', obj.doctor_id.id), ('start_date', '=', obj.next_appointment_date), ('start_time', '>=', obj.next_appointment_hour), ('start_time', '<=', (obj.next_appointment_hour + 0.5))])
                if records:
                    return False
        return True

    def _check_next_date_appointment_vals(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.next_appointment_date and (obj.next_appointment_date <= datetime.now().date or obj.next_appointment_date <= obj.start_date):
                return False 
            if obj.next_appointment_date and obj.next_appointment_hour and (obj.next_appointment_hour <= 0 or obj.next_appointment_hour >= 24):
                return False               
        return True

    _constraints = [    
        (_check_start_time, 'La hora de inicio esta incorrecta', []),   
        (_check_date_start_end, 'La fecha y hora de inicio no puede ser posterior a la fecha final', []),   
        (_check_overlapped, 'En la fecha y hora seleccionada el doctor ya tiene una cita, debe escoger otro horario', []),
        (_check_stimated_time, 'El tiempo estimado de la cita esta incorrecto, el rango correcto es [15-120]', []),
        (_check_next_date_appointment, 'La fecha y hora de la proxima cita estan incorrectas. El doctor ya tiene una cita agendada en esa fecha y hora', []),        
        (_check_next_date_appointment_vals, 'La fecha y hora de la proxima cita estan incorrectas. La fecha y hora deben ser posteriores a la fecha y hora actual y de esta cita', []),        
    ]

    def onchange_patient_doctor(self, cr, uid, ids, patient_id, doctor_id, context=None):
        res = {}
        if patient_id:
            res['value'] = {}
            patient = self.pool.get('oemedical.patient').browse(cr, uid, patient_id)
            res['value']['cardiopatia'] = patient.cardiopatia
            res['value']['diabetes'] = patient.diabetes
            res['value']['enf_car'] = patient.enf_car
            res['value']['hipertension'] = patient.hipertension
            res['value']['cancer'] = patient.cancer
            res['value']['tuberculosis'] = patient.tuberculosis
            res['value']['enf_men'] = patient.enf_men
            res['value']['enf_inf'] = patient.enf_inf
            res['value']['mal_for'] = patient.mal_for
            res['value']['antibotic_allergic'] = patient.antibotic_allergic
            res['value']['anesthesia_allergic'] = patient.anesthesia_allergic
            res['value']['hemorrhage'] = patient.hemorrhage
            res['value']['vih_sida'] = patient.vih_sida
            res['value']['asma'] = patient.asma
            res['value']['other'] = patient.other
            res['value']['others_antecedents'] = patient.others_antecedents

            if doctor_id:
                recordIds = self.search(cr,uid, [('patient_id', '=', patient_id),('doctor_id', '=', doctor_id)], order = "appointment_stimated_endtime")
                if recordIds and recordIds[-1]: 
                    end_datetime = datetime.strptime(self.browse(cr, uid, recordIds[-1]).appointment_stimated_endtime, '%Y-%m-%d %H:%M:%S')      
                    end_datetime = end_datetime + timedelta(minutes = 5)
                    hour = end_datetime.hour
                    minutes = round(float(end_datetime.minute)/60, 2)              
                    res['value']['start_date'] = str(end_datetime.date())
                    res['value']['start_time'] = hour + minutes
        return res

    def onchange_specialty_id(self, cr, uid, ids, specialty_id, doctor_id=False, context=None):
        res = {}
        if specialty_id:
            is_valid = False
            if doctor_id:
                specialty = self.pool.get('oemedical.physician').browse(cr, uid, doctor_id).specialty_id
                if specialty and specialty.id == specialty_id:
                    is_valid = True
            else:
                records = self.pool.get('oemedical.physician').search(cr, uid, [('specialty_id', '=', specialty_id)])
                if not records:
                    warning = {
                        'title': _('No Doctors Found!'),
                        'message': _('No doctors were found for the selected specialty')
                    }
                    res['warning'] = warning
                else:
                    is_valid = True
                    doctor_id = records[0]
            res['value'] = {'doctor_id': doctor_id if is_valid else False}
            res['domain'] = {'doctor_id': [('specialty_id', '=', specialty_id)]}
        return res

    def create(self, cr, uid, vals, context=None):
        val_history = {}
        val_history['user_id'] = uid
        val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        val_history['action'] = _("Appointment Created")
        vals['history_ids'] = [(0, 0, val_history)] 
        
        hour = int(vals['start_time'])
        minute = int(round(vals['start_time'] - hour, 2) * 60)

        start_date = datetime.strptime(str(vals['start_date']) + ' ' + str(hour) + '-' + str(minute), '%Y-%m-%d %H-%M')
        if start_date < datetime.now():
            raise osv.except_osv(_('Error!'), _('The start datetime must be higher the current datetime'))
        return super(OeMedicalAppointment, self).create(cr, uid, vals, context=context)     

    def button_back(self, cr, uid, ids, context=None):

        ait_obj = self.pool.get('oemedical.appointment.history')
        for order in self.browse(cr, uid, ids, context=context):
            val_history = {}
            if order.state == 'confirm':
                self.write(cr, uid, ids, {'state': 'draft'}, context=context)
                val_history['action'] = _("Changed to Draft")
            if order.state == 'waiting':
                val_history['action'] = _("Changed to Confirmed")
                self.write(cr, uid, ids, {'state': 'confirm'}, context=context)
            if order.state == 'in_consultation':
                val_history['action'] = _("Changed to Waiting")
                self.write(cr, uid, ids, {'state': 'waiting'}, context=context)
            if order.state == 'done':
                val_history['action'] = _("Changed to In Consultation")
                self.write(cr, uid, ids, {'state': 'in_consultation'}, context=context)
            if order.state == 'canceled':
                val_history['action'] = _("Changed to Draft")
                self.write(cr, uid, ids, {'state': 'draft'}, context=context)
            val_history['appointment_id'] = order.id
            val_history['user_id'] = uid
            val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            ait_obj.create(cr, uid, val_history)

        return True

    def button_confirm(self, cr, uid, ids, context=None):
        ait_obj = self.pool.get('oemedical.appointment.history')
        self.write(cr, uid, ids, {'state': 'confirm'}, context=context)
        for rec_id in ids:
            val_history = {}
            val_history['appointment_id'] = rec_id
            val_history['user_id'] = uid
            val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            val_history['action'] = _("Changed to Confirmed")
            ait_obj.create(cr, uid, val_history)
        return True

    def button_waiting(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'waiting'}, context=context)
        ait_obj = self.pool.get('oemedical.appointment.history')
        for appointment in self.browse(cr, uid, ids, context=context):
            appointment_time = datetime.strptime(appointment.appointment_time, '%Y-%m-%d %H:%M:%S')
            if appointment_time > datetime.now():
                raise osv.except_osv(_('Error!'), _('You can not change the status until the appointment datetime is reached'))
            val_history = {}
            val_history['appointment_id'] = appointment.id
            val_history['user_id'] = uid
            val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            val_history['action'] = _("Changed to Waiting")
            ait_obj.create(cr, uid, val_history)
        return True

    def button_in_consultation(self, cr, uid, ids, context=None):
        ait_obj = self.pool.get('oemedical.appointment.history')
        self.write(cr, uid, ids, {'state': 'in_consultation'}, context=context)
        for appointment in self.browse(cr, uid, ids, context=context):
            appointment_time = datetime.strptime(appointment.appointment_time, '%Y-%m-%d %H:%M:%S')
            if appointment_time > datetime.now():
                raise osv.except_osv(_('Error!'), _('You can not change the status until the appointment datetime is reached'))
            val_history = {}
            val_history['appointment_id'] = appointment.id
            val_history['user_id'] = uid
            val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            val_history['action'] = _("Changed to In Consultation")
            ait_obj.create(cr, uid, val_history)
        return True

    def button_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'done', 'end_date': time.strftime('%Y-%m-%d %H:%M:%S')}, context=context)
        ait_obj = self.pool.get('oemedical.appointment.history')
        for appointment in self.browse(cr, uid, ids, context=context):
            appointment_time = datetime.strptime(appointment.appointment_time, '%Y-%m-%d %H:%M:%S')
            if appointment_time > datetime.now():
                raise osv.except_osv(_('Error!'), _('You can not change the status until the appointment datetime is reached'))
            val_history = {}
            val_history['appointment_id'] = appointment.id
            val_history['user_id'] = uid
            val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            val_history['action'] = _("Changed to Done")
            ait_obj.create(cr, uid, val_history)
        return True

    def button_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'canceled'}, context=context)
        ait_obj = self.pool.get('oemedical.appointment.history')
        for rec_id in ids:
            val_history = {}
            val_history['appointment_id'] = rec_id
            val_history['user_id'] = uid
            val_history['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            val_history['action'] = _("Changed to Canceled")
            ait_obj.create(cr, uid, val_history)
        return True

    def write(self, cr, uid, ids, vals, context=None):
        if 'next_appointment_date' in vals or 'next_appointment_hour' in vals:
            obj = self.browse(cr, uid, ids[0])
            next_appointment_date = vals['next_appointment_date'] if 'next_appointment_date' in vals else obj.next_appointment_date or time.strftime('%Y-%m-%d')
            next_appointment_hour = vals['next_appointment_hour'] if 'next_appointment_hour' in vals else obj.next_appointment_hour or 8.5
            
            record_ids = self.search(cr,uid, [('id', '!=', obj.id ),('patient_id', '=', obj.patient_id.id),('doctor_id', '=', obj.doctor_id.id),('state', 'in', ('draft','confirmed')),('start_date', '>', obj.start_date)])
            if not record_ids:
                create_vals = {
                    'patient_id'   : obj.patient_id.id,
                    'doctor_id'    : obj.doctor_id.id,
                    'specialty_id' : obj.specialty_id.id,
                    'type'         : 'cp',
                    'start_date'   : next_appointment_date,
                    'start_time'   : next_appointment_hour,
                    'is_planned'   : True
                }
                linked_appointment_id = super(OeMedicalAppointment, self).create(cr, uid, create_vals, context=context)
                vals['linked_appointment_id'] = linked_appointment_id
            elif obj.linked_appointment_id:
                update_vals = {
                   'start_date': next_appointment_date,
                   'start_time': next_appointment_hour
                }
                super(OeMedicalAppointment, self).write(cr, uid, [obj.linked_appointment_id.id], update_vals, context=context)
                
        return super(OeMedicalAppointment, self).write(cr, uid, ids, vals, context=context)

    def check_status(self, cr, uid, ids = False, context=None):
        """WARNING: meant for cron usage only"""

        one_hour_late = datetime.now() - timedelta(hours=1)
        late_appointment_ids = self.search(cr, uid, [('state', 'in', ('draft', 'confirm')), ('appointment_time', '<=', one_hour_late.strftime('%Y-%m-%d %H:%M:%S'))])
        if late_appointment_ids:
            self.button_cancel(cr, uid, late_appointment_ids)
            self.write(cr, uid, late_appointment_ids, {
                'comments': _('Canceled by the system due to no actions were not made over the current appointment')
            })
            send_email_notification(self, cr, uid, 'patient_appointment_canceled', late_appointment_ids, context)

        two_hours = datetime.now() - timedelta(hours=2)
        two_hours_waiting_ids = self.search(cr, uid, [('state', '=', 'waiting'), ('appointment_time', '<=', two_hours.strftime('%Y-%m-%d %H:%M:%S'))])
        if two_hours_waiting_ids:
            self.button_cancel(cr, uid, two_hours_waiting_ids)
            self.write(cr, uid, two_hours_waiting_ids, {
                'comments': _('Canceled by the system due to no actions were not made over the current appointment')
            })
            send_email_notification(self, cr, uid, 'patient_waiting_appointment_canceled', two_hours_waiting_ids, context)
            send_email_notification(self, cr, uid, 'doctor_waiting_appointment_canceled', two_hours_waiting_ids, context)

        one_hour = datetime.now() - timedelta(hours=1)
        one_hour_waiting_ids = self.search(cr, uid, [('state', '=', 'waiting'), ('appointment_time', '<=', one_hour.strftime('%Y-%m-%d %H:%M:%S'))])
        if one_hour_waiting_ids:
            send_email_notification(self, cr, uid, 'patient_appointment_waiting', one_hour_waiting_ids, context)

        tree_hours = datetime.now() - timedelta(hours=3)
        tree_hours_under_treatment_ids = self.search(cr, uid, [('state', '=', 'in_consultation'), ('appointment_time', '<=', tree_hours.strftime('%Y-%m-%d %H:%M:%S'))])
        if tree_hours_under_treatment_ids:
            self.button_done(cr, uid, tree_hours_under_treatment_ids)
            self.write(cr, uid, late_appointment_ids, {
                'comments': _('Done by the system due to no actions were not made over the current appointment')
            })
            send_email_notification(self, cr, uid, 'patient_appointment_done', tree_hours_under_treatment_ids, context)

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
