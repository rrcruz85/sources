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
from openerp.tools.translate import _

class account_invoice(osv.osv):
    _inherit = "account.invoice"

    _columns = {
        'pedido_cliente_id' : fields.many2one('pedido.cliente', string ="Pedido Cliente"),
    }

account_invoice()


class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    def _get_bunches(self, cr, uid, ids, field_name, arg, context):
        result = {}
        uom = {'FB':1,'HB':2,'QB':4,'OB':8}
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = obj.quantity /(int(obj.bunch_type) * uom[obj.uom]) if obj.bunch_type and obj.uom and not obj.is_box_qty else  obj.quantity * obj.bunch_per_box / uom[obj.uom] if obj.uom else 0
        return result

    _columns = {
        'sequence_box'  : fields.integer(string = "SQ", help='Sequence'),
        'box'               : fields.float(string='FB', help="Full Boxes"),
        'qty_bxs'              : fields.char(string='BXS', size = 10),
        'uom'                   : fields.selection([('FB', 'FB'),
                                                            ('HB', 'HB'),
                                                            ('QB', 'QB'),
                                                            ('OB', 'OB')], string = "UOM", help='Unit of Measure'),
        'bunch_type'            : fields.selection([('6', '6'),
                                                    ('10', '10'),
                                                    ('12', '12'),
													('15', '15'),
													('20', '20'),
                                                    ('25', '25')], 'Stems x Bunch'),
        'bunches'            : fields.function(_get_bunches, type='integer', string='Total Bunches'),
        'is_box_qty'            : fields.boolean('Box Packing?'),
        'bunch_per_box'   : fields.integer('Bunch per Box'),
   }

    _defaults = {
        'uom': 'HB',
        'bunch_per_box' : 10,
        'bunch_type': '25',
    }

account_invoice_line()
