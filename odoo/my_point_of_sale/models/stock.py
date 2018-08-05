# -*- coding: utf-8 -*-

import logging
from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)

class stock_production_lot(osv.osv):
    _inherit = 'stock.production.lot'

    def get_lots(self, cr, uid, ids, context=None):
        quant_obj = self.pool.get("stock.quant")
        quants = quant_obj.search(cr, uid, [('lot_id', 'in', ids[0])], context=context)
        #line_ids = self.pool.get('stock.inventory.line').search(cr, uid, [('prod_lot_id', 'in', ids[0])], order ="id desc", limit=1)
        lots = {}
        qtys = []
        for quant in quant_obj.browse(cr, uid, quants, context=context):
            if quant.qty > 0:
                if quant.lot_id.id not in lots:
                    line_ids = self.pool.get('pos.order.line').search(cr, uid,[('lot_id', '=', quant.lot_id.id)])
                    cant_sold = 0
                    if line_ids:
                        vals = self.pool.get('pos.order.line').read(cr, uid, line_ids, ['qty'])
                        cant_sold = reduce(lambda x, y: x+y, map(lambda x: x['qty'], vals))
                    lots[quant.lot_id.id] = {'name': quant.lot_id.name, "qty": quant.qty, "cant_sold" : cant_sold}
                else:
                    lots[quant.lot_id.id]['qty'] += quant.qty
        for key in lots.keys():
            if lots[key]['qty'] > lots[key]['cant_sold']:
                qty = lots[key]['qty'] - lots[key]['cant_sold']
                qtys.append((key, lots[key]['name'], qty, qty))
        return qtys


