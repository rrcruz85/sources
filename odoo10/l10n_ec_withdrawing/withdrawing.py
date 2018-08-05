# -*- coding: utf-8 -*-
# © <2016> <Cristian Salamea>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time
import logging

from openerp import (
    models,
    fields,
    api,
    _
)
from openerp.exceptions import (
    except_orm,
    Warning as UserError,
    RedirectWarning
    )
import openerp.addons.decimal_precision as dp

UNIDADES = ('','UN ','DOS ','TRES ','CUATRO ','CINCO ','SEIS ','SIETE ','OCHO ','NUEVE ','DIEZ ','ONCE ','DOCE ','TRECE ','CATORCE ','QUINCE ',   'DIECISEIS ', 'DIECISIETE ',
        'DIECIOCHO ', 'DIECINUEVE ', 'VEINTE ')
DECENAS = ( 'VENTI', 'TREINTA ', 'CUARENTA ', 'CINCUENTA ', 'SESENTA ', 'SETENTA ', 'OCHENTA ', 'NOVENTA ', 'CIEN ')
CENTENAS = ('CIENTO ', 'DOSCIENTOS ', 'TRESCIENTOS ', 'CUATROCIENTOS ', 'QUINIENTOS ', 'SEISCIENTOS ', 'SETECIENTOS ', 'OCHOCIENTOS ', 'NOVECIENTOS ')

# mapping invoice type to journal type
TYPE2JOURNAL = {
    'out_invoice': 'sale',
    'in_invoice': 'purchase',
    'out_refund': 'sale_refund',
    'in_refund': 'purchase_refund',
    'liq_purchase': 'purchase',
}

class PartnerAts(models.Model):

    _inherit = 'res.partner'

    parte_relacion = fields.Boolean('Parte Relacionada')
    
    _defaults = {
        'parte_relacion': False,
    }

class AccountWithdrawing(models.Model):
    """ Implementacion de documento de retencion """

    @api.multi
    def name_get(self):
        """
        TODO
        """
        result = []
        for withdrawing in self:
            result.append((withdrawing.id, withdrawing.name))
        return result

    @api.one
    @api.depends('tax_ids.amount')
    def _amount_total(self):
        """
        TODO
        """
        self.amount_total = sum(tax.amount for tax in self.tax_ids)

    @api.multi
    def _get_period(self):
        result = {}
        for obj in self:
            result[obj.id] = self.env['account.period'].find(obj.date)[0]
        return result

    @api.multi
    def _get_type(self):
        context = self._context
        if 'type' in context and context['type'] in ['in_invoice', 'out_invoice']:  # noqa
            return 'in_invoice'
        else:
            return 'liq_purchase'

    @api.multi
    def _get_in_type(self):
        context = self._context
        if 'type' in context and context['type'] in ['in_invoice', 'liq_purchase']:  # noqa
            return 'ret_in_invoice'
        else:
            return 'ret_out_invoice'

    STATES_VALUE = {'draft': [('readonly', False)]}

    _name = 'account.retention'
    _description = 'Withdrawing Documents'
    _order = 'date ASC'

    name = fields.Char(
        'Número',
        size=64,
        readonly=True,
        required=True,
        states=STATES_VALUE
        )
    internal_number = fields.Char(
        'Número Interno',
        size=64,
        readonly=True,
        required=True,
        default='/'
        )
    manual = fields.Boolean(
        'Numeración Manual',
        readonly=True,
        states=STATES_VALUE,
        default=True
        )
    num_document = fields.Char(
        'Num. Comprobante',
        size=50,
        readonly=True,
        states=STATES_VALUE
        )
    auth_id = fields.Many2one(
        'account.authorisation',
        'Autorizacion',
        required=True,
        readonly=True,
        states=STATES_VALUE,
        domain=[('in_type', '=', 'interno')]
        )
    type = fields.Selection(
        related='invoice_id.type',
        string='Tipo Comprobante',
        readonly=True,
        store=True
        )
    in_type = fields.Selection(
        [
            ('ret_in_invoice', u'Retención a Proveedor'),
            ('ret_out_invoice', u'Retención de Cliente')
        ],
        string='Tipo',
        states=STATES_VALUE,
        readonly=True,
        default=_get_in_type
        )
    date = fields.Date(
        'Fecha Emision',
        readonly=True,
        states={'draft': [('readonly', False)]}, required=True)
    period_id = fields.Many2one(
        'account.period',
        'Periodo',
        required=True,
        default=_get_period
        )
    tax_ids = fields.One2many(
        'account.invoice.tax',
        'retention_id',
        'Detalle de Impuestos',
        readonly=True,
        states=STATES_VALUE
        )
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Documento',
        required=False,
        readonly=True,
        states=STATES_VALUE,
        domain=[('state', '=', 'open')]
        )
    partner_id = fields.Many2one(
        'res.partner',
        string='Empresa',
        required=True,
        readonly=True,
        states=STATES_VALUE
        )
    move_id = fields.Many2one(
        related='invoice_id.move_id',
        string='Asiento Contable',
        readonly=True,
        store=True
        )
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('early', 'Anticipado'),
            ('done', 'Validado'),
            ('cancel', 'Anulado')
        ],
        readonly=True,
        string='Estado',
        default='draft'
        )
    amount_total = fields.Float(
        compute='_amount_total',
        string='Total',
        store=True,
        digits_compute=dp.get_precision('Account')
        )
    to_cancel = fields.Boolean(
        string='Para anulación',
        readonly=True,
        states=STATES_VALUE
        )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        change_default=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env['res.company']._company_default_get('account.invoice')  # noqa
        )

    _sql_constraints = [
        (
            'unique_number_partner',
            'unique(name,partner_id,type)',
            u'El número de retención es único.'
        )
    ]

    @api.multi
    def unlink(self):
        for obj in self:
            if obj.state in ['done']:
                raise UserError('No se permite borrar retenciones validadas.')
        res = super(AccountWithdrawing, self).unlink()
        return res

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.name = self.name.zfill(9)

    @api.onchange('to_cancel')
    def onchange_tocancel(self):
        if self.to_cancel:
            self.partner_id = self.company_id.partner_id.id

    @api.onchange('date')
    def onchange_date(self):
        self.period_id = self.env['account.period'].find(self.date)

