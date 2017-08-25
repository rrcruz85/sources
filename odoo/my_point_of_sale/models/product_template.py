# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class ProductTemplate(osv.osv):
    _inherit = "product.template"
    _columns = {
        # To select the TPVs list where the product will be available...
        'tpv_list_ids': fields.many2many(
            'pos.config', 'my_pos_product_pos_config_rel', 'product_id', 'tpv_id',
            string='TPVs where the product will be available...'
        )
    }
