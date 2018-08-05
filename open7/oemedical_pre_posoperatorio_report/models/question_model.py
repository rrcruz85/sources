# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class OeMedicalPatient(osv.osv):
    _inherit = 'oemedical.patient'
    _columns = {
        'evolution_question_ids': fields.one2many('oemedical.question_model', 'patient_id',
                                                  string='Operation and Evolutions')
    }
OeMedicalPatient()


class QuestionModel(osv.osv):
    _name = 'oemedical.question_model'
    _description = 'oemedical.question_model'

    _columns = {
        'patient_id': fields.many2one('oemedical.patient', string='Patient'),
        'date': fields.date(string='Date', required=True),

        # Preoperatorio...
        'hipertension_arterial_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
        'hipertension_medication': fields.char(string='Medicacion'),
        'hipertension_dosis': fields.char(string='Dosis'),
        'hipertension_values': fields.char(string='Valores de Laboratorio'),

        'diabetes_melitus_dm': fields.boolean(string='Diabetes Melitus (DM)'),
        'diabetes_melitus_medication': fields.char(string='Medicacion'),
        'diabetes_melitus_dosis': fields.char(string='Dosis'),
        'diabetes_melitus_values': fields.char(string='Valores de Laboratorio'),

        'dislipidemias': fields.boolean(string='Dislipidemias'),
        'dislipidemias_medication': fields.char(string='Medicacion'),
        'dislipidemias_dosis': fields.char(string='Dosis'),
        'dislipidemias_values': fields.char(string='Valores de Laboratorio'),

        'higado_graso': fields.boolean(string='Higado Graso'),
        'higado_graso_medication': fields.char(string='Medicacion'),
        'higado_graso_dosis': fields.char(string='Dosis'),
        'higado_graso_values': fields.char(string='Valores de Laboratorio'),

        # 1er Mes Pos operatorio...
        'primer_mes_hipertension_arterial_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
        'primer_mes_hipertension_medication': fields.char(string='Medicacion'),
        'primer_mes_hipertension_dosis': fields.char(string='Dosis'),
        'primer_mes_hipertension_values': fields.char(string='Valores de Laboratorio'),
        'primer_mes_hipertension_evolution': fields.char(string='Evolucion'),

        'primer_mes_diabetes_melitus_dm': fields.boolean(string='Diabetes Melitus (DM)'),
        'primer_mes_diabetes_melitus_medication': fields.char(string='Medicacion'),
        'primer_mes_diabetes_melitus_dosis': fields.char(string='Dosis'),
        'primer_mes_diabetes_melitus_values': fields.char(string='Valores de Laboratorio'),
        'primer_mes_diabetes_melitus_evolution': fields.char(string='Evolucion'),

        'primer_mes_dislipidemias': fields.boolean(string='Dislipidemias'),
        'primer_mes_dislipidemias_medication': fields.char(string='Medicacion'),
        'primer_mes_dislipidemias_dosis': fields.char(string='Dosis'),
        'primer_mes_dislipidemias_values': fields.char(string='Valores de Laboratorio'),
        'primer_mes_dislipidemias_evolution': fields.char(string='Evolucion'),

        'primer_mes_higado_graso': fields.boolean(string='Higado Graso'),
        'primer_mes_higado_graso_medication': fields.char(string='Medicacion'),
        'primer_mes_higado_graso_dosis': fields.char(string='Dosis'),
        'primer_mes_higado_graso_values': fields.char(string='Valores de Laboratorio'),
        'primer_mes_higado_graso_evolution': fields.char(string='Evolucion'),

        # 3er Mes Pos operatorio...
        'tercer_mes_hipertension_arterial_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
        'tercer_mes_hipertension_medication': fields.char(string='Medicacion'),
        'tercer_mes_hipertension_dosis': fields.char(string='Dosis'),
        'tercer_mes_hipertension_values': fields.char(string='Valores de Laboratorio'),
        'tercer_mes_hipertension_evolution': fields.char(string='Evolucion'),

        'tercer_mes_diabetes_melitus_dm': fields.boolean(string='Diabetes Melitus (DM)'),
        'tercer_mes_diabetes_melitus_medication': fields.char(string='Medicacion'),
        'tercer_mes_diabetes_melitus_dosis': fields.char(string='Dosis'),
        'tercer_mes_diabetes_melitus_values': fields.char(string='Valores de Laboratorio'),
        'tercer_mes_diabetes_melitus_evolution': fields.char(string='Evolucion'),

        'tercer_mes_dislipidemias': fields.boolean(string='Dislipidemias'),
        'tercer_mes_dislipidemias_medication': fields.char(string='Medicacion'),
        'tercer_mes_dislipidemias_dosis': fields.char(string='Dosis'),
        'tercer_mes_dislipidemias_values': fields.char(string='Valores de Laboratorio'),
        'tercer_mes_dislipidemias_evolution': fields.char(string='Evolucion'),

        'tercer_mes_higado_graso': fields.boolean(string='Higado Graso'),
        'tercer_mes_higado_graso_medication': fields.char(string='Medicacion'),
        'tercer_mes_higado_graso_dosis': fields.char(string='Dosis'),
        'tercer_mes_higado_graso_values': fields.char(string='Valores de Laboratorio'),
        'tercer_mes_higado_graso_evolution': fields.char(string='Evolucion'),

        # 6to Mes Pos opertorio...
        'sexto_mes_hipertension_arterial_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
        'sexto_mes_hipertension_medication': fields.char(string='Medicacion'),
        'sexto_mes_hipertension_dosis': fields.char(string='Dosis'),
        'sexto_mes_hipertension_values': fields.char(string='Valores de Laboratorio'),
        'sexto_mes_hipertension_evolution': fields.char(string='Evolucion'),

        'sexto_mes_diabetes_melitus_dm': fields.boolean(string='Diabetes Melitus (DM)'),
        'sexto_mes_diabetes_melitus_medication': fields.char(string='Medicacion'),
        'sexto_mes_diabetes_melitus_dosis': fields.char(string='Dosis'),
        'sexto_mes_diabetes_melitus_values': fields.char(string='Valores de Laboratorio'),
        'sexto_mes_diabetes_melitus_evolution': fields.char(string='Evolucion'),

        'sexto_mes_dislipidemias': fields.boolean(string='Dislipidemias'),
        'sexto_mes_dislipidemias_medication': fields.char(string='Medicacion'),
        'sexto_mes_dislipidemias_dosis': fields.char(string='Dosis'),
        'sexto_mes_dislipidemias_values': fields.char(string='Valores de Laboratorio'),
        'sexto_mes_dislipidemias_evolution': fields.char(string='Evolucion'),

        'sexto_mes_higado_graso': fields.boolean(string='Higado Graso'),
        'sexto_mes_higado_graso_medication': fields.char(string='Medicacion'),
        'sexto_mes_higado_graso_dosis': fields.char(string='Dosis'),
        'sexto_mes_higado_graso_values': fields.char(string='Valores de Laboratorio'),
        'sexto_mes_higado_graso_evolution': fields.char(string='Evolucion'),

        # 9no Mes Pos operatorio...
        'noveno_mes_hipertension_arterial_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
        'noveno_mes_hipertension_medication': fields.char(string='Medicacion'),
        'noveno_mes_hipertension_dosis': fields.char(string='Dosis'),
        'noveno_mes_hipertension_values': fields.char(string='Valores de Laboratorio'),
        'noveno_mes_hipertension_evolution': fields.char(string='Evolucion'),

        'noveno_mes_diabetes_melitus_dm': fields.boolean(string='Diabetes Melitus (DM)'),
        'noveno_mes_diabetes_melitus_medication': fields.char(string='Medicacion'),
        'noveno_mes_diabetes_melitus_dosis': fields.char(string='Dosis'),
        'noveno_mes_diabetes_melitus_values': fields.char(string='Valores de Laboratorio'),
        'noveno_mes_diabetes_melitus_evolution': fields.char(string='Evolucion'),

        'noveno_mes_dislipidemias': fields.boolean(string='Dislipidemias'),
        'noveno_mes_dislipidemias_medication': fields.char(string='Medicacion'),
        'noveno_mes_dislipidemias_dosis': fields.char(string='Dosis'),
        'noveno_mes_dislipidemias_values': fields.char(string='Valores de Laboratorio'),
        'noveno_mes_dislipidemias_evolution': fields.char(string='Evolucion'),

        'noveno_mes_higado_graso': fields.boolean(string='Higado Graso'),
        'noveno_mes_higado_graso_medication': fields.char(string='Medicacion'),
        'noveno_mes_higado_graso_dosis': fields.char(string='Dosis'),
        'noveno_mes_higado_graso_values': fields.char(string='Valores de Laboratorio'),
        'noveno_mes_higado_graso_evolution': fields.char(string='Evolucion'),

        # 1 Año Pos oepratorio...
        'primer_anno_hipertension_arterial_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
        'primer_anno_hipertension_medication': fields.char(string='Medicacion'),
        'primer_anno_hipertension_dosis': fields.char(string='Dosis'),
        'primer_anno_hipertension_values': fields.char(string='Valores de Laboratorio'),
        'primer_anno_hipertension_evolution': fields.char(string='Evolucion'),

        'primer_anno_diabetes_melitus_dm': fields.boolean(string='Diabetes Melitus (DM)'),
        'primer_anno_diabetes_melitus_medication': fields.char(string='Medicacion'),
        'primer_anno_diabetes_melitus_dosis': fields.char(string='Dosis'),
        'primer_anno_diabetes_melitus_values': fields.char(string='Valores de Laboratorio'),
        'primer_anno_diabetes_melitus_evolution': fields.char(string='Evolucion'),

        'primer_anno_dislipidemias': fields.boolean(string='Dislipidemias'),
        'primer_anno_dislipidemias_medication': fields.char(string='Medicacion'),
        'primer_anno_dislipidemias_dosis': fields.char(string='Dosis'),
        'primer_anno_dislipidemias_values': fields.char(string='Valores de Laboratorio'),
        'primer_anno_dislipidemias_evolution': fields.char(string='Evolucion'),

        'primer_anno_higado_graso': fields.boolean(string='Higado Graso'),
        'primer_anno_higado_graso_medication': fields.char(string='Medicacion'),
        'primer_anno_higado_graso_dosis': fields.char(string='Dosis'),
        'primer_anno_higado_graso_values': fields.char(string='Valores de Laboratorio'),
        'primer_anno_higado_graso_evolution': fields.char(string='Evolucion'),

        # 1 Año y Medio Pos operatorio...
        'anno_medio_hipertension_arterial_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
        'anno_medio_hipertension_medication': fields.char(string='Medicacion'),
        'anno_medio_hipertension_dosis': fields.char(string='Dosis'),
        'anno_medio_hipertension_values': fields.char(string='Valores de Laboratorio'),
        'anno_medio_hipertension_evolution': fields.char(string='Evolucion'),

        'anno_medio_diabetes_melitus_dm': fields.boolean(string='Diabetes Melitus (DM)'),
        'anno_medio_diabetes_melitus_medication': fields.char(string='Medicacion'),
        'anno_medio_diabetes_melitus_dosis': fields.char(string='Dosis'),
        'anno_medio_diabetes_melitus_values': fields.char(string='Valores de Laboratorio'),
        'anno_medio_diabetes_melitus_evolution': fields.char(string='Evolucion'),

        'anno_medio_dislipidemias': fields.boolean(string='Dislipidemias'),
        'anno_medio_dislipidemias_medication': fields.char(string='Medicacion'),
        'anno_medio_dislipidemias_dosis': fields.char(string='Dosis'),
        'anno_medio_dislipidemias_values': fields.char(string='Valores de Laboratorio'),
        'anno_medio_dislipidemias_evolution': fields.char(string='Evolucion'),

        'anno_medio_higado_graso': fields.boolean(string='Higado Graso'),
        'anno_medio_higado_graso_medication': fields.char(string='Medicacion'),
        'anno_medio_higado_graso_dosis': fields.char(string='Dosis'),
        'anno_medio_higado_graso_values': fields.char(string='Valores de Laboratorio'),
        'anno_medio_higado_graso_evolution': fields.char(string='Evolucion'),

        # 2 Años Pos operatorio...
        'dos_annos_hipertension_arterial_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
        'dos_annos_hipertension_medication': fields.char(string='Medicacion'),
        'dos_annos_hipertension_dosis': fields.char(string='Dosis'),
        'dos_annos_hipertension_values': fields.char(string='Valores de Laboratorio'),
        'dos_annos_hipertension_evolution': fields.char(string='Evolucion'),

        'dos_annos_diabetes_melitus_dm': fields.boolean(string='Diabetes Melitus (DM)'),
        'dos_annos_diabetes_melitus_medication': fields.char(string='Medicacion'),
        'dos_annos_diabetes_melitus_dosis': fields.char(string='Dosis'),
        'dos_annos_diabetes_melitus_values': fields.char(string='Valores de Laboratorio'),
        'dos_annos_diabetes_melitus_evolution': fields.char(string='Evolucion'),

        'dos_annos_dislipidemias': fields.boolean(string='Dislipidemias'),
        'dos_annos_dislipidemias_medication': fields.char(string='Medicacion'),
        'dos_annos_dislipidemias_dosis': fields.char(string='Dosis'),
        'dos_annos_dislipidemias_values': fields.char(string='Valores de Laboratorio'),
        'dos_annos_dislipidemias_evolution': fields.char(string='Evolucion'),

        'dos_annos_higado_graso': fields.boolean(string='Higado Graso'),
        'dos_annos_higado_graso_medication': fields.char(string='Medicacion'),
        'dos_annos_higado_graso_dosis': fields.char(string='Dosis'),
        'dos_annos_higado_graso_values': fields.char(string='Valores de Laboratorio'),
        'dos_annos_higado_graso_evolution': fields.char(string='Evolucion'),
    }

    def action_print_report(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'module_report',
            'datas': {},
        }
QuestionModel()
