# -*- coding: utf-8 -*-

import logging
from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)

class res_company(osv.osv):
    _inherit = 'res.company'

    _columns = {
        'warranty': fields.text('Product Warranty'),
    }
