# -*- coding: utf-8 -*-

from openerp import (
    models,
    fields,
    api
)


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'
   
    @api.one
    @api.depends('auth_inv_id')
    def _get_invoice_number(self):    
        if self.auth_inv_id and self.auth_inv_id.sequence_id:
            inv_number = self.env['ir.sequence'].get_id(self.auth_inv_id.sequence_id.id)            
            inv_number = str(inv_number).zfill(self.auth_inv_id.sequence_id.padding)
            inv_number = '{0}{1}{2}'.format(self.auth_inv_id.serie_entidad, self.auth_inv_id.serie_emision, inv_number)
            self.invoice_number = inv_number
            self.supplier_invoice_number = inv_number
        else:    
            self.invoice_number = '*'
            self.supplier_invoice_number = '*'

    invoice_number = fields.Char(
        compute='_get_invoice_number',
        store=True,
        readonly=True,
        copy=False
    )
    
    supplier_invoice_number = fields.Char(
        compute='_get_invoice_number',
        store=True,
        readonly=True,
        copy=False
    )