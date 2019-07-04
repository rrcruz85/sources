
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class product(osv.Model):
    _inherit = 'product.product'
    
    _columns = {
        # To select the TPVs list where the product will
        # be available...
        'tpv_list_ids'     : fields.many2many('pos.config', 'my_pos_product_pos_config_rel', 'product_id', 'tpv_id', string='TPVs where the product will be available...', limit=20),
        'sale_price_ids'   : fields.one2many('product.price', 'product_id', 'Alternative Sale Prices'),
    }

product()


class product_price(osv.Model):
    _name = 'product.price'
    _description = 'Product Prices'
    _rec_name = 'price'
    _columns = {
        'name'         : fields.char('Name', size = 7, required=True, help='Promotion Name'),
        'price'        : fields.float('Sale Price', digits_compute = dp.get_precision('Product Price'), help='Alternative Sale Price'),
        'product_id'   : fields.many2one('product.product', 'Product', required=True),
    }
    
    def _check_price(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.price > 0  
        
    _constraints = [
        (_check_price, 'El precio del producto debe ser mayor que cero.', []),
    ]
    
    _sql_constraints = [
        ('name_product_uniq', 'unique(name, product_id)', 'No se pueden repetir los nombres de los precios por producto'),
        ('price_product_uniq', 'unique(price, product_id)', 'No se pueden repetir los precios por producto'),
    ]
    
    _defaults = {
        'product_id'  :  lambda self, cr, uid, context : context['product_id'] if context and 'product_id' in context else None,
    }
    
product_price()


class pos_config(osv.Model):
    _inherit = 'pos.config' 
    _columns = {
        'products_ids'          : fields.many2many('product.product', 'my_pos_product_pos_config_rel', 'tpv_id', 'product_id', string='Available products...', limit=20)
    }
    
pos_config()
    