# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime
import dateutil.relativedelta

class Users(osv.osv):
    _name = 'res.users'
    _inherit = 'res.users'
    
    _columns = {
        'receive_patient_notification' : fields.boolean('Receive Patient Surgery Notification'),
        'notify_before'       : fields.integer('Notify', help = "This field sets the number of unit of time to notify before the the last date comes."),
        'unit_time'           : fields.selection([('minute','Minutes'),('hour','Hours'),('day','Days'),('week','Week')], 'Unit Time'),
        'first_monthly'       : fields.boolean('1st Month'),
        'third_monthly'       : fields.boolean('3rd Month'),
        'sixth_monthly'       : fields.boolean('6th Month'),
        'nineth_monthly'      : fields.boolean('9th Month'),
        'yearly'              : fields.boolean('Yearly'), 
        'show_notification'   : fields.integer('Show Notification Every', help = "Show the notification every times set by this field, e.g: 5 minutes"),
        'show_unit_time'      : fields.selection([('minute','Minutes'),('hour','Hours')], 'Show Notification Unit Time'),       
    }   
    
    _defaults = {
        'notify_before'     : 1,
        'unit_time'         : 'day',
        'first_monthly'     : True,
        'third_monthly'     : True,
        'sixth_monthly'     : True,
        'nineth_monthly'    : True,
        'yearly'            : True,
        'show_notification' : 30,
        'show_unit_time'    : 'minute',
    }
    
    def call_patient_notification(self, cr, uid, ids=None, context=None):
        
        notify_before = 1
        unit_time = 'hour'
        first_monthly= True
        third_monthly = True
        sixth_monthly = True
        nineth_monthly = True
        yearly = True
        if ids:
            obj = self.browse(cr, uid, ids[0])
            notify_before = obj.notify_before
            unit_time = obj.unit_time
            first_monthly = obj.first_monthly
            third_monthly = obj.third_monthly
            sixth_monthly = obj.sixth_monthly
            nineth_monthly = obj.nineth_monthly
            yearly = obj.yearly            
        if unit_time == 'week':
            unit_time = 'day'
            notify_before *= 7  
        
        interval = {
            'minute': dateutil.relativedelta.relativedelta(minutes=notify_before),
            'hour': dateutil.relativedelta.relativedelta(hours=notify_before),
            'day': dateutil.relativedelta.relativedelta(days=notify_before)             
        }      
        
        notify_before_date = datetime.now() - interval[unit_time] 
        patients = '<br/>'       
        if first_monthly:
            patients += self.get_patients_per_month(cr, 1, notify_before_date)
              
        if third_monthly:
            patients += self.get_patients_per_month(cr, 3, notify_before_date)  
        
        if sixth_monthly:
            patients += self.get_patients_per_month(cr, 6, notify_before_date)          
            
        if nineth_monthly:
            patients += self.get_patients_per_month(cr, 9, notify_before_date)
        
        if yearly:
            patients += self.get_patients_per_month(cr, 12, notify_before_date)
        
        if patients and patients != '<br/>':
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
            
        return ''
    
    
    def get_patients_per_month(self, cr, month, notify_before_date):
        
        if notify_before_date >= datetime.now():
            notify_before_date -= dateutil.relativedelta.relativedelta(days=1)
        
        cr.execute("""
                select pp.display_name, p.ced_ruc, pp.mobile, pp.email from oemedical_bariatric_evaluation s
                inner join oemedical_patient p on s.patient_id = p.id
                inner join res_partner pp on p.partner_id = pp.id
                where (s.date + interval '%s' """ + ('year' if month == 12 else 'month') + """) between %s and %s
            """,((1 if month == 12 else month), notify_before_date, datetime.now()))  
            
        lines = cr.fetchall()
        patients = ''
        if lines:
            patients += '<b>Operated patients ' + ('1 year ' if month == 12 else str(month) + ' months ') + 'ago:</b><ul>'
            patients += ''.join(map(lambda r: '<li>' + (r[0] or '') + ('<br/>Ced.:' + r[1] if r[1] else '') + ('<br/>Tel.:' + r[2] if r[2] else '') + ('<br/>Email:' + r[3] if r[3] else '') + '</li>' , lines))
            patients += '</ul>'
        return patients   
    
Users()