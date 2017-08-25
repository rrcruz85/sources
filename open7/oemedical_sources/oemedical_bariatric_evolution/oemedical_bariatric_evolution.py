# -*- encoding: utf-8 -*-
 
#importamos la clase osv del modulo osv y fields
import time
from openerp.osv import fields, osv, orm
from time import strftime
 
 
class OeMedicalBariatricEvolution(osv.osv):
   
    _name = 'oemedical.bariatric.evolution' 

    def _pac_ant(self, cr, uid, context):
        # primera vez: peso de la evaluacion
        # las otras veces: el peso de la evolucion anterior
        if not context or not context.get('evaluation_id', False):
            return False
        evols = self.pool.get('oemedical.bariatric.evolution').search(cr, uid, [])
        if len(evols) > 0:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, [evols[len(evols)]], context=context)[0]
            return evol.pes_ini
        else:
            eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, [context.get('evaluation_id', False)], context=context)[0]
            return eval.epa_pac
        
    def _imc_ant(self, cr, uid, context):
        # primera vez: peso de la evaluacion
        # las otras veces: el peso de la evolucion anterior
        if not context or not context.get('evaluation_id', False):
            return False
        evols = self.pool.get('oemedical.bariatric.evolution').search(cr, uid, [])
        if len(evols) > 0:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, [evols[len(evols)]], context=context)[0]
            return evol.imc_ini
        else:
            eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, [context.get('evaluation_id', False)], context=context)[0]
            return eval.epa_imc
    
    def _imc_hoy(self, cr, uid, ids, name, args, context=None):
        res = {}
        evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids, context=context)[0]
        eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, [evol.evaluation_id.id], context=context)[0]
        res[evol.id] = 0.0
        if eval.epa_tal > 0.0:
            res[evol.id] = evol.evo_peso_hoy / (eval.epa_tal * eval.epa_tal)
        return res
  
    def _peso_perdido(self, cr, uid, ids, name, args, context=None):
        # primera vez: peso de inicio (epa_pac) de la evaluacion menos peso de hoy
        # para las demas: peso inicial de la evolucion anterior (pes_ini) menos el peso de hoy
        evols = 0
        res = {}
        evols = self.pool.get('oemedical.bariatric.evolution').search(cr, uid, [])
        if len(evols) > 1:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids[-1], context=context)
        else:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids, context=context)[0]
            eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, [evol.evaluation_id.id], context=context)[0] 
            res[evol.id] = 0.0
            res[evol.id] = eval.epa_pac - evol.evo_peso_hoy
        return res
  
    def _imc_perdido(self, cr, uid, ids, name, args, context=None):
        # primera vez: imc de la evaluacion menos el imc de hoy
        # otras veces: imc de la evolucion anterior menos el imc de hoy
        evols = 0
        res = {}
        evols = self.pool.get('oemedical.bariatric.evolution').search(cr, uid, [])
        if len(evols) > 1:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids[-1], context=context)
            res[evol.id] = evol.pes_ini - evol.evo_peso_hoy
        else:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids, context=context)[0]
            res[evol.id] = 0.0
            eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, [evol.evaluation_id.id], context=context)[0]
            if eval.epa_tal > 0.0:
                res[evol.id] = eval.epa_imc - round((evol.evo_peso_hoy / (eval.epa_tal * eval.epa_tal)),2)
        return res
    
    def _exceso_peso(self, cr, uid, ids, field_name, arg, context=None):
        # primera vez: peso de hoy menos peso ideal de la evaluacion
        # las otras veces: el peso de la evolucion anterior menos peso ideal de la evaluacion
        evols = 0
        evols = self.pool.get('oemedical.bariatric.evolution').search(cr, uid, [])
        res = {}
        if len(evols) > 1:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids[-1], context=context)
            res[evol.id] = evol.pes_ini - evol.evo_peso_hoy
        else:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids, context=context)[0]
            res[evol.id] = 0.0
            eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, [evol.evaluation_id.id], context=context)[0]
            res[evol.id] = evol.evo_peso_hoy - eval.epa_pid
        return res

    def _perc_pep(self, cr, uid, ids, field_name, arg, context=None):
        # primera vez: peso perdido de la evolucion actual * 100 / exceso de peso de la evaluacion
        # las otras veces: peso perdido de la evolucion actual * / exceso de peso de la evolucion anterior
        evols = 0
        evols = self.pool.get('oemedical.bariatric.evolution').search(cr, uid, [])
        res = {}
        if len(evols) > 1:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids[-1], context=context)
            res[evol.id] = evol.pes_ini - evol.evo_peso_hoy
        else:
            evol = self.pool.get('oemedical.bariatric.evolution').browse(cr, uid, ids, context=context)[0]
            res[evol.id] = 0.0
            eval = self.pool.get('oemedical.bariatric.evaluation').browse(cr, uid, [evol.evaluation_id.id], context=context)[0]
            if eval.epa_pex > 0.0:
                res[evol.id] = (eval.epa_pac - evol.evo_peso_hoy) * 100.00 / eval.epa_pex
        return res
    
    _columns = {
                'evaluation_id':fields.many2one('oemedical.bariatric.evaluation', 'Evaluación : ', required=True),
                'doctor': fields.many2one('oemedical.physician', string='Doctor : '),
                'evo_date': fields.date(string='Fecha', readonly=True),
                'cir_date': fields.date(string='Fecha cirugia : ', ),
                'cir_tmp': fields.date(string='Tiempo cirugia : ', ),
                'pes_ini': fields.related('evaluation_id', 'epa_pac',type='float', string='Peso inicio : '),
                'imc_ini': fields.related('evaluation_id', 'epa_imc',type='float', string='IMC inicio : ' ),
                'cir_tip': fields.char(size=60, string='Tipo cirugia : '),
                'evo_die': fields.char(string='Dieta : ', size=256),
                'evo_liq': fields.char(string='Liquidos : ', size=256),
                'evo_eje': fields.char(string='Ejercicio :', size=256),
                'evo_dep': fields.char(string='Deposición : ', size=256),
                'evo_vom': fields.char(string='Vomito : ', size=256),
                'evo_med': fields.char(string='Medicamento : ', size=256),
                'evo_peso_hoy': fields.float(string='Peso hoy : ', digits=(3,2)),
                'evo_imc_hoy': fields.function(_imc_hoy, type='float', string='IMC hoy : ', digits=(3,2), store=True),
                'evo_pes_perd': fields.function(_peso_perdido, type='float', string='Peso perdido : ', digits=(3,2), store=True),
                'evo_imc_perd': fields.function(_imc_perdido, type='float', string='IMC perdido : ', digits=(3,2), store=True),
                'evo_exceso_pes': fields.function(_exceso_peso, type='float', string='Exceso peso : ', digits=(3,2), store=True),
                'evo_perc_pep': fields.function(_perc_pep, type='float', string='% PEP : ', digits=(3,2), store=True),
                'evo_hta': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='HTA :'),
                'evo_hdr': fields.char(string='Duración :', size=256),
                'evo_hmd': fields.char(string='Medicación :', size=256),
                'evo_hdc': fields.char(string='Dosis :', size=256),
                'evo_dm': fields.selection([
                                          ('s', 'Si'),
                                          ('n', 'No'),
                                          ], string='DM :'),
                'evo_ddr': fields.char(string='Duración :', size=256),
                'evo_dmd': fields.char(string='Medicación :', size=256),
                'evo_ddc': fields.char(string='Dosis :', size=256),
                'evo_dlp': fields.selection([
                                          ('s', 'Si'),
                                          ('n', 'No'),
                                          ], string='DLP :'),
                'evo_ldr': fields.char(string='Duración :', size=256),
                'evo_lmd': fields.char(string='Medicación :', size=256),
                'evo_ldc': fields.char(string='Dosis :', size=256),
                'evo_apn': fields.selection([
                                           ('s', 'Si'),
                                           ('n', 'No'),
                                           ], string='Apnea :'),
                'evo_adr': fields.char(string='Duración :', size=256),
                'evo_amd': fields.char(string='Medicación :', size=256),
                'evo_adc': fields.char(string='Dosis :', size=256),
                'evo_ost': fields.selection([
                                          ('s', 'Si'),
                                          ('n', 'No'),
                                          ], string='Osteoartritis :'),
                'evo_odr': fields.char(string='Duración :', size=256),
                'evo_omd': fields.char(string='Medicación :', size=256),
                'evo_odc': fields.char(string='Dosis :', size=256),
                'evo_sop': fields.selection([
                                          ('s', 'Si'),
                                          ('n', 'No'),
                                          ], string='SOP :'),
                'evo_sdr': fields.char(string='Duración :', size=256),
                'evo_smd': fields.char(string='Medicación :', size=256),
                'evo_sdc': fields.char(string='Dosis :', size=256),
                'evo_hg': fields.selection([
                                          ('s', 'Si'),
                                          ('n', 'No'),
                                          ], string='HG :'),
                'evo_cole': fields.selection([
                                          ('s', 'Si'),
                                          ('n', 'No'),
                                          ], string='COLE :'),
                'evo_compli': fields.selection([
                                          ('s', 'Si'),
                                          ('n', 'No'),
                                          ], string='Complicaciones :'),
                'evo_compli_cual': fields.text(string='Cual :',),
                'evo_compli_tto': fields.text(string='TTO :',),
                'evo_coment': fields.text(string='Comentarios :',),
                'evo_pres_1': fields.char(size=60, string='OMEPRAZOL :',),
                'evo_pres_2': fields.char(size=60, string='NEUROBION :',),
                'evo_pres_3': fields.char(size=60, string='HIERRO :',),
                'evo_pres_4': fields.char(size=60, string='CALCIO :',),
                'evo_pres_5': fields.char(size=60, string='SUPLEMENTO :',),
                'evo_pres_6': fields.char(size=60, string='PROTEINA :',),
                'evo_pres_7': fields.char(size=60, string='EJERCICIO :',),
                'evo_pres_exam': fields.char(size=60, string='EXAMENES :',),
                'evo_pres_nutri': fields.char(size=60, string='NUTRICIONISTA :',),
                'evo_pres_psico': fields.char(size=60, string='PSICOLOGA :',),
                'evo_pres_otro': fields.char(size=60, string='OTROS :',),
                'evo_exam_ctl_1': fields.char(size=256, string='Leucos :',),
                'evo_exam_ctl_2': fields.char(size=256, string='HB :',),
                'evo_exam_ctl_3': fields.char(size=256, string='HCTO :',),
                'evo_exam_ctl_4': fields.char(size=256, string='TGO :',),
                'evo_exam_ctl_5': fields.char(size=256, string='TGP :',),
                'evo_exam_ctl_6': fields.char(size=256, string='BIL D :',),
                'evo_exam_ctl_7': fields.char(size=256, string='GGT :',),
                'evo_exam_ctl_8': fields.char(size=256, string='PROT :',),
                'evo_exam_ctl_9': fields.char(size=256, string='ALBUBINA :',),
                'evo_exam_ctl_10': fields.char(size=256, string='COLESTEROL :',),
                'evo_exam_ctl_11': fields.char(size=256, string='TG :',),
                'evo_exam_ctl_12': fields.char(size=256, string='HDL :',),
                'evo_exam_ctl_13': fields.char(size=256, string='LDL :',),
                'evo_exam_ctl_14': fields.char(size=256, string='VLDL :',),
                'evo_exam_ctl_15': fields.char(size=256, string='GLUCOSA :',),
                'evo_exam_ctl_16': fields.char(size=256, string='CREATININA :',),
                'evo_exam_ctl_17': fields.char(size=256, string='AC URICO :',),
                'evo_exam_ctl_18': fields.char(size=256, string='BUM :',),
                'evo_exam_ctl_19': fields.char(size=256, string='HG GLIC :',),
                'evo_exam_ctl_20': fields.char(size=256, string='T3 :',),
                'evo_exam_ctl_21': fields.char(size=256, string='T4 :',),
                'evo_exam_ctl_22': fields.char(size=256, string='TSH :',),
                'evo_exam_ctl_23': fields.char(size=256, string='NA :',),
                'evo_exam_ctl_24': fields.char(size=256, string='K :',),
                'evo_exam_ctl_25': fields.char(size=256, string='CALCIO :',),
                'evo_exam_ctl_26': fields.char(size=256, string='CA ION :',),
                'evo_exam_ctl_27': fields.char(size=256, string='P :',),
                'evo_exam_ctl_28': fields.char(size=256, string='OTRO :',),
                }
            
            
    _defaults = {
                 'evo_date': time.strftime('%Y-%m-%d'),
                 'evaluation_id': lambda self, cr, uid, context: context.get('evaluation_id', False),
                 #'pes_ini': _pac_ant,
                 #'imc_ini': _imc_ant,
                }
        
OeMedicalBariatricEvolution()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
