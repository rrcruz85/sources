# -*- coding: utf-8 -*-

import openerp
from openerp.osv import fields, osv

class test_model(osv.osv):
    _name = "test.model"
    _description = "Test Model"

    _columns = {
        'name': fields.char('Name', size=128, required = True),
        'description': fields.text('Description'),
        'int_value': fields.integer('Int Value'),
    }
