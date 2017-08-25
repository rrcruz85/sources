# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp import tools


class TestOrderReportPrintWizard(osv.osv_memory):
    _name = 'oemedical_test_order.test_order_report_print_wizard'
    _description = 'oemedical_test_order.test_order_report_print_wizard'

    _columns = {
        'preoperatorio': fields.boolean('Examenes preoperatorios.'),
        'primer_mes': fields.boolean('Examenes primer mes.'),
        'tercer_mes': fields.boolean('Examenes tercer mes.'),
        'sexto_o_neoveno_mes': fields.boolean('Examenes sexto o noveno mes.'),
        'primer_anno': fields.boolean(tools.ustr('Examenes primer año.')),

        # In order to send the report to the patient...
        'send_report': fields.boolean('¿Enviar reporte al paciente?'),
    }

    def action_print_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context)
        test_order = self.pool.get('oemedical.test_order').browse(cr, uid, context['active_id'], context)

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'test_order_report',
            'datas': {
                'preoperatorio': wizard.preoperatorio,
                'primer_mes': wizard.primer_mes,
                'tercer_mes': wizard.tercer_mes,
                'sexto_o_neoveno_mes': wizard.sexto_o_neoveno_mes,
                'primer_anno': wizard.primer_anno,
                'test_order_id': test_order.id,
                'send_report': wizard.send_report
            },
        }
