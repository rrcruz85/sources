# -*- coding: utf-8 -*-

from openerp import models,api
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

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        base_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_untaxed = base_untaxed
        if self.pos_order_ids:
            for order in self.pos_order_ids:
                self.amount_tax = order.amount_tax
                self.amount_total = order.amount_total
                break
        else:
            self.amount_untaxed = self.amount_vat = self.amount_tax = self.amount_vat_cero = 0.00
            self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)  # noqa
            for line in self.tax_line:
                if line.tax_group == 'imp_ad':
                    # self.amount_duty += line.base
                    self.amount_duty += line.amount
                    self.amount_tax += line.amount
                if line.tax_group == 'vat':
                    self.amount_vat += line.base
                    self.amount_tax += line.amount
                elif line.tax_group == 'vat0':
                    self.amount_vat_cero += line.base
                    # self.__logger.info('vat0 %s ' % (self.amount_vat_cero))
                elif line.tax_group == 'novat':
                    self.amount_novat += line.base
                elif line.tax_group == 'no_ret_ir':
                    self.amount_noret_ir += line.base
                elif line.tax_group in ['ret_vat_b', 'ret_vat_srv', 'ret_ir']:
                    self.amount_tax_retention += line.amount
                    if line.tax_group == 'ret_vat_b':
                        self.amount_tax_ret_vatb += line.base
                        self.taxed_ret_vatb += line.amount
                    elif line.tax_group == 'ret_vat_srv':
                        self.amount_tax_ret_vatsrv += line.base
                        self.taxed_ret_vatsrv += line.amount
                    elif line.tax_group == 'ret_ir':
                        self.amount_tax_ret_ir += line.base
                        self.taxed_ret_ir += line.amount
                elif line.tax_group == 'ice':
                    self.amount_ice += line.amount
            if self.amount_vat == 0 and self.amount_vat_cero == 0:
                self.amount_vat_cero = self.amount_untaxed
            self.amount_total = self.amount_untaxed + self.amount_tax + self.amount_tax_retention  # noqa
            self.amount_total_letras = self.toWord(self.amount_total)
            self.amount_pay = self.amount_tax + self.amount_untaxed


    _columns = {
        'pos_order_ids': fields.one2many('pos.order', 'invoice_id', string='Pos Orders'),
        'iva_compensation': fields.function(_get_iva_compensation, type='float', string='IVA Compensation'),
        'amount_total_with_iva_compensation': fields.function(_get_amount_total_with_iva_compensation, type='float', string='Total'),
        'card_comition': fields.float(string='Card Comition'),
    }

class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    _columns = {
        'lot_id': fields.many2one('stock.production.lot', 'Product Lot', ondelete='set null'),
    }




