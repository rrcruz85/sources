# -*- encoding: utf-8 -*-
 
#importamos la clase osv del modulo osv y fields
import time
from openerp.osv import fields, osv, orm
from time import strftime
 
 
class OeMedicalBariatricEvaluation(osv.osv):
   
    _name = 'oemedical.bariatric.evaluation' 
    
    def _compute_imc(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        if eval.epa_tal > 0.0:
            res[eval.id] = eval.epa_pac / (eval.epa_tal * eval.epa_tal)

        return res
    
    def _compute_plb(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_pac * 2.2

        return res

    def _compute_pid(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_tal * eval.epa_tal * 25.0

        return res

    def _compute_pex(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_pac - eval.epa_pid

        return res

    def _compute_pep(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_pex / 2.0

        return res

    def _compute_exi(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_tal * eval.epa_tal * 25.0 + eval.epa_pep

        return res
        
    _columns={
              'patient_id':fields.many2one('oemedical.patient', 'Paciente', required=True),
              'doctor': fields.many2one('oemedical.physician', string='Doctor'),
              'eva_date': fields.date(string='Date', readonly=True),
              'mot_cta': fields.text(string='Motivo de consulta :'),
              'ant_qur': fields.text(string='Antecedentes quirúrgicos :'),
              'ang_g': fields.integer(string='G :'),
              'ang_p': fields.char(string='P :', size=256),
              'ang_c': fields.char(string='C :', size=256),
              'ang_a': fields.char(string='A :', size=256),
              'ang_hv': fields.char(string='HV :', size=256),
              'ang_fum': fields.date(string='FUM :', help='Fecha de ultima menstruación'),
              'ang_ant': fields.char(string='Anticoncepción :', size=500),
              'anc_hta': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='HTA :'),
              'anc_hdr': fields.char(string='Duración :', size=256),
              'anc_hto': fields.char(string='TTO :', size=256, help='Tratamiento seguido'),
              'anc_hmd': fields.char(string='Medicación :', size=256),
              'anc_hdc': fields.char(string='Dosis :', size=256),
              'anc_dm': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='DM :'),
              'anc_ddr': fields.char(string='Duración :', size=256),
              'anc_dto': fields.char(string='TTO :', size=256, help='Tratamiento seguido'),
              'anc_dmd': fields.char(string='Medicación :', size=256),
              'anc_ddc': fields.char(string='Dosis :', size=256),
              'anc_dlp': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='DLP :'),
              'anc_ldr': fields.char(string='Duración :', size=256),
              'anc_lto': fields.char(string='TTO :', size=256, help='Tratamiento seguido'),
              'anc_lmd': fields.char(string='Medicación :', size=256),
              'anc_ldc': fields.char(string='Dosis :', size=256),
              'anc_apn': fields.selection([
                                         ('s', 'Si'),
                                         ('n', 'No'),
                                         ], string='Apnea :'),
              'anc_adr': fields.char(string='Duración :', size=256),
              'anc_ato': fields.char(string='TTO :', size=256, help='Tratamiento seguido'),
              'anc_amd': fields.char(string='Medicación :', size=256),
              'anc_adc': fields.char(string='Dosis :', size=256),
              'anc_ost': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Osteoartritis :'),
              'anc_odr': fields.char(string='Duración :', size=256),
              'anc_oto': fields.char(string='TTO :', size=256, help='Tratamiento seguido'),
              'anc_omd': fields.char(string='Medicación :', size=256),
              'anc_odc': fields.char(string='Dosis :', size=256),
              'anc_sop': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='SOP :'),
              'anc_sdr': fields.char(string='Duración :', size=256),
              'anc_sto': fields.char(string='TTO :', size=256, help='Tratamiento seguido'),
              'anc_smd': fields.char(string='Medicación :', size=256),
              'anc_sdc': fields.char(string='Dosis :', size=256),
              'anc_otr': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Otros :'),
              'anc_rdr': fields.char(string='Duración :', size=256),
              'anc_rto': fields.char(string='TTO :', size=256, help='Tratamiento seguido'),
              'anc_rmd': fields.char(string='Medicación :', size=256),
              'anc_rdc': fields.char(string='Dosis :', size=256),
              'anc_ots': fields.text(string='Otros antecedentes clínicos :'),  
              'anc_tab': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Tabaco :'),
              'anc_alc': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Alcohol :'),
              'anc_drg': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Drogas :'),
              'anc_tad': fields.text(string='Comentarios :'),
              'anf_pdr': fields.char(size=256, string='Padre :'),
              'anf_mdr': fields.char(size=256, string='Madre :'),
              'anf_hrm': fields.char(size=256, string='Hermanos :'),
              'anf_hij': fields.char(size=256, string='Hijos :'),
              'anf_abp': fields.char(size=256, string='Abuelo paterno :'),
              'anf_aap': fields.char(size=256, string='Abuela paterna :'),
              'anf_abm': fields.char(size=256, string='Abuelo materno :'),
              'anf_aam': fields.char(size=256, string='Abuela materna :'),
              'anf_abp': fields.char(size=256, string='Abuelo paterno :'),
              'anf_otr': fields.text(string='Otros :'),
              'med_med1': fields.char(size=60,string="Medicamento"),
              'med_dos1': fields.char(size=60,string="Dosis"),
              'med_tmp1': fields.char(size=60,string="Tiempo"),
              'med_med2': fields.char(size=60,string="Medicamento"),
              'med_dos2': fields.char(size=60,string="Dosis"),
              'med_tmp2': fields.char(size=60,string="Tiempo"),
              'med_med3': fields.char(size=60,string="Medicamento"),
              'med_dos3': fields.char(size=60,string="Dosis"),
              'med_tmp3': fields.char(size=60,string="Tiempo"),
              'epa_apa': fields.char(size=256, string='Aparecimiento :'),
              'epa_lug': fields.char(size=256, string='Lugar :'),
              'epa_int': fields.char(size=256, string='Intensidad :'),
              'epa_aco': fields.char(size=256, string='Acompañantes :'),
              'epa_rea': fields.text(string='Relación a :'),
              'epa_die': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Dieta :'),
              'epa_cdi': fields.char(string='Cuál? :', size=256),
              'epa_ddi': fields.char(string='Duración :', size=256),
              'epa_dre': fields.char(string='Resultado :', size=256),
              'epa_eje': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Ejercicio :'),
              'epa_cej': fields.char(string='Cuál? :', size=256),
              'epa_dej': fields.char(string='Duración :', size=256),
              'epa_rej': fields.char(string='Resultado :', size=256),
              'epa_med': fields.selection([
                                         ('s', 'Si'),
                                         ('n', 'No'),
                                         ], string='Medicamentos :'),
              'epa_cme': fields.char(string='Cuál? :', size=256),
              'epa_dme': fields.char(string='Duración :', size=256),
              'epa_rme': fields.char(string='Resultado :', size=256),
              'epa_nut': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Nutricionista :'),
              'epa_cnu': fields.char(string='Cuál? :', size=256),
              'epa_dnu': fields.char(string='Duración :', size=256),
              'epa_rnu': fields.char(string='Resultado :', size=256),
              'epa_afr': fields.char(string='Frecuencia :', size=256),
              'epa_sal': fields.boolean(string='Sal :'),
              'epa_dul': fields.boolean(string='Dulce :'),
              'epa_pic': fields.boolean(string='Picadora :'),
              'epa_atr': fields.boolean(string='Atracones :'),
              'epa_ans': fields.boolean(string='Ansiedad :'),
              'epa_vom': fields.boolean(string='Vómitos :'),
              'epa_otr': fields.boolean(string='Otros :'),
              'epa_ode': fields.char(string='Descripción :', size=256),
              'epa_pmx': fields.float(string='Peso máximo :', digits=(2,6)),
              'epa_pmn': fields.float(string='Peso mínimo :', digits=(2,6)),
              'epa_imc': fields.function(_compute_imc, type='float', string='IMC :', store=True, digits=(3,2)),
              #'epa_imc': fields.float(string='IMC :', digits=(2,6)),
              'epa_tal': fields.float(string='Talla mts :', digits=(2,2)),
              'epa_pac': fields.float(string='Peso Kg :', digits=(3,2)),
              'epa_plb': fields.function(_compute_plb, type='float', string='Peso libras', store=True, digits=(3,2)),
              #'epa_pid': fields.float(string='Peso ideal :', digits=(3,2)),
              'epa_pid': fields.function(_compute_pid, type='float', string='Peso ideal', store=True, digits=(3,2)),
              #'epa_pex': fields.float(string='Exceso de peso :', digits=(3,2)),
              'epa_pex' :fields.function(_compute_pex, type='float', string='Exceso de peso :', store=True, digits=(3,2)),
              'epa_pep' :fields.function(_compute_pep, type='float', string='50% PEP :', store=True, digits=(3,2)),
              #'epa_exi': fields.float(string='Exito :', digits=(3,2)),
              'epa_exi': fields.function(_compute_exi, type='float', string='Exito :', store=True, digits=(3,2)),
              'epa_qqx': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Quiere QX? :'),
              'epa_cqx': fields.char(string='Cuál? :', size=256),
              'epa_qcu': fields.char(string='Cuándo? :', size=256),
              'ros_des': fields.text(string='Revisión actual de organos y sistemas :'),
              'tem_info': fields.float('Temperatura °C', digits=(12,3)),
              'pat_info': fields.char(size=60, string='Presión arterial'),
              'ppm_info': fields.integer('Pulso por minuto'),
              'cir_cad': fields.float(string='Circunferencia cadera: ',digits=(12,6)),
              'cir_cin': fields.float(string='Circunferencia cintura: ',digits=(12,6)),
              'eva_pil': fields.char(string='Piel: ', size=256),
              'eva_cab': fields.char(string='Cabeza: ', size=256),
              'eva_cue': fields.char(string='Cuello: ', size=256),
              'eva_tir': fields.char(string='Tiroides: ', size=256),
              'eva_pul': fields.char(string='Pulmonar: ', size=256),
              'eva_car': fields.char(string='Cardiaco: ', size=256),
              'eva_abd': fields.char(string='Abdomen: ', size=256),
              'eva_gen': fields.char(string='Genitales: ', size=256),
              'eva_ext': fields.text(string='Extremidades : '),
              'eva_ene': fields.char(string='ENE : ', size=256),
              'eva_otr': fields.text(string='Otros : '),
              'diag_bariatric': fields.many2many('oemedical.pathology', 'oemedical_patient_diagbariatric_rel', 'patient_id', 'diagnosis_id', 'Diagnósticos Presuntivos'),
              'diag_bariatric_def': fields.many2many('oemedical.pathology', 'oemedical_patient_diagbariatric_def_rel', 'patient_id', 'diagnosis_id', 'Diagnósticos Definitivos'),
              'exams': fields.text(string='Exámenes : '),
              'evalucs': fields.text(string='Evaluaciones : '),
              'cirugia': fields.text(string='Cirugía : '),
              'fechaqx': fields.date(string='Fecha QX : '),
              'costo': fields.float(string='Costo : ', digits=(6,2) ),
              'fianc': fields.text(string='Financiamiento : '),
              'fecha_control': fields.date(string='Fecha para control : ' ),
              'hora_fin': fields.char(size=10, string='Hora fin : '),
              'evolution_ids': fields.one2many('oemedical.bariatric.evolution', 'evaluation_id', 'Evoluciones')
            }
    
    _defaults = {
            'patient_id': lambda self, cr, uid, context: context.get('patient_id', False),
            'eva_date': time.strftime('%Y-%m-%d'),
              }
            
OeMedicalBariatricEvaluation()

class MedicalBariatricEvaluation(osv.osv):

    _inherit = 'oemedical.patient'
    
    _columns = {
        'bar_eval': fields.one2many('oemedical.bariatric.evaluation', 'patient_id', string='Evaluación Bariátrica'),
        }

MedicalBariatricEvaluation()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
