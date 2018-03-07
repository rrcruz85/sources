# -*- coding: utf-8 -*-

import  time
from openerp.osv import osv, fields

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
        'date_start': lambda *a: time.strftime('%Y-%m-01'),
        'date_end': fields.date.context_today,
    }

    def print_report(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        obj = self.browse(cr, uid, ids[0])
        query = """
            SELECT
                *
            FROM
                (
                    SELECT      
                        s.partner_id AS partner_id,
                        l.product_id AS product_id,
                        SUM (l.qty * u.factor) AS product_qty,
                        MIN (l.price_unit) AS product_unit_price,
                        SUM (l.qty * l.price_unit) AS price_total,
                        to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::text as date_order,                  
                        ROW_NUMBER() OVER (PARTITION BY s.partner_id ORDER BY SUM (l.qty * u.factor) DESC ) row_num
                    FROM
                        pos_order_line AS l
                        LEFT JOIN pos_order s ON (s. ID = l.order_id)                            
                        LEFT JOIN product_product P ON (P . ID = l.product_id)
                        LEFT JOIN product_template pt ON (pt. ID = P .product_tmpl_id)
                        LEFT JOIN product_uom u ON (u. ID = pt.uom_id) 
                    %s 
                    GROUP BY
                        s.partner_id,
                        l.product_id,
                        to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::text
                    ORDER BY
                        s.partner_id,
                        l.product_id,
                        to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::text,
                        SUM (l.qty * u.factor) DESC
                ) A
            WHERE
                row_num <= %s
        """

        partner_ids = []
        with_customers = False
        if obj.partner_ids:
            with_customers = True
            for p in obj.partner_ids:
                if p.id not in partner_ids:
                    partner_ids.append(p.id)

        whereCondition = ' '
        if with_customers:
            filter_values = (obj.date_start, obj.date_end, tuple(partner_ids))
            whereCondition = " where s.date_order BETWEEN '%s' and '%s' and s.partner_id in %s " % filter_values
        else:
            filter_values = (obj.date_start, obj.date_end)
            whereCondition = " where s.date_order BETWEEN '%s' and '%s'" % filter_values

        str_query = query % (whereCondition, obj.nbr_product)
        cr.execute(str_query)

        lines = cr.fetchall()
        line_ids = self.pool.get('pos.most.sold.product.line').search(cr, uid, [])
        self.pool.get('pos.most.sold.product.line').unlink(cr, uid, line_ids)

        rpt_lines = []
        for line in lines:
            if line[0]:
                vals = {
                    'partner_id': line[0],
                    'product_id': line[1],
                    'product_qty': line[2],
                    'product_unit_price': line[3],
                    'price_total': line[4],
                    'date_order': line[5]
                }
                rpt_lines.append(self.pool.get('pos.most.sold.product.line').create(cr,uid,vals))
        if rpt_lines:
            mod_obj = self.pool.get('ir.model.data')
            res = mod_obj.get_object_reference(cr, uid, 'my_point_of_sale', 'view_report_pos_most_sold_product_graph')
            res_id = res and res[1] or False
            return {
                'name': 'Products Sale Analysis',
                'view_type': 'form',
                'view_mode': 'graph',
                'view_id': [res_id],
                'res_model': 'pos.most.sold.product.line',
                'type': 'ir.actions.act_window',
                'target': 'current',
            }

class pos_most_sold_product_line(osv.osv):
    _name = "pos.most.sold.product.line"
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'product_qty': fields.integer('Product Qty', readonly=True),
        'product_unit_price': fields.float('Product Unit Price', readonly=True),
        'price_total': fields.float('Price Total', readonly=True),
        'date_order': fields.date('Date', readonly=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
