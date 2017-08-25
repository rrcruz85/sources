# -*- coding: utf-8 -*-

from lxml import etree
from openerp.osv import fields, osv


class AccountBankStatement(osv.osv):
    _inherit = "account.bank.statement"

    # def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
    #     res = super(AccountBankStatement, self).fields_view_get(
    #         cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=False
    #     )
    #
    #     doc = etree.XML(res['arch'])
    #     for node in doc.xpath("//field[@name='line_ids']"):
    #         node.set('context', "{'tree_view_ref': 'my_point_of_sale.my_point_of_sale_account_bank_statement_line_tree_view_for_check'}")
    #
    #     res['arch'] = etree.tostring(doc)
    #     return res

    def _get_journal_type(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = obj.journal_id.type
        return res

    _columns = {
        'journal_type': fields.function(_get_journal_type, type='char', string='Payment Type')
    }


class AccountBankStatementLine(osv.osv):
    _inherit = "account.bank.statement.line"

    def _get_order_info(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, {})
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {
                'approval_number': obj.pos_statement_id.approval_number,
                'check_number': obj.pos_statement_id.check_number,
                'card_number': obj.pos_statement_id.card_number,
                'lot_number': obj.pos_statement_id.lot_number,
                'reference': obj.pos_statement_id.reference,
                'bank_id': obj.pos_statement_id.acquirer.id,
                'card_type_id': obj.pos_statement_id.card_type.id,
            }

        return res

    _columns = {
        'check_number': fields.function(_get_order_info, type='char', string='Check Number', multi='_get_order_info'),
        'card_number': fields.function(_get_order_info, type='char', string='Card Number', multi='_get_order_info'),
        'lot_number': fields.function(_get_order_info, type='char', string='Lot Number', multi='_get_order_info'),
        'reference': fields.function(_get_order_info, type='char', string='Reference', multi='_get_order_info'),

        'card_type_id': fields.function(
            _get_order_info, type='many2one', string='Card Type', multi='_get_order_info', relation='pos.credit_card'
        ),

        'bank_id': fields.function(
            _get_order_info, type='many2one', string='Bank', multi='_get_order_info', relation='res.bank'
        ),

        'approval_number': fields.function(
            _get_order_info, type='char', string='Approval Number', multi='_get_order_info'
        ),
    }
