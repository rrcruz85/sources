# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class OperationInformation(osv.osv):
    _name = 'oemedical.operation_information'
    _description = 'oemedical.operation_information'

    _columns = {
        # Protocolo operatorio...
        'patient_id': fields.many2one('oemedical.patient', string='Patient'),
        'medical_procedure': fields.char(string='Medical procedure', required=True),
        'date': fields.date(string='Date', required=True),

        'dx_pre_qx': fields.char(string='Dx PreQx'),
        'dx_post_qx': fields.char(string='Dx PostQx'),

        'doctor_id': fields.many2one('oemedical.physician', string='Cirujano'),
        'primer_ayudante': fields.many2one('oemedical.physician', string='Primer ayudante'),
        'segundo_ayudante': fields.many2one('oemedical.physician', string='Segundo ayudante'),
        'anestesiologo': fields.many2one('oemedical.physician', string='Anestesiologo'),

        'instrumentista': fields.many2one('oemedical.physician', string='Instrumentista'),
        'circulante': fields.many2one('oemedical.physician', string='Circulante'),

        'tipo_anestesia': fields.many2one('oemedical.anesthetize_type', string='Tipo anestesia'),
        'sangrado': fields.char(string='Sangrado'),
        'liquidos': fields.char(string='Liquidos'),
        'histopatologico': fields.char(string='Histopatologico'),
        'diuresis': fields.char(string='Diuresis'),
        'complicaciones': fields.char(string='Complicaciones'),
        'drenes': fields.char(string='Drenes'),
        'hallazgos': fields.text(string='Hallazgos'),

        # Descripcion de la operacion...
        'hora_inicio': fields.float(string='Hora de inicio'),
        'hora_finalizacion': fields.float(string='Hora de finalizacion'),
        'dieresis': fields.char(string='Dieresis'),
        'procedimiento': fields.text(string='Procedimiento'),
        'sintesis': fields.text(string='Sintesis'),
        'realizado_por': fields.char(string='Realizado por'),

        # Epicrisis...
        'diagnostico_provisional': fields.text(string='Diagnostico provisional'),
        'diagnostico_definitivo_primario': fields.text(string='Diagnostico definitivo primario'),
        'diagnostico_secundario': fields.text(string='Diagnostico secundario'),
        'operaciones': fields.text(string='Operaciones'),
        'historial_breve': fields.text(string='Historia breve y hallazgos especiales de examen fisico'),
        'hallasgos_laboratorio': fields.text(string='Hallazgos de laboratorio, Rayos X e interconsultas'),
        'evolucion': fields.text(string='Evolucion, complicaciones si las hubo'),
        'condicion_tratamiento': fields.text(string='Condicion tratamiento referencia final al dar el alta y pronostico'),

        # En caso de internacion...
        'dias_en_hospital': fields.integer(string='Dias de hospitalizacion'),
        'medico_internacion': fields.many2one('oemedical.physician', string='Medico'),
        'fecha_internacion': fields.date(string='Fecha'),

        # Evolucion...
        'evolution_ids': fields.one2many('oemedical.patient_evolution', 'operation_id', string='Evolucion'),
        'prescription_ids': fields.one2many('oemedical.patient_prescription', 'operation_id', string='Prescripciones'),

        # Endoscopia...
        'endoscopy_evolution_ids': fields.one2many('oemedical.endoscopy_patient_evolution', 'operation_id', string='Evolucion'),
        'endoscopy_prescription_ids': fields.one2many('oemedical.endoscopy_patient_prescription', 'operation_id', string='Prescripciones'),

    }

    def action_print_report(self, cr, uid, ids, context=None):
        data = {}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'operation_information_report',
            'datas': data,
        }
OperationInformation()


class OeMedicalPatient(osv.osv):
    _inherit = 'oemedical.patient'
    _columns = {
        'operation_ids': fields.one2many('oemedical.operation_information', 'patient_id', string='Operations')
    }
OeMedicalPatient()


class AnesthetizeType(osv.osv):
    _name = 'oemedical.anesthetize_type'
    _columns = {
        'name': fields.char(string='Tipo de anestesia', required=True)
    }
AnesthetizeType()


class PatientEvolution(osv.osv):
    _name = 'oemedical.patient_evolution'
    _description = 'oemedical.patient_evolution'

    _columns = {
        'date': fields.date(string='Fecha'),
        'time': fields.float(string='Hora'),
        'notes': fields.char(string='Notas de evolucion'),
        'operation_id': fields.many2one('oemedical.operation_information'),
    }
PatientEvolution()

class PatientEndoscopyEvolution(osv.osv):
    _name = 'oemedical.endoscopy_patient_evolution'
    _description = 'oemedical.endoscopy_patient_evolution'

    _columns = {
        'date': fields.date(string='Fecha'),
        'time': fields.float(string='Hora'),
        'notes': fields.char(string='Notas de evolucion'),
        'operation_id': fields.many2one('oemedical.operation_information'),
    }
PatientEndoscopyEvolution()

class PatientPrescription(osv.osv):
    _name = 'oemedical.patient_prescription'
    _description = 'oemedical.patient_prescription'

    _columns = {
        'operation_id': fields.many2one('oemedical.operation_information'),
        'indication': fields.char(string='Farmacoterapia e indicaciones para enfermeria y otro personal'),
        'administration': fields.char(string='Administracion'),
    }
PatientPrescription()

class PatientEndoscopyPrescription(osv.osv):
    _name = 'oemedical.endoscopy_patient_prescription'
    _description = 'oemedical.endoscopy_patient_prescription'

    _columns = {
        'operation_id': fields.many2one('oemedical.operation_information'),
        'indication': fields.char(string='Farmacoterapia e indicaciones para enfermeria y otro personal'),
        'administration': fields.char(string='Administracion'),
    }
PatientEndoscopyPrescription()
