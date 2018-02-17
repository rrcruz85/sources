# -*- coding: utf-8 -*-

from openerp.osv import osv

class PosInvoiceReport(osv.AbstractModel):
    _name = 'report.point_of_sale.report_invoice'

    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        posorder_obj = self.pool['pos.order']
        report = report_obj._get_report_from_name(cr, uid, 'account.report_invoice')

        selected_orders = posorder_obj.browse(cr, uid, ids, context=context)

        ids_to_print = []
        invoiced_posorders_ids = []
        iva_compensation = 0.0

        for order in selected_orders:
            if order.invoice_id:
                ids_to_print.append(order.invoice_id.id)
                invoiced_posorders_ids.append(order.id)
                iva_compensation += order.amount_iva_compensation

        if not ids_to_print:
            return report_obj.render(cr, uid, ids, 'my_point_of_sale.report_invoice_message', {}, context=context)
        else:
            docargs = {
                'doc_ids': ids_to_print,
                'doc_model': report.model,
                'docs': selected_orders,
                'iva_compensation': iva_compensation
            }
            return report_obj.render(cr, uid, ids, 'account.report_invoice', docargs, context=context)

