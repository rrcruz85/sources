# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class AccountJournal(osv.osv):
    _inherit = "account.journal"
    _columns = {
        'type': fields.selection(
            [('sale', 'Sale'), ('sale_refund', 'Sale Refund'), ('purchase', 'Purchase'),
             ('purchase_refund', 'Purchase Refund'), ('cash', 'Cash'), ('card', 'Credit/Debit Card'),
             ('check', 'Check'), ('bank', 'Bank'), ('general', 'General'), ('situation', 'Opening/Closing Situation')],
            string='Type', size=32, required=True,
            help="Select 'Sale' for customer invoices journals. Select 'Purchase' for supplier invoices journals."\
                 "Select 'Cash' or 'Credit/Debit Card' or 'Check' or 'Bank' for journals that are used in customer or"\
                 "supplier payments. Select 'General' for miscellaneous operations journals."\
                 "Select 'Opening/Closing Situation' for entries generated for new fiscal years."),
    }
