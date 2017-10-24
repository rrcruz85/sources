# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.tools.translate import _


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

        '''
        not_invoiced_orders_ids = list(set(ids) - set(invoiced_posorders_ids))
        if not_invoiced_orders_ids:
            not_invoiced_posorders = posorder_obj.browse(cr, uid, not_invoiced_orders_ids, context=context)
            not_invoiced_orders_names = list(map(lambda a: a.name, not_invoiced_posorders))
            raise osv.except_osv(_('Error!'), _('No link to an invoice for %s.' % ', '.join(not_invoiced_orders_names)))
        '''
        docargs = {
            'doc_ids': ids_to_print,
            'doc_model': report.model,
            'docs': selected_orders,
            'iva_compensation': iva_compensation
        }
        return report_obj.render(cr, uid, ids, 'account.report_invoice', docargs, context=context)
