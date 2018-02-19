# -*- coding: utf-8 -*-

from openerp import models, fields


class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'
    year = fields.Char('Year')


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    motor_nro = fields.Char('Motor Nro')
    body_nro = fields.Char('Body Nro')
