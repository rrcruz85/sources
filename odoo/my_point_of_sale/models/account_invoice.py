# -*- coding: utf-8 -*-

from openerp import models
from openerp.osv import fields, osv


class AccountInvoice(osv.osv):
    _inherit = "account.invoice"

    def _get_iva_compensation(self, cr, uid, ids, fields, args, context=None):
        if not ids:
           return {}

        res = {}
        for i in self.browse(cr, uid, ids, context):
            if i.pos_order_ids:
               res[i.id] = i.pos_order_ids[0].amount_iva_compensation
        return res

    def _get_amount_total_with_iva_compensation(self, cr, uid, ids, fields, args, context=None):
        if not ids:
           return {}

        res = {}
        for i in self.browse(cr, uid, ids, context):
            if i.pos_order_ids:
               res[i.id] = i.amount_total - i.pos_order_ids[0].amount_iva_compensation
        return res

    _columns = {
        'pos_order_ids': fields.one2many('pos.order', 'invoice_id', string='Pos Orders'),
        'iva_compensation': fields.function(_get_iva_compensation, type='float', string='IVA Compensation'),
        'amount_total_with_iva_compensation': fields.function(
            _get_amount_total_with_iva_compensation, type='float', string='Total'
        ),
    }
