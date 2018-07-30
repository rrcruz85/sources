# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from osv import osv
from osv import fields

class group_box_wizard(osv.osv_memory):
    _name = 'group.box.wizard'
    _description = 'Group Lines By Box'

    _columns = {
        'pedido_id'         : fields.many2one('pedido.cliente', 'Pedido'),  
        'lines_selected'    : fields.char(size=128, string='Lines'),
        'line_ids'          : fields.one2many('group.box.line.wizard', 'group_id', 'Lines'),             
    }
    
    _defaults = {
        'pedido_id'    :  lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else False,
    }
    
    def on_chance_line_ids(self, cr, uid, ids, line_ids, context=None):
        result = {}        
        if line_ids:             
            lines = [l[2]['lines'] for l in line_ids if l[0] == 0]         
            result['value'] = {
                'lines_selected': ','.join(lines)
            }
        return result
    
    def save(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0])
        lines = []
        for l in obj.line_ids:
            lines += [ll.detalle_id.id for ll in l.detalle_ids]
       
        self.pool.get('detalle.lines').write(cr, uid, lines, {'box': True})
         
        return {
            'name'      : 'Pedidos de Clientes',
            'view_type' : 'form',
            'view_mode' : 'form,tree',
            'res_model' : 'pedido.cliente',
            'type'      : 'ir.actions.act_window',
            #'res_id'    : obj.pedido_id.id,
        }

        
group_box_wizard()

class group_box_line_wizard(osv.osv_memory):
    _name = 'group.box.line.wizard'
    _description = 'Group Lines By Box'
   
    _columns = {
        'group_id'          : fields.many2one('group.box.wizard', 'Group'), 
        'pedido_id'         : fields.many2one('pedido.cliente', 'Pedido'), 
        'box'               : fields.char(size=2, string='Box'),
        'lines'             : fields.char(size=128, string='Lines'),
        'lines_selected'    : fields.char(size=128, string='Lines'),
        'detalle_ids'       : fields.many2many('purchase.lines.wzd', 'group_box_purchase_lines_relation', 'group_id', 'detalle_id', 'Lines'),             
    }
    
    def on_chance_detalle_ids(self, cr, uid, ids, detalle_ids, context=None):
        result = {}        
        if detalle_ids and detalle_ids[0] :
            lines = self.pool.get('purchase.lines.wzd').read(cr, uid, detalle_ids[0][2], ['line_number'])            
            result['value'] = {
                'lines':  ','.join([str(l['line_number']) for l in lines])
            }
        return result
    
    _defaults = {
        'box'               :  '1',
        'group_id'          :  lambda self, cr, uid, context : context['group_id'] if context and 'group_id' in context else False,
        'pedido_id'         :  lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else False,
        'lines_selected'    :  lambda self, cr, uid, context : context['lines_selected'] if context and 'lines_selected' in context else False,
    }
        
group_box_line_wizard()


           
