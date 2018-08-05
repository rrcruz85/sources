# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

def execute_query(cr, fieldname, patient_id):
    if fieldname and patient_id:
        cr.execute("select %s from oemedical_nutritional where patient_id = %s and eva_date in (select max(eva_date) from oemedical_nutritional where patient_id = %s)" % (fieldname, patient_id ,patient_id))
        result = cr.fetchone()
        return result[0] if ',' not in fieldname else result if result else False        
    else:
        return False   
 

class QuestionModel(osv.osv):
    _inherit = 'oemedical.question_model' 
    
    def _get_vals(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {}  
            res[obj.id]['hipertension_arterial_hta'] = False
            res[obj.id]['hipertension_medication'] = ''
            res[obj.id]['hipertension_dosis'] = ''
            res[obj.id]['hipertension_values'] = ''
            res[obj.id]['diabetes_melitus_dm'] = False
            res[obj.id]['diabetes_melitus_medication'] = ''
            res[obj.id]['diabetes_melitus_dosis'] = ''
            res[obj.id]['diabetes_melitus_values'] = ''
            res[obj.id]['dislipidemias'] = False
            res[obj.id]['dislipidemias_medication'] = ''
            res[obj.id]['dislipidemias_dosis'] = ''
            res[obj.id]['dislipidemias_values'] = ''
            res[obj.id]['higado_graso'] = False
            res[obj.id]['higado_graso_medication'] = ''
            res[obj.id]['higado_graso_dosis'] = ''
            res[obj.id]['higado_graso_values'] = ''
            
            result = execute_query(cr, 'preop_hta,hip_preop_med,hip_preop_dos,hip_preop_val,diab_mel_dm,diab_mel_med,diab_mel_dos,diab_mel_val,preop_dis,preop_dis_med,preop_dis_dos,preop_dis_val,hig_gra,hig_gra_med,hig_gra_dos,hig_gra_val', obj.patient_id.id)
            if result:                       
                res[obj.id] = {}
                res[obj.id]['hipertension_arterial_hta'] = result[0]
                res[obj.id]['hipertension_medication'] = result[1]
                res[obj.id]['hipertension_dosis'] = result[2]
                res[obj.id]['hipertension_values'] = result[3]
                res[obj.id]['diabetes_melitus_dm'] = result[4]
                res[obj.id]['diabetes_melitus_medication'] = result[5]
                res[obj.id]['diabetes_melitus_dosis'] = result[6]
                res[obj.id]['diabetes_melitus_values'] = result[7]
                res[obj.id]['dislipidemias'] = result[8]
                res[obj.id]['dislipidemias_medication'] = result[9]
                res[obj.id]['dislipidemias_dosis'] = result[10]
                res[obj.id]['dislipidemias_values'] = result[11]
                res[obj.id]['higado_graso'] = result[12]
                res[obj.id]['higado_graso_medication'] = result[13]
                res[obj.id]['higado_graso_dosis'] = result[14]
                res[obj.id]['higado_graso_values'] = result[15]
        return res
    
    _columns = {
        'hipertension_arterial_hta'  : fields.function(_get_vals, type='boolean', string='Hipertension Arterial (HTA)', multi = "vals"),
        'hipertension_medication'    : fields.function(_get_vals, type='char', string='Medicacion', multi = "vals"),
        'hipertension_dosis'         : fields.function(_get_vals, type='char', string='Dosis', multi = "vals"),
        'hipertension_values'        : fields.function(_get_vals, type='char', string='Valores de Laboratorio', multi = "vals"),
        
        'diabetes_melitus_dm'        : fields.function(_get_vals, type='boolean', string='Diabetes Melitus (DM)', multi = "vals"),
        'diabetes_melitus_medication': fields.function(_get_vals, type='char', string='Medicacion', multi = "vals"),
        'diabetes_melitus_dosis'     : fields.function(_get_vals, type='char', string='Dosis', multi = "vals"),
        'diabetes_melitus_values'    : fields.function(_get_vals, type='char', string='Valores de Laboratorio', multi = "vals"),
        
        'dislipidemias'              : fields.function(_get_vals, type='boolean', string='Dislipidemias', multi = "vals"),
        'dislipidemias_medication'   : fields.function(_get_vals, type='char', string='Medicacion', multi = "vals"),
        'dislipidemias_dosis'        : fields.function(_get_vals, type='char', string='Dosis', multi = "vals"),
        'dislipidemias_values'       : fields.function(_get_vals, type='char', string='Valores de Laboratorio', multi = "vals"),
        
        'higado_graso'               : fields.function(_get_vals, type='boolean', string='Higado Graso', multi = "vals"),
        'higado_graso_medication'    : fields.function(_get_vals, type='char', string='Medicacion', multi = "vals"),
        'higado_graso_dosis'         : fields.function(_get_vals, type='char', string='Dosis', multi = "vals"),
        'higado_graso_values'        : fields.function(_get_vals, type='char', string='Valores de Laboratorio', multi = "vals"),
    }
    
    _defaults={
        'hipertension_arterial_hta'  : lambda self, cr, uid, context:  execute_query(cr, 'preop_hta', context.get('patient_id', False)),
        'hipertension_medication'    : lambda self, cr, uid, context:  execute_query(cr, 'hip_preop_med', context.get('patient_id', False)),
        'hipertension_dosis'         : lambda self, cr, uid, context:  execute_query(cr, 'hip_preop_dos', context.get('patient_id', False)),
        'hipertension_values'        : lambda self, cr, uid, context:  execute_query(cr, 'hip_preop_val', context.get('patient_id', False)),
    
        'diabetes_melitus_dm'        : lambda self, cr, uid, context:  execute_query(cr, 'diab_mel_dm', context.get('patient_id', False)),
        'diabetes_melitus_medication': lambda self, cr, uid, context:  execute_query(cr, 'diab_mel_med', context.get('patient_id', False)),
        'diabetes_melitus_dosis'     : lambda self, cr, uid, context:  execute_query(cr, 'diab_mel_dos', context.get('patient_id', False)),
        'diabetes_melitus_values'    : lambda self, cr, uid, context:  execute_query(cr, 'diab_mel_val', context.get('patient_id', False)),
       
        'dislipidemias'              : lambda self, cr, uid, context:  execute_query(cr, 'preop_dis', context.get('patient_id', False)),
        'dislipidemias_medication'   : lambda self, cr, uid, context:  execute_query(cr, 'preop_dis_med', context.get('patient_id', False)),
        'dislipidemias_dosis'        : lambda self, cr, uid, context:  execute_query(cr, 'preop_dis_dos', context.get('patient_id', False)),
        'dislipidemias_values'       : lambda self, cr, uid, context:  execute_query(cr, 'preop_dis_val', context.get('patient_id', False)),
  
        'higado_graso'               : lambda self, cr, uid, context:  execute_query(cr, 'hig_gra', context.get('patient_id', False)),
        'higado_graso_medication'    : lambda self, cr, uid, context:  execute_query(cr, 'hig_gra_med', context.get('patient_id', False)),
        'higado_graso_dosis'         : lambda self, cr, uid, context:  execute_query(cr, 'hig_gra_dos', context.get('patient_id', False)),
        'higado_graso_values'        : lambda self, cr, uid, context:  execute_query(cr, 'hig_gra_val', context.get('patient_id', False)),
    }     
    
QuestionModel()
