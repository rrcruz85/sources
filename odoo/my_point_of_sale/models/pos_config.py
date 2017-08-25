# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class PosConfig(osv.osv):
    _inherit = 'pos.config'
    _columns = {
        'show_all_products': fields.boolean(
            'Show all products?', help='If not checked, the product list in the point of sale will be limited...'
        ),

        'iva_compensation': fields.float(
            'IVA Compensation (%)', digits=(16, 2),
            help="It's the value of the IVA compensation that will be apply to the products..."
        ),

        'products_ids': fields.many2many(
            'product.template', 'my_pos_product_pos_config_rel', 'tpv_id', 'product_id', string='Available products...'
        ),

        'journal_ids' : fields.many2many('account.journal', 'pos_config_journal_rel',
                     'pos_config_id', 'journal_id', 'Available Payment Methods',
                     domain="[('journal_user', '=', True ), ('type', 'in', ['bank', 'cash','card', 'check'])]",),
    }

    _defaults = {
        'show_all_products': lambda *a: True,
    }


class pos_session(osv.osv):
    _inherit = 'pos.session'

    def wkf_action_close(self, cr, uid, ids, context=None):
        # Close CashBox
        for record in self.browse(cr, uid, ids, context=context):
            for st in record.statement_ids:
                if abs(st.difference) > st.journal_id.amount_authorized_diff:
                    # The pos manager can close statements with maximums.
                    if not self.pool.get('ir.model.access').check_groups(cr, uid, "point_of_sale.group_pos_manager"):
                        raise osv.except_osv(_('Error!'), _("Your ending balance is too different from the theoretical cash closing (%.2f), the maximum allowed is: %.2f. You can contact your manager to force it.") % (
                                             st.difference, st.journal_id.amount_authorized_diff))
                if (st.journal_id.type not in ['bank', 'cash', 'card', 'check']):
                    raise osv.except_osv(_('Error!'),_("The type of the journal for your payment method should be bank, cash or card "))

                str = st.journal_id.type
                if (str == 'card' or str == 'check'):
                    str = 'bank'
                getattr(st, 'button_confirm_%s' % str)(context=context)
        self._confirm_orders(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'state': 'closed'}, context=context)
