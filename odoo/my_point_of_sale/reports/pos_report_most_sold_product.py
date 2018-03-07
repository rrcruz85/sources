# -*- coding: utf-8 -*-

import  time
from openerp.osv import osv, fields
from openerp import tools

class pos_report_most_sold_product(osv.osv):
    _name = "pos.report.most.sold.product"
    _description = "Most Sold Products"
    _auto = False
    _columns = {
        'date_create': fields.char('Date', size=16, readonly=True),
        'journal_id': fields.many2one('account.journal', 'Sales Journal', readonly=True),
        'jl_id': fields.many2one('account.journal', 'Cash Journals', readonly=True),
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'no_trans': fields.float('Number of Transaction', readonly=True),
        'amount': fields.float('Amount', readonly=True),
        'invoice_id': fields.float('Nbr Invoice', readonly=True),
        'invoice_am': fields.float('Invoice Amount', readonly=True),
        'product_nb': fields.float('Product Nb.', readonly=True),
        'disc': fields.float('Disc.', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'pos_report_most_sold_product')
        cr.execute("""
            create or replace view pos_report_most_sold_product as (
               
                
               
               
                )
        """)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
