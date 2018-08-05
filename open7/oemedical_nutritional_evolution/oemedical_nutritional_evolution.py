# -*- encoding: utf-8 -*-
 
#importamos la clase osv del modulo osv y fields
import time
from openerp.osv import fields, osv, orm
from time import strftime
 
 
class OeMedicalNutritionalEvolution(osv.osv):
   
    _name = 'oemedical.nutritional.evolution' 

    def get_epp(self, cr, uid, ids, name, args, context=None):
        res = {}
        for r in self.browse(cr, uid, ids, context=context):
            res[r.id] = ((r.pso_ant - r.pso_act) / r.exs_ini) * 100.00 if r.exs_ini and r.pso_ant else 0
        return res
    
    def get_imc2(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.pso_act / (r.tal_ini * r.tal_ini) if r.tal_ini != 0 else 0 
           print "IMC", res
        return res
    
    
    _columns = {
                'evaluation_id':fields.many2one('oemedical.nutritional', 'Evaluación : ', required=True),
                'doctor': fields.many2one('oemedical.physician', string='Doctor : '),
                'patient_id':fields.many2one('oemedical.patient', 'Paciente', required=True),
                'imc_ini':fields.related('evaluation_id', 'imc', type='float'),
                'tal_ini':fields.related('evaluation_id', 'est_pac', type='float'),
                'exs_ini': fields.related('evaluation_id', 'exs_pes', type='float'),
                #'pak_ini':fields.related('patient_id', 'pea_pok', type='float'),
                #'date_str': fields.function(_date_to_str, store=True, string='Fecha', type='char', size=8),
                'date_nut': fields.date(string='Fecha', readonly=True),
                'pso_act': fields.float(string='Peso actual Kg: ',digits=(12,6), required=True),
                'pso_ant': fields.related('evaluation_id', 'pea_pok', type='float', string='Peso anterior Kg :', readonly=True),
                'pgr_act': fields.float(string='Porcentaje actual de grasa %: ',digits=(12,6)),
                'pgr_ant': fields.float(string='Porcentaje ant de grasa %: ',digits=(12,6)),
                'cin_act': fields.float(string='Medida Cintura actual (cm): ',digits=(12,6)),
                'cin_ant': fields.related('evaluation_id', 'cin_pac', type='float', string='Medida cintura anterior (cm): ', readonly=True),
                'imc_cot': fields.function(get_imc2, type='float', string='IMC: '),
                'exp_per': fields.function(get_epp, type='float', string='Exeso de peso perdido : ', readonly=True),
                #Control
                'date_control': fields.date(string='Fecha de Control', readonly=True),
                'cita': fields.integer(string='Cita'),
                'tip_dta': fields.text(string='Tipo de Dieta:'),
                'sup_prt': fields.char(size=256, string='Suplemento proteico'),
                'sup_vit': fields.char(size=256, string='Suplemento vitamínico'),
                'eje_dia': fields.selection([
                                           ('s', 'Si'),
                                           ('n', 'No'),
                                           ], string='Hace Ejercicio :'),
                'eje_freq': fields.integer(string='Nro Veces:'),
                'tie_eje': fields.integer(string='Tiempo (minutos):'),
                'car_die':fields.text('Características de la dieta :'),
                'hidratacion': fields.char('Hidratación', size=100),
                'observ': fields.text(string='Observación :'),
                }
            
            
    _defaults = {
                 'date_nut': time.strftime('%Y-%m-%d'),
                 'evaluation_id': lambda self, cr, uid, context: context.get('evaluation_id', False),
                }
            
    
        
OeMedicalNutritionalEvolution()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
