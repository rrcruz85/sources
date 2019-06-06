# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.techreceptives.com>)
#    Special Credit and Thanks to Thymbra Latinoamericana S.A.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################

import time
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import tools

class OeMedicalPatient(osv.Model):
    _inherit = 'oemedical.patient'

    _columns = {
        'is_pregnant': fields.boolean(string='Is Pregnant'),        
    }

OeMedicalPatient()

class OeMedicalPatientOdontogramOperation(osv.Model):
    _name = 'oemedical.patient.odontogram.operation'

    def get_zone_list(self,cr,uid,context):
        return [(1,1),(2,2),(3,3),(4,4),(5,5)]
    
    def get_operation_list(self):
        return [('1','Carie'),
                ('2','Restauración'),
                ('3','Retos radic'),
                ('4','Corona'),
                ('5','Prótesis remov.'),
                ('6','Prótesis total'),
                ('7','Sellante'),
                ('8','Estracción'),
                ('9','Ausente'),
                ('10','Trat. endodon.'),
                ('11','Prótesis fija')]
    
    _columns = {
        'name'                  : fields.selection(get_zone_list, string='Zona', required=True),
        'color'                 : fields.selection([('red', 'Rojo'), ('blue', 'Azul')],string='Color'),
        'symbol'                : fields.selection(get_operation_list, string='Simbolo'),
        'odontogram_id'         : fields.many2one('oemedical.patient.odontogram', string='Odontograma', required=True ),
    }

OeMedicalPatientOdontogramOperation()

class OeMedicalPatientOdontogram(osv.Model):
    _name = 'oemedical.patient.odontogram'

    def get_piece_list(self,cr,uid,context):
        return [(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),
                (21,21),(22,22),(23,23),(24,24),(25,25),(26,26),(27,27),(28,28),
                (31,31),(32,32),(33,33),(34,34),(35,35),(36,36),(37,37),(38,38),
                (41,41),(42,42),(43,43),(44,44),(45,45),(46,46),(47,47),(48,48),
                (51,51),(52,52),(53,53),(54,54),(55,55),
                (61,61),(62,62),(63,63),(64,64),(65,65),
                (71,71),(72,72),(73,73),(74,74),(75,75),
                (81,81),(82,82),(83,83),(84,84),(85,85),
                ]

    _columns = {
        'name': fields.selection(get_piece_list,string='Pieza',required=True),
        'operation_ids': fields.one2many('oemedical.patient.odontogram.operation','odontogram_id','Operaciones'),
        'dentist_test_id': fields.many2one('oemedical.dentist.test',string='Examen Odontologico',required=True ),
    }

OeMedicalPatientOdontogram()

