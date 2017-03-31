
import time
from openerp.report import report_sxw

class account_invoice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_invoice, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw('report.my_pos.account.invoice', 'account.invoice', 'addons/my_pos/reports/account_invoice_report.rml', parser=account_invoice)
