# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _

class PosConfig(osv.osv):
    _inherit = 'pos.config'
    _columns = {

        'pos_ticket_report': fields.boolean(
            'Print Pos Ticket Report', help='If not checked, the pos ticket will be printed as defaults'
        ),

        'iva_compensation': fields.float(
            'IVA Compensation (%)', digits=(16, 2),
            help="It's the value of the IVA compensation that will be apply to the products"
        ),

        'card_comition': fields.float(
            'Card Comition (%)', digits=(16, 2),
            help="It's the value of the charged comition for the use of card payment"
        ),

        'journal_ids' : fields.many2many('account.journal', 'pos_config_journal_rel',
                     'pos_config_id', 'journal_id', 'Available Payment Methods',
                     domain="[('journal_user', '=', True ), ('type', 'in', ['bank', 'cash','card', 'check'])]",),
    }

    def _check_iva_comp_value(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return (obj.iva_compensation >= 0.0 and obj.iva_compensation <= 100)

    def _check_card_comition(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        return (obj.card_comition >= 0.0 and obj.card_comition <= 100)

    _constraints = [
        (_check_iva_comp_value, _('Error: Invalid value for the iva_compensation number. This value must be between 0 and 100.'), ['iva_compensation']),
        (_check_card_comition, _('Error: Invalid value for the card comition. This value must be between 0 and 100.'),['card_comition']),
    ]

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
