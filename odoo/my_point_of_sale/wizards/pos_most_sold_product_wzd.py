# -*- coding: utf-8 -*-

import  time
from openerp.osv import osv, fields
from openerp.report import report_sxw

class pos_most_sold_product_wzd(osv.osv_memory):
    _name = 'pos.most.sold.product.wzd'
    _description = 'Most Sold Products'

    _columns = {
        'nbr_product': fields.integer('Nr. Products', help="Number of most sold products"),
        'date_start': fields.date('Date Start', required=True),
        'date_end': fields.date('Date End', required=True),
        'partner_ids': fields.many2many('res.partner', 'pos_most_sold_product_partner_rel', 'partner_id', 'wizard_id', 'Customers'),
    }

    _defaults = {
        'nbr_product': 1,
        'date_start': fields.date.context_today,
        'date_end': fields.date.context_today,
    }

    def print_report(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        obj = self.browse(cr, uid, ids[0])
        query = 'select * from ('\
                'select '\
                's.partner_id as partner_id,'\
                'l.product_id as product_id,'\
                'sum(l.qty * u.factor) as product_qty,'\
                'min(l.price_unit) as product_unit_price,'\
                'sum(l.qty * l.price_unit) as price_total,'\
                'ROW_NUMBER() OVER (PARTITION BY s.partner_id ORDER BY sum(l.qty * u.factor) DESC) row_num '\
                'from pos_order_line as l '\
                'left join pos_order s on (s.id=l.order_id) '\
                'left join product_product p on (p.id=l.product_id) '\
                'left join product_template pt on (pt.id=p.product_tmpl_id) '\
                'left join product_uom u on (u.id=pt.uom_id) '\
                'where '\
                's.date_order BETWEEN %s and %s '
        partner_ids = []
        with_customers = False;
        if obj.partner_ids:
            with_customers = True
            for p in obj.partner_ids:
                if p.id not in partner_ids:
                    partner_ids.append(p.id)
            query += ' and s.partner_id in %s '
        query += 'group by '\
                 's.partner_id, l.product_id '\
                 'ORDER BY '\
                 's.partner_id,l.product_id, sum(l.qty * u.factor) desc) A '\
                 'where row_num <= %s '

        if with_customers:
            filter_values = (obj.date_start, obj.date_end, tuple(partner_ids),obj.nbr_product)
        else:
            filter_values = (obj.date_start, obj.date_end, obj.nbr_product)
        cr.execute(query, filter_values)
        lines = cr.fetchall()
        context['show_email'] = True

        rpt_lines = []
        for line in lines:
            if line[0]:
                rpt_lines.append((0,0,{
                    'partner_id': line[0],
                    'product_id': line[1],
                    'product_qty': line[2],
                    'product_unit_price': line[3],
                    'price_total': line[4]
                }))
        if rpt_lines:
            vals ={
                'nbr_product': obj.nbr_product,
                'date_start': obj.date_start,
                'date_end': obj.date_end,
                'line_ids': rpt_lines
            }
            id = self.pool.get('pos.most.sold.product.rpt').create(cr,uid,vals)
            #cr.execute("delete from pos_most_sold_product_rpt")

            datas = {
                'ids': [id],
                'model': 'pos.most.sold.product.rpt',
            }

            #res = self.read(cr, uid, ids, ['date_start', 'date_end', 'user_ids'], context=context)
            #res = res and res[0] or {}
            #datas['form'] = res
            #if res.get('id',False):
            #    datas['ids']=[res['id']]
            rpt = self.pool['report'].get_action(cr, uid, [], 'my_point_of_sale.report_pos_most_sold_product', data=datas, context=context)
            return rpt


class pos_most_sold_product_rpt(osv.osv):
    _name = 'pos.most.sold.product.rpt'
    _description = 'Most Sold Products'

    _columns = {
        'nbr_product': fields.integer('Nr. Products', help="Number of most sold products"),
        'date_start': fields.date('Date Start', required=True),
        'date_end': fields.date('Date End', required=True),
        'line_ids': fields.one2many('pos.most.sold.product.line', 'rpt_id', string='Lines'),
    }


class pos_most_sold_product_line(osv.osv):
    _name = "pos.most.sold.product.line"
    _columns = {
        'rpt_id': fields.many2one('pos.most.sold.product.rpt', string = 'Report', ondelete="cascade"),
        'partner_id': fields.many2one('res.partner', 'Customer', readonly=True),
        'product_id': fields.many2one('product.product', 'Cash Journals', readonly=True),
        'product_qty': fields.float('Product Qty', readonly=True),
        'product_unit_price': fields.float('Product Unit Price', readonly=True),
        'price_total': fields.float('Price Total', readonly=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