#    @api.onchange('invoice_id')
#    def onchange_invoice(self):

    @api.multi
    def onchange_invoice(self, invoice_id):
        if not self.invoice_id:
            return
        self.num_document = self.invoice_id.invoice_number
        self.type = self.invoice_id.type

    @api.multi
    def button_validate(self):
        """
        Botón de validación de Retención que se usa cuando
        se creó una retención manual, esta se relacionará
        con la factura seleccionada.
        """
        for ret in self:
            if ret.manual:
                self.action_validate(ret.name)
                invoice = self.env['account.invoice'].browse(ret.invoice_id.id)
                invoice.write({'retention_id': ret.id})
            else:
                self.action_validate()
        return True

    @api.multi
    def action_validate(self, number=None):
        """
        number: Número posible para usar en el documento

        Método que valida el documento, su principal
        accion es numerar el documento segun el parametro number
        """
        for wd in self:
            if wd.to_cancel:
                raise UserError('El documento fue marcado para anular.')
            sequence = wd.invoice_id.journal_id.auth_ret_id.sequence_id
            if wd.internal_number and not number:
                wd_number = wd.internal_number[6:]
            elif number is None:
                wd_number = self.env['ir.sequence'].get_id(sequence.id)
            else:
                wd_number = str(number).zfill(sequence.padding)
            number = '{0}{1}{2}'.format(wd.auth_id.serie_entidad,
                                        wd.auth_id.serie_emision,
                                        wd_number)
            wd.write({'state': 'done',
                      'name': number,
                      'internal_number': number})
        return True

    @api.multi
    def action_cancel(self):
        """
        Método para cambiar de estado a cancelado el documento
        """
        auth_obj = self.env['account.authorisation']
        for ret in self:
            data = {'state': 'cancel'}
            if ret.to_cancel:
                if len(ret.name) == 9 and auth_obj.is_valid_number(ret.auth_id.id, int(ret.name)):  # noqa
                    number = ret.auth_id.serie_entidad + ret.auth_id.serie_emision + ret.name  # noqa
                    data.update({'name': number})
                else:
                    raise except_orm(
                        'Error',
                        u'El número no es de 9 dígitos y/o no pertenece a la autorización seleccionada.'  # noqa
                    )
            self.write({'state': 'cancel'})
        return True

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.multi
    def action_early(self):
        # Método para cambiar de estado a cancelado el documento
        self.write({'state': 'early'})
        return True

    @api.multi
    def action_print(self):
        report_name = 'l10n_ec_withdrawing.account_withdrawing'
        datas = {'ids': [self.id], 'model': 'account.retention'}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': report_name,
            'model': 'account.retention',
            'datas': datas,
            'nodestroy': True,
            }


