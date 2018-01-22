# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.tools.translate import _


class Partner(osv.osv):
    _inherit = 'res.partner'

    
    def _check_ced_ruc(self, cr, uid, ids):
        partners = self.browse(cr, uid, ids)
        for partner in partners:
            if not partner.ced_ruc:
                return True
            if partner.type_ced_ruc == 'pasaporte':
                return True
            if partner.ced_ruc == '9999999999999':
                return True
            if partner.tipo_persona == '9':
                return self._check_ruc(partner.ced_ruc, partner.property_account_position.name)
            else:
                if partner.ced_ruc[:2] == '51':
                    return True
                else:
                    return self._check_cedula(partner.ced_ruc)

    def _check_cedula(self, identificador):
        try:
            ident =identificador and int(identificador)
        except ValueError:
            raise osv.except_osv(('Aviso !'), 'La cedula no puede contener caracteres')

        if len(identificador) == 13 and not identificador[10:13] == '001':
            return False
        else:
            if len(identificador) < 10:
                return False

        coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        cedula = identificador[:9]
        suma = 0

        for c in cedula:
            val = int(c) * coef.pop()
            suma += val > 9 and val-9 or val

        result = 10 - ((suma % 10) != 0 and suma % 10 or 10)
        if result == int(identificador[9:10]): return True
        return False

    def _check_ruc(self, ced_ruc, position):
        ruc = ced_ruc
        if not len(ruc) == 13: return False

        if position == 'SECTOR PUBLICO':
            coef = [3, 2, 7, 6, 5, 4, 3, 2, 0, 0]
            coef.reverse()
            verificador = int(ruc[8:9])
        else:
            if int(ruc[2:3]) < 6: return self._check_cedula(ced_ruc)
            if ruc[2:3] == '9':
                coef = [4, 3, 2, 7, 6, 5, 4, 3, 2, 0]
                coef.reverse()
                verificador = int(ruc[9:10])
            elif ruc[2:3] == '6':
                coef = [3, 2, 7, 6, 5, 4, 3, 2, 0, 0]
                coef.reverse()
                verificador = int(ruc[9:10])
            else:
                raise osv.except_osv('Error', 'Cambie el tipo de persona')

        suma = 0
        for c in ruc[:10]:
            suma += int(c) * coef.pop()
            result = 11 - (suma > 0 and suma % 11 or 11)

        if result == verificador:
            return True
        return False

    _columns = {
        'ced_ruc': fields.char('No. Identificacion', size=15, required=False, readonly=False),
        'tipo_persona': fields.char('Tipo Persona', size=15,  required=False, readonly=False),
        'type_ced_ruc': fields.selection(
            [('ruc', 'Ruc'), ('cedula', 'Cedula'), ('pasaporte', 'Pasaporte')],
            string='Tipo identificacion', select=True, readonly=False),
    }

    _defaults = {
        'tipo_persona': '1',
    }

    _constraints = [
        (_check_ced_ruc, _('Error: Invalid value for the identification number...'), ['ced_ruc']),
    ]
