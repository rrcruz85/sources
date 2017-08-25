# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp import tools


class TestOrder(osv.osv):
    _name = 'oemedical.test_order'
    _description = 'oemedical.test_order'

    _columns = {
        'patient_id': fields.many2one('oemedical.patient', string='Patient'),
        'doctor_id': fields.many2one('oemedical.physician', string='Doctor', required=True),
        'date': fields.date(string='Date', required=True),
        'notes': fields.text('Notas'),

        # Preoperatorios...
        'pre_biometria_hematica': fields.boolean(string='Biometria hematica'),
        'pre_plaquetas': fields.boolean(string='Plaquetas'),
        'pre_globulos_blancos': fields.boolean(string='Globulos blancos'),
        'pre_linfocitos': fields.boolean(string='Linfocitos'),
        'pre_hematocritos': fields.boolean(string='Hematocritos'),
        'pre_hemoglobina': fields.boolean(string='Hemoglobina'),
        'pre_urea': fields.boolean(string='Urea'),
        'pre_creatinina': fields.boolean(string='Creatinina'),
        'pre_glucosa': fields.boolean(string='Glucosa (añadir hemoglobina glicosilada en caso de diabetes)'),
        'pre_tp_ttp_inr': fields.boolean(string='TP TTP INR'),
        'pre_acido_urico': fields.boolean(string='Acido urico'),
        'pre_bun': fields.boolean(string='BUN'),
        'pre_proteinas_totales': fields.boolean(string='Proteinas totales'),
        'pre_albumina': fields.boolean(string='Albumina'),
        'pre_perfil_lipidico': fields.boolean(string='Perfil lipidico (Trigliceridos, colesterol, HDL, LDL)'),
        'pre_perfil_hepatico': fields.boolean(
            string='Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)'),
        'pre_perfil_anemia': fields.boolean(
            string='Perfil de anemia (hierro serico, transferrina, ferritina, capacidad de fijacion de hierro, vitamina B12, acido folico)'),
        'pre_minerales': fields.boolean(string='Minerales: Sodio, Potasio, Calcio'),
        'pre_pruebas_tiroideas': fields.boolean(string='Pruebas tiroideas: TSH, FT4, (beta HCG si es mujer)'),
        'pre_emo': fields.boolean(string='EMO'),
        'pre_ecografia_abdominal': fields.boolean(string='Ecografia abdominal'),
        'pre_composicion_dexa': fields.boolean(string='Composicion DEXA'),
        'pre_radiografia_torax': fields.boolean(string='Radiografia de torax PA-L'),
        'pre_evaluacion_cardiologica': fields.boolean(
            string='Evaluacion cardiologica preoperatoria + test de esfuerzo si amerita'),
        'pre_evaluacion_neumologica': fields.boolean(string='Evaluacion neumologica preoperatoria'),
        'pre_endoscopia_digestiva_alta': fields.boolean(
            string='Endoscopia digestiva alta (Dr. Napoleon Salgado) Clínica Sandoval. (En ayunas)'),
        'pre_evaluacion_nutricional': fields.boolean(string='Evaluacion nutricional'),
        'pre_evaluacion_psicologica': fields.boolean(string='Evaluacion psicologica'),
        'pre_oma': fields.boolean(string='OMA'),
        'pre_peptido_c': fields.boolean(string='Peptido C'),
        'pre_curva_glucosa_dos': fields.boolean(string='Curva de Glucosa 2 horas'),
        'pre_curva_glucosa_cuatro': fields.boolean(string='Curva de Glucosa 4 horas'),
        'pre_others': fields.boolean(string='Otros'),
        'pre_others_text': fields.char(string='Otros examenes a realizar'),
        'pre_select_all': fields.boolean(string='Seleccionar todos...'),

        # Primer mes...
        'one_biometria_hematica': fields.boolean(string='Biometria hematica'),
        'one_urea': fields.boolean(string='Urea'),
        'one_creatinina': fields.boolean(string='Creatinina'),
        'one_glucosa': fields.boolean(string='Glucosa'),
        'one_acido_urico': fields.boolean(string='Acido urico'),
        'one_bun': fields.boolean(string='BUN'),
        'one_proteinas_totales': fields.boolean(string='Proteinas totales'),
        'one_albumina': fields.boolean(string='Albumina'),
        'one_perfil_lipidico': fields.boolean(string='Perfil lipidico (Trigliceridos, colesterol, HDL, LDL)'),
        'one_perfil_hepatico': fields.boolean(
            string='Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)'),
        'one_sodio': fields.boolean(string='Sodio'),
        'one_potasio': fields.boolean(string='Potasio'),
        'one_oma': fields.boolean(string='OMA'),
        'one_peptido_c': fields.boolean(string='Peptido C'),
        'one_curva_glucosa_dos': fields.boolean(string='Curva de Glucosa 2 horas'),
        'one_curva_glucosa_cuatro': fields.boolean(string='Curva de Glucosa 4 horas'),
        'one_others': fields.boolean(string='Otros'),
        'one_others_text': fields.char(string='Otros examenes a realizar'),
        'one_select_all': fields.boolean(string='Seleccionar todos...'),

        # Tercer mes...
        'three_biometria_hematica': fields.boolean(string='Biometria hematica'),
        'three_urea': fields.boolean(string='Urea'),
        'three_creatinina': fields.boolean(string='Creatinina'),
        'three_glucosa': fields.boolean(string='Glucosa'),
        'three_acido_urico': fields.boolean(string='Acido urico'),
        'three_bun': fields.boolean(string='BUN'),
        'three_proteinas_totales': fields.boolean(string='Proteinas totales'),
        'three_albumina': fields.boolean(string='Albumina'),
        'three_perfil_lipidico': fields.boolean(string='Perfil lipidico (Trigliceridos, colesterol, HDL, LDL)'),
        'three_perfil_hepatico': fields.boolean(
            string='Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)'),
        'three_sodio': fields.boolean(string='Sodio'),
        'three_potasio': fields.boolean(string='Potasio'),
        'three_calcio': fields.boolean(string='Calcio'),
        'three_oma': fields.boolean(string='OMA'),
        'three_peptido_c': fields.boolean(string='Peptido C'),
        'three_curva_glucosa_dos': fields.boolean(string='Curva de Glucosa 2 horas'),
        'three_curva_glucosa_cuatro': fields.boolean(string='Curva de Glucosa 4 horas'),
        'three_others': fields.boolean(string='Otros'),
        'three_others_text': fields.char(string='Otros examenes a realizar'),
        'three_select_all': fields.boolean(string='Seleccionar todos...'),

        # Sexto o noveno mes...
        'six_or_nine_month': fields.selection(selection=[('six', 'Six month'), ('nine', 'Nine month')], string='Month'),

        'six_or_nine_biometria_hematica': fields.boolean(string='Biometria hematica'),
        'six_or_nine_urea': fields.boolean(string='Urea'),
        'six_or_nine_creatinina': fields.boolean(string='Creatinina'),
        'six_or_nine_glucosa': fields.boolean(string='Glucosa'),
        'six_or_nine_hemoglobina_glicosilada': fields.boolean(string='Hemoglobina glicosilada (en caso de Diabetes)'),
        'six_or_nine_acido_urico': fields.boolean(string='Acido urico'),
        'six_or_nine_bun': fields.boolean(string='BUN'),
        'six_or_nine_proteinas_totales': fields.boolean(string='Proteinas totales'),
        'six_or_nine_albumina': fields.boolean(string='Albumina'),
        'six_or_nine_perfil_lipidico': fields.boolean(string='Perfil lipidico (Trigliceridos, colesterol, HDL, LDL)'),
        'six_or_nine_perfil_hepatico': fields.boolean(
            string='Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)'),
        'six_or_nine_perfil_hierro': fields.boolean(
            string='Perfil de hierro (Hierro sérico, ferritinina, transferrina, ácido fólico, capacidad de fijación de hierro)'),
        'six_or_nine_sodio': fields.boolean(string='Sodio'),
        'six_or_nine_potasio': fields.boolean(string='Potasio'),
        'six_or_nine_calcio': fields.boolean(string='Calcio'),
        'six_or_nine_eco_abdomen': fields.boolean(string='Eco de abdomen superior (solo 6to mes)'),
        'six_or_nine_oma': fields.boolean(string='OMA'),
        'six_or_nine_peptido_c': fields.boolean(string='Peptido C'),
        'six_or_nine_curva_glucosa_dos': fields.boolean(string='Curva de Glucosa 2 horas'),
        'six_or_nine_curva_glucosa_cuatro': fields.boolean(string='Curva de Glucosa 4 horas'),
        'six_or_nine_others': fields.boolean(string='Otros'),
        'six_or_nine_others_text': fields.char(string='Otros examenes a realizar'),
        'six_or_nine_select_all': fields.boolean(string='Seleccionar todos...'),

        # Primer año...
        'first_year_biometria_hematica': fields.boolean(string='Biometria hematica'),
        'first_year_urea': fields.boolean(string='Urea'),
        'first_year_creatinina': fields.boolean(string='Creatinina'),
        'first_year_glucosa': fields.boolean(string='Glucosa (si es diabetico hemoglobina glicosilada)'),
        'first_year_tp_ttp_inr': fields.boolean(string='TP TTP INR'),
        'first_year_acido_urico': fields.boolean(string='Acido urico'),
        'first_year_bun': fields.boolean(string='BUN'),
        'first_year_proteinas_totales': fields.boolean(string='Proteinas totales'),
        'first_year_albumina': fields.boolean(string='Albumina'),
        'first_year_perfil_lipidico': fields.boolean(string='Perfil lipidico (Trigliceridos, colesterol, HDL, LDL)'),
        'first_year_perfil_hepatico': fields.boolean(
            string='Perfil hepático (TGO, TGP, GGT, fosfatasa alcalina, bilirrubinas)'),
        'first_year_perfil_hierro': fields.boolean(
            string='Perfil de hierro (Hierro sérico, ferritinina, transferrina, ácido fólico, capacidad de fijación de hierro)'),
        'first_year_minerales': fields.boolean(string='Minerales: Sodio, Potasio, Calcio'),
        'first_year_pruebas_tiroideas': fields.boolean(string='Pruebas tiroideas: TSH, FT4'),
        'first_year_emo': fields.boolean(string='EMO'),
        'first_year_ecografia_abdominal': fields.boolean(string='Ecografia abdominal'),
        'first_year_composicion_dexa': fields.boolean(string='Composicion corporal DEXA'),
        'first_year_oma': fields.boolean(string='OMA'),
        'first_year_peptido_c': fields.boolean(string='Peptido C'),
        'first_year_curva_glucosa_dos': fields.boolean(string='Curva de Glucosa 2 horas'),
        'first_year_curva_glucosa_cuatro': fields.boolean(string='Curva de Glucosa 4 horas'),
        'first_year_others': fields.boolean(string='Otros'),
        'first_year_others_text': fields.char(string='Otros examenes a realizar'),
        'first_year_select_all': fields.boolean(string='Seleccionar todos...'),
    }

    _defaults = {
        'date': fields.date.today()
    }

    def action_print_report(self, cr, uid, ids, context=None):
        return {
            'name': tools.ustr('Asistente de impresión...'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'oemedical_test_order.test_order_report_print_wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
        }

    def onchange_global_selector_pre(self, cr, uid, ids, selector_value, context=None):
        return {
            'value': {
                'pre_biometria_hematica': selector_value,
                'pre_plaquetas': selector_value,
                'pre_globulos_blancos': selector_value,
                'pre_linfocitos': selector_value,
                'pre_hematocritos': selector_value,
                'pre_hemoglobina': selector_value,
                'pre_urea': selector_value,
                'pre_creatinina': selector_value,
                'pre_glucosa': selector_value,
                'pre_tp_ttp_inr': selector_value,
                'pre_acido_urico': selector_value,
                'pre_bun': selector_value,
                'pre_proteinas_totales': selector_value,
                'pre_albumina': selector_value,
                'pre_perfil_lipidico': selector_value,
                'pre_perfil_hepatico': selector_value,
                'pre_perfil_anemia': selector_value,
                'pre_minerales': selector_value,
                'pre_pruebas_tiroideas': selector_value,
                'pre_emo': selector_value,
                'pre_ecografia_abdominal': selector_value,
                'pre_composicion_dexa': selector_value,
                'pre_radiografia_torax': selector_value,
                'pre_evaluacion_cardiologica': selector_value,
                'pre_evaluacion_neumologica': selector_value,
                'pre_endoscopia_digestiva_alta': selector_value,
                'pre_evaluacion_nutricional': selector_value,
                'pre_evaluacion_psicologica': selector_value,
                'pre_oma': selector_value,
                'pre_peptido_c': selector_value,
                'pre_curva_glucosa_dos': selector_value,
                'pre_curva_glucosa_cuatro': selector_value,
            }
        }

    def onchange_global_selector_one(self, cr, uid, ids, selector_value, context=None):
        return {
            'value': {
                'one_biometria_hematica': selector_value,
                'one_urea': selector_value,
                'one_creatinina': selector_value,
                'one_glucosa': selector_value,
                'one_acido_urico': selector_value,
                'one_bun': selector_value,
                'one_proteinas_totales': selector_value,
                'one_albumina': selector_value,
                'one_perfil_lipidico': selector_value,
                'one_perfil_hepatico': selector_value,
                'one_sodio': selector_value,
                'one_potasio': selector_value,
                'one_oma': selector_value,
                'one_peptido_c': selector_value,
                'one_curva_glucosa_dos': selector_value,
                'one_curva_glucosa_cuatro': selector_value,
            }
        }

    def onchange_global_selector_three(self, cr, uid, ids, selector_value, context=None):
        return {
            'value': {
                'three_biometria_hematica': selector_value,
                'three_urea': selector_value,
                'three_creatinina': selector_value,
                'three_glucosa': selector_value,
                'three_acido_urico': selector_value,
                'three_bun': selector_value,
                'three_proteinas_totales': selector_value,
                'three_albumina': selector_value,
                'three_perfil_lipidico': selector_value,
                'three_perfil_hepatico': selector_value,
                'three_sodio': selector_value,
                'three_potasio': selector_value,
                'three_calcio': selector_value,
                'three_oma': selector_value,
                'three_peptido_c': selector_value,
                'three_curva_glucosa_dos': selector_value,
                'three_curva_glucosa_cuatro': selector_value,
            }
        }

    def onchange_global_selector_six_or_nine(self, cr, uid, ids, selector_value, context=None):
        return {
            'value': {
                'six_or_nine_biometria_hematica': selector_value,
                'six_or_nine_urea': selector_value,
                'six_or_nine_creatinina': selector_value,
                'six_or_nine_glucosa': selector_value,
                'six_or_nine_hemoglobina_glicosilada': selector_value,
                'six_or_nine_acido_urico': selector_value,
                'six_or_nine_bun': selector_value,
                'six_or_nine_proteinas_totales': selector_value,
                'six_or_nine_albumina': selector_value,
                'six_or_nine_perfil_lipidico': selector_value,
                'six_or_nine_perfil_hepatico': selector_value,
                'six_or_nine_perfil_hierro': selector_value,
                'six_or_nine_sodio': selector_value,
                'six_or_nine_potasio': selector_value,
                'six_or_nine_calcio': selector_value,
                'six_or_nine_eco_abdomen': selector_value,
                'six_or_nine_oma': selector_value,
                'six_or_nine_peptido_c': selector_value,
                'six_or_nine_curva_glucosa_dos': selector_value,
                'six_or_nine_curva_glucosa_cuatro': selector_value,
            }
        }

    def onchange_global_selector_first_year(self, cr, uid, ids, selector_value, context=None):
        return {
            'value': {
                'first_year_biometria_hematica': selector_value,
                'first_year_urea': selector_value,
                'first_year_creatinina': selector_value,
                'first_year_glucosa': selector_value,
                'first_year_tp_ttp_inr': selector_value,
                'first_year_acido_urico': selector_value,
                'first_year_bun': selector_value,
                'first_year_proteinas_totales': selector_value,
                'first_year_albumina': selector_value,
                'first_year_perfil_lipidico': selector_value,
                'first_year_perfil_hepatico': selector_value,
                'first_year_perfil_hierro': selector_value,
                'first_year_minerales': selector_value,
                'first_year_pruebas_tiroideas': selector_value,
                'first_year_emo': selector_value,
                'first_year_ecografia_abdominal': selector_value,
                'first_year_composicion_dexa': selector_value,
                'first_year_oma': selector_value,
                'first_year_peptido_c': selector_value,
                'first_year_curva_glucosa_dos': selector_value,
                'first_year_curva_glucosa_cuatro': selector_value,
            }
        }


TestOrder()


class OeMedicalPatient(osv.osv):
    _inherit = 'oemedical.patient'
    _columns = {
        'test_order_ids': fields.one2many('oemedical.test_order', 'patient_id', string='Test Orders')
    }


OeMedicalPatient()
