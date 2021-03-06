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
from openerp.osv import osv
from openerp.osv import fields

class summary_by_farm_wizard(osv.osv_memory):
    _name = 'summary.by.farm.wizard'
    _description = 'Summary By Farms'

    _columns = {
        'pedido_id'       : fields.many2one('pedido.cliente', 'Pedido',),
        'farm_id'         : fields.many2one('res.partner', 'Farm'),
        'subclient_id'    : fields.many2one('res.partner', 'SubCliente'),
        'hb'              : fields.float('HB'),
        'qb'              : fields.float('QB'),
        'box'             : fields.float('FBX', help='Full Boxes'),
        'stems'           : fields.integer('Stems'),
        'total_sale'      : fields.float('Total Sale')
    } 

summary_by_farm_wizard()