class AccountInvoiceTax(models.Model):

    _inherit = 'account.invoice.tax'

    fiscal_year = fields.Char('Ejercicio Fiscal', size=4)
    tax_group = fields.Selection(
        [
            ('vat', 'IVA Diferente de 0%'),
            ('vat0', 'IVA 0%'),
            ('novat', 'No objeto de IVA'),
            ('ret_vat_b', 'Retención de IVA (Bienes)'),
            ('ret_vat_srv', 'Retención de IVA (Servicios)'),
            ('ret_ir', 'Ret. Imp. Renta'),
            ('no_ret_ir', 'No sujetos a Ret. de Imp. Renta'),
            ('imp_ad', 'Imps. Aduanas'),
            ('ice', 'ICE'),
            ('other', 'Other')
        ],
        'Grupo',
        required=True,
        default='vat'
    )
    percent = fields.Char('Porcentaje', size=20)
    num_document = fields.Char('Num. Comprobante', size=50)
    retention_id = fields.Many2one(
        'account.retention',
        'Retención',
        select=True
    )

    @api.v8
    def compute(self, invoice):
        tax_grouped = {}
        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))  # noqa
        company_currency = invoice.company_id.currency_id
        for line in invoice.invoice_line:
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, invoice.partner_id)['taxes']
            for tax in taxes:
                val = {
                    'invoice_id': invoice.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'base': currency.round(tax['price_unit'] * line['quantity']),  # noqa
                    'tax_group': tax['tax_group'],
                    'percent': tax['porcentaje'],
                }
                # Hack to EC
                if tax['tax_group'] in ['ret_vat_b', 'ret_vat_srv']:
                    ret = float(str(tax['porcentaje'])) / 100
                    #ret = float(str(tax['porcentaje']))
                    #bi = tax['price_unit'] * line['quantity'] * .14
                    bi = tax['price_unit'] * line['quantity']
                    imp = (abs(tax['amount']) / (ret * bi)) * 100
                    val['base'] = (tax['price_unit'] * line['quantity']) * imp / 100  # noqa
                    #val['base'] = bi
                else:
                    val['base'] = tax['price_unit'] * line['quantity']

                if invoice.type in ['out_invoice', 'in_invoice']:
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)  # noqa
                    val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)  # noqa
                    val['account_id'] = tax['account_collected_id'] or line.account_id.id  # noqa
                    val['account_analytic_id'] = tax['account_analytic_collected_id']  # noqa
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = currency.compute(val['base'] * tax['ref_base_sign'], company_currency, round=False)  # noqa
                    val['tax_amount'] = currency.compute(val['amount'] * tax['ref_tax_sign'], company_currency, round=False)  # noqa
                    val['account_id'] = tax['account_paid_id'] or line.account_id.id  # noqa
                    val['account_analytic_id'] = tax['account_analytic_paid_id']  # noqa

                # If the taxes generate moves on the same financial account as the invoice line  # noqa
                # and no default analytic account is defined at the tax level, propagate the  # noqa
                # analytic account from the invoice line to the tax line. This is necessary  # noqa
                # in situations were (part of) the taxes cannot be reclaimed,
                # to ensure the tax move is allocated to the proper analytic account.  # noqa
                if not val.get('account_analytic_id') and line.account_analytic_id and val['account_id'] == line.account_id.id:  # noqa
                    val['account_analytic_id'] = line.account_analytic_id.id

                key = (val['tax_code_id'], val['base_code_id'], val['account_id'])  # noqa
                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
            t['base_amount'] = currency.round(t['base_amount'])
            t['tax_amount'] = currency.round(t['tax_amount'])
        return tax_grouped

    _defaults = {
        'fiscal_year': time.strftime('%Y'),
    }


