# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Module - Ecuador
#    Copyright (C) 2017 Core Cloud Cia Ltda All Rights Reserved
#    osantacruz@corecloud.ec
#    $Id$
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tools.translate import _
from openerp import models, fields
import logging

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    taxes_id = fields.Many2many(
            'account.tax', 'categ_taxes_rel',
            'prod_id', 'tax_id', 'Customer Taxes',
            domain=[('parent_id', '=', False), ('type_tax_use', 'in', ['sale', 'all'])])  # noqa
    supplier_taxes_id = fields.Many2many(
            'account.tax',
            'categ_supplier_taxes_rel', 'prod_id', 'tax_id',
            'Supplier Taxes',
            domain=[('parent_id', '=', False), ('type_tax_use', 'in', ['purchase', 'all'])])  # noqa

class ProductProduct(models.Model):

    _inherit = 'product.template'

    def get_product_accounts(self, cr, uid, product_id, context=None):
        """ To get the stock input account, stock output account and stock journal related to product.
        @param product_id: product id
        @return: dictionary which contains information regarding stock input account, stock output account and stock journal
        """
        if not context.get('force_company', False):
            user_company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
            context.update({'force_company': user_company_id})

        property_obj = self.pool.get('ir.property')

        if context is None:
            context = {}
        product_obj = self.browse(cr, uid, product_id, context=context)

        stock_input_acc = product_obj.property_stock_account_input and product_obj.property_stock_account_input.id or False
        if not stock_input_acc:
            stock_input_acc = product_obj.categ_id.property_stock_account_input_categ and product_obj.categ_id.property_stock_account_input_categ.id or False
        if not stock_input_acc:
            # 2017-07-14
            # Cuando no encuentra la cuenta en las propiedades de compania actual
            # se asume que la compania actual es la madre la compania para la transaccion
            # por tanto se forza para buscar en la propiedad de la compania del usuario conectado
            # y el periodo tambien se cambia a la compania del usuario conectado
            user_company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
            context['force_company'] = user_company_id
            _logger.info('user co: %s ' % (user_company_id))
            _logger.info('acount input contest: %s ' % (context))
            stock_input_acc = property_obj.get(cr, uid, 'property_stock_account_input_categ', 'product.category', context=context).id
            period_obj = self.pool.get('account.period')
            context['force_period'] = False
            date = fields.date.today()
            period_id = period_obj.find(cr, uid, date, context)[0]
            context['force_period'] = period_id
            ###################################################################################

        stock_output_acc = product_obj.property_stock_account_output and product_obj.property_stock_account_output.id or False
        if not stock_output_acc:
            stock_output_acc = product_obj.categ_id.property_stock_account_output_categ and product_obj.categ_id.property_stock_account_output_categ.id or False
        if not stock_output_acc:
            _logger.info('account output context ' % (context))
            stock_output_acc = property_obj.get(cr, uid, 'property_stock_account_output_categ', 'product.category', context=context).id

        journal_id = product_obj.categ_id.property_stock_journal and product_obj.categ_id.property_stock_journal.id or False
        # 2017-07-14
        if not journal_id:
            journal_id = property_obj.get(cr, uid, 'property_stock_journal', 'product.category', context=context).id
        account_valuation = product_obj.categ_id.property_stock_valuation_account_id and product_obj.categ_id.property_stock_valuation_account_id.id or False
        if not account_valuation:
            account_valuation = property_obj.get(cr, uid, 'property_stock_valuation_account_id', 'product.category', context=context).id

        if not all([stock_input_acc, stock_output_acc, account_valuation, journal_id]):
            raise osv.except_osv(_('Error!'), _('''One of the following information is missing on the product or product category and prevents the accounting valuation entries to be created:
    Product: %s
    Stock Input Account: %s
    Stock Output Account: %s
    Stock Valuation Account: %s
    Stock Journal: %s
    ''') % (product_obj.name, stock_input_acc, stock_output_acc, account_valuation, journal_id))
        return {
            'stock_account_input': stock_input_acc,
            'stock_account_output': stock_output_acc,
            'stock_journal': journal_id,
            'property_stock_valuation_account_id': account_valuation
        }

    def do_change_standard_price(self, cr, uid, ids, new_price, context=None):
        """ Changes the Standard Price of Product and creates an account move accordingly."""
        location_obj = self.pool.get('stock.location')
        period_obj = self.pool.get('account.period')
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        property_obj = self.pool.get('ir.property')
        if context is None:
            context = {}
        user_company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        loc_ids = location_obj.search(cr, uid, [('usage', '=', 'internal'), ('company_id', '=', user_company_id)])
        for rec_id in ids:
            datas = self.get_product_accounts(cr, uid, rec_id, context=context)
            for location in location_obj.browse(cr, uid, loc_ids, context=context):
                c = context.copy()
                c.update({'location': location.id, 'compute_child': False})
                product = self.browse(cr, uid, rec_id, context=c)

                diff = product.standard_price - new_price
                if not diff:
                    raise osv.except_osv(_('Error!'), _("No difference between standard price and new price!"))
                for prod_variant in product.product_variant_ids:
                    qty = prod_variant.qty_available
                    if qty:
                        # Accounting Entries
                        move_vals = {
                            'journal_id': datas['stock_journal'],
                            'company_id': location.company_id.id,
                        }
                        move_id = move_obj.create(cr, uid, move_vals, context=context)
                        
                        # 22 feb 2017
                        # Al crear el movimiento cambia la compania a 5, por ejemplo
                        query = 'UPDATE "%s" SET %s WHERE id = %s' % (
                                move_obj._table, '"company_id"=%s' % move_vals['company_id'], move_id)
                        cr.execute(query)
                        if cr.rowcount == 0:
                            raise osv.except_osv(_('Error!'), _("No existe el registro del movimiento contable!"))
                        # Obtener company_id del movimiento para obtener las cuentas y journal
                        # Se obtiene el periodo de la compania del movimiento, p.ej 5
                        #cid = context.get('company_id', 1)
                        #company_id = move_obj.browse(cr, uid, [move_id], context)[0].company_id.id
                        #context.update({'force_company': company_id})
                        #context.update({'company_id': company_id})
                        #date = fields.date.today()
                        #period_id = period_obj.find(cr, uid, date, context)[0]
                        #context.update({'company_id': cid})
                        #context.update({'period_id': period_id})
                        # el 22 feb 2017

                        counterpart_account = product.property_account_expense and product.property_account_expense.id or False
                        if not counterpart_account:
                            counterpart_account = product.categ_id.property_account_expense_categ and product.categ_id.property_account_expense_categ.id or False
                        if not counterpart_account:
                            counterpart_account = property_obj.get(cr, uid, 'property_account_expense_categ', 'product.category', context=context).id
                        if not counterpart_account:
                            raise osv.except_osv(_('Error!'), _('No expense account defined on the product %s or on its category') % (product.name))
                        if diff * qty > 0:
                            amount_diff = qty * diff
                            debit_account_id = counterpart_account
                            credit_account_id = datas['property_stock_valuation_account_id']
                        else:
                            amount_diff = qty * -diff
                            debit_account_id = datas['property_stock_valuation_account_id']
                            credit_account_id = counterpart_account

                        move_line_obj.create(cr, uid, {
                                        'name': _('Standard Price changed'),
                                        'account_id': debit_account_id,
                                        'debit': amount_diff,
                                        'credit': 0,
                                        'move_id': move_id,
                                        }, context=context)
                        move_line_obj.create(cr, uid, {
                                        'name': _('Standard Price changed'),
                                        'account_id': credit_account_id,
                                        'debit': 0,
                                        'credit': amount_diff,
                                        'move_id': move_id
                                        }, context=context)
            self.write(cr, uid, rec_id, {'standard_price': new_price})
        return True
