# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime

class OdooTest(models.Model):
    _name = 'odoo.test'
    _description = 'Prueba'
    firstname = fields.Char(string="First Name")
    secondname = fields.Char(string="Second Name")
    datebirth = fields.Datetime(string="Date Birth")
    age = fields.Integer(string="Age", compute = "_get_age")

    @api.depends('age')
    def _get_age(self):
        fecha_actual = datetime.datetime.now()
        for obj in self:
            obj.age = 1