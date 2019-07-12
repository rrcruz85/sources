# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import tools

def get_datetime(pdate, float_time):
    hour = int(float_time)
    minute = int(round(float_time - hour, 2) * 60)
    return datetime.strptime(str(pdate) + ' ' + str(hour) + '-' + str(minute), '%Y-%m-%d %H-%M')

class OeMedicalPatient(osv.Model):
    _inherit = 'oemedical.patient'

    _columns = {
        'is_pregnant': fields.boolean(string='Is Pregnant'),        
    }

OeMedicalPatient()

class OeMedicalMouthHealthIndicator(osv.Model):
    _name = 'oemedical.mouth.health.indicator'

    _columns = {
         'piece1': fields.selection([(16,16),(11,11),(26,26),(36,36),(31,31),(46,46)],'Pieza 1', required=True),
         'piece2': fields.selection([(17,17),(21,21),(27,27),(37,37),(41,41),(47,47)],'Pieza 2', required=True),
         'piece3': fields.selection([(55,55),(51,51),(65,65),(75,75),(71,71),(85,85)],'Pieza 3', required=True),
         'plate': fields.integer('Placa'),
         'stone': fields.integer('Calculo'),
         'genvitis': fields.integer('Gengivitis'),
         'dentist_test_id': fields.many2one('oemedical.odontology.exam',string='Examen Odontologico',required=True ),
    }

    def _check_piece1_repeated(self, cr, uid, ids):
        for ind in self.browse(cr, uid, ids):
            cant_piece1 = self.search(cr,uid,[('id','!=',ind.id),('dentist_test_id','=',ind.dentist_test_id.id),('piece1','=',ind.piece1)],count=True)
            if(cant_piece1 > 0):
                return False
        return True

    def _check_piece2_repeated(self, cr, uid, ids):
        for ind in self.browse(cr, uid, ids):
            cant_piece2 = self.search(cr,uid,[('id','!=',ind.id),('dentist_test_id','=',ind.dentist_test_id.id),('piece2','=',ind.piece2)],count=True)
            if(cant_piece2 > 0):
                return False
        return True

    def _check_piece3_repeated(self, cr, uid, ids):
        for ind in self.browse(cr, uid, ids):
            cant_piece3 = self.search(cr,uid,[('id','!=',ind.id),('dentist_test_id','=',ind.dentist_test_id.id),('piece3','=',ind.piece3)],count=True)
            if(cant_piece3 > 0):
                return False
        return True

    _constraints = [
                    (_check_piece1_repeated, _('La pieza 1 se encuentra repetida.'), []),
                    (_check_piece2_repeated, _('La pieza 2 se encuentra repetida.'), []),
                    (_check_piece3_repeated, _('La pieza 3 se encuentra repetida.'), []),
                ]

OeMedicalMouthHealthIndicator()

