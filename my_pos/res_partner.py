
import openerp
import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger('INFO')

class res_partner(osv.Model):
    _inherit = 'res.partner'
    
#    def create(self, cr, uid, vals, context={}):
#        i=1
#        while i<2000:
#            res_id = super(res_partner, self).create(cr, uid, vals, context)
#            _logger.info(i)
#            i+=1
#        
#        return res_id
    
    def write_partner_from_pos(self, cr, uid, cid, cname, czip, cphone, cmobile, cemail, cid_type, cid_number, context=None):
        if context is None: context = {}
        client_id = int(cid)
        
        try:
            if client_id != 0 and client_id != -1:
                self.write(cr, uid, client_id, {'name': cname, 'street': czip, 'phone': cphone, 'mobile': cmobile, 'email': cemail, 'ced_ruc': cid_number, 'type_ced_ruc': cid_type}, context=context)
                idClient = client_id
            else:
                company_id =  self.pool.get('res.company')._company_default_get(cr, uid, 'res.partner', context=context),
                idClient = self.create(cr, uid, {'name': cname, 'street': czip, 'phone': cphone, 'mobile': cmobile, 'email': cemail, 'ced_ruc': cid_number, 'type_ced_ruc': cid_type, 'company_id': company_id}, context=context)
        except Exception, e:
            cr.rollback()
            return _('Error! %s') % (str(e))
        
        return idClient
    
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
            ident = int(identificador)
        except ValueError:
            raise osv.except_osv(('Aviso !'), 'La cedula no puede contener caracteres')

        if len(identificador) == 13 and not identificador[10:13] == '001': return False
        else:
            if len(identificador) < 10: return False

        coef = [2,1,2,1,2,1,2,1,2]
        cedula = identificador[:9]
        suma = 0

        for c in cedula:
            val = int(c) * coef.pop()
            suma += val > 9 and val-9 or val

        result = 10 - ((suma % 10)!=0 and suma%10 or 10)
        if result == int(identificador[9:10]): return True
        return False

    def _check_ruc(self, ced_ruc, position):
        ruc = ced_ruc
        if not len(ruc) == 13: return False

        if position == 'SECTOR PUBLICO':
            coef = [3,2,7,6,5,4,3,2,0,0]
            coef.reverse()
            verificador = int(ruc[8:9])
        else:
            if int(ruc[2:3]) < 6: return self._check_cedula(ced_ruc)
            if ruc[2:3] == '9':
                coef = [4,3,2,7,6,5,4,3,2,0]
                coef.reverse()
                verificador = int(ruc[9:10])
            elif ruc[2:3] == '6':
                coef = [3,2,7,6,5,4,3,2,0,0]
                coef.reverse()
                verificador = int(ruc[9:10])
            else: raise osv.except_osv('Error', 'Cambie el tipo de persona')

        suma = 0
        for c in ruc[:10]:
            suma += int(c) * coef.pop()
            result = 11 - (suma > 0 and suma % 11 or 11)

        if result == verificador: return True
        return False

    _columns = {
        'ced_ruc'               : fields.char('No. Identificacion', size = 15, required=False, readonly=False),
        'type_ced_ruc'          : fields.selection([('ruc', 'Ruc'), ('cedula', 'Cedula'), ('pasaporte', 'Pasaporte')], 'Tipo identificacion', select=True, readonly=False),
        'tipo_persona'               : fields.char('Tipo Persona',size = 15,  required=False, readonly=False),

    }

    _defaults = {
        'tipo_persona': '9',
    }

    _constraints = [
        (_check_ced_ruc, _('Error: Invalid value for the identification number...'), ['ced_ruc']),
    ]

res_partner()