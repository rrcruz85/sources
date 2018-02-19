# -*- coding: utf-8 -*-
# (c) 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons import decimal_precision as dp
from openerp import models, fields, api, _


class Machinery(models.Model):
    _name = "machinery"
    _description = "Holds records of Machines"

    def _def_company(self):
        return self.env.user.company_id.id

    name = fields.Char('Machine Name', required=True)
    company = fields.Many2one('res.company', 'Company', required=True,
                              default=_def_company)
    assetacc = fields.Many2one('account.account', string='Asset Account')
    depracc = fields.Many2one('account.account', string='Depreciation Account')
    year = fields.Char('Year')
    model = fields.Char('Model')
    product = fields.Many2one(
        comodel_name='product.product', string='Associated product',
        help="This product will contain information about the machine such as"
        " the manufacturer.")
    manufacturer = fields.Many2one(
        comodel_name='res.partner', related='product.manufacturer',
        readonly=True, help="Manufacturer is related to the associated product"
        " defined for the machine.")
    serial_char = fields.Char('Product Serial #')
    serial = fields.Many2one('stock.production.lot', string='Product Serial #',
                             domain="[('product_id', '=', product)]")
    model_type = fields.Many2one('machine.model', 'Type')
    status = fields.Selection([('active', 'Active'), ('inactive', 'InActive'),
                               ('outofservice', 'Out of Service')],
                              'Status', required=True, default='active')
    ownership = fields.Selection([('own', 'Own'), ('lease', 'Lease'),
                                  ('rental', 'Rental')],
                                 'Ownership', default='own', required=True)
    bcyl = fields.Float('Base Cycles', digits=(16, 3),
                        help="Last recorded cycles")
    bdate = fields.Date('Record Date',
                        help="Date on which the cycles is recorded")
    purch_date = fields.Date('Purchase Date',
                             help="Machine's date of purchase")
    purch_cost = fields.Float('Purchase Value', digits=(16, 2))
    purch_partner = fields.Many2one('res.partner', 'Purchased From')
    purch_inv = fields.Many2one('account.invoice', string='Purchase Invoice')
    purch_cycles = fields.Integer('Cycles at Purchase')
    actcycles = fields.Integer('Actual Cycles')
    deprecperc = fields.Float('Depreciation in %', digits=(10, 2))
    deprecperiod = fields.Selection([('monthly', 'Monthly'),
                                     ('quarterly', 'Quarterly'),
                                     ('halfyearly', 'Half Yearly'),
                                     ('annual', 'Yearly')], 'Depr. period',
                                    default='annual', required=True)
    primarymeter = fields.Selection([('calendar', 'Calendar'),
                                     ('cycles', 'Cycles'),
                                     ('hourmeter', 'Hour Meter')],
                                    'Primary Meter', default='cycles',
                                    required=True)
    warrexp = fields.Date('Date', help="Expiry date for warranty of product")
    warrexpcy = fields.Integer('(or) cycles',
                               help="Expiry cycles for warranty of product")
    location = fields.Many2one('stock.location', 'Stk Location',
                               help="This association is necessary if you want"
                               " to make repair orders with the machine")
    enrolldate = fields.Date('Enrollment date', required=True,
                             default=lambda
                             self: fields.Date.context_today(self))
    ambit = fields.Selection([('local', 'Local'), ('national', 'National'),
                              ('international', 'International')],
                             'Ambit', default='local')
    card = fields.Char('Card')
    cardexp = fields.Date('Card Expiration')
    frame = fields.Char('Frame Number')
    phone = fields.Char('Phone number')
    mac = fields.Char('MAC Address')
    insurance = fields.Char('Insurance Name')
    policy = fields.Char('Machine policy')
    users = fields.One2many('machinery.users', 'machine', 'Machine Users')
    power = fields.Char('Power (Kw)')
    product_categ = fields.Many2one('product.category', 'Internal category',
                                    related='product.categ_id')
    salvage_value = fields.Float('Salvage Value',
                                 digits=dp.get_precision('Product Price'))

    # Informacion referente al reporte...
    reception_date = fields.Date(default=fields.Date.today)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo')

    customer_id = fields.Many2one('res.partner', string='Customer')
    broker_id = fields.Many2one('res.partner', string='Agente')
    consultant_id = fields.Many2one('hr.employee', string='Asesor')

    work_order = fields.Char(string='Orden de Trabajo')
    cia = fields.Char()

    antenna = fields.Boolean(string='Antena')
    radio = fields.Boolean()
    plumas = fields.Boolean()
    extinguidor = fields.Boolean()
    triangulos = fields.Boolean()
    seguro_aros = fields.Boolean()
    signos = fields.Boolean()
    encendedor = fields.Boolean()
    moquetas = fields.Boolean()
    espejos = fields.Boolean()
    llave_ruedas = fields.Boolean()
    compac = fields.Boolean()
    tapacubos = fields.Integer()
    llanta = fields.Boolean()
    gata = fields.Boolean()
    herramientas = fields.Boolean()
    botiquin = fields.Boolean()
    tapagas = fields.Boolean()

    otros = fields.Boolean()
    otros_description = fields.Char()

    work_to_realize_ids = fields.Many2many('fleet.vehicle.log.services', string='Trabajos a realizar')
    observation_ids = fields.Many2many('machinery.observation', string='Observaciones')
    coordinates = fields.Char()

    @api.one
    def action_clear(self):
        self.coordinates = ''


class Observation(models.Model):
    _name = 'machinery.observation'
    _description = 'machinery.observation'
    name = fields.Char(required=True)


class MachineryUsers(models.Model):
    _name = 'machinery.users'

    m_user = fields.Many2one('res.users', 'User')
    machine = fields.Many2one('machinery', 'Machine')
    start_date = fields.Date('Homologation Start Date')
    end_date = fields.Date('Homologation End Date')

    _sql_constraints = [
        ('uniq_machine_user', 'unique(machine, m_user)', _('User already defined for the machine'))
    ]
