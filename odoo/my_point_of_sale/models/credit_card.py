# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class PosCreditCard(osv.osv):
    _name = 'pos.credit_card'
    _description = 'pos.credit_card'

    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Name', required=True),
        'is_active': fields.boolean('Active')
    }

    _defaults = {
        'is_active': True,
    }
