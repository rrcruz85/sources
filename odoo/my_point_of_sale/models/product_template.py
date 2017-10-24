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

class product_product(osv.osv):
    _inherit = "product.product"

    def _get_stock_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, 0)
        for product_id in ids:
            lot_ids = self.pool.get('stock.production.lot').search(cr, uid, [('product_id', '=', product_id)])
            if lot_ids:
                qty_per_lot = 0
                quant_ids = self.pool.get("stock.quant").search(cr, uid, [('lot_id', 'in', lot_ids)], context=context)
                if quant_ids:
                    records = self.pool.get("stock.quant").read(cr, uid, quant_ids, ['qty'], context=context)
                    qty_per_lot = reduce(lambda x, y: x + y,  map(lambda x: x['qty'], records))
                line_ids = self.pool.get('pos.order.line').search(cr, uid, [('lot_id', 'in', lot_ids)])
                qty_sold = 0
                if line_ids:
                    lines = self.pool.get('pos.order.line').read(cr, uid, line_ids, ['qty'])
                    qty_sold = reduce(lambda x, y: x + y, map(lambda x: x['qty'], lines))
                res[product_id] = qty_per_lot - qty_sold
            else:
                record = self.read(cr, uid, product_id, ['virtual_available'])
                res[product_id] = record['virtual_available']
        return res

    _columns = {
        'stock_qty': fields.function(_get_stock_qty, type='integer', string='Stock Qty')
    }