class OeMedicalPatientOdontogramPiece(osv.Model):
    _name = "oemedical.patient.odontogram_piece"
    
    def _get_symbols(self, cr, uid, context):
        return [('O', 'O'),
                ('/', '/'),
                ('F', 'F'),
                ('C', 'C'),
                ('w', 'w'),
                ('*', '*'),
                ('X', 'X'),
                ('A', 'A'),
                ('I', 'I'),
                ('K', 'K'),
                ('0-0', '0-0')]
    
    def button_save(self, cr, uid, ids, context=None):
        str_field = 'piece' + str(context['number'])
        self.pool.get('oemedical.dentist.test').write(cr, uid, context['active_id'], {str_field: ids[0]}, context=context)
        obj = self.browse(cr, uid, ids[0],context)
        '''
        if obj.operation_rank:
            visible = self._get_visible(cr,uid,ids,"","",context)
            if visible[ids[0]]:
                current_piece = context['number']
                piece = obj.final_piece_rank1
                pos = 0
                pos_f = 0
                pieces = [18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28]
                for p in pieces:
                    if current_piece == str(p):
                        pos_f = pos
                        for v in pieces[pos:]:
                            if v == str(piece):
                                break
                            pos_f += 1
                        break                        
                    pos += 1
                list_fields = ['piece' + str(p) for p in pieces[pos : pos_f]]
                values = self.pool.get('oemedical.dentist.test').read(cr,uid,context['active_id'],list_fields,context)
        '''     
        return True
    
    def _get_operation(self, cr, uid, context):
        return [('w', 'w'),('0-0', '0-0')]
    
    def get_piece_list_rank1(self,cr,uid,context):
        pieces = [18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28]
        current_piece = context['number']        
        list_pieces = []
        pos = 0
        for v in pieces:
            if str(v) == current_piece:
                if pos != len(pieces) - 1:
                    list_pieces = [(str(e),str(e)) for e in pieces[pos + 1:]]
                break
            pos += 1
        return list_pieces
    
    def get_piece_list_rank2(self,cr,uid,context):
        pieces = [48,47,46,45,44,43,42,41,31,32,33,34,35,36,37,38]
        current_piece = context['number']        
        list_pieces = []
        pos = 0
        for v in pieces:
            if str(v) == current_piece:
                if pos != len(pieces) - 1:
                    list_pieces = [(str(e),str(e)) for e in pieces[pos + 1:]]
                break
            pos += 1
        return list_pieces
    
    def _get_visible(self, cr, uid, ids, field_name, arg, context=None):
        pieces = ['18','17','16','15','14','13','12','11','21','22','23','24','25','26','27','28']
        current_piece = context['number']   
        return {}.fromkeys(ids, current_piece in pieces)   
     
    
    _columns = {
        # Zona 1...
        'zone_one_symbol'           : fields.selection(_get_symbols, string='Symbol'),
        'zone_one_color'            : fields.selection([('red', 'Rojo'), ('blue', 'Azul')], string='Color'),
        
        # Zona 2...
        'zone_two_symbol'           : fields.selection(_get_symbols, string='Symbol'),
        'zone_two_color'            : fields.selection([('red', 'Rojo'), ('blue', 'Azul')], string='Color'),
        
        # Zona 3...
        'zone_three_symbol'           : fields.selection(_get_symbols, string='Symbol'),
        'zone_three_color'            : fields.selection([('red', 'Rojo'), ('blue', 'Azul')], string='Color'),
        
        # Zona 4...
        'zone_four_symbol'           : fields.selection(_get_symbols, string='Symbol'),
        'zone_four_color'            : fields.selection([('red', 'Rojo'), ('blue', 'Azul')], string='Color'),
        
        # Zona 5...
        'zone_five_symbol'           : fields.selection(_get_symbols, string='Symbol'),
        'zone_five_color'            : fields.selection([('red', 'Rojo'), ('blue', 'Azul')], string='Color'),
        
        # Checked if is total prosthesis...
        'total_prosthesis'           : fields.boolean(tools.ustr('Prótesis total')),
        
        #'operation_rank'             : fields.boolean(tools.ustr('Grupo Operaciones')),
        #'operation'                  : fields.selection(_get_operation, string='Symbol'),
        #'operation_color'            : fields.selection([('red', 'Rojo'), ('blue', 'Azul')], string='Color'),
        #'final_piece_rank1'          : fields.selection(get_piece_list_rank1, string='Pieza Final'),
        #'final_piece_rank2'          : fields.selection(get_piece_list_rank2, string='Pieza Final'),
        #'rank1_visible'              : fields.function(_get_visible, type='char', string='Rank Visible')
    }
    
OeMedicalPatientOdontogramPiece

