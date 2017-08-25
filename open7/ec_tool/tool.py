# -*- coding: utf-8 -*-
###############################################################################
#                              
#    Gnuthink Cia. Ltda., Cuenca, Ecuador
#    OpenERP ready partner, open source editor.
#    www.gnuthink.com, (+593) 074092170
#     
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#
##############################################################################
from openerp.osv import osv
from datetime import datetime, date, timedelta

def day_between_dates(date_start, date_stop):
    return True

def compute_age(birth):
    v={}
    result={}
    if birth:
        fecha_n = datetime.strptime(birth, "%Y-%m-%d")
        if fecha_n <= datetime.today():
            today = date.today().strftime("%Y-%m-%d")
            now = today.split('-')
            birth = birth.split('-')
            datenow = date( int(now[0]), int(now[1]), int(now[2]) )
            datebirth = date( int(birth[0]), int(birth[1]), int(birth[2]) )
            delta = datenow - datebirth
            age = delta.days/365
            return int(age)
        else:
            return False

def _check_cedula(identificador):
    try:
        ident=int(identificador)
    except ValueError:
        raise osv.except_osv(('Aviso !'), 'La cedula no puede contener caracteres')
#    return True
    if len(identificador) == 13 and not identificador[10:13] == '001':
        return False
    else:
        if len(identificador) < 10:
            return False
    coef = [2,1,2,1,2,1,2,1,2]
    cedula = identificador[:9]
    suma = 0
    for c in cedula:
        val = int(c) * coef.pop()
        suma += val > 9 and val-9 or val
    result = 10 - ((suma % 10)!=0 and suma%10 or 10)
    if result == int(identificador[9:10]):
        return True
    else:
        return False
 
def _check_ruc(ced_ruc, position):
    ruc = ced_ruc
    if not len(ruc) == 13:
        return False
    if position == 'SECTOR PUBLICO':
        coef = [3,2,7,6,5,4,3,2,0,0]
        coef.reverse()
        verificador = int(ruc[8:9])
    else:
        if int(ruc[2:3]) < 6:
            return _check_cedula(ced_ruc) 
        if ruc[2:3] == '9':
            coef = [4,3,2,7,6,5,4,3,2,0]
            coef.reverse()
            verificador = int(ruc[9:10])
        elif ruc[2:3] == '6':
            coef = [3,2,7,6,5,4,3,2,0,0]
            coef.reverse()
            verificador = int(ruc[9:10])
        else:
            raise osv.except_osv('Error', 'Cambie el tipo de persona')
    suma = 0
    for c in ruc[:10]:
        suma += int(c) * coef.pop()
        result = 11 - (suma>0 and suma % 11 or 11)
    if result == verificador:
        return True
    else:
        return False


def _check_ced_ruc(self, cr, uid, ids):
    partners = self.browse(cr, uid, ids)
    for partner in partners:
        if not partner.ced_ruc:
            return True
        if partner.type_ced_ruc == 'pasaporte':
            return True
        if partner.ced_ruc == '9999999999999':
            return True
        #if partner.tipo_persona == '9':
        if partner.type_ced_ruc == 'ruc' and partner.tipo_persona == '9':
            return _check_ruc(partner.ced_ruc, partner.property_account_position.name)
        else:
            if partner.ced_ruc[:2] == '51':
                return True
            else:
                return _check_cedula(partner.ced_ruc)


UNIDADES = ('','UN ','DOS ','TRES ','CUATRO ','CINCO ','SEIS ','SIETE ','OCHO ','NUEVE ','DIEZ ','ONCE ','DOCE ','TRECE ','CATORCE ','QUINCE ',   'DIECISEIS ', 'DIECISIETE ',
	    'DIECIOCHO ', 'DIECINUEVE ', 'VEINTE ')
DECENAS = ( 'VENTI', 'TREINTA ', 'CUARENTA ', 'CINCUENTA ', 'SESENTA ', 'SETENTA ', 'OCHENTA ', 'NOVENTA ', 'CIEN ')
CENTENAS = ('CIENTO ', 'DOSCIENTOS ', 'TRESCIENTOS ', 'CUATROCIENTOS ', 'QUINIENTOS ', 'SEISCIENTOS ', 'SETECIENTOS ', 'OCHOCIENTOS ', 'NOVECIENTOS ')

def toWord(number):

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
            converted += '%sMILLONES ' % __convertNumber(millones)

    if(miles):
        if(miles == '001'):
            converted += 'MIL '
        elif(int(miles) > 0):
            converted += '%sMIL ' % __convertNumber(miles)

    if(cientos):
        if(cientos == '001'):
            converted += 'UN '
        elif(int(cientos) > 0):
            converted += '%s ' % __convertNumber(cientos)

    converted += ''

    return converted.title() + 'Con ' + decimal + '/100'

def __convertNumber(n):
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

def higher_than(num, reference):
    """
    Return true if NUM is higher than REFERENCE
    """
    if (num>reference):
        return True
    else:
        return False

def lesser_than(num, reference):
    """
    Return true if NUM is lesser than REFERENCE
    """
    if (num<reference):
        return True
    else:
        return False
