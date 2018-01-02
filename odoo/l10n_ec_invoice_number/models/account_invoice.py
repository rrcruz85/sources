# -*- coding: utf-8 -*-
import logging
from openerp.osv import osv
from l10n_ec_einvoice import utils
import datetime

from openerp import (
    models,
    fields,
    api,
    _
)

_logger = logging.getLogger(__name__)


class pos_order(osv.osv):
    _inherit = "pos.order"

    def action_invoice(self, cr, uid, ids, context=None):
        inv_ref = self.pool.get('account.invoice')
        inv_line_ref = self.pool.get('account.invoice.line')
        product_obj = self.pool.get('product.product')
        inv_ids = []

        for order in self.pool.get('pos.order').browse(cr, uid, ids, context=context):
            if order.invoice_id:
                inv_ids.append(order.invoice_id.id)
                continue

            if not order.partner_id:
                raise osv.except_osv(_('Error!'), _('Please provide a partner for the sale.'))

            acc = order.partner_id.property_account_receivable.id
            inv = {
                'name': order.name,
                'origin': order.name,
                'account_id': acc,
                'journal_id': order.sale_journal.id or None,
                'type': 'out_invoice',
                'reference': order.name,
                'partner_id': order.partner_id.id,
                'comment': order.note or '',
                'currency_id': order.pricelist_id.currency_id.id,  # considering partner's sale pricelist's currency
                'from_pos':True,
                'date_invoice': datetime.datetime.now().strftime('%Y-%m-%d')
            }
            inv.update(inv_ref.onchange_partner_id(cr, uid, [], 'out_invoice', order.partner_id.id)['value'])

            inv.update({'fiscal_position': order.partner_id.property_account_position and order.partner_id.property_account_position.id or False})
            if not inv.get('account_id', None):
                inv['account_id'] = acc
                
            if order.sale_journal and order.sale_journal.auth_id:
                inv['auth_inv_id'] = order.sale_journal.auth_id.id
                inv_number = self.pool.get('ir.sequence').get_id(cr, uid, order.sale_journal.auth_id.sequence_id.id)
                inv_number = str(inv_number).zfill(order.sale_journal.auth_id.sequence_id.padding)
                inv['supplier_invoice_number'] = '{0}{1}{2}'.format(order.sale_journal.auth_id.serie_entidad, order.sale_journal.auth_id.serie_emision, inv_number)
                
            inv_id = inv_ref.create(cr, uid, inv, context=context)

            self.write(cr, uid, [order.id], {'invoice_id': inv_id, 'state': 'invoiced'}, context=context)
            inv_ids.append(inv_id)
            for line in order.lines:
                inv_line = {
                    'invoice_id': inv_id,
                    'product_id': line.product_id.id,
                    'quantity': line.qty,
                }
                inv_name = product_obj.name_get(cr, uid, [line.product_id.id], context=context)[0][1]
                inv_line.update(inv_line_ref.product_id_change(cr, uid, [],
                                                               line.product_id.id,
                                                               line.product_id.uom_id.id,
                                                               line.qty, partner_id=order.partner_id.id)['value'])
                if not inv_line.get('account_analytic_id', False):
                    inv_line['account_analytic_id'] = \
                        self._prepare_analytic_account(cr, uid, line,
                                                       context=context)
                inv_line['price_unit'] = line.price_unit
                inv_line['discount'] = line.discount
                inv_line['name'] = inv_name
                if order.apply_taxes or order.amount_card_comition:
                    taxes_lines = inv_line['invoice_line_tax_id']
                    if order.amount_card_comition:
                        inv_line['price_unit'] = inv_line['price_unit'] + order.amount_card_comition
                    inv_line['invoice_line_tax_id'] = [(6, 0, taxes_lines)]
                else:
                    inv_line['invoice_line_tax_id'] = []
                inv_line_ref.create(cr, uid, inv_line, context=context)

            inv_ref.button_reset_taxes(cr, uid, [inv_id], context=context)
            self.signal_workflow(cr, uid, [order.id], 'invoice')
            inv_ref.signal_workflow(cr, uid, [inv_id], 'validate')

        if not inv_ids:
            return {}

        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
        res_id = res and res[1] or False
        return {
            'name': _('Customer Invoice'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': 'account.invoice',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': inv_ids and inv_ids[0] or False,
        }
        
class Invoice(models.Model):

    _inherit = 'account.invoice'
    
    @api.one
    @api.depends(
        'state',
        'supplier_invoice_number',
        'journal_id',
        'from_pos'
    )
    def _get_invoice_number(self):
        """
        Calcula el numero de factura segun el
        establecimiento seleccionado
        """
        if self.supplier_invoice_number or self.journal_id:
            
            if not self.supplier_invoice_number and self.journal_id and self.journal_id.auth_id:
                inv_number = self.env['ir.sequence'].get_id(self.journal_id.auth_id.sequence_id.id)
                inv_number = str(inv_number).zfill(self.journal_id.auth_id.sequence_id.padding)
                if not self.supplier_invoice_number:
                    self.invoice_number = '{0}{1}{2}'.format(self.journal_id.auth_id.serie_entidad, self.journal_id.auth_id.serie_emision, inv_number)
                self.supplier_invoice_number = self.invoice_number
            else:
                if not self.supplier_invoice_number:
                    self.invoice_number = '{0}{1}{2}'.format(
                        self.auth_inv_id.serie_entidad,
                        self.auth_inv_id.serie_emision,
                        self.supplier_invoice_number
                    )
                else:
                    self.invoice_number = self.supplier_invoice_number
        else:            
            self.invoice_number = '*'       
       
    
    from_pos = fields.Boolean(
        string='Creada Desde POS',
        readonly=True)     
   
    @api.onchange('supplier_invoice_number')
    def check_invoice_supplier(self):
        if self.supplier_invoice_number and len(self.supplier_invoice_number) != 9:  # noqa
            self.supplier_invoice_number = self.supplier_invoice_number.zfill(9)  # noqa

    @api.constrains('reference')
    def check_reference(self):
        """
        Metodo que verifica la longitud de la autorizacion
        10: documento fisico
        35: factura electronica modo online
        49: factura electronica modo offline
        """
        if not self.from_pos and self.reference and len(self.reference) not in [10, 35, 49]:
            raise Warning(
                'Error',
                u'Debe ingresar 10, 35 o 49 dígitos según el documento.'
            )
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