class OeMedicalOdontologyExam(osv.Model):
    _name='oemedical.odontology.exam'

    def _get_total_carie(self, cr, uid, ids, name, args, context):
        res = {}.fromkeys(ids,{'totalCarieD': 0, 'totalCarie_d': 0})
        
        for obj in self.browse(cr,uid,ids):
            res[obj.id]['totalCarieD'] =  obj.carieDC + obj.carieDP + obj.carieDO
            res[obj.id]['totalCarie_d'] =  obj.carie_dc + obj.carie_de + obj.carie_do
        
        return res

    def _get_total(self, cr, uid, ids, name, args, context):
        res = {}.fromkeys(ids, {'totalPlate': 0, 'totalStone': 0, 'totalGengivitis': 0})
        
        for obj in self.browse(cr,uid,ids):
            totalPlate = obj.section_1_placa + obj.section_2_placa + obj.section_3_placa + obj.section_4_placa + obj.section_5_placa + obj.section_6_placa
            totalStone = obj.section_1_calculo + obj.section_2_calculo + obj.section_3_calculo + obj.section_4_calculo + obj.section_5_calculo + obj.section_6_calculo
            totalGengivitis = obj.section_1_gingivitis + obj.section_2_gingivitis + obj.section_3_gingivitis + obj.section_4_gingivitis + obj.section_5_gingivitis + obj.section_6_gingivitis
           
            res[obj.id]['totalPlate'] =  totalPlate
            res[obj.id]['totalStone'] = totalStone
            res[obj.id]['totalGengivitis'] = totalGengivitis
        
        return res
    
    def _get_appointment_info(self, cr, uid, ids, field_name, arg, context=None):
        res = {}.fromkeys(ids, {'patient_id': False, 'doctor_id': False, 'exam_date': False, 'exam_time': False}) 
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id]['patient_id'] = record.appointment_id.patient_id.id
            res[record.id]['doctor_id'] = record.appointment_id.doctor_id.id
            res[record.id]['exam_date'] = record.appointment_id.start_date
            res[record.id]['exam_time'] = record.appointment_id.start_time
        return res

    def _get_model_ids(self, cr, uid, ids, context=None):
        return self.pool.get('oemedical.odontology.exam').search(cr, uid, [('appointment_id', 'in', ids)])

    _columns = {

        'appointment_id'    : fields.many2one('oemedical.appointment', 'Appointment', domain="[('state','!=','done'),('state','!=','canceled')]", required=True, context="{'search_odonto_appointment': 1}"),
        
        #Appointment Info...
        'patient_id'        : fields.related('appointment_id','patient_id', type='many2one', relation='oemedical.patient', string='Patient', required=True, store = True),
        'doctor_id'         : fields.related('appointment_id','doctor_id', type='many2one', relation='oemedical.physician', string='Odontologo', required=True, store = True),
        'exam_date'         : fields.related('appointment_id','start_date', type='date', string='Fecha', store = True),
        'exam_time'         : fields.related('appointment_id','start_time', type='float', string='Hora'),
        
        # stomatognathic system test...
        'libs': fields.boolean('Labios'),
        #'libs_observation': fields.text(),
        
        'cheeks': fields.boolean('Mejillas'),
        #'cheeks_observation': fields.text(),
        
        'top_max': fields.boolean('Maxilar Superior'),
        #'top_max_observation': fields.text(),
        
        'bottom_max': fields.boolean('Maxilar Inferior'),
        #'bottom_max_observation': fields.text(),
        
        'tongle': fields.boolean('Lengua'),
        #'tongle_observation': fields.text(),
        
        'taste': fields.boolean('Paladar'),
        #'taste_observation': fields.text(),
        
        'floor': fields.boolean('Piso'),
        #'floor_observation': fields.text(),
        
        'jowls': fields.boolean('Carrillos'),
        #'jowls_observation': fields.text(),
        
        'sal_glands': fields.boolean('Glandulas salivales'),
        #'sal_glands_observation': fields.text(),
        
        'pharynx': fields.boolean('Oro faringe'),
        #'pharynx_observation': fields.text(),
        
        'atm': fields.boolean('ATM'),
        #'atm_observation': fields.text(),
        
        'lymph': fields.boolean('Glanglios'),
        #'lymph_observation': fields.text(),
        
        'stomatognathic_system_observation': fields.text(string='Observaciones del examen del Sistema Estomatognático'),
        
        #INDICADORES DE SALUD BUCAL...
        '_16'                        : fields.boolean('16'),
        '_17'                        : fields.boolean('17'),
        '_55'                        : fields.boolean('55'),
        'section_1_placa'            : fields.integer(),
        'section_1_calculo'          : fields.integer(),
        'section_1_gingivitis'       : fields.integer(),
        
        '_11'                        : fields.boolean('11'),
        '_21'                        : fields.boolean('21'),
        '_51'                        : fields.boolean('51'),
        'section_2_placa'            : fields.integer(),
        'section_2_calculo'          : fields.integer(),
        'section_2_gingivitis'       : fields.integer(),
        
        '_26'                        : fields.boolean('26'),
        '_27'                        : fields.boolean('27'),
        '_65'                        : fields.boolean('65'),
        'section_3_placa'            : fields.integer(),
        'section_3_calculo'          : fields.integer(),
        'section_3_gingivitis'       : fields.integer(),
        
        '_36'                        : fields.boolean('36'),
        '_37'                        : fields.boolean('37'),
        '_75'                        : fields.boolean('75'),
        'section_4_placa'            : fields.integer(),
        'section_4_calculo'          : fields.integer(),
        'section_4_gingivitis'       : fields.integer(),
        
        '_31'                        : fields.boolean('31'),
        '_41'                        : fields.boolean('41'),
        '_71'                        : fields.boolean('71'),
        'section_5_placa'            : fields.integer(),
        'section_5_calculo'          : fields.integer(),
        'section_5_gingivitis'       : fields.integer(),
        
        '_46'                        : fields.boolean('16'),
        '_47'                        : fields.boolean('16'),
        '_85'                        : fields.boolean('16'),
        'section_6_placa'            : fields.integer(),
        'section_6_calculo'          : fields.integer(),
        'section_6_gingivitis'       : fields.integer(),
        
        'mouth_health_ind_ids'       : fields.one2many('oemedical.mouth.health.indicator','dentist_test_id','Higiene Oral Simplificada'),
        'periodontale_illness'       : fields.selection([('leve','Leve'),('moderada','Moderada'),('severa','Severa')],string = 'Enfermedad Periodontal'),
        'malocclusion'               : fields.selection([('angle1','Angle I'),('angle2','Angle II'),('angle3','Angle III')],string = 'Maloclusion'),
        'fluorosis'                  : fields.selection([('leve','Leve'),('moderada','Moderada'),('severa','Severa')],string = 'Fluorosis'),
        
        'carieDC'                    :fields.integer('DC'),
        'carieDP'                    :fields.integer('DP'),
        'carieDO'                    :fields.integer('DO'),
        'carie_dc'                   :fields.integer('dc'),
        'carie_de'                   :fields.integer('de'),
        'carie_do'                   :fields.integer('do'),
        
        'totalCarieD'   : fields.function(_get_total_carie, string='Total carie D', type='integer',
                            store={
                                     'oemedical.odontology.exam': (lambda self, cr, uid, ids, c=None: ids, ['carieDC','carieDP','carieDO'], 10),
                                  }, multi = "_carie"),
        'totalCarie_d'  : fields.function(_get_total_carie, string='Total carie d', type='integer',
                            store={
                                     'oemedical.odontology.exam': (lambda self, cr, uid, ids, c=None: ids, ['carie_dc','carie_de','carie_do'], 10),
                                  }, multi = "_carie"),
        
        'totalPlate'        : fields.function(_get_total, string='Total Placas', type='integer', multi = "_total"),
        'totalStone'        : fields.function(_get_total, string='Total Calculo', type='integer',multi = "_total"),
        'totalGengivitis'   : fields.function(_get_total, string='Total Gengivitis', type='integer',multi = "_total"),
        
        # 9. PLAN DIAGNOSTICO...
        'biometric'                  : fields.boolean('Biometria'),
        'blood_chemistry'            : fields.boolean('Quimica sanguinea'),
        'x_rays'                     : fields.boolean('Rayos X'),
        'other'                      : fields.boolean('Otros'),
        'other_observation'          : fields.text('Observaciones'),
        
        # 10. DIAGNOSTICOS...
        'diagnosis_ids'              : fields.many2many('oemedical.pathology', 'oemedical_dentist_test_diagnosis', 'test_id', 'diagnosis_id', 'Diagnosis'),
        'diagnosis_observation'      : fields.text('Observaciones'),
        
        # 11.PLAN DE TRATAMIENTO
        'interconsult'               : fields.boolean('InterConsulta'),
        'internation'                : fields.boolean('Internacion'),
        'extern_consult'             : fields.boolean('Consulta Externa'),
        'fluor_topification'         : fields.boolean('Topicacion Fluor'),
        'sealment'                   : fields.boolean('Sellante'),
        'reference'                  : fields.boolean('Referencia'),
        'procedure'                  : fields.boolean('Procedimiento'),        
        'incapacity_days'            : fields.integer('Dias de incapacidad'),
        'service'                    : fields.char('Servicio'),
        
        # 12. NOTAS DE EVOLUCION
        'evolution_ids'              : fields.one2many('oemedical.odontology.exam.evolution', 'dentist_test_id', 'Notas de Evolucion'),
        
        # Odontograma ...  
        'odontogram_img'             : fields.binary("Odontogram"), 

        # Row 1 -------------------------------------------------------
        'p18_symbol'                 : fields.char('Symbol', size = 6),
        'p18_z1'                     : fields.char('Zone 1', size = 4),
        'p18_z2'                     : fields.char('Zone 2', size = 4),
        'p18_z3'                     : fields.char('Zone 3', size = 4),
        'p18_z4'                     : fields.char('Zone 4', size = 4),
        'p18_z5'                     : fields.char('Zone 5', size = 4),

        'p17_symbol'                 : fields.char('Symbol', size = 6),
        'p17_z1'                     : fields.char('Zone 1', size = 4),
        'p17_z2'                     : fields.char('Zone 2', size = 4),
        'p17_z3'                     : fields.char('Zone 3', size = 4),
        'p17_z4'                     : fields.char('Zone 4', size = 4),
        'p17_z5'                     : fields.char('Zone 5', size = 4),

        'p16_symbol'                 : fields.char('Symbol', size = 6),
        'p16_z1'                     : fields.char('Zone 1', size = 4),
        'p16_z2'                     : fields.char('Zone 2', size = 4),
        'p16_z3'                     : fields.char('Zone 3', size = 4),
        'p16_z4'                     : fields.char('Zone 4', size = 4),
        'p16_z5'                     : fields.char('Zone 5', size = 4),

        'p15_symbol'                 : fields.char('Symbol', size = 6),
        'p15_z1'                     : fields.char('Zone 1', size = 4),
        'p15_z2'                     : fields.char('Zone 2', size = 4),
        'p15_z3'                     : fields.char('Zone 3', size = 4),
        'p15_z4'                     : fields.char('Zone 4', size = 4),
        'p15_z5'                     : fields.char('Zone 5', size = 4),

        'p14_symbol'                 : fields.char('Symbol', size = 6),
        'p14_z1'                     : fields.char('Zone 1', size = 4),
        'p14_z2'                     : fields.char('Zone 2', size = 4),
        'p14_z3'                     : fields.char('Zone 3', size = 4),
        'p14_z4'                     : fields.char('Zone 4', size = 4),
        'p14_z5'                     : fields.char('Zone 5', size = 4),

        'p13_symbol'                 : fields.char('Symbol', size = 6),
        'p13_z1'                     : fields.char('Zone 1', size = 4),
        'p13_z2'                     : fields.char('Zone 2', size = 4),
        'p13_z3'                     : fields.char('Zone 3', size = 4),
        'p13_z4'                     : fields.char('Zone 4', size = 4),
        'p13_z5'                     : fields.char('Zone 5', size = 4),

        'p12_symbol'                 : fields.char('Symbol', size = 6),
        'p12_z1'                     : fields.char('Zone 1', size = 4),
        'p12_z2'                     : fields.char('Zone 2', size = 4),
        'p12_z3'                     : fields.char('Zone 3', size = 4),
        'p12_z4'                     : fields.char('Zone 4', size = 4),
        'p12_z5'                     : fields.char('Zone 5', size = 4),

        'p11_symbol'                 : fields.char('Symbol', size = 6),
        'p11_z1'                     : fields.char('Zone 1', size = 4),
        'p11_z2'                     : fields.char('Zone 2', size = 4),
        'p11_z3'                     : fields.char('Zone 3', size = 4),
        'p11_z4'                     : fields.char('Zone 4', size = 4),
        'p11_z5'                     : fields.char('Zone 5', size = 4),

        'p21_symbol'                 : fields.char('Symbol', size = 6),
        'p21_z1'                     : fields.char('Zone 1', size = 4),
        'p21_z2'                     : fields.char('Zone 2', size = 4),
        'p21_z3'                     : fields.char('Zone 3', size = 4),
        'p21_z4'                     : fields.char('Zone 4', size = 4),
        'p21_z5'                     : fields.char('Zone 5', size = 4),

        'p22_symbol'                 : fields.char('Symbol', size = 6),
        'p22_z1'                     : fields.char('Zone 1', size = 4),
        'p22_z2'                     : fields.char('Zone 2', size = 4),
        'p22_z3'                     : fields.char('Zone 3', size = 4),
        'p22_z4'                     : fields.char('Zone 4', size = 4),
        'p22_z5'                     : fields.char('Zone 5', size = 4),

        'p23_symbol'                 : fields.char('Symbol', size = 6),
        'p23_z1'                     : fields.char('Zone 1', size = 4),
        'p23_z2'                     : fields.char('Zone 2', size = 4),
        'p23_z3'                     : fields.char('Zone 3', size = 4),
        'p23_z4'                     : fields.char('Zone 4', size = 4),
        'p23_z5'                     : fields.char('Zone 5', size = 4),

        'p24_symbol'                 : fields.char('Symbol', size = 6),
        'p24_z1'                     : fields.char('Zone 1', size = 4),
        'p24_z2'                     : fields.char('Zone 2', size = 4),
        'p24_z3'                     : fields.char('Zone 3', size = 4),
        'p24_z4'                     : fields.char('Zone 4', size = 4),
        'p24_z5'                     : fields.char('Zone 5', size = 4),

        'p25_symbol'                 : fields.char('Symbol', size = 6),
        'p25_z1'                     : fields.char('Zone 1', size = 4),
        'p25_z2'                     : fields.char('Zone 2', size = 4),
        'p25_z3'                     : fields.char('Zone 3', size = 4),
        'p25_z4'                     : fields.char('Zone 4', size = 4),
        'p25_z5'                     : fields.char('Zone 5', size = 4),

        'p26_symbol'                 : fields.char('Symbol', size = 6),
        'p26_z1'                     : fields.char('Zone 1', size = 4),
        'p26_z2'                     : fields.char('Zone 2', size = 4),
        'p26_z3'                     : fields.char('Zone 3', size = 4),
        'p26_z4'                     : fields.char('Zone 4', size = 4),
        'p26_z5'                     : fields.char('Zone 5', size = 4),

        'p27_symbol'                 : fields.char('Symbol', size = 6),
        'p27_z1'                     : fields.char('Zone 1', size = 4),
        'p27_z2'                     : fields.char('Zone 2', size = 4),
        'p27_z3'                     : fields.char('Zone 3', size = 4),
        'p27_z4'                     : fields.char('Zone 4', size = 4),
        'p27_z5'                     : fields.char('Zone 5', size = 4),

        'p28_symbol'                 : fields.char('Symbol', size = 6),
        'p28_z1'                     : fields.char('Zone 1', size = 4),
        'p28_z2'                     : fields.char('Zone 2', size = 4),
        'p28_z3'                     : fields.char('Zone 3', size = 4),
        'p28_z4'                     : fields.char('Zone 4', size = 4),
        'p28_z5'                     : fields.char('Zone 5', size = 4),

         #Row 2 ----------------------------------------------------------
        'p55_symbol'                 : fields.char('Symbol', size = 6),
        'p55_z1'                     : fields.char('Zone 1', size = 4),
        'p55_z2'                     : fields.char('Zone 2', size = 4),
        'p55_z3'                     : fields.char('Zone 3', size = 4),
        'p55_z4'                     : fields.char('Zone 4', size = 4),
        'p55_z5'                     : fields.char('Zone 5', size = 4),

        'p54_symbol'                 : fields.char('Symbol', size = 6),
        'p54_z1'                     : fields.char('Zone 1', size = 4),
        'p54_z2'                     : fields.char('Zone 2', size = 4),
        'p54_z3'                     : fields.char('Zone 3', size = 4),
        'p54_z4'                     : fields.char('Zone 4', size = 4),
        'p54_z5'                     : fields.char('Zone 5', size = 4),

        'p53_symbol'                 : fields.char('Symbol', size = 6),
        'p53_z1'                     : fields.char('Zone 1', size = 4),
        'p53_z2'                     : fields.char('Zone 2', size = 4),
        'p53_z3'                     : fields.char('Zone 3', size = 4),
        'p53_z4'                     : fields.char('Zone 4', size = 4),
        'p53_z5'                     : fields.char('Zone 5', size = 4),

        'p52_symbol'                 : fields.char('Symbol', size = 6),
        'p52_z1'                     : fields.char('Zone 1', size = 4),
        'p52_z2'                     : fields.char('Zone 2', size = 4),
        'p52_z3'                     : fields.char('Zone 3', size = 4),
        'p52_z4'                     : fields.char('Zone 4', size = 4),
        'p52_z5'                     : fields.char('Zone 5', size = 4),

        'p51_symbol'                 : fields.char('Symbol', size = 6),
        'p51_z1'                     : fields.char('Zone 1', size = 4),
        'p51_z2'                     : fields.char('Zone 2', size = 4),
        'p51_z3'                     : fields.char('Zone 3', size = 4),
        'p51_z4'                     : fields.char('Zone 4', size = 4),
        'p51_z5'                     : fields.char('Zone 5', size = 4),

        'p61_symbol'                 : fields.char('Symbol', size = 6),
        'p61_z1'                     : fields.char('Zone 1', size = 4),
        'p61_z2'                     : fields.char('Zone 2', size = 4),
        'p61_z3'                     : fields.char('Zone 3', size = 4),
        'p61_z4'                     : fields.char('Zone 4', size = 4),
        'p61_z5'                     : fields.char('Zone 5', size = 4),

        'p62_symbol'                 : fields.char('Symbol', size = 6),
        'p62_z1'                     : fields.char('Zone 1', size = 4),
        'p62_z2'                     : fields.char('Zone 2', size = 4),
        'p62_z3'                     : fields.char('Zone 3', size = 4),
        'p62_z4'                     : fields.char('Zone 4', size = 4),
        'p62_z5'                     : fields.char('Zone 5', size = 4),

        'p63_symbol'                 : fields.char('Symbol', size = 6),
        'p63_z1'                     : fields.char('Zone 1', size = 4),
        'p63_z2'                     : fields.char('Zone 2', size = 4),
        'p63_z3'                     : fields.char('Zone 3', size = 4),
        'p63_z4'                     : fields.char('Zone 4', size = 4),
        'p63_z5'                     : fields.char('Zone 5', size = 4),

        'p64_symbol'                 : fields.char('Symbol', size = 6),
        'p64_z1'                     : fields.char('Zone 1', size = 4),
        'p64_z2'                     : fields.char('Zone 2', size = 4),
        'p64_z3'                     : fields.char('Zone 3', size = 4),
        'p64_z4'                     : fields.char('Zone 4', size = 4),
        'p64_z5'                     : fields.char('Zone 5', size = 4),

        'p65_symbol'                 : fields.char('Symbol', size = 6),
        'p65_z1'                     : fields.char('Zone 1', size = 4),
        'p65_z2'                     : fields.char('Zone 2', size = 4),
        'p65_z3'                     : fields.char('Zone 3', size = 4),
        'p65_z4'                     : fields.char('Zone 4', size = 4),
        'p65_z5'                     : fields.char('Zone 5', size = 4),

        #Row 3 ----------------------------------------------------------
        'p85_symbol'                 : fields.char('Symbol', size = 6),
        'p85_z1'                     : fields.char('Zone 1', size = 4),
        'p85_z2'                     : fields.char('Zone 2', size = 4),
        'p85_z3'                     : fields.char('Zone 3', size = 4),
        'p85_z4'                     : fields.char('Zone 4', size = 4),
        'p85_z5'                     : fields.char('Zone 5', size = 4),

        'p84_symbol'                 : fields.char('Symbol', size = 6),
        'p84_z1'                     : fields.char('Zone 1', size = 4),
        'p84_z2'                     : fields.char('Zone 2', size = 4),
        'p84_z3'                     : fields.char('Zone 3', size = 4),
        'p84_z4'                     : fields.char('Zone 4', size = 4),
        'p84_z5'                     : fields.char('Zone 5', size = 4),

        'p83_symbol'                 : fields.char('Symbol', size = 6),
        'p83_z1'                     : fields.char('Zone 1', size = 4),
        'p83_z2'                     : fields.char('Zone 2', size = 4),
        'p83_z3'                     : fields.char('Zone 3', size = 4),
        'p83_z4'                     : fields.char('Zone 4', size = 4),
        'p83_z5'                     : fields.char('Zone 5', size = 4),

        'p82_symbol'                 : fields.char('Symbol', size = 6),
        'p82_z1'                     : fields.char('Zone 1', size = 4),
        'p82_z2'                     : fields.char('Zone 2', size = 4),
        'p82_z3'                     : fields.char('Zone 3', size = 4),
        'p82_z4'                     : fields.char('Zone 4', size = 4),
        'p82_z5'                     : fields.char('Zone 5', size = 4),

        'p81_symbol'                 : fields.char('Symbol', size = 6),
        'p81_z1'                     : fields.char('Zone 1', size = 4),
        'p81_z2'                     : fields.char('Zone 2', size = 4),
        'p81_z3'                     : fields.char('Zone 3', size = 4),
        'p81_z4'                     : fields.char('Zone 4', size = 4),
        'p81_z5'                     : fields.char('Zone 5', size = 4),

        'p71_symbol'                 : fields.char('Symbol', size = 6),
        'p71_z1'                     : fields.char('Zone 1', size = 4),
        'p71_z2'                     : fields.char('Zone 2', size = 4),
        'p71_z3'                     : fields.char('Zone 3', size = 4),
        'p71_z4'                     : fields.char('Zone 4', size = 4),
        'p71_z5'                     : fields.char('Zone 5', size = 4),

        'p72_symbol'                 : fields.char('Symbol', size = 6),
        'p72_z1'                     : fields.char('Zone 1', size = 4),
        'p72_z2'                     : fields.char('Zone 2', size = 4),
        'p72_z3'                     : fields.char('Zone 3', size = 4),
        'p72_z4'                     : fields.char('Zone 4', size = 4),
        'p72_z5'                     : fields.char('Zone 5', size = 4),

        'p73_symbol'                 : fields.char('Symbol', size = 6),
        'p73_z1'                     : fields.char('Zone 1', size = 4),
        'p73_z2'                     : fields.char('Zone 2', size = 4),
        'p73_z3'                     : fields.char('Zone 3', size = 4),
        'p73_z4'                     : fields.char('Zone 4', size = 4),
        'p73_z5'                     : fields.char('Zone 5', size = 4),

        'p74_symbol'                 : fields.char('Symbol', size = 6),
        'p74_z1'                     : fields.char('Zone 1', size = 4),
        'p74_z2'                     : fields.char('Zone 2', size = 4),
        'p74_z3'                     : fields.char('Zone 3', size = 4),
        'p74_z4'                     : fields.char('Zone 4', size = 4),
        'p74_z5'                     : fields.char('Zone 5', size = 4),

        'p75_symbol'                 : fields.char('Symbol', size = 6),
        'p75_z1'                     : fields.char('Zone 1', size = 4),
        'p75_z2'                     : fields.char('Zone 2', size = 4),
        'p75_z3'                     : fields.char('Zone 3', size = 4),
        'p75_z4'                     : fields.char('Zone 4', size = 4),
        'p75_z5'                     : fields.char('Zone 5', size = 4),

        # Row 4 -------------------------------------------------------
        'p48_symbol'                 : fields.char('Symbol', size = 6),
        'p48_z1'                     : fields.char('Zone 1', size = 4),
        'p48_z2'                     : fields.char('Zone 2', size = 4),
        'p48_z3'                     : fields.char('Zone 3', size = 4),
        'p48_z4'                     : fields.char('Zone 4', size = 4),
        'p48_z5'                     : fields.char('Zone 5', size = 4),

        'p47_symbol'                 : fields.char('Symbol', size = 6),
        'p47_z1'                     : fields.char('Zone 1', size = 4),
        'p47_z2'                     : fields.char('Zone 2', size = 4),
        'p47_z3'                     : fields.char('Zone 3', size = 4),
        'p47_z4'                     : fields.char('Zone 4', size = 4),
        'p47_z5'                     : fields.char('Zone 5', size = 4),

        'p46_symbol'                 : fields.char('Symbol', size = 6),
        'p46_z1'                     : fields.char('Zone 1', size = 4),
        'p46_z2'                     : fields.char('Zone 2', size = 4),
        'p46_z3'                     : fields.char('Zone 3', size = 4),
        'p46_z4'                     : fields.char('Zone 4', size = 4),
        'p46_z5'                     : fields.char('Zone 5', size = 4),

        'p45_symbol'                 : fields.char('Symbol', size = 6),
        'p45_z1'                     : fields.char('Zone 1', size = 4),
        'p45_z2'                     : fields.char('Zone 2', size = 4),
        'p45_z3'                     : fields.char('Zone 3', size = 4),
        'p45_z4'                     : fields.char('Zone 4', size = 4),
        'p45_z5'                     : fields.char('Zone 5', size = 4),

        'p44_symbol'                 : fields.char('Symbol', size = 6),
        'p44_z1'                     : fields.char('Zone 1', size = 4),
        'p44_z2'                     : fields.char('Zone 2', size = 4),
        'p44_z3'                     : fields.char('Zone 3', size = 4),
        'p44_z4'                     : fields.char('Zone 4', size = 4),
        'p44_z5'                     : fields.char('Zone 5', size = 4),

        'p43_symbol'                 : fields.char('Symbol', size = 6),
        'p43_z1'                     : fields.char('Zone 1', size = 4),
        'p43_z2'                     : fields.char('Zone 2', size = 4),
        'p43_z3'                     : fields.char('Zone 3', size = 4),
        'p43_z4'                     : fields.char('Zone 4', size = 4),
        'p43_z5'                     : fields.char('Zone 5', size = 4),

        'p42_symbol'                 : fields.char('Symbol', size = 6),
        'p42_z1'                     : fields.char('Zone 1', size = 4),
        'p42_z2'                     : fields.char('Zone 2', size = 4),
        'p42_z3'                     : fields.char('Zone 3', size = 4),
        'p42_z4'                     : fields.char('Zone 4', size = 4),
        'p42_z5'                     : fields.char('Zone 5', size = 4),

        'p41_symbol'                 : fields.char('Symbol', size = 6),
        'p41_z1'                     : fields.char('Zone 1', size = 4),
        'p41_z2'                     : fields.char('Zone 2', size = 4),
        'p41_z3'                     : fields.char('Zone 3', size = 4),
        'p41_z4'                     : fields.char('Zone 4', size = 4),
        'p41_z5'                     : fields.char('Zone 5', size = 4),

        'p31_symbol'                 : fields.char('Symbol', size = 6),
        'p31_z1'                     : fields.char('Zone 1', size = 4),
        'p31_z2'                     : fields.char('Zone 2', size = 4),
        'p31_z3'                     : fields.char('Zone 3', size = 4),
        'p31_z4'                     : fields.char('Zone 4', size = 4),
        'p31_z5'                     : fields.char('Zone 5', size = 4),

        'p32_symbol'                 : fields.char('Symbol', size = 6),
        'p32_z1'                     : fields.char('Zone 1', size = 4),
        'p32_z2'                     : fields.char('Zone 2', size = 4),
        'p32_z3'                     : fields.char('Zone 3', size = 4),
        'p32_z4'                     : fields.char('Zone 4', size = 4),
        'p32_z5'                     : fields.char('Zone 5', size = 4),

        'p33_symbol'                 : fields.char('Symbol', size = 6),
        'p33_z1'                     : fields.char('Zone 1', size = 4),
        'p33_z2'                     : fields.char('Zone 2', size = 4),
        'p33_z3'                     : fields.char('Zone 3', size = 4),
        'p33_z4'                     : fields.char('Zone 4', size = 4),
        'p33_z5'                     : fields.char('Zone 5', size = 4),

        'p34_symbol'                 : fields.char('Symbol', size = 6),
        'p34_z1'                     : fields.char('Zone 1', size = 4),
        'p34_z2'                     : fields.char('Zone 2', size = 4),
        'p34_z3'                     : fields.char('Zone 3', size = 4),
        'p34_z4'                     : fields.char('Zone 4', size = 4),
        'p34_z5'                     : fields.char('Zone 5', size = 4),

        'p35_symbol'                 : fields.char('Symbol', size = 6),
        'p35_z1'                     : fields.char('Zone 1', size = 4),
        'p35_z2'                     : fields.char('Zone 2', size = 4),
        'p35_z3'                     : fields.char('Zone 3', size = 4),
        'p35_z4'                     : fields.char('Zone 4', size = 4),
        'p35_z5'                     : fields.char('Zone 5', size = 4),

        'p36_symbol'                 : fields.char('Symbol', size = 6),
        'p36_z1'                     : fields.char('Zone 1', size = 4),
        'p36_z2'                     : fields.char('Zone 2', size = 4),
        'p36_z3'                     : fields.char('Zone 3', size = 4),
        'p36_z4'                     : fields.char('Zone 4', size = 4),
        'p36_z5'                     : fields.char('Zone 5', size = 4),

        'p37_symbol'                 : fields.char('Symbol', size = 6),
        'p37_z1'                     : fields.char('Zone 1', size = 4),
        'p37_z2'                     : fields.char('Zone 2', size = 4),
        'p37_z3'                     : fields.char('Zone 3', size = 4),
        'p37_z4'                     : fields.char('Zone 4', size = 4),
        'p37_z5'                     : fields.char('Zone 5', size = 4),

        'p38_symbol'                 : fields.char('Symbol', size = 6),
        'p38_z1'                     : fields.char('Zone 1', size = 4),
        'p38_z2'                     : fields.char('Zone 2', size = 4),
        'p38_z3'                     : fields.char('Zone 3', size = 4),
        'p38_z4'                     : fields.char('Zone 4', size = 4),
        'p38_z5'                     : fields.char('Zone 5', size = 4),
    }

    def onchange_appointment(self, cr, uid, ids, appointment_id, context=None):
        res = {}
        if appointment_id:
            res['value'] = {}
            appointment = self.pool.get('oemedical.appointment').browse(cr, uid, appointment_id)
            res['value']['cardiopatia'] = appointment.patient_id.cardiopatia
            res['value']['diabetes'] = appointment.patient_id.diabetes
            res['value']['enf_cardiaca'] = appointment.patient_id.enf_car
            res['value']['hipertension'] = appointment.patient_id.hipertension
            res['value']['cancer'] = appointment.patient_id.cancer
            res['value']['tuberculosis'] = appointment.patient_id.tuberculosis
            res['value']['enf_men'] = appointment.patient_id.enf_men
            res['value']['enf_inf'] = appointment.patient_id.enf_inf
            res['value']['mal_for'] = appointment.patient_id.mal_for
            res['value']['antibotic_allergic'] = appointment.patient_id.antibotic_allergic
            res['value']['anesthesia_allergic'] = appointment.patient_id.anesthesia_allergic
            res['value']['hemorrhage'] = appointment.patient_id.hemorrhage
            res['value']['vih_sida'] = appointment.patient_id.vih_sida
            res['value']['asma'] = appointment.patient_id.asma
            res['value']['other'] = appointment.patient_id.other
            res['value']['others_antecedents'] = appointment.patient_id.others_antecedents
            res['value']['patient_id'] = appointment.patient_id.id
            res['value']['doctor_id'] = appointment.doctor_id.id
            res['value']['exam_date'] = appointment.start_date
            res['value']['exam_time'] = appointment.start_time
            res['value']['mdc_info'] = appointment.motive
            res['value']['info_diagnosis'] = appointment.info_diagnosis
            res['value']['is_planned'] = appointment.is_planned
            res['value']['pat_info'] = appointment.pat_info
            res['value']['ppm_info'] = appointment.ppm_info
            res['value']['ppr_info'] = appointment.ppr_info
            res['value']['tem_info'] = appointment.tem_info
            res['value']['tem2_info'] = appointment.tem2_info
            res['value']['pes_info'] = appointment.pes_info
            res['value']['size_info'] = appointment.size_info

        return res
    
    def _get_patient(self, cr, uid, context):
        run_pool = self.pool.get('oemedical.patient')
        run_data = {}
        if context and context.get('active_id', False):
            run_data = run_pool.read(cr, uid, context['active_id'], ['patient_id'])
            patient_id = run_data.get('id', False)
            if patient_id:
                return patient_id
        return False
    
    _defaults = {
        'patient_id': _get_patient,
    }

    def _check_indicators(self, cr, uid, ids):
        for obj in self.browse(cr, uid, ids):
            if(len(obj.mouth_health_ind_ids) > 6):
                return False
        return True
    
    def _check_diagnosis(self, cr, uid, ids):
        for obj in self.browse(cr, uid, ids):
            if(len(obj.diagnosis_ids) > 4):
                return False
        return True
    
    _constraints = [
                    (_check_indicators, _('La cantidad de grupos de indicadores no puede exceder de 6.'), []),
                    (_check_diagnosis, _('La cantidad de diagnosticos no puede exceder de 4.'), []),
                   ]

    def print_odontogram(self, cr, uid, ids, context = None):
        datas = {'ids' : ids}
        if context:
            datas['context'] = context         
        datas['model'] = 'oemedical.odontology.exam'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'odontogram_report',
            'datas': datas,
        }
    
OeMedicalOdontologyExam()

class OeMedicalPathology(osv.Model):
    _inherit = 'oemedical.pathology'

    _columns = {
     'definitive': fields.boolean(string='Definitivo'),
     'presuntive': fields.boolean(string='Presuntivo'),
     'foment'    : fields.boolean(string='Fomento'),
    } 

OeMedicalPathology()

class OeMedicalOdontologyExamEvolution(osv.Model):
    _name = 'oemedical.odontology.exam.evolution'
    _rec_name = 'evolution_date'
    _columns = {
     #'name'             : fields.char(size=256, string='Medicamento Generico', required=True),        
     'evolution_date'   : fields.datetime(string='Fecha y Hora'),
     'observation'      : fields.text('Observaciones'),
     'dentist_test_id'  : fields.many2one('oemedical.odontology.exam', 'Odontology Exam', required=True),
    } 

    _defaults = {
        'dentist_test_id': lambda self, cr, uid, context: context.get('exam_id', False) or False,
    }

OeMedicalOdontologyExamEvolution()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
