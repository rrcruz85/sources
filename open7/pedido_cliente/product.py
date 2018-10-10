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

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    
    _columns = {
        'variants_ids'          : fields.one2many('product.variant', 'product_id', 'Variantes')
    }
product_product()

class product_variant(osv.osv):
    _name = 'product.variant'
    _description = 'product.variant'
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context={}, count=False):
        if (context.has_key('product_id')):
            args += [('product_id', '=', context['product_id'])]
        return super(product_variant, self).search(cr, uid, args, offset, limit, order, context, count)

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if context and 'request_id' in context:
            p = self.pool.get('pedido.cliente').browse(cr, user, context['request_id'])
            variants = [v.variant_id.id for v in p.variant_ids]
            return  self.name_get(cr, user, variants, context)
        return super(product_variant, self).name_search(cr, user, name, args, operator=operator, context=context, limit=limit)

    _columns = {
        'code'                  : fields.char('Codigo', size = 10, required = True),
        'name'                  : fields.char('Nombre', size = 128, required = True),
        'price'                 : fields.float('Precio', digits=(16, 6)),
        'description'           : fields.text('Length or Weigth'),
        'product_id'            : fields.many2one('product.product', 'Producto', required = True)
    }

product_variant()

class product_supplierinfo(osv.osv):
    _name = 'product.supplierinfo'
    _inherit = 'product.supplierinfo'
    
    _defaults = {
        'product_id'            : lambda self, cr, uid, context : context['product_id'] if context and 'product_id' in context else None,
    }

product_supplierinfo()