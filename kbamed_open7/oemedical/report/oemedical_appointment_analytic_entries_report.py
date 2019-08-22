# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import fields, osv

class oemedical_appointment_analytic_entries_report(osv.osv):
    _name = "oemedical.appointment.analytic.entries.report"
    _description = "Analytic Entries Statistics"
    _auto = False
    _columns = {
        'state': fields.selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('waiting', 'Waiting'), ('in_consultation', 'In Consultation'),
                                   ('done', 'Done'), ('canceled', 'Canceled')], string='Appointment Status'),
        'patient_id': fields.many2one('oemedical.patient', string='Patient'),
        'doctor_id': fields.many2one('oemedical.physician', string='Doctor'),
        'specialty_id': fields.many2one('oemedical.specialty', string='Specialty'),
        'start_datetime': fields.datetime(string='Start DateTime'),
        'end_datetime': fields.datetime(string='End DateTime'),
        'hours': fields.float('Hours Duration'),
        'minutes': fields.float('Minutes Duration'),
        'patient_creation_datetime': fields.datetime(string='Patient Creation DateTime'),
        'total_invoiced': fields.float(string='Total Invoiced'),
        'year': fields.char('Year', size=4,),
        'day': fields.char('Day', size=128),
        'month': fields.selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
                                   ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
                                   ('10', 'October'), ('11', 'November'), ('12', 'December')], 'Month')
    }

    #def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
    #    if context is None:
    #        context = {}
    #    return super(oemedical_appointment_analytic_entries_report, self).search(cr, uid, args, offset, limit, order, context=context, count=count)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'oemedical_appointment_analytic_entries_report')
        cr.execute("""
            create or replace view oemedical_appointment_analytic_entries_report as (
                select
                a.id, a.state, a.patient_id, a.doctor_id, a.specialty_id,
                a.appointment_time as start_datetime, a.end_date as end_datetime,
                DATE_PART('day', COALESCE(a.end_date, a.appointment_time) - a.appointment_time) * 24 
                + DATE_PART('hour', COALESCE(a.end_date, a.appointment_time) - a.appointment_time)
                + DATE_PART('minute', COALESCE(a.end_date, a.appointment_time) - a.appointment_time)/60 as hours,
                DATE_PART('day', COALESCE(a.end_date, a.appointment_time) - a.appointment_time) * 24 * 60 
                + DATE_PART('hour', COALESCE(a.end_date, a.appointment_time) - a.appointment_time) * 60
                + DATE_PART('minute', COALESCE(a.end_date, a.appointment_time) - a.appointment_time) as minutes,
                p.create_date as patient_creation_datetime,
                /*(select COALESCE(sum(ta.cost), 0.0) from oemedical_appointment_treatment ta where ta.appointment_id = a.id) + sp.cost - a.discount as subtotal,
                ((select COALESCE(sum(ta.cost), 0.0) from oemedical_appointment_treatment ta where ta.appointment_id = a.id) + sp.cost - a.discount) *
                (select c.iva_tax/100 from oemedical_physician pp inner join res_partner part on pp.physician_id = part.id
                inner join res_company c on part.company_id = c.id where pp.id = a.doctor_id limit 1) as iva,*/
                case when a.state = 'done' then
                ((select COALESCE(sum(ta.cost), 0.0) from oemedical_appointment_treatment ta where ta.appointment_id = a.id) + sp.cost - a.discount) *
                (select (1 + c.iva_tax/100) from oemedical_physician pp inner join res_partner part on pp.physician_id = part.id
                inner join res_company c on part.company_id = c.id where pp.id = a.doctor_id limit 1) else 0.00 end as total_invoiced,
                to_char(a.appointment_time, 'YYYY') as year,
                to_char(a.appointment_time, 'MM') as month,
                to_char(a.appointment_time, 'YYYY-MM-DD') as day
                from oemedical_appointment a
                inner join oemedical_patient p on a.patient_id = p.id
                inner join oemedical_specialty sp on a.specialty_id = sp.id
                order by a.appointment_time desc
            )
        """)

oemedical_appointment_analytic_entries_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