class OeMedicalMouthHealthIndicator(osv.Model):
    _name = 'oemedical.mouth.health.indicator'

    _columns = {
         'piece1': fields.selection([(16,16),(11,11),(26,26),(36,36),(31,31),(46,46)],'Pieza 1', required=True),
         'piece2': fields.selection([(17,17),(21,21),(27,27),(37,37),(41,41),(47,47)],'Pieza 2', required=True),
         'piece3': fields.selection([(55,55),(51,51),(65,65),(75,75),(71,71),(85,85)],'Pieza 3', required=True),
         'plate': fields.integer('Placa'),
         'stone': fields.integer('Calculo'),
         'genvitis': fields.integer('Gengivitis'),
         'dentist_test_id': fields.many2one('oemedical.dentist.test',string='Examen Odontologico',required=True ),
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

class OeMedicalDentistTest(osv.Model):
    _name='oemedical.dentist.test'

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
    
    def _get_piece_summary(self, cr, uid, ids, field, args, context):
        res = {}
        fields = field.split('_')
        
        parent_obj = fields[0]
        zone = fields[1] + '_' + fields[2]
        
        for obj in self.browse(cr, uid, ids, context):
            try:
                parent_obj = getattr(obj, parent_obj)
                res[obj.id] = '<font color="' + getattr(parent_obj, zone + '_color') + '"><b>' + getattr(parent_obj, zone + '_symbol') + '</b></font>' if parent_obj else ''
            except:
                res[obj.id] = ''
                
        return res
    
    def _get_piece_tp(self, cr, uid, ids, field, args, context):
        res = {}
        parent_obj = field.split('_')[0]
        for obj in self.browse(cr, uid, ids, context):
            try:
                parent_obj = getattr(obj, parent_obj)
                res[obj.id] = getattr(parent_obj, 'total_prosthesis')
            except:
                res[obj.id] = False
                
        return res
    
    def button_catch(self, cr, uid, ids, context=None):
        context['form_view_ref'] = 'oemedical_patient_odontogram_piece_form_view' if context['type'] == 'square' else 'oemedical_patient_odontogram_piece_form2_view'
        view_ids = self.pool.get('ir.ui.view').search(cr, uid, [('name', '=', context['form_view_ref'])])
        view_id = view_ids[0] if len(view_ids) > 0 else False
        field_id = context['piece']
        
        if field_id:
            pass
        
        return {
            'type'      :   'ir.actions.act_window',
            'res_model' :   'oemedical.patient.odontogram_piece',
            'view_id'   :   view_id,
            'target'    :   'new',
            'view_mode' :   'form',
            'context'   :   context,
            'name'      :   tools.ustr('Captura de datos de la pieza: ' + str(context['number'])),
            'res_id'    :   field_id
        }
    
    _columns = {
        'patient_id'        :fields.many2one('oemedical.patient', 'Patient', required=True),
        'test_date'         : fields.date(string='Fecha'),
        'mdc_info'          : fields.text(string='Motivo de Consulta'),
        'info_diagnosis'    : fields.text(string='Enfermedad Actual'),        
        'is_planned'        : fields.boolean('Consulta programada?'),
        
        # Signos vitales y mediciones...
        'pat_info'  : fields.char(size=256, string='Presion arterial'),
        'ppm_info'  : fields.integer('Frecuencia cardiaca'),
        'ppr_info'  : fields.integer('Frecuencia respiratoria'),
        'tem_info'  : fields.float('Temperatura bucal', digits=(2,2)),
        'tem2_info' : fields.float('Temperatura axilar', digits=(2,2)),
        'pes_info'  : fields.float('Peso (Kg)', digits=(3,2)),
        'size_info' : fields.float('Talla (m)', digits=(3,2)),
        'not_apply' : fields.boolean('No aplica?'),
        
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
        
        #Personal antecedents and family antecedents...
        'antibotic_allergic'        : fields.boolean(string='Alergia a antibioticos'),
        'anesthesia_allergic'       : fields.boolean(string='Alergia a anestesia'),
        'hemorrhage'                : fields.boolean(string='VIH/SIDA'),
        'vih_sida'                  : fields.boolean(string='Hemorragia'),
        'tuberculosis'              : fields.boolean(string='Tuberculosis'),
        'asma'                      : fields.boolean(string='Asma'),
        'diabetes'                  : fields.boolean(string='Diabetes'),
        'hipertension'              : fields.boolean(string='hipertension'),
        'enf_cardiaca'              : fields.boolean(string='Enf. Cardiaca'),
        'others'                    : fields.boolean(string='Otro'),
        'others_antecedents'        : fields.text(string='Otros antecedentes'),
        
        # Odontograma...
        'protesis_total'            : fields.boolean("Protesis total?"),
        
        'piece11'                   : fields.many2one('oemedical.patient.odontogram_piece', string="11", required=False),
        'piece11_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece11_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece11_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece11_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece11_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece11_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece12'                   : fields.many2one('oemedical.patient.odontogram_piece', string="12", required=False),
        'piece12_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece12_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece12_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece12_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece12_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece12_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece13'                   : fields.many2one('oemedical.patient.odontogram_piece', string="13", required=False),
        'piece13_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece13_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece13_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece13_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece13_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece13_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece14'                   : fields.many2one('oemedical.patient.odontogram_piece', string="14", required=False),
        'piece14_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece14_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece14_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece14_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece14_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece14_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece15'                   : fields.many2one('oemedical.patient.odontogram_piece', string="15", required=False),
        'piece15_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece15_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece15_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece15_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece15_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece15_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece16'                   : fields.many2one('oemedical.patient.odontogram_piece', string="16", required=False),
        'piece16_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece16_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece16_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece16_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece16_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece16_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece17'                   : fields.many2one('oemedical.patient.odontogram_piece', string="17", required=False),
        'piece17_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece17_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece17_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece17_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece17_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece17_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece18'                   : fields.many2one('oemedical.patient.odontogram_piece', string="18", required=False),
        'piece18_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece18_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece18_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece18_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece18_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece18_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece21'                   : fields.many2one('oemedical.patient.odontogram_piece', string="21", required=False),
        'piece21_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece21_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece21_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece21_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece21_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece21_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece22'                   : fields.many2one('oemedical.patient.odontogram_piece', string="22", required=False),
        'piece22_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece22_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece22_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece22_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece22_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece22_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece23'                   : fields.many2one('oemedical.patient.odontogram_piece', string="23", required=False),
        'piece23_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece23_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece23_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece23_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece23_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece23_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece24'                   : fields.many2one('oemedical.patient.odontogram_piece', string="24", required=False),
        'piece24_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece24_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece24_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece24_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece24_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece24_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece25'                   : fields.many2one('oemedical.patient.odontogram_piece', string="25", required=False),
        'piece25_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece25_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece25_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece25_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece25_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece25_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece26'                   : fields.many2one('oemedical.patient.odontogram_piece', string="26", required=False),
        'piece26_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece26_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece26_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece26_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece26_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece26_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece27'                   : fields.many2one('oemedical.patient.odontogram_piece', string="27", required=False),
        'piece27_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece27_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece27_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece27_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece27_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece27_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece28'                   : fields.many2one('oemedical.patient.odontogram_piece', string="28", required=False),
        'piece28_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece28_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece28_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece28_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece28_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece28_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece31'                   : fields.many2one('oemedical.patient.odontogram_piece', string="31", required=False),
        'piece31_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece31_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece31_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece31_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece31_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece31_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece32'                   : fields.many2one('oemedical.patient.odontogram_piece', string="32", required=False),
        'piece32_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece32_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece32_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece32_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece32_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece32_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece33'                   : fields.many2one('oemedical.patient.odontogram_piece', string="33", required=False),
        'piece33_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece33_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece33_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece33_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece33_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece33_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece34'                   : fields.many2one('oemedical.patient.odontogram_piece', string="34", required=False),
        'piece34_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece34_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece34_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece34_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece34_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece34_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece35'                   : fields.many2one('oemedical.patient.odontogram_piece', string="35", required=False),
        'piece35_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece35_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece35_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece35_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece35_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece35_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece36'                   : fields.many2one('oemedical.patient.odontogram_piece', string="36", required=False),
        'piece36_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece36_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece36_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece36_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece36_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece36_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece37'                   : fields.many2one('oemedical.patient.odontogram_piece', string="37", required=False),
        'piece37_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece37_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece37_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece37_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece37_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece37_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece38'                   : fields.many2one('oemedical.patient.odontogram_piece', string="38", required=False),
        'piece38_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece38_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece38_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece38_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece38_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece38_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece41'                   : fields.many2one('oemedical.patient.odontogram_piece', string="41", required=False),
        'piece41_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece41_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece41_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece41_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece41_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece41_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece42'                   : fields.many2one('oemedical.patient.odontogram_piece', string="42", required=False),
        'piece42_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece42_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece42_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece42_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece42_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece42_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece43'                   : fields.many2one('oemedical.patient.odontogram_piece', string="43", required=False),
        'piece43_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece43_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece43_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece43_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece43_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece43_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece44'                   : fields.many2one('oemedical.patient.odontogram_piece', string="44", required=False),
        'piece44_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece44_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece44_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece44_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece44_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece44_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece45'                   : fields.many2one('oemedical.patient.odontogram_piece', string="45", required=False),
        'piece45_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece45_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece45_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece45_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece45_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece45_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece46'                   : fields.many2one('oemedical.patient.odontogram_piece', string="46", required=False),
        'piece46_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece46_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece46_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece46_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece46_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece46_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece47'                   : fields.many2one('oemedical.patient.odontogram_piece', string="47", required=False),
        'piece47_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece47_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece47_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece47_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece47_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece47_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece48'                   : fields.many2one('oemedical.patient.odontogram_piece', string="48", required=False),
        'piece48_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece48_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece48_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece48_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece48_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        'piece48_total_prosthesis'  : fields.function(_get_piece_tp, type="boolean"),
        
        'piece51'                   : fields.many2one('oemedical.patient.odontogram_piece', string="51", required=False),
        'piece51_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece51_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece51_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece51_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece51_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece52'                   : fields.many2one('oemedical.patient.odontogram_piece', string="52", required=False),
        'piece52_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece52_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece52_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece52_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece52_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece53'                   : fields.many2one('oemedical.patient.odontogram_piece', string="53", required=False),
        'piece53_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece53_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece53_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece53_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece53_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece54'                   : fields.many2one('oemedical.patient.odontogram_piece', string="54", required=False),
        'piece54_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece54_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece54_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece54_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece54_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece55'                   : fields.many2one('oemedical.patient.odontogram_piece', string="55", required=False),
        'piece55_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece55_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece55_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece55_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece55_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece61'                   : fields.many2one('oemedical.patient.odontogram_piece', string="61", required=False),
        'piece61_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece61_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece61_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece61_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece61_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece62'                   : fields.many2one('oemedical.patient.odontogram_piece', string="62", required=False),
        'piece62_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece62_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece62_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece62_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece62_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece63'                   : fields.many2one('oemedical.patient.odontogram_piece', string="63", required=False),
        'piece63_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece63_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece63_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece63_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece63_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece64'                   : fields.many2one('oemedical.patient.odontogram_piece', string="64", required=False),
        'piece64_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece64_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece64_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece64_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece64_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece65'                   : fields.many2one('oemedical.patient.odontogram_piece', string="65", required=False),
        'piece65_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece65_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece65_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece65_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece65_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece71'                   : fields.many2one('oemedical.patient.odontogram_piece', string="71", required=False),
        'piece71_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece71_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece71_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece71_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece71_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece72'                   : fields.many2one('oemedical.patient.odontogram_piece', string="72", required=False),
        'piece72_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece72_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece72_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece72_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece72_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece73'                   : fields.many2one('oemedical.patient.odontogram_piece', string="73", required=False),
        'piece73_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece73_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece73_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece73_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece73_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece74'                   : fields.many2one('oemedical.patient.odontogram_piece', string="74", required=False),
        'piece74_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece74_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece74_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece74_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece74_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece75'                   : fields.many2one('oemedical.patient.odontogram_piece', string="75", required=False),
        'piece75_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece75_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece75_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece75_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece75_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece81'                   : fields.many2one('oemedical.patient.odontogram_piece', string="81", required=False),
        'piece81_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece81_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece81_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece81_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece81_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece82'                   : fields.many2one('oemedical.patient.odontogram_piece', string="82", required=False),
        'piece82_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece82_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece82_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece82_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece82_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece83'                   : fields.many2one('oemedical.patient.odontogram_piece', string="83", required=False),
        'piece83_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece83_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece83_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece83_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece83_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece84'                   : fields.many2one('oemedical.patient.odontogram_piece', string="84", required=False),
        'piece84_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece84_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece84_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece84_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece84_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'piece85'                   : fields.many2one('oemedical.patient.odontogram_piece', string="85", required=False),
        'piece85_zone_one_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece85_zone_two_summary'  : fields.function(_get_piece_summary, type="char"),
        'piece85_zone_three_summary': fields.function(_get_piece_summary, type="char"),
        'piece85_zone_four_summary' : fields.function(_get_piece_summary, type="char"),
        'piece85_zone_five_summary' : fields.function(_get_piece_summary, type="char"),
        
        'odontogram_ids'            : fields.one2many('oemedical.patient.odontogram','dentist_test_id','Odontograma'),
        
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
        
        'mouth_health_ind_ids': fields.one2many('oemedical.mouth.health.indicator','dentist_test_id','Higiene Oral Simplificada'),
        'periodontale_illness':fields.selection([('leve','Leve'),('moderada','Moderada'),('severa','Severa')],string = 'Enfermedad Periodontal'),
        'malocclusion':fields.selection([('angle1','Angle I'),('angle2','Angle II'),('angle3','Angle III')],string = 'Maloclusion'),
        'fluorosis':fields.selection([('leve','Leve'),('moderada','Moderada'),('severa','Severa')],string = 'Fluorosis'),
        
        'carieDC':fields.integer('DC'),
        'carieDP':fields.integer('DP'),
        'carieDO':fields.integer('DO'),
        'carie_dc':fields.integer('dc'),
        'carie_de':fields.integer('de'),
        'carie_do':fields.integer('do'),
        
        'totalCarieD': fields.function(_get_total_carie, string='Total carie D', type='integer',
                            store={
                                     'oemedical.dentist.test': (lambda self, cr, uid, ids, c=None: ids, ['carieDC','carieDP','carieDO'], 10),
                                  }, multi = "_carie"),
        'totalCarie_d': fields.function(_get_total_carie, string='Total carie d', type='integer',
                            store={
                                     'oemedical.dentist.test': (lambda self, cr, uid, ids, c=None: ids, ['carie_dc','carie_de','carie_do'], 10),
                                  }, multi = "_carie"),
        
        'totalPlate': fields.function(_get_total, string='Total Placas', type='integer', multi = "_total"),
        'totalStone': fields.function(_get_total, string='Total Calculo', type='integer',multi = "_total"),
        'totalGengivitis': fields.function(_get_total, string='Total Gengivitis', type='integer',multi = "_total"),
        
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
        'treatment_ids'              : fields.one2many('oemedical.treatment','dentist_test_id','Plan de Tratamiento'),
        'interconsult'               : fields.boolean('InterConsulta'),
        'internation'                : fields.boolean('Internacion'),
        'extern_consult'             : fields.boolean('Consulta Externa'),
        'fluor_topification'         : fields.boolean('Topicacion Fluor'),
        'sealment'                   : fields.boolean('Sellante'),
        'reference'                  : fields.boolean('Referencia'),
        'procedure'                  : fields.boolean('Procedimiento'),
        
        'incapacity_days'            : fields.integer('Dias de incapacidad'),
        'service'                    : fields.char('Servicio'),
        'treatment_observation'      : fields.text('Observaciones'),
        
        'next_appointment_date'      : fields.date(string='Fecha Proxima Cita'),    
        'doctor'                     : fields.many2one('oemedical.physician', string='Odontologo'),
        
        # 12. NOTAS DE EVOLUCION
        'evolution_ids'              : fields.one2many('oemedical.dentist.evolution', 'dentist_test_id', 'Notas de Evolucion'),
    
    
        # Odontograma 2 ...          
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
                    'test_date': time.strftime('%Y-%m-%d'),
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
OeMedicalDentistTest()

class OeMedicalPathology(osv.Model):
    _inherit = 'oemedical.pathology'

    _columns = {
     'definitive': fields.boolean(string='Definitivo'),
     'presuntive': fields.boolean(string='Presuntivo'),
     'foment': fields.boolean(string='Fomento'),
    } 
OeMedicalPathology()

class OeMedicalTreatment(osv.Model):
    _name = 'oemedical.treatment'
    
    _columns = {
     'name': fields.char(size=256, string='Medicamento Generico', required=True),        
     'concentration': fields.char(size=256, string='Concentracion'), 
     'presentation': fields.char(size=256, string='Presentacion'),       
     'via': fields.char(size=256, string='Via'),
     'dosis': fields.char(size=256, string='Dosis'),
     'frequency': fields.char(size=256, string='Frecuencia'),        
     'days': fields.char(size=256, string='Dias'),
     'dentist_test_id': fields.many2one('oemedical.dentist.test', 'Dentist Test', required=True),
    }
OeMedicalTreatment()

class OeMedicalDentistEvolution(osv.Model):
    _name = 'oemedical.dentist.evolution'
    _columns = {
     'name': fields.char(size=256, string='Medicamento Generico', required=True),        
     'evolution_date': fields.datetime(string='Fecha'),
     'observation': fields.text('Observaciones'),
     'dentist_test_id': fields.many2one('oemedical.dentist.test', 'Dentist Test', required=True),
    }    
OeMedicalDentistEvolution()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
