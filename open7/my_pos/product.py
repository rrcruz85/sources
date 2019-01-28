
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class product(osv.Model):
    _inherit = 'product.product'
    
    _columns = {
        # To select the TPVs list where the product will
        # be available...
        'secondary_price' : fields.float('Secondary Sale Price', digits_compute = dp.get_precision('Product Price')),
        'tpv_list_ids'    : fields.many2many('pos.config', 'my_pos_product_pos_config_rel', 'product_id', 'tpv_id', string='TPVs where the product will be available...', limit=20)
    }

product()

class pos_config(osv.Model):
    _inherit = 'pos.config' 
    _columns = {
        'products_ids'          : fields.many2many('product.product', 'my_pos_product_pos_config_rel', 'tpv_id', 'product_id', string='Available products...', limit=20)
    }
    
pos_config()
    