# -*- coding: utf-8 -*-

from openerp.osv import osv

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
        
OeMedicalAppointment()