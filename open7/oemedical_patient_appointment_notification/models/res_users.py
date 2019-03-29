# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime
import dateutil.relativedelta

APPOINTMENT_STATES = [
    ('draft','Draft'),
    ('confirm', 'Confirm'),
    ('waiting', 'Wating'),
    ('in_consultation', 'In consultation'),
    ('done', 'Done'),
    ('canceled', 'Canceled')
]

class Users(osv.osv):
    _name = 'res.users'
    _inherit = 'res.users'
    
    _columns = {
        'enable_appointment_notification'         : fields.boolean('Enable Notifications'),
        'show_every_appointment_notification'     : fields.integer('Show Every', help = "Show the notification every times set by this field, e.g: 5 minutes"),
        'show_unit_time_appointment_notification' : fields.selection([('minute','Minutes'),('hour','Hours')], 'Unit Time'),  
        'appointment_status_ids'                  : fields.one2many('oemedical.appointment.notification.status', 'user_id', string='States'),     
    }   
    
    _defaults = {
        'enable_appointment_notification'          : False,
        'show_every_appointment_notification'      : 5,
        'show_unit_time_appointment_notification'  : 'minute',
    }
    
    def call_patient_appointment_notification(self, cr, uid, ids=None, context=None):
        
        notification = ''
        obj = self.browse(cr, uid,ids[0])

        if obj.enable_appointment_notification and len(obj.appointment_status_ids) > 0:
            filters = [('appointment_date','>=', datetime.now()),('state', 'in', map(lambda s : s.appointment_state, obj.appointment_status_ids))] 
            appointment_ids = self.pool.get('oemedical.appointment').search(cr, uid, filters)
            
            def filter_fnc(state):
                return filter(lambda r : r[0] == state , APPOINTMENT_STATES)[0][1]

            def split_string(string, length):
                return [string[y-length:y] for y in range(length, length(string) + length , length)]

            records = map(lambda x: (filter_fnc(x.state), x.patient_id.patient_id.name, x.comments), self.pool.get('oemedical.appointment').browse(cr, uid, appointment_ids)) 

            res = dict.fromkeys(map(lambda x: x[0], records), [])
    
            notification = '<ul>'            
            for k in res.keys():
                notification += '<li><u>' + k + ':</u>' 
                notification +=  '<br/>'.join(list(map(lambda x: x[1] + '<br/>'.join(split_string(x[2], 30)), filter(lambda x: x[0] == k, records)))) + '</li>'
            notification = '</ul>'
            
        
        if notification:
            return {
                'type'    : 'ir.actions.client',
                'tag'     : 'notify.appointment',  
                'context' : context,
                'params'  : {
                               'title'  : 'Appointment Notifications',
                               'text'   : notification,
                               'sticky' : True                                      
                            }
            }
            
        return ''       
    
Users()

class OemedicalAppointmentNotificationStatus(osv.osv):
       
    _name = 'oemedical.appointment.notification.status' 
        
    _columns = {
        'user_id'            : fields.many2one('res.users', 'User', required=True),
        'appointment_state'  : fields.selection(APPOINTMENT_STATES, string='State')        
    }
    
    _defaults = {
        'user_id': lambda self, cr, uid, context: context.get('user_id', False),        
    }

    _sql_constraints = [
        ('state_uniq', 'unique(user_id, appointment_state)', 'The state must be unique !'),
    ]
            
OemedicalAppointmentNotificationStatus()