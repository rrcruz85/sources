# -*- encoding: utf-8 -*-
 
#importamos la clase osv del modulo osv y fields
import time
from openerp.osv import fields, osv, orm
from time import strftime
 
 
class OeMedicalNutritional(osv.osv):
   
    _name = 'oemedical.nutritional' 
    
    def _compute_imc(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.nutritional').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        if eval.est_pac > 0.0:
            res[eval.id] = eval.pea_pok / (eval.est_pac * eval.est_pac)

        return res
    
    def _compute_plb(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.nutritional').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_pac * 2.2

        return res

    def _compute_pid(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.nutritional').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_tal * eval.epa_tal * 25.0

        return res

    def _compute_pex(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.nutritional').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_pac - eval.epa_pid

        return res

    def _compute_pep(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.nutritional').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_pex / 2.0

        return res

    def _compute_exi(self, cr, uid, ids, name, args, context=None):
        res = {}
        eval = self.pool.get('oemedical.nutritional').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        res[eval.id] = eval.epa_tal * eval.epa_tal * 25.0 + eval.epa_pep

        return res
    
    def get_tkc(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.des_kca + r.mma_kca + r.alm_kca + r.mta_kca + r.cen_kca
           print "TOTALKCAL", res
        return res
    
    def get_imc(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.pea_pok / (r.est_pac * r.est_pac)
           print "IMC", res
        return res
    
    def get_pik(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = (r.est_pac * r.est_pac) * 25
           print "PESOIDEALKG", res
        return res
    
    def get_pil(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.pei_pek * 2.2
           print "PIL", res
        return res
    
    def get_icc(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        eval = self.pool.get('oemedical.nutritional').browse(cr, uid, ids, context=context)[0]
        res[eval.id] = 0
        if eval.cad_pac > 0.0:
            res[eval.id] = eval.cin_pac / eval.cad_pac
        return res
    
        
    
    def get_exp(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.pea_pok - r.max_prk
           print "EXP", res
        return res
    
    def get_pml(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.max_pak * 2.2
           print "PML", res
        return res
    
    def get_pnl(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.min_pak * 2.2
           print "PNL", res
        return res
    
    def get_psl(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.pes_pak * 2.2
           print "PSL", res
        return res
    
    def get_pol(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.pob_pok * 2.2
           print "POL", res
        return res
    
    def get_mrl(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.max_prk * 2.2
           print "MRL", res
        return res
    
    def get_pal(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.max_prk * 2.2
           print "PAL", res
        return res
    
    def get_prk(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.est_pac * r.est_pac * 25.0
           print "PRK", res
        return res
    
    def get_exl(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        res = {}
        for r in records:
           res[r.id] = r.exs_pes * 2.2
           print "EXL", res
        return res
        
    _columns={
                'patient_id':fields.many2one('oemedical.patient', 'Paciente', required=True),
                'doctor': fields.many2one('oemedical.physician', string='Doctor'),
                'eva_date': fields.date(string='Fecha de Evaluación'),
                'fec_cir': fields.date(string='Fecha de Cirugía'),
                'cita': fields.integer(string='Cita'),
                'tip_dta': fields.text(string='Tipo de Dieta:'),
                'met_qur': fields.char(size=256, string='Método Quirúrgico :'),
                'com_con': fields.char(size=256, string='Como llego a la consulta? :'),
                'vec_com': fields.char(size=20, string='Cuantas veces al día come? :'),
                'hab_des': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ('a', 'A veces'),
                                        ], string='Tiene el hábito de desayunar? :'),
                'reg_com': fields.selection([
                                        ('c', 'Casa'),
                                        ('r', 'Restaurante'),
                                        ('o', 'Oficna'),
                                        ('l', 'Lleva comida de casa'),
                                        ], string='Regularmente donde come? :'),
                'com_com': fields.selection([
                                        ('r', 'Rapido'),
                                        ('l', 'Lento'),
                                        ('n', 'Normal'),
                                        ], string='Come :'),
                'ans_com': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Ansiedad? :'),
                'pic_dia': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Pica durante el día? :'),
                'sin_cnt': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Sindrome de comedor nocturno? :'),
                'mod_hal': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Ha modificado sus hábitos alimentarios? :'),
                'por_qha': fields.char(size=256, string='Por qué? :'),
                'ioa_alm': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Intolerancia o alergias alimentarias? :'),
                'cua_ioa': fields.char(size=256, string='Cuales? :'),
                'mez_car': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Mezcla carbohidratos? :'),
                'frq_car': fields.char(size=256, string='Frecuencia :'),
                'con_frt': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Consumo de Frituras :'),
                'frq_frt': fields.char(size=256, string='Frecuencia :'),
                'tom_joa': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Al comer toma jugo o agua? :'),
                'frq_tom': fields.char(size=256, string='Frecuencia :'),
                'con_sal': fields.selection([
                                        ('n', 'Normal'),
                                        ('a', 'Alto'),
                                        ('b', 'Bajo'),
                                        ], string='Consumo de sal :'),
                'sal_ext': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Se pone sal extra? :'),
                'con_snk': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Consume snacks? :'),
                'frq_snk': fields.char(size=256, string='Frecuencia :'),
                'con_azu': fields.selection([
                                        ('n', 'Normal'),
                                        ('a', 'Alto'),
                                        ('b', 'Bajo'),
                                        ], string='Consumo de azucar :'),
                'azu_ext': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Se pone azucar extra? :'),
                'con_dlc': fields.char(size=256, string='Consumo de dulces :'),
                'con_cfe': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Consume café? :'),
                'cta_dia': fields.integer(string='Cuántas tazas al día? :'),
                'con_baz': fields.selection([
                                        ('d', 'Diario'),
                                        ('s', 'Semanal'),
                                        ('o', 'Ocacional'),
                                        ], string='Consumo de bebidas azucaradas :'),
                'azc_bln': fields.boolean(string='Azucar blanca'),
                'miel': fields.boolean(string='Miel'),
                'azc_mor': fields.boolean(string='Azucar morena'),
                'pan_ras': fields.boolean(string='Panela'),
                'sin_azu': fields.boolean(string='Sin nada de azúcar'),
                'edu_azu': fields.boolean(string='Mixto, edulcorante + azúcar'),
                'tip_edu': fields.boolean(string='Edulcorante'),
                'edu_usa': fields.char(size=256, string='Que edulcorante usa? :'),
                'sbe_dia': fields.integer(string='Cuántos sobres al día? :'),
                'vda_dia': fields.integer(string='Cuántos vasos de agua pura toma al día? : '),
                'vda_dia1': fields.char(size=256, string='Cuántos vasos de agua pura toma al día? : '),
                'prf_ali': fields.text(string='Preferencias alimentarias :'),
                'dis_ali': fields.text(string='Disgustos alimentarios :'),
                'con_alc': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Consume alcohol? :'),
                'frq_cal': fields.char(size=256, string='Frecuencia :'),
                'con_cig': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Fuma? :'),
                'frq_cig': fields.char(size=256, string='Frecuencia :'),
                'ale_mdc': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Alergia a algún medicamento? :'),
                'que_mdc': fields.char(size=256, string='Cuál? :'),
                'tom_mdc': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Toma medicación continua o suplemento alimentario? :'),
                'cal_mdc': fields.char(size=500, string='Cuáles? :'),
                'tom_asp': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Toma aspirina? :'),
                'tmp_tap': fields.char(size=500, string='Que tiempo? :'),
                'pln_tnh': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Planea tener hijos? :'),
                'can_tnh': fields.char(size=500, string='Cuándo? :'),
                'met_ant': fields.char(size=500, string='Metodo anticonceptivo? :'),
                'fam_hcb': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Familiar que se ha hecho la CB? :'),
                'fam_qun': fields.char(size=500, string='Quién? :'),
                'con_dep': fields.selection([
                                        ('s', 'Sedentario'),
                                        ('m', 'Moderado'),
                                        ('a', 'Activo'),
                                        ('t', 'Muy activo'),
                                        ('d', 'Deportista'),
                                        ], string='Te consideras? :'),
                'lgh_eje': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Le gusta hacer ejercicio? :'),
                'pct_eje': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Practica algún ejercicio? :'),
                'lgh_eje': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Le gusta hacer ejercicio? :'),
                'cvs_pre': fields.char(size=500, string='Cuantas veces a la semana? :'),
                'qdp_pra': fields.char(size=500, string='Que deporte practica? :'),
                'pro_pac': fields.char(size=500, string='Profesión :'),
                'ofi_cmp': fields.selection([
                                        ('p', 'De pie'),
                                        ('s', 'Sentado'),
                                        ('m', 'Mixto'),
                                        ], string='La mayor parte del tiempo pasa :'),
                #Patologías Preoperatorio
                'preop_hta': fields.boolean(string='Hipertension Arterial (HTA)'),
                'hip_preop_med': fields.char(string='Medicacion'),
                'hip_preop_dos': fields.char(string='Dosis'),
                'hip_preop_val': fields.char(string='Valores de Laboratorio'),
                'hip_preop_hac': fields.char(string='Hace que tiempo'),

                'diab_mel_dm': fields.boolean(string='Diabetes Melitus (DM)'),
                'diab_mel_med': fields.char(string='Medicacion'),
                'diab_mel_dos': fields.char(string='Dosis'),
                'diab_mel_val': fields.char(string='Valores de Laboratorio'),
                'diab_mel_hac': fields.char(string='Hace que tiempo'),

                'preop_dis': fields.boolean(string='Dislipidemias'),
                'preop_dis_med': fields.char(string='Medicacion'),
                'preop_dis_dos': fields.char(string='Dosis'),
                'preop_dis_val': fields.char(string='Valores de Laboratorio'),
                'preop_dis_hac': fields.char(string='Hace que tiempo'),

                'hig_gra': fields.boolean(string='Higado Graso'),
                'hig_gra_med': fields.char(string='Medicacion'),
                'hig_gra_dos': fields.char(string='Dosis'),
                'hig_gra_val': fields.char(string='Valores de Laboratorio'),
                'hig_gra_hac': fields.char(string='Hace que tiempo'),
                
                'otr_pat': fields.boolean(string='Otras'),
                'otr_pat_med': fields.char(string='Medicacion'),
                'otr_pat_dos': fields.char(string='Dosis'),
                'otr_pat_val': fields.char(string='Valores de Laboratorio'),
                'otr_pat_hac': fields.char(string='Hace que tiempo'),
                
                'pro_vom': fields.boolean(string='Vómito'),
                'pro_nau': fields.boolean(string='Nausea'),
                'pro_drr': fields.boolean(string='Diarrea'),
                'pro_aci': fields.boolean(string='Acidez'),
                'pro_flt': fields.boolean(string='Flatulencia'),
                'pro_est': fields.boolean(string='Estreñimiento'),
                'frq_dep1': fields.char(size=65, string='Frecuencia de la deposición al día: '),
                'frq_dep': fields.integer(string='Frecuencia de la deposición al día: '),
                'pro_gas': fields.boolean(string='Gastritis'),
                'pro_hel': fields.boolean(string='Helicobacter'),
                'des_hel': fields.char(string='Evaluacion Endoscopia', size=256),
                'pro_rge': fields.boolean(string='Reflujo Gastro_Esofagico'),
                'pro_ulc': fields.boolean(string='Ulceras'),
                'pro_cir': fields.boolean(string='Colon Irritable'),
                'pro_dia': fields.boolean(string='Diabetes'),
                'tmp_dia': fields.char(string='Hace que tiempo?: ', size=50),
                'pre_dia': fields.boolean(string='Pre-Diabetes'),
                'pro_hta': fields.boolean(string='HTA'),
                'pro_dsp': fields.boolean(string='Dislipidemias'),
                'pro_hpu': fields.boolean(string='Hiperuricemia'),
                'pro_hgr': fields.boolean(string='Higado graso'),
                'pro_aps': fields.boolean(string='Apnea del sueño'),
                'pro_aod': fields.boolean(string='Artrosis o dolor articular'),
                'pro_pco': fields.boolean(string='Problemas coronarios'),
                'pro_her': fields.boolean(string='Hernias'),
                'pro_dvr': fields.boolean(string='Divertículos'),
                'pro_tir': fields.boolean(string='Problemas tiroideos'),
                'pro_otr': fields.boolean(string='Otras'),
                'pro_dot1': fields.text(string='Descripción :'),
		        'pro_dot': fields.char(string='Descripción : ', size=100),
                'prf_dia': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Diabetes'),
                'par_dia': fields.char(size=200, string='Parentesco :'),
                'prf_ptr': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Problemas tiroideos'),
                'par_prt': fields.char(size=200, string='Parentesco :'),
                'prf_car': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Problemas cardiacos'),
                'par_car': fields.char(size=200, string='Parentesco :'),
                'prf_hip': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Hipertensión'),
                'par_hip': fields.char(size=200, string='Parentesco :'),
                'prf_oys': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Obesidad / Sobrepeso'),
                'par_oys': fields.char(size=200, string='Parentesco :'),
                'prf_dis': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Dislipidemias'),
                'par_dis': fields.char(size=200, string='Parentesco :'),
                #Recordatorio de 24 horas
                'des_hor': fields.char(string='Hora', size=50),
                'des_aar': fields.boolean(string='Agua aromática'),
                'des_bat': fields.boolean(string='Batidos'),
                'des_ayu': fields.boolean(string='Ayunas'),
                'des_cea': fields.boolean(string='Café en agua'),
                'des_cel': fields.boolean(string='Café en Leche'),
                'des_lec': fields.char(string='Cantidad de leche', size=250),
                'des_tle': fields.selection([
                                        ('e', 'Entera'),
                                        ('s', 'Semidescremada'),
                                        ('d', 'Descremada'),
                                        ('m', 'Deslactosada semidescremeda'),
                                        ('n', 'Deslactosada descremeda'),
                                        ], string='Tipo de leche'),
                'des_azu': fields.boolean(string='Azucar'),
                'des_lsl': fields.boolean(string='Leche sola'),
                'des_lyc': fields.boolean(string='Leche y café'),
                'des_yog': fields.boolean(string='Yogurt'),
                'des_tla': fields.selection([
                                        ('e', 'Entera'),
                                        ('s', 'Semidescremada'),
                                        ('d', 'Descremada'),
                                        ], string='Tipo de lacteo'),
                'des_azl': fields.boolean(string='Azucar'),
                'des_pae': fields.selection([
                                        ('i', 'Integral'),
                                        ('s', 'Blanco'),
                                        ], string='Pan entero'),
                'des_rbn': fields.selection([
                                        ('i', 'Integral'),
                                        ('s', 'Blanco'),
                                        ], string='Pan rbn'),
                'des_cer': fields.boolean(string='Cereal'),
                'des_arr': fields.boolean(string='Arroz'),
                'des_otr': fields.boolean(string='Otros'),
                'des_dot': fields.char(string='Descripción', size=100),
                'des_que': fields.boolean(string='Queso'),
                'des_tqu': fields.char(string='Tipo de queso', size=100),
                'des_jam': fields.boolean(string='Jamón'),
                'des_pyc': fields.boolean(string='Pollo/Carne'),
                'des_hue': fields.boolean(string='Huevo'),
                'des_pre': fields.text(string='Preparación'),
                'des_fre': fields.boolean(string='Fruta entera'),
                'des_frp': fields.boolean(string='Fruta picada'),
                'des_jup': fields.boolean(string='Jugo puro'),
                'des_jua': fields.boolean(string='Jugo con agua'),
                'des_azf': fields.boolean(string='Azucar'),
                'des_man': fields.boolean(string='Mantequilla'),
                'des_mar': fields.boolean(string='Margarina'),
                'des_ace': fields.boolean(string='Aceite'),
                'des_mcr': fields.boolean(string='Manteca de cerdo'),
                'ext_inf': fields.text('Información Adicional'),
                'des_kca': fields.integer(string='KCal : '),
                #1/2 mañana
                'mma_hor': fields.char(string='Hora', size=5),
                'mma_snc': fields.char(string='Snack', size=256),
                'mma_frt': fields.boolean(string='Fruta'),
                'mma_ygt': fields.boolean(string='Yogurt'),
                'mma_otr': fields.char(string='Otro', size=256),
                'mma_kca': fields.integer(string='KCal : '),
                #Almuerzo
                'alm_hor': fields.char(string='Hora', size=5),
                'alm_sop': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ('a', 'A veces'),
                                        ], string='Sopa'),
                'alm_con': fields.selection([
                                        ('p', 'Proteínas'),
                                        ('c', 'CHO'),
                                        ('v', 'Verduras'),
                                        ], string='Contenido de la sopa'),
                'alm_asp': fields.selection([
                                        ('e', 'Espesa'),
                                        ('l', 'Líquida'),
                                        ], string='Consistencia de la Sopa'),
                #plato fuerte
                'alm_arr': fields.boolean(string='Arroz'),
                'alm_pco': fields.boolean(string='Papa cocida'),
                'alm_pfr': fields.boolean(string='Papa frita'),
                'alm_fid': fields.boolean(string='Fideo'),
                'alm_pas': fields.boolean(string='Pasta'),
                'alm_cam': fields.boolean(string='Camote'),
                'alm_grm': fields.boolean(string='Granos y menestras'),
                'alm_otr': fields.char(string='Otros', size=500),
                'alm_ver': fields.selection([
                                        ('s', 'Siempre'),
                                        ('n', 'No siempre'),
                                        ('a', 'A veces'),
                                        ('u', 'Nunca'),
                                        ], string='Verduras'),
                'alm_grn': fields.boolean(string='Con granos'),
                'alm_pol': fields.boolean(string='Pollo'),
                'alm_pes': fields.boolean(string='Pescado'),
                'alm_atn': fields.selection([
                                        ('g', 'Agua'),
                                        ('c', 'Aceite'),
                                        ], string='Atún'),
                'alm_cro': fields.boolean(string='Carne roja'),
                'alm_emb': fields.boolean(string='Embutidos'),
                'alm_grs': fields.char(string='Grasa', size=500),
                #De tomar
                'alm_agu': fields.boolean(string='Agua'),
                'alm_te': fields.boolean(string='Té'),
                'alm_coc': fields.boolean(string='Coca cola'),
                'alm_jup': fields.boolean(string='Jugo puro'),
                'alm_jua': fields.boolean(string='Jugo con agua'),
                'alm_azb': fields.char(string='Azucar en la bebida', size=500),
                'alm_pos': fields.boolean(string='Postre'),
                'alm_tps': fields.char(string='Cuál postre? :', size=100),
                'alm_frp': fields.char(string='Frecuencia con que consume postre :', size=500),
                'exi_alm': fields.text(string='Información Adicional del Almuerzo'),
                'alm_kca': fields.integer(string='KCal : '),
                #1/2 tarde
                'mta_hor': fields.char(string='Hora', size=5),
                'mta_snc': fields.char(string='Snack', size=256),
                'mta_frt': fields.boolean(string='Fruta'),
                'mta_ygt': fields.boolean(string='Yogurt'),
                'mta_otr': fields.char(string='Otro', size=256),
                'mta_kca': fields.integer(string='KCal : '),
                #Cena
                'cen_hor': fields.char(string='Hora', size=5),
                'cen_alm': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Come como un almuerzo? :'),
                'exi_cen': fields.text(string='Información Adicional Cena'),
                'cen_kca': fields.integer(string='KCal : '),
                'tot_kca': fields.function(get_tkc, type='float', string='Total de KCal : ', readonly=True),
                'fds_com': fields.selection([
                                        ('f', 'Fuera'),
                                        ('e', 'En casa'),
                                        ], string='Fin de semana come :'),
                'fds_dia': fields.integer(string='¿Cuántos días sale a comer fuera? :'),
                'fds_cpf': fields.char(string='Que come por fuera', size=500),
                #Datos antropometricos y crono patología del peso corporal
                'ini_obe': fields.selection([
                                        ('i', 'Infancia'),
                                        ('d', 'Adolescencia'),
                                        ('a', 'Adultez'),
                                        ('l', 'Luego del embarazo'),
                                        ('s', 'Sociales (Divorcio / casamiento)'),
                                        ], string='Inicio de la obesidad :'),
                'int_otr': fields.char(string='Otros', size=500),
                'int_ppp': fields.char(string='Intentos previos de perdida de peso', size=500),
                'vis_nut': fields.selection([
                                        ('s', 'Si'),
                                        ('n', 'No'),
                                        ], string='Ha visitado al nutricionista :'),
                 'mot_ppp': fields.char(string='Motivaciones para perder peso / cirugía :', size=500),
                 'min_pak': fields.float(string='Cuál es el peso mínimo alcanzado en Kg :', digits=(2,2)),
                 'min_pal': fields.function(get_pnl, type='float', string='Peso mínimo alcanzado en Lb :', readonly=True),
                 'min_hac': fields.char(string='Hace :', size=500),
                 'max_pak': fields.float(string='Peso máximo alcanzado en Kg :', digits=(2,2)),
                 'max_pal': fields.function(get_pml, type='float', string='Peso máximo alcanzado en Lb :', readonly=True),
                 'pes_pak': fields.float(string='Peso antes de la cirugía en Kg :', digits=(2,2)),
                 'pes_pal': fields.function(get_psl, type='float', string='Peso antes de la cirugía en Lb :', readonly=True),
                 'imc': fields.function(_compute_imc, type='float', string='IMC (Kg/m2):', readonly=True),
                 'por_gde': fields.char(string='% de grasa DEXA', size=35),
                 'por_gbi': fields.char(string='% de grasa BIO', size=35),
                 'pes_kgm2': fields.float(string='Kg/m2:', digits=(2,2)),
                 'pea_pok': fields.float(string='Peso actual en Kg :', digits=(2,2)),
                 'pea_pol': fields.function(get_pal, type='float', string='Peso actual en Lb :', readonly=True),
                 'pei_pek': fields.function(get_pik, type='float', string='Peso ideal en Kg :', readonly=True),
                 'pei_pek1':fields.float(string='Peso ideal en Kg : ', digits=(2,2)),
                 'pei_pel': fields.function(get_pil, type='float', string='Peso ideal en Lb :', readonly=True),
                 'est_pac': fields.float(string='Talla (mts):', digits=(2,2), required=True),
                 'por_gra': fields.float(string='Porcentaje de grasa : %', digits=(2,2)),
                 'est_obe': fields.selection([
                                        ('n', 'Normopeso'),
                                        ('s', 'Sobrepeso I'),
                                        ('s2', 'Sobrepeso II'),
                                        ('o', 'Obesidad I'),
                                        ('o2', 'Obesidad II'),
                                        ('o3', 'Obesidad III'),
                                        ('so', 'Super obesidad'),
                                        ('sso', 'Super super obesidad'),
                                        ], string='Estado :'),
               'cin_pac': fields.float(string='Cintura : cm', digits=(2,2)), 
               'cad_pac': fields.float(string='Cadera : cm', digits=(2,2)),
               'pob_pok': fields.float(string='Peso objetivo en Kg :', digits=(2,2)),
               'pob_pol': fields.function(get_pol, type='float', string='Peso objetivo en Lb :', readonly=True),
               'exs_pes': fields.function(get_exp, type='float', string='Exceso de peso Kg:', readonly=True),
               'exs_pel': fields.function(get_exl, type='float', string='Exceso de peso Lb:', readonly=True),               
               'max_prk': fields.function(get_prk, type='float', string='Peso máximo recomendado en Kg :', readonly=True),
               'max_prl': fields.function(get_mrl, type='float', string='Peso máximo recomendado en Lb :', readonly=True),
               'min_prk': fields.float(string='Rango peso máximo Kg :', digits=(2,2)),
               'min_prl': fields.float(string='Rango peso mínimo Kg :', digits=(2,2)),
               'pac_age': fields.integer('Edad', size=2),
               'imc2': fields.function(_compute_imc, type='float', string='IMC (Kg/m2):', readonly=True),
               'diagnosis_ids' : fields.many2many('oemedical.pathology', 'oemedical_bariatric_diagnosis_rel', 'bariatric_id', 'diagnosis_id', 'diagnosis'),
               'bariatric_directions' : fields.text(string='Planes'),
               'icc': fields.function(get_icc, type='float', string='ICC:', readonly=True),
               'evolution_ids': fields.one2many('oemedical.nutritional.evolution', 'evaluation_id', 'Evoluciones'),               
               'es_diabetico': fields.boolean("Es diabético? :"),
               'diabetico': fields.char("Diabético", size=25, readonly=True),
            }
    
    _defaults = {
            'patient_id': lambda self, cr, uid, context: context.get('patient_id', False),
            #'eva_date': time.strftime('%Y-%m-%d'),
              }
            
OeMedicalNutritional()

class MedicalNutritional(osv.osv):

    _inherit = 'oemedical.patient'
    
    _columns = {
        'nut_eval': fields.one2many('oemedical.nutritional', 'patient_id', string='Evaluación Nutricional'),
    }

MedicalNutritional()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
