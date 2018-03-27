# -*- coding: utf-8 -*-

import  time
from openerp.osv import osv, fields

class pos_most_sold_product_wzd(osv.osv_memory):
    _name = 'pos.most.sold.product.wzd'
    _description = 'Most sold products report'

    _columns = {
        'nbr_product': fields.integer('Nr. Products', help="Nr of most sold products per customer"),
        'nbr_records': fields.integer('Nr. Records', help="Nr of records to retrieve"),
        'date_start': fields.date('Date Start', required=True),
        'date_end': fields.date('Date End', required=True),
        'partner_ids': fields.many2many('res.partner', 'pos_most_sold_product_partner_rel', 'partner_id', 'wizard_id', 'Customers'),
    }

    _defaults = {
        'nbr_product': 1,
        'nbr_records': 10,
        'date_start': lambda *a: time.strftime('%Y-%m-01'),
        'date_end': fields.date.context_today,
    }

    def execute_query(self, cr, uid, ids, create_parent = False, context = None):

        obj = self.browse(cr, uid, ids[0])
        query = """
            SELECT * from (
            SELECT *, ROW_NUMBER() OVER () as fila
            FROM
                (
                    SELECT      
                        s.partner_id AS partner_id,
                        l.product_id AS product_id,
                        SUM (l.qty * u.factor) AS product_qty,
                        MIN (l.price_unit) AS product_unit_price,
                        SUM (l.qty * l.price_unit) AS price_total,
                        to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::text as date_order,                  
                        ROW_NUMBER() OVER (PARTITION BY s.partner_id ORDER BY SUM (l.qty * u.factor) DESC ) row_num,
                        cl.name as client_name
                    FROM
                        pos_order_line AS l
                        LEFT JOIN pos_order s ON (s. ID = l.order_id) 
                        LEFT JOIN res_partner cl ON (s.partner_id = cl.ID)                           
                        LEFT JOIN product_product P ON (P . ID = l.product_id)
                        LEFT JOIN product_template pt ON (pt. ID = P .product_tmpl_id)
                        LEFT JOIN product_uom u ON (u. ID = pt.uom_id) 
                    %s 
                    GROUP BY
                        s.partner_id,
                        cl.name,
                        l.product_id,
                        to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::text
                    ORDER BY
                        cl.name, 
                        l.product_id,
                        to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::text DESC,
                        SUM (l.qty * u.factor) DESC
                ) A
                WHERE A.row_num <= %s
            ) B WHERE B.fila <= %s
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
            whereCondition = " where cast(s.date_order as date) BETWEEN '%s' and '%s' and s.partner_id in %s " % filter_values
        else:
            filter_values = (obj.date_start, obj.date_end)
            whereCondition = " where cast(s.date_order as date) BETWEEN '%s' and '%s'" % filter_values

        str_query = query % (whereCondition, obj.nbr_product, obj.nbr_records)
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
                if not create_parent:
                    rpt_lines.append(self.pool.get('pos.most.sold.product.line').create(cr, uid, vals))
                else:
                    rpt_lines.append((0, 0, vals))
        if create_parent:
            line_ids = self.pool.get('pos.most.sold.product').search(cr, uid, [])
            self.pool.get('pos.most.sold.product').unlink(cr, uid, line_ids)

            dict_parent = {
                'nbr_product': obj.nbr_product,
                'date_start' : obj.date_start,
                'date_end': obj.date_end,
                'user_id': uid,
                'line_ids': rpt_lines
            }
            return [self.pool.get('pos.most.sold.product').create(cr, uid, dict_parent)]
        else:
            return rpt_lines

    def print_report_pdf(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        rpt_lines = self.execute_query(cr, uid, ids, True, context)
        datas = {
            'ids': rpt_lines
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'pos_most_sold_product_report',
            'datas': datas,
        }

class pos_most_sold_product(osv.osv):
    _name = 'pos.most.sold.product'
    _description = 'Most sold products'

    _columns = {
        'nbr_product': fields.integer('Nr. Products'),
        'date_start': fields.date('Date Start'),
        'date_end': fields.date('Date End'),
        'user_id': fields.many2one('res.users','User'),
        'line_ids': fields.one2many('pos.most.sold.product.line', 'parent_id','Sale Lines'),
    }

class pos_most_sold_product_line(osv.osv):
    _name = "pos.most.sold.product.line"
    _columns = {
        'parent_id': fields.many2one('pos.most.sold.product', 'Parent'),
        'partner_id': fields.many2one('res.partner', 'Customer', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'product_qty': fields.integer('Quantity', readonly=True),
        'product_unit_price': fields.float('Unit Price', readonly=True),
        'price_total': fields.float('Total', readonly=True),
        'date_order': fields.date('Date', readonly=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
