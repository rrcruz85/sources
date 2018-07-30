
from openerp.osv import osv
from openerp.osv import fields

class wizard_to_print_movements(osv.osv_memory):
    _name = 'pedido_cliente.wizard_to_print_report'
    _description = 'pedido_cliente.wizard_to_print_report'

    _columns = {
        'make_by'           : fields.char('Elaborated by'),
        'served_by'          : fields.char('Sent away by'),
        'gross_weight'      : fields.char('Gross Weight'),
        'pedido_id'            : fields.many2one('pedido.cliente', 'Pedido'),
        'report': fields.selection([('type_one', 'Report by Varieties'),
                                    ('type_two', 'Report by Farm')], string='Report'),
    }

    _defaults = {
        'report': 'type_one',
    }

    def action_print(self, cr, uid, ids, context=None):
        if not context:
            context = {}

        wizard = self.browse(cr, uid, ids[0], context)
        #p_ids = self.pool.get('confirm.invoice').search(cr, uid, [('pedido_id', '=', wizard.pedido_id.id)])
        #if not p_ids:
        #    raise osv.except_osv('Error',"Para el pedido seleccionado no se ha confirmado ninguna linea de factura a los proveedores.")
        #elif not self.pool.get('confirm.invoice.line').search(cr, uid, [('invoice_id', 'in', p_ids)], count=True):
        #    raise osv.except_osv('Error',"Para el pedido seleccionado no se ha confirmado ninguna linea de factura a los proveedores.")

        datas = {
            'make_by': wizard.make_by,
            'served_by': wizard.served_by,
            'gross_weight': wizard.gross_weight,
            'request_id': wizard.pedido_id.id,
        }

        if wizard.report == 'type_two':
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'account_invoice_report',
                'datas': datas,
            }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account_invoice_variety_report',
            'datas': datas,
        }
wizard_to_print_movements()
