# -*- encoding: utf-8 -*-
from osv import osv
from osv import fields

class group_box_wizard(osv.osv_memory):
    _name = 'group.box.wizard'
    _description = 'Group Lines By Box'

    _columns = {
        'pedido_id'         : fields.many2one('pedido.cliente', 'Pedido'),  
        'lines_selected'    : fields.char(size=128, string='Lines'),
        'box'               : fields.integer(string='Box Id', help = 'Box id must be unique per client request'),
        'line_ids'          : fields.one2many('group.box.line.wizard', 'group_id', 'Lines'), 
        'last_box'          : fields.integer(string='Last Box Id'),             
    }
    
    _defaults = {
        'pedido_id'    :  lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else False,
    }
    
    def on_chance_line_ids(self, cr, uid, ids, line_ids, lines_selected, context=None):
        result = {}        
        if line_ids:             
            lines = [l[2]['lines'] for l in line_ids if l[0] == 0] 
            added = filter(lambda r: r[0] == 0, line_ids)            
            last_box = added[-1][2]['box'] if added else 0       
            
            result['value'] = {                 
                'lines_selected' : (lines_selected + ','  if lines_selected else '')  + ','.join(lines),
                'last_box' : last_box + 1
            }
        return result
    
    def save(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0])   
        pedido_id = obj.pedido_id.id     
        groups = []
        for l in obj.line_ids:
            boxes = [d.box_id.id for d in l.detalle_ids if d.box_id]
            if boxes:
                groups += list(set(boxes))               
            group_id = self.pool.get('detalle.lines.box').create(cr, uid, {'box': l.box,'pedido_id': pedido_id})
            self.pool.get('detalle.lines').write(cr, uid, [d.detalle_id.id for d in l.detalle_ids], {'box_id': group_id})
        if groups:
            self.pool.get('detalle.lines.box').write(cr, uid, list(set(groups)),{'active':False})
            
        return {
            'name'      : 'Pedidos de Clientes',
            'view_type' : 'form',
            'view_mode' : 'form,tree',
            'res_model' : 'pedido.cliente',
            'type'      : 'ir.actions.act_window',
            'res_id'    : pedido_id,
        }
        
group_box_wizard()

class group_box_line_wizard(osv.osv_memory):
    _name = 'group.box.line.wizard'
    _description = 'Group Lines By Box'
   
    _columns = {         
        'group_id'          : fields.many2one('group.box.wizard', 'Group'), 
        'pedido_id'         : fields.many2one('pedido.cliente', 'Pedido'), 
        'box'               : fields.integer(string='Box Id', help = 'Box id must be unique per client request'),
        'lines'             : fields.char(size=128, string='Lines'),
        'lines_selected'    : fields.char(size=128, string='Lines'),
        'detalle_ids'       : fields.many2many('purchase.lines.wzd', 'group_box_purchase_lines_relation', 'group_id', 'detalle_id', 'Lines'),             
    }
    
    def on_chance_detalle_ids(self, cr, uid, ids, detalle_ids, lines_selected, context=None):
        result = {}        
        if detalle_ids and detalle_ids[0] :
            lines = self.pool.get('purchase.lines.wzd').read(cr, uid, detalle_ids[0][2], ['line_number'])            
            result['value'] = {
                'lines'          : ','.join([str(l['line_number']) for l in lines]),
                'lines_selected' : (lines_selected + ','  if lines_selected  else '') + ','.join([str(l['line_number'] or '') for l in lines])
            }     
        return result
    
    def get_box_number(self, cr, uid, context=None):
        return context['last_box'] if 'last_box' in context and context['last_box'] else context['box'] if 'box' in context else 1                    
        
    _defaults = {
        'box'               :  get_box_number,
        'group_id'          :  lambda self, cr, uid, context : context['group_id'] if context and 'group_id' in context else False,
        'pedido_id'         :  lambda self, cr, uid, context : context['pedido_id'] if context and 'pedido_id' in context else False,
        'lines_selected'    :  lambda self, cr, uid, context : context['lines_selected'] if context and 'lines_selected' in context else False,
    }
        
group_box_line_wizard()


           
