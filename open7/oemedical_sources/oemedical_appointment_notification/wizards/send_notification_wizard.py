# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import osv, fields


class SendNotificationWizard(osv.TransientModel):
    _name = 'oemedical.send_notification_wizard'
    _description = 'oemedical.send_notification_wizard'

    def default_get(self, cr, uid, fields_list, context=None):
        values = {}

        if context.get('active_model', False) == 'oemedical.appointment':
            for field in fields_list:
                if field == 'email_to':
                    values[field] = [
                        self.pool.get(context['active_model']).browse(
                            cr, uid, context['active_id'], context=context
                        ).patient_id.partner_id.id
                    ]
                elif field == 'body_html':
                    values[field] = 'Estimado paciente: [nombre_paciente]...<br><br>' \
                                    'Usted tiene una cita médica el día: [fecha], a las: [hora], con el ' \
                                    'doctor: [doctor]. <br><br>' \
                                    'PD: No debe responder esta notificación automática del sistema.'
                elif field == 'subject':
                    values[field] = 'Notificación de cita médica.'

        return values

    def action_create(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        user = self.pool.get('res.users').browse(cr, uid, uid, context)

        _ids = []
        appointment = self.pool.get('oemedical.appointment').browse(
            cr, uid, context.get('appointment_id', False), context
        )

        for patient in obj.email_to:
            if not patient.email:
                raise osv.except_osv(
                    'Error', tools.ustr('El destinatario no tiene definida su dirección de correo electrónico...')
                )

            body_html = obj.body_html.replace('[nombre_paciente]', tools.ustr(patient.name))
            if context.get('appointment_id', False):
                body_html.replace('[fecha]', appointment.appointment_day) \
                    .replace('[hora]', appointment.appointment_hour + ':' + appointment.appointment_minute) \
                    .replace('[doctor]', appointment.doctor.name)

            vals = {
                'state': 'outgoing',
                'subject': obj.subject,
                'body_html': '<pre>%s</pre>' % body_html,
                'email_to': patient.email,
                'email_from': user.company_id.email or False,
                'auto_delete': True,
                'attachment_ids': [(6, 0, [attach.id for attach in obj.attachment_ids])],
            }

            _ids.append(self.pool.get('mail.mail').create(cr, uid, vals, context=context))
            if context.get('appointment_id', False) and appointment.doctor and appointment.doctor.physician_id.email:
                vals['email_to'] = appointment.doctor.physician_id.email
                _ids.append(self.pool.get('mail.mail').create(cr, uid, vals, context=context))

        self.pool.get('mail.mail').send(cr, uid, _ids)
        return True

    def _get_templates(self, cr, uid, context=None):
        email_template_obj = self.pool.get('email.template')
        record_ids = email_template_obj.search(
            cr, uid, [('model', '=', 'oemedical.send_notification_wizard')], context=context
        )

        return email_template_obj.name_get(cr, uid, record_ids, context) + [(False, '')]

    def save_as_template(self, cr, uid, ids, context=None):
        email_template = self.pool.get('email.template')
        ir_model_pool = self.pool.get('ir.model')

        for record in self.browse(cr, uid, ids, context=context):
            model_ids = ir_model_pool.search(
                cr, uid, [('model', '=', 'oemedical.send_notification_wizard')], context=context
            )

            model_id = model_ids and model_ids[0] or False

            values = {
                'name': record.subject,
                'subject': record.subject or False,
                'body_html': record.body_html or False,
                'model_id': model_id or False
            }

            email_template.create(cr, uid, values, context=context)

            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': record.id,
                'res_model': self._name,
                'target': 'new',
                'context': {'default_model': 'oemedical.send_notification_wizard'},
            }

    def on_change_template(self, cr, uid, ids, template_id, context=None):
        if not template_id:
            return {'value': {}}

        obj = self.pool.get('email.template').browse(cr, uid, template_id, context)
        res = {'subject': obj.subject, 'body_html': obj.body_html}
        return {'value': res}

    _columns = {
        'subject': fields.char('Asunto', size=250, required=False, readonly=False),
        'email_template_id': fields.selection(_get_templates, 'Template', size=-1),
        'body_html': fields.text('Message', required=True),

        'email_to': fields.many2many(
            'res.partner', 'notification_partner_rel', 'notification_id', 'partner_id', 'Patients',
            required=True, readonly=False, domain=[('is_patient', '=', True)]
        ),

        'attachment_ids': fields.many2many(
            'ir.attachment', 'notification_attachment_rel', 'notification_id', 'attachment_id', 'Attachments'
        ),
    }
