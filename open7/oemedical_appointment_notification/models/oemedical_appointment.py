# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from datetime import datetime
import dateutil.relativedelta

class OeMedicalAppointment(osv.Model):
    _inherit = 'oemedical.appointment'

    def button_send_notification(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'oemedical.send_notification_wizard',
            'context': {'default_appointment_id': ids[0]},
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
 
class OeMedicalAppointmentNotification(osv.Model):
    _name = 'oemedical.appointment.notification'
    _rec_name = 'company_id'
    _columns = {
        'notify_before'       : fields.integer('Notify', help = "This field sets the number of unit of time to notify before the the last date comes."),
        'unit_time'           : fields.selection([('minute','Minutes'),('hour','Hours'),('day','Days'),('week','Week')], 'Unit Time'),
        'first_monthly'       : fields.boolean('1st Month'),
        'third_monthly'       : fields.boolean('3rd Month'),
        'sixth_monthly'       : fields.boolean('6th Month'),
        'nineth_monthly'      : fields.boolean('9th Month'),
        'yearly'              : fields.boolean('Yearly'), 
        'show_notification'   : fields.integer('Show Notification Every', help = "Show the notification every times set by this field, e.g: 5 minutes"),
        'show_unit_time'      : fields.selection([('minute','Minutes'),('hour','Hours')], 'Show Notification Unit Time'),
        'company_id'          : fields.many2one('res.company', string = 'Company', required = True)
    }
    
    _defaults = {
        'notify_before'     : 1,
        'unit_time'         : 'hour',
        'first_monthly'     : True,
        'third_monthly'     : True,
        'sixth_monthly'     : True,
        'nineth_monthly'    : True,
        'yearly'            : True,
        'show_notification' : 5,
        'show_unit_time'    : 'minute',
        'company_id'        : lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'oemedical.appointment.notification',context=c),
    }
    
    _sql_constraints = [('company_unique', 'unique(company_id)','Company Must Be Unique'),]
    
    def call_patient_notification(self, cr, uid, ids=None, context=None):
        
        notify_before = 1
        unit_time = 'hour'
        first_monthly= True
        third_monthly = True
        sixth_monthly = True
        nineth_monthly = True
        yearly = True
        show_notification = 5
        show_unit_time = 'minute'
        if ids:
            obj = self.browse(cr, uid, ids[0])
            notify_before = obj.notify_before
            unit_time = obj.unit_time
            first_monthly = obj.first_monthly
            third_monthly = obj.third_monthly
            sixth_monthly = obj.sixth_monthly
            nineth_monthly = obj.nineth_monthly
            yearly = obj.yearly
            show_notification = obj.show_notification
            show_unit_time = obj.show_unit_time
        if unit_time == 'week':
            unit_time = 'day'
            notify_before *= 7  
        
        interval = {
            'minute': dateutil.relativedelta.relativedelta(minutes=notify_before),
            'hour': dateutil.relativedelta.relativedelta(hours=notify_before),
            'day': dateutil.relativedelta.relativedelta(days=notify_before)
        }      
        
        today_date = datetime.now().date()  
        patients = '<br/>'       
        if first_monthly:
            patients += self.get_patients_per_month(cr, 1, today_date)
              
        if third_monthly:
            patients += self.get_patients_per_month(cr, 3, today_date)  
        
        if sixth_monthly:
            patients += self.get_patients_per_month(cr, 6, today_date)          
            
        if nineth_monthly:
            patients += self.get_patients_per_month(cr, 9, today_date)
        
        if yearly:
            patients += self.get_patients_per_month(cr, 12, today_date)
        
        if patients:
            return {
                'type'    : 'ir.actions.client',
                'tag'     : 'notify.patient',  
                'context' : context,
                'params'  : {
                               'title'  : 'Operated Patients Notification',
                               'text'   : patients,
                               'sticky' : True                                      
                            }
            }
            
    def get_patients_per_month(self, cr, month, today_date):
            
        cr.execute("""
                select pp.display_name, p.ced_ruc, pp.mobile, pp.email from oemedical_surgery s
                inner join oemedical_patient p on s.patient_id = p.id
                inner join res_partner pp on p.partner_id = pp.id
                where (s.date + interval '%s' """ + ('year' if month == 12 else 'month') + """)::date = %s
            """,((1 if month == 12 else month), today_date,))  
            
        lines = cr.fetchall()
        patients = ''
        if lines:
            patients += '<b>Operated patients ' + ('1 year ' if month == 12 else str(month) + ' months ') + 'ago:</b><ul>'
            patients += ''.join(map(lambda r: '<li>' + (r[0] or '') + ('<br/>Ced.:' + r[1] if r[1] else '') + ('<br/>Tel.:' + r[2] if r[2] else '') + ('<br/>Email:' + r[3] if r[3] else '') + '</li>' , lines))
            patients += '</ul>'
        return patients
    
OeMedicalAppointmentNotification()
    