class Invoice(models.Model):

    _inherit = 'account.invoice'
    __logger = logging.getLogger(_inherit)

    @api.multi
    def onchange_company_id(self, company_id, part_id, type, invoice_line, currency_id):  # noqa
        """
        TODO: add the missing context parameter
        when forward-porting in trunk so we can remove
        this hack!
        """
        self = self.with_context(self.env['res.users'].context_get())

        values = {}
        domain = {}

        if company_id and part_id and type:
            p = self.env['res.partner'].browse(part_id)
            if p.property_account_payable and p.property_account_receivable and p.property_account_payable.company_id.id != company_id and p.property_account_receivable.company_id.id != company_id:  # noqa
                prop = self.env['ir.property']
                rec_dom = [('name', '=', 'property_account_receivable'), ('company_id', '=', company_id)]  # noqa
                pay_dom = [('name', '=', 'property_account_payable'), ('company_id', '=', company_id)]  # noqa
                res_dom = [('res_id', '=', 'res.partner,%s' % part_id)]
                rec_prop = prop.search(rec_dom + res_dom) or prop.search(rec_dom)  # noqa
                pay_prop = prop.search(pay_dom + res_dom) or prop.search(pay_dom)  # noqa
                rec_account = rec_prop.get_by_record(rec_prop)
                pay_account = pay_prop.get_by_record(pay_prop)
                if not rec_account and not pay_account:
                    action = self.env.ref('account.action_account_config')
                    msg = _('Cannot find a chart of account for this company, You should configure it. \nPlease go to Account Configuration.')  # noqa
                    raise RedirectWaring(msg, action.id, _('Go to the configuration panel'))  # noqa

                if type in ('out_invoice', 'out_refund'):
                    acc_id = rec_account.id
                else:
                    acc_id = pay_account.id
                values = {'account_id': acc_id}

            if self:
                if company_id:
                    for line in self.invoice_line:
                        if not line.account_id:
                            continue
                        if line.account_id.company_id.id == company_id:
                            continue
                        accounts = self.env['account.account'].search([('name', '=', line.account_id.name), ('company_id', '=', company_id)])  # noqa
                        if not accounts:
                            action = self.env.ref('account.action_account_config')  # noqa
                            msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')  # noqa
                            raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))  # noqa
                        line.write({'account_id': accounts[-1].id})
            else:
                for line_cmd in invoice_line or []:
                    if len(line_cmd) >= 3 and isinstance(line_cmd[2], dict):
                        line = self.env['account.account'].browse(line_cmd[2]['account_id'])  # noqa
                        if line.company_id.id != company_id:
                            raise except_orm(
                                _('Configuration Error!'),
                                _("Invoice line account's company and invoice's company does not match."))  # noqa

        if company_id and type:
            journal_type = TYPE2JOURNAL[type]
            journals = self.env['account.journal'].search([('type', '=', journal_type), ('company_id', '=', company_id)])  # noqa
            if journals:
                values['journal_id'] = journals[0].id
            journal_defaults = self.env['ir.values'].get_defaults_dict('account.invoice', 'type=%s' % type)  # noqa
            if 'journal_id' in journal_defaults:
                values['journal_id'] = jounral_defaults['journal_id']  # noqa
            if not values.get('journal_id'):
                field_desc = journals.fields_get(['type'])
                type_label = next(t for t, label in field_desc['type']['selection'] if t == journal_type)  # noqa
                action = self.env.ref('account.action_account_journal_form')
                msg = _('Cannot find any account journal of type "%s" for this company, You should create one.\n Please go to Journal Configuration') % type_label  # noqa
                raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))  # noqa
            domain = {'journal_id':  [('id', 'in', journals.ids)]}

        return {'value': values, 'domain': domain}

    @api.multi
    def onchange_sustento(self, sustento_id):
        res = {'value': {}}
        if not sustento_id:
            return res
        sustento = self.env['account.ats.sustento'].browse(sustento_id)
        res['value']['name'] = sustento.type
        return res

    @api.multi
    def print_invoice(self):
        # Método para imprimir reporte de liquidacion de compra
        datas = {'ids': [self.id], 'model': 'account.invoice'}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'invoice_report',
            'model': 'account.invoice',
            'datas': datas,
            'nodestroy': True,
            }

    @api.multi
    def print_move(self):
        # Método para imprimir comprobante contable
        return self.env['report'].get_action(
            self.move_id,
            'l10n_ec_withdrawing.account_move_report'
        )

    @api.multi
    def print_liq_purchase(self):
        # Método para imprimir reporte de liquidacion de compra
        datas = {'ids': [self.id], 'model': 'account.invoice'}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'report_liq_purchase',
            'model': 'account.invoice',
            'datas': datas,
            'nodestroy': True,
            }

    @api.multi
    def print_retention(self):
        """
        Método para imprimir reporte de retencion
        """
        datas = {
            'ids': [self.retention_id.id],
            'model': 'account.retention'
        }
        if not self.retention_id:
            raise UserError('Aviso', u'No tiene retención')
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.retention',
            'model': 'account.retention',
            'datas': datas,
            'nodestroy': True,
        }

    def toWord(self,number):

        """
        Converts a number into string representation
        """
        converted = ''

        if not (0 < number < 999999999):

            return 'No es posible convertir el numero a letras'

        num = '%.2f' % number
        if '.' in num:
            decimal = num.split('.')[1][:2]
        elif ',' in num:
            decimal = num.split(',')[1][:2]
        else:
            decimal = '00'
        number = int(number)
        number_str = str(number).zfill(9)
        millones = number_str[:3]
        miles = number_str[3:6]
        cientos = number_str[6:]

        if(millones):
            if(millones == '001'):
                converted += 'UN MILLON '
            elif(int(millones) > 0):
                converted += '%sMILLONES ' % self.__convertNumber(millones)

        if(miles):
            if(miles == '001'):
                converted += 'MIL '
            elif(int(miles) > 0):
                converted += '%sMIL ' % self.__convertNumber(miles)

        if(cientos):
            if(cientos == '001'):
                converted += 'UN '
            elif(int(cientos) > 0):
                converted += '%s ' % self.__convertNumber(cientos)

        converted += ''

        return converted.title() + 'Con ' + decimal + '/100'

    def __convertNumber(self,n):
        """
        Max length must be 3 digits
        """
        output = ''

        if(n == '100'):
            output = "CIEN "
        elif(n[0] != '0'):
            output = CENTENAS[int(n[0])-1]

        k = int(n[1:])
        if(k <= 20):
            output += UNIDADES[k]
        else:
            if((k > 30) & (n[2] != '0')):
                output += '%sY %s' % (DECENAS[int(n[1])-2], UNIDADES[int(n[2])])
            else:
                output += '%s%s' % (DECENAS[int(n[1])-2], UNIDADES[int(n[2])])

        return output

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        self.amount_untaxed = self.amount_vat = self.amount_tax = self.amount_vat_cero = 0.00
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)  # noqa
        for line in self.tax_line:
            if line.tax_group == 'imp_ad':
                #self.amount_duty += line.base
                self.amount_duty += line.amount
                self.amount_tax += line.amount
            if line.tax_group == 'vat':
                self.amount_vat += line.base
                self.amount_tax += line.amount
            elif line.tax_group == 'vat0':
                self.amount_vat_cero += line.base
                #self.__logger.info('vat0 %s ' % (self.amount_vat_cero))
            elif line.tax_group == 'novat':
                self.amount_novat += line.base
            elif line.tax_group == 'no_ret_ir':
                self.amount_noret_ir += line.base
            elif line.tax_group in ['ret_vat_b', 'ret_vat_srv', 'ret_ir']:
                self.amount_tax_retention += line.amount
                if line.tax_group == 'ret_vat_b':
                    self.amount_tax_ret_vatb += line.base
                    self.taxed_ret_vatb += line.amount
                elif line.tax_group == 'ret_vat_srv':
                    self.amount_tax_ret_vatsrv += line.base
                    self.taxed_ret_vatsrv += line.amount
                elif line.tax_group == 'ret_ir':
                    self.amount_tax_ret_ir += line.base
                    self.taxed_ret_ir += line.amount
            elif line.tax_group == 'ice':
                self.amount_ice += line.amount
        # base vat not defined, amount_vat_cero by default
        #self.__logger.info('amount_vat_cero: %s ' % (self.amount_vat_cero))
        if self.amount_vat == 0 and self.amount_vat_cero == 0:
            self.amount_vat_cero = self.amount_untaxed
        #self.__logger.info('amount_untaxed: %s ' % (self.amount_untaxed))
        #self.__logger.info('amount_vat_cero: %s ' % (self.amount_vat_cero))
        self.amount_total = self.amount_untaxed + self.amount_tax + self.amount_tax_retention  # noqa
        self.amount_total_letras = self.toWord(self.amount_total)
        self.amount_pay = self.amount_tax + self.amount_untaxed
    @api.multi
    def name_get(self):
        TYPES = {
            'out_invoice': _('Invoice'),
            'in_invoice': _('Supplier Invoice'),
            'out_refund': _('Refund'),
            'in_refund': _('Supplier Refund'),
            'liq_purchase': _('Liquid. de Compra')
        }
        result = []
        for inv in self:
            result.append((inv.id, "%s %s" % (inv.number or TYPES[inv.type], inv.name or '')))  # noqa
        return result

    @api.one
    @api.depends('tax_line.tax_group')
    def _check_retention(self):
        for inv in self:
            for tax in inv.tax_line:
                if tax.tax_group in ['ret_vat_b', 'ret_vat_srv']:
                    self.retention_vat = True
                elif tax.tax_group == 'ret_ir':
                    self.retention_ir = True
                elif tax.tax_group == 'no_ret_ir':
                    self.no_retention_ir = True

    HELP_RET_TEXT = '''Automatico: El sistema identificara los impuestos
    y creara la retencion automaticamente,
    Manual: El usuario ingresara el numero de retencion
    Agrupar: Podra usar la opcion para agrupar facturas
    del sistema en una sola retencion.'''

    PRECISION_DP = dp.get_precision('Account')

    amount_salva = fields.Float(
        string='Salvaguarda', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_duty = fields.Float(
        string='Arancel', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_ice = fields.Float(
        string='ICE', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_vat = fields.Float(
        string='Base 12 %', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_untaxed = fields.Float(
        string='Untaxed', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_tax = fields.Float(
        string='Tax', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Float(
        string='Total a Pagar', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_pay = fields.Float(
        string='Total', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_noret_ir = fields.Float(
        string='Monto no sujeto a IR', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_tax_retention = fields.Float(
        string='Total Retenciones', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_tax_ret_ir = fields.Float(
        string='Base IR', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    taxed_ret_ir = fields.Float(
        string='Impuesto IR', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_tax_ret_vatb = fields.Float(
        string='Base Ret. IVA', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    taxed_ret_vatb = fields.Float(
        string='Retencion en IVA', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_tax_ret_vatsrv = fields.Float(
        string='Base Ret. IVA', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    taxed_ret_vatsrv = fields.Float(
        string='Retencion en IVA', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_vat_cero = fields.Float(
        string='Base IVA 0%', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    amount_novat = fields.Float(
        string='Base No IVA', digits_compute=PRECISION_DP,
        store=True, readonly=True, compute='_compute_amount')
    retention_id = fields.Many2one(
        'account.retention',
        string='Retención de Impuestos',
        store=True, readonly=True,
        copy=False
    )
    retention_ir = fields.Boolean(
        compute='_check_retention',
        string="Tiene Retención en IR",
        store=True,
        readonly=True,
        )
    retention_vat = fields.Boolean(
        compute='_check_retention',
        string='Tiene Retencion en IVA',
        store=True,
        readonly=True,
        )
    no_retention_ir = fields.Boolean(
        string='No objeto de Retención',
        store=True, readonly=True, compute='_check_retention')
    type = fields.Selection(
        [
            ('out_invoice', 'Customer Invoice'),
            ('in_invoice', 'Supplier Invoice'),
            ('out_refund', 'Customer Refund'),
            ('in_refund', 'Supplier Refund'),
            ('liq_purchase', 'Liquidacion de Compra')
        ], 'Type', readonly=True, select=True, change_default=True)
    payment_method = fields.Selection(
        [
            ('01', 'SIN UTILIZACIÓN DEL SISTEMA FINANCIERO'),
            ('16', 'TARJETA DE DEBITO'),
            ('17', 'DINERO ELECTRONICO'),
            #('18', 'TARJETA PREPAGO'),
            ('19', 'TARJETA DE CREDITO'),
            ('20', 'OTROS CON UTILIZACION DEL SISTEMA FINANCIERO'),
            ('21', 'ENDOSO DE TITULOS'),
        ],
        string='Metodo de Pago',
        help="Metodo de pago negociado con el cliente",
        required=True,
        default='20')
    amount_total_letras = fields.Char(string='Monto en Letras', size=256,
        store=True, readonly=True, compute='_compute_amount')
    withdrawing_number = fields.Integer(
        'Num. Retención',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False
    )
    create_retention_type = fields.Selection(
        [('auto', 'Automático'),
         ('manual', 'Manual'),
         ('no_retention', 'No Generar')],
        string='Numerar Retención',
        required=True,
        default='manual'
    )
    sustento_id = fields.Many2one(
        'account.ats.sustento',
        string='Sustento del Comprobante'
    )

    @api.multi
    def onchange_journal_id(self, journal_id=False):
        # Método redefinido para cargar la autorizacion de facturas de venta
        if journal_id:
            journal = self.env['account.journal'].browse(journal_id)

            if self.type == 'out_invoice' and not journal.auth_id:
                return {
                    'warning': {
                        'title': 'Error',
                        'message': u'No se ha configurado una autorización en este diario.'  # noqa
                        }
                    }
            return {
                'value': {
                    'currency_id': journal.currency.id or journal.company_id.currency_id.id,  # noqa
                    'company_id': journal.company_id.id,
                    'auth_inv_id': journal.auth_id.id
                }
            }
        return {}

    @api.multi
    def _check_invoice_number(self):
        """Método de validacion de numero de factura y numero de
        retencion

        número de factura: suppplier_invoice_number
        número de retención: withdrawing_number
        """
        INV_LIMIT = 9  # CHECK: mover a compañia ?

        for obj in self:
            if obj.state in ['open', 'paid', 'cancel']:
                return True
            if obj.type == 'out_invoice':
                return True
            if not len(obj.supplier_invoice_number) == INV_LIMIT:
                raise UserError('Error', u'Son %s dígitos en el núm. de Factura.' % INV_LIMIT)  # noqa

            auth = obj.auth_inv_id

            inv_number = obj.supplier_invoice_number

            if not auth:
                raise except_orm(
                    'Error!',
                    u'No se ha configurado una autorización de documentos, revisar Partner y Diario Contable.'  # noqa
                )

            if not self.env['account.authorisation'].is_valid_number(auth.id, int(inv_number)):  # noqa
                raise UserError('Error!', u'Número de factura fuera de rango.')

            # validacion de numero de retencion para facturas de proveedor
            if obj.type == 'in_invoice':
                if not obj.journal_id.auth_ret_id:
                    raise except_orm(
                        'Error!',
                        u'No ha configurado una autorización de retenciones.'
                    )
                if obj.create_retention_type == 'no_retention':
                    return True


                if not self.env['account.authorisation'].is_valid_number(obj.journal_id.auth_ret_id.id, int(obj.withdrawing_number)):  # noqa
                    raise except_orm(
                        'Error!',
                        u'El número de retención no es válido.'
                    )
        return True

    _constraints = [
        (
            _check_invoice_number,
            u'Número fuera de rango de autorización activa.',
            [u'Número Factura']
        ),
    ]

    _sql_constraints = [
        (
            'unique_inv_supplier',
            'unique(supplier_invoice_number,type,partner_id)',
            u'El número de factura es único.'
        )
    ]

    @api.onchange('supplier_invoice_number')
    def check_invoice_supplier(self):
        if self.supplier_invoice_number and len(self.supplier_invoice_number) != 9:  # noqa
            self.supplier_invoice_number = self.supplier_invoice_number.zfill(9)  # noqa

#    @api.constrains('reference')
#    def check_reference(self):
#        """
#        Metodo que verifica la longitud de la autorizacion
#        10: documento fisico
#        35: factura electronica modo online
#        49: factura electronica modo offline
#        """
#        if self.reference and len(self.reference) not in [10, 35, 49]:
#            raise Warning(
#                'Error',
#                u'Debe ingresar 10, 35 o 49 dígitos según el documento.'
#            )

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
                            payment_term=False, partner_bank_id=False,
                            company_id=False):
        res1 = super(Invoice, self).onchange_partner_id(type, partner_id, date_invoice,  # noqa
                                                        payment_term, partner_bank_id,  # noqa
                                                        company_id)
        if 'reference_type' in res1['value']:
            res1['value'].pop('reference_type')
        res = self.env['account.authorisation'].search([('partner_id', '=', partner_id), ('in_type', '=', 'externo')], limit=1)  # noqa
        if res:
            res1['value']['auth_inv_id'] = res[0]
        return res1

    @api.multi
    def action_cancel_draft(self):
        """
        Redefinicion de metodo para borrar la retencion asociada.
        CHECK: saber si es correcto eliminar o hacer cache del
        numero del documento.
        """
        for inv in self:
            if inv.retention_id:
                inv.retention_id.unlink()
        super(Invoice, self).action_cancel_draft()
        return True

    @api.multi
    def action_retention_create(self):
        """
        Este método genera el documento de retencion en varios escenarios
        considera casos de:
        * Generar retencion automaticamente
        * Generar retencion de reemplazo
        * Cancelar retencion generada
        """
        TYPES_TO_VALIDATE = ['in_invoice', 'liq_purchase']
        for inv in self:

            if not (inv.retention_ir or inv.retention_vat):
                continue

            if inv.create_retention_type == 'no_retention':
                continue

            wd_number = False

            if inv.create_retention_type == 'auto':
                sequence = inv.journal_id.auth_ret_id.sequence_id
                wd_number = self.env['ir.sequence'].get(sequence.code)
            else:
                if inv.withdrawing_number <= 0:
                    raise except_orm(_('Error!'),
                                     u'El número de retención es incorrecto.')
                wd_number = inv.withdrawing_number  # TODO: validate number

            if inv.retention_id:
                inv.retention_id.action_validate(wd_number)
                continue

            if inv.type in ['in_invoice', 'liq_purchase'] and not inv.journal_id.auth_ret_id:  # noqa
                raise except_orm(
                    'Error',
                    'No ha configurado la autorización de retenciones en el diario.'  # noqa
                )

            withdrawing_data = {
                'partner_id': inv.partner_id.id,
                'name': wd_number,
                'invoice_id': inv.id,
                'auth_id': inv.journal_id.auth_ret_id.id,
                'type': inv.type,
                'in_type': 'ret_%s' % inv.type,
                'date': inv.date_invoice,
                'period_id': inv.period_id.id,
                'num_document': self.invoice_number,
            }

            withdrawing = self.env['account.retention'].create(withdrawing_data)  # noqa

            tids = [l.id for l in inv.tax_line if l.tax_group in ['ret_vat_b', 'ret_vat_srv', 'ret_ir']]  # noqa
            account_invoice_tax = self.env['account.invoice.tax'].browse(tids)
            account_invoice_tax.write({'retention_id': withdrawing.id, 'num_document': inv.supplier_invoice_number})  # noqa

            if inv.type in TYPES_TO_VALIDATE:
                withdrawing.action_validate(wd_number)

            inv.write({'retention_id': withdrawing.id})
        return True

    @api.multi
    def recreate_retention(self):
        """Método que implementa la recreacion de la retención
        TODO: recibir el numero de retención del campo manual
        """
        self._context.update({'recreate_retention': True})
        for inv in self:
            self.action_retention_cancel()
            self.action_retention_create([inv.id])
        return True

    @api.multi
    def action_retention_cancel(self):
        for inv in self:
            if inv.retention_id:
                inv.retention_id.action_cancel()
        return True


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def move_line_get(self, invoice_id):
        inv = self.env['account.invoice'].browse(invoice_id)
        currency = inv.currency_id.with_context(date=inv.date_invoice)
        company_currency = inv.company_id.currency_id

        res = []
        for line in inv.invoice_line:
            mres = self.move_line_get_item(line)
            mres['invl_id'] = line.id
            res.append(mres)
            tax_code_found = False
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1.0 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, inv.partner_id)['taxes']
            for tax in taxes:
                if inv.type in ('out_invoice', 'in_invoice', 'liq_purchase'):
                    tax_code_id = tax['base_code_id']
                    tax_amount = tax['price_unit'] * line.quantity * tax['base_sign']  # noqa
                else:
                    tax_code_id = tax['ref_base_code_id']
                    tax_amount = tax['price_unit'] * line.quantity * tax['ref_base_sign']  # noqa

                if tax_code_found:
                    if not tax_code_id:
                        continue
                    res.append(self.move_line_get_item(line))
                    res[-1]['price'] = 0.0
                    res[-1]['account_analytic_id'] = False
                elif not tax_code_id:
                    continue
                tax_code_found = True

                res[-1]['tax_code_id'] = tax_code_id
                res[-1]['tax_amount'] = currency.compute(tax_amount, company_currency)  # noqa
        return res

    @api.multi
    def product_id_change(self, product, uom_id, qty=0,
                          name='', type='out_invoice',
                          partner_id=False, fposition_id=False,
                          price_unit=False, currency_id=False,
                          company_id=None):
    #@api.onchange('product', 'uom_id', 'qty', 'name', 'type', 'partner_id', 'fposition_id', 'price_unit', 'currency_id', 'company_id')
    #def product_id_change(self):
        context = self._context
        company_id = company_id if company_id is not None else context.get('company_id', False)  # noqa
        self = self.with_context(company_id=company_id, force_company=company_id)  # noqa

        if not partner_id:
            raise except_orm(_('No Partner Defined!'), _("You must first select a partner!"))  # noqa
        if not product:
            if type in ('in_invoice', 'in_refund'):
                return {'value': {}, 'domain': {'uos_id': []}}
            else:
                return {'value': {'price_unit': 0.0}, 'domain': {'uos_id': []}}

        values = {}

        part = self.env['res.partner'].browse(partner_id)
        fpos = self.env['account.fiscal.position'].browse(fposition_id)

        if part.lang:
            self = self.with_context(lang=part.lang)
        product = self.env['product.product'].browse(product)

        values['name'] = product.partner_ref
        if type in ['out_invoice', 'out_refund']:
            account = product.property_account_income or product.categ_id.property_account_income_categ  # noqa
        else:
            account = product.property_account_expense or product.categ_id.property_account_expense_categ  # noqa
        account = fpos.map_account(account)
        if account:
            values['account_id'] = account.id

        if type in ('out_invoice', 'out_refund'):
            taxes = product.taxes_id or account.tax_ids
            if product.description_sale:
                values['name'] += '\n' + product.description_sale
        else:
            taxes = product.supplier_taxes_id or account.tax_ids
            if product.description_purchase:
                values['name'] += '\n' + product.description_purchase

        taxes = fpos.map_tax(taxes)
        values['invoice_line_tax_id'] = taxes.ids

        if type in ('in_invoice', 'in_refund'):
            values['price_unit'] = price_unit or product.standard_price
        else:
            values['price_unit'] = product.list_price

        values['uos_id'] = product.uom_id.id
        if uom_id:
            uom = self.env['product.uom'].browse(uom_id)
            if product.uom_id.category_id.id == uom.category_id.id:
                values['uos_id'] = uom_id

        domain = {'uos_id': [('category_id', '=', product.uom_id.category_id.id)]}  # noqa

        company = self.env['res.company'].browse(company_id)
        currency = self.env['res.currency'].browse(currency_id)

        if company and currency:
            if company.currency_id != currency:
                if type in ('in_invoice', 'in_refund'):
                    values['price_unit'] = product.standard_price
                values['price_unit'] = values['price_unit'] * currency.rate

            if values['uos_id'] and values['uos_id'] != product.uom_id.id:
                values['price_unit'] = self.env['product.uom']._compute_price(
                    product.uom_id.id, values['price_unit'], values['uos_id'])

        return {'value': values, 'domain': domain}


class AccountInvoiceRefund(models.Model):

    _inherit = 'account.invoice.refund'

    @api.model
    def _get_description(self):
        number = '/'
        active_id = self._context.get('active_id', False)
        if not active_id:
            return number
        invoice = self.env['account.invoice'].browse(active_id)
        if invoice.type == 'out_invoice':
            number = invoice.number
        else:
            number = invoice.supplier_invoice_number
        return number

    description = fields.Char(default=_get_description)
