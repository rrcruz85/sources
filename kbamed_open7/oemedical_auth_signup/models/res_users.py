# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from ast import literal_eval
import random
import re
from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.addons.auth_signup.res_users import SignupError
from openerp.tools.translate import _
from urlparse import urljoin
from dateutil.relativedelta import relativedelta
import logging
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.SystemRandom().choice(chars) for i in xrange(20))

def now(**kwargs):
    dt = datetime.now() + timedelta(**kwargs)
    return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

def _check_cedula(identificador):
    try:
        ident = int(identificador)
    except ValueError:
        raise osv.except_osv(('Aviso !'), 'La cedula no puede contener caracteres')

    if len(identificador) == 13 and not identificador[10:13] == '001':
        return False
    elif len(identificador) < 10:
        return False

    coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    cedula = identificador[:9]
    suma = 0
    for c in cedula:
        val = int(c) * coef.pop()
        suma += val > 9 and val - 9 or val
    result = 10 - ((suma % 10) != 0 and suma % 10 or 10)
    if result == int(identificador[9:10]):
        return True
    else:
        return False

def _check_ruc(ced_ruc, position):
    ruc = ced_ruc
    if not len(ruc) == 13:
        return False
    if position == 'SECTOR PUBLICO':
        coef = [3, 2, 7, 6, 5, 4, 3, 2, 0, 0]
        coef.reverse()
        verificador = int(ruc[8:9])
    else:
        if int(ruc[2:3]) < 6:
            return _check_cedula(ced_ruc)
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
    else:
        return False

class res_users(osv.Model):
    _inherit = 'res.users'

    def signup(self, cr, uid, values, token=None, context=None):
        if token:
            # signup with a token: find the corresponding partner id
            res_partner = self.pool.get('res.partner')
            partner = res_partner._signup_retrieve_partner(
                            cr, uid, token, check_validity=True, raise_exception=True, context=None)
            # invalidate signup token
            partner.write({'signup_token': False, 'signup_type': False, 'signup_expiration': False})

            partner_user = partner.user_ids and partner.user_ids[0] or False
            if partner_user:
                # user exists, modify it according to values
                values.pop('login', None)
                values.pop('name', None)
                partner_user.write(values)
                return (cr.dbname, partner_user.login, values.get('password'))
            else:
                # user does not exist: sign up invited user
                values.update({
                    'name': partner.name,
                    'partner_id': partner.id,
                    'email': values.get('email') or values.get('login'),
                })
                if partner.company_id:
                    values['company_id'] = partner.company_id.id
                    values['company_ids'] = [(6, 0, [partner.company_id.id])]
                self._signup_create_user(cr, uid, values, context=context)
        else:
            # no token, sign up an external user
            if values.get('use_email'):
                values['login'] = values.get('email')
            else:
                values['login'] = values.get('name')
            if not context:
                context = {
                    'create_patient': True
                }
            values['birthdate'] = datetime.strptime(values.get('birthdate'), '%d-%m-%Y')
            self._signup_create_user(cr, uid, values, context=context)

        return (cr.dbname, values.get('login'), values.get('password'))

    def _signup_create_user(self, cr, uid, values, context=None):
        """ create a new user from the template user """
        ir_config_parameter = self.pool.get('ir.config_parameter')
        template_user_id = literal_eval(ir_config_parameter.get_param(cr, uid, 'auth_signup.template_user_id', 'False'))
        assert template_user_id and self.exists(cr, uid, template_user_id, context=context), 'Signup: invalid template user'

        # check that uninvited users may sign up
        if 'partner_id' not in values:
            if not literal_eval(ir_config_parameter.get_param(cr, uid, 'auth_signup.allow_uninvited', 'False')):
                raise SignupError('Signup is not allowed for uninvited users')

        assert values.get('login'), "Signup: no login given for new user"
        assert values.get('partner_id') or values.get('name'), "Signup: no name or partner given for new user"

        # create a copy of the template user (attached to a specific partner_id if given)
        values['active'] = False
        return self.copy(cr, uid, template_user_id, values, context=context)

    def create(self, cr, uid, values, context=None):
        # overridden to automatically invite user to sign up
        if context and context.get('reset_password'):
            context.pop('reset_password')

        if context and context.get('create_patient'):
            values['active'] = False

        values['tmp_name'] = values['login']
        if values['use_email']:
            values['login'] = values['email']

        user_id = super(res_users, self).create(cr, uid, values, context=context)
        user = self.browse(cr, uid, user_id, context=context)

        token = random_token()
        if context and context.get('create_patient') and user.partner_id:
            country = self.pool.get('res.country').search(cr, uid, [('code', '=', 'EC')])
            state = self.pool.get('res.country.state').search(cr, uid, [('country_id', '=', country[0]), ('code', '=', 'PIC')])

            self.pool.get('res.partner').write(cr, uid, [user.partner_id.id], {
                'name': values['first_name'] + ' ' + values['last_name'] + ' ' + values['slastname'],
                'user_id': user_id,
                'country_id': country[0],
                'state_id': state[0],
                'city': 'Quito',
                'signup_token': token,
                'signup_type': 'signup',
                'signup_expiration': now(days=+1),
                'notification_email_send': 'none',
                'tz': 'America/Guayaquil'
            }, context=None)

            self.pool.get('oemedical.patient').create(cr, uid, {
                'partner_id': user.partner_id.id,
                'ref': self.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'),
            }, context=None)

            patient_group = self.pool.get('ir.model.data').get_object(cr, uid, 'oemedical', 'patient_group')
            portal_group = self.pool.get('ir.model.data').get_object(cr, uid, 'portal', 'group_portal')
            employee_group = self.pool.get('ir.model.data').get_object(cr, uid, 'base', 'group_user')

            if patient_group:
                self.write(cr, uid, [user_id], {
                    'groups_id': [(4, patient_group.id)]
                }, context=context)
            if portal_group:
                self.write(cr, uid, [user_id], {
                    'groups_id': [(3, portal_group.id)]
                }, context=context)

            if employee_group:
                self.write(cr, uid, [user_id], {
                    'groups_id': [(3, employee_group.id)]
                }, context=context)
        else:
            is_patient = False
            is_doctor = False
            patient_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'patient_group')
            patient_group_id = filter(lambda g: g.id == patient_group[1], user.groups_id)
            if len(patient_group_id):
                is_patient = True
                self.pool.get('oemedical.patient').create(cr, uid, {
                    'partner_id': user.partner_id.id,
                    'ref': self.pool.get('ir.sequence').get(cr, uid, 'oemedical.patient'),
                }, context=None)

            doctor_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'doctor_group')
            doctor_group_id = filter(lambda g: g.id == doctor_group[1], user.groups_id)
            if len(doctor_group_id):
                is_doctor = True
                self.pool.get('oemedical.physician').create(cr, uid, {
                    'physician_id': user.partner_id.id
                }, context=None)

            self.pool.get('res.partner').write(cr, uid, [user.partner_id.id], {
                'user_id': user_id,
                'signup_token': token,
                'signup_type': 'reset',
                'signup_expiration': now(days=+1),
                'is_patient': is_patient,
                'is_doctor': is_doctor
            }, context=None)

        if context and context.get('create_patient'):
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'oemedical_auth_signup', 'activation_account_email')
        else:
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'oemedical_auth_signup', 'activation_created_account_email')

        try:
            if not template:
                raise osv.except_osv(_("Cannot send email: email template not found."), user.name)
            if not user.email:
                raise osv.except_osv(_("Cannot send email: user has no email address."), user.name)
            mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, user.id, True, context=context)
            mail_obj = self.pool.get('mail.mail')
            mail_state = mail_obj.read(cr, uid, mail_id, ['state'], context=context)
            if mail_state and mail_state['state'] == 'exception':
                raise osv.except_osv(_("Cannot send email: no outgoing email server configured.\nYou can configure it under Settings/General Settings."), user.name)
        except ValueError as e:
            _logger.exception(e.message)
            pass
        return user_id

    def write(self, cr, uid, ids, values, context=None):
        for user in self.browse(cr, uid, ids):
            if 'use_email' in values:
                if values['use_email']:
                    values['login'] = values['email'] if 'email' in values else user.email
                else:
                    values['login'] = user.tmp_name if 'login' not in values else values['login']

            if 'login' in values and not values['use_email']:
                values['tmp_name'] = values['login']
        return super(res_users, self).write(cr, uid, ids, values, context=context)

    def action_reset_password(self, cr, uid, ids, context=None):
        """ create signup token for each user, and send their signup url by email """
        # prepare reset password signup
        res_partner = self.pool.get('res.partner')
        partner_ids = [user.partner_id.id for user in self.browse(cr, uid, ids, context)]
        res_partner.signup_prepare(cr, uid, partner_ids, signup_type="reset", expiration=now(days=+1), context=context)
        self.write(cr, uid, ids, {'active': False})

        if not context:
            context = {}

        # send email to users with their signup url
        template = self.pool.get('ir.model.data').get_object(cr, uid, 'auth_signup', 'reset_password_email')
        mail_obj = self.pool.get('mail.mail')
        assert template._name == 'email.template'
        for user in self.browse(cr, uid, ids, context):
            if not user.email:
                raise osv.except_osv(_("Cannot send email: user has no email address."), user.name)
            mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, user.id, True, context=context)
            mail_state = mail_obj.read(cr, uid, mail_id, ['state'], context=context)
            if mail_state and mail_state['state'] == 'exception':
                raise osv.except_osv(_("Cannot send email: no outgoing email server configured.\nYou can configure it under Settings/General Settings."), user.name)
            else:
                return True

    def change_password(self, cr, uid, old_passwd, new_passwd, context=None):
        self.check(cr.dbname, uid, old_passwd)
        if new_passwd:
            return self.write(cr, SUPERUSER_ID, uid, {'password': new_passwd, 'active': True})
        raise osv.except_osv(_('Warning!'), _("Setting empty passwords is not allowed for security reasons!"))

    def onchange_name(self, cr, uid, ids, first_name, last_name, slastname, context=None):
        if first_name == False:
            first_name = ''
        if last_name == False:
            last_name = ''
        if slastname == False:
            slastname = ''
        res = {
            'value': {
                'name': first_name + ' ' + last_name + ' ' + slastname
            }
        }
        return res

    def onchange_dob(self, cr, uid, ids, birthdate, context=None):
        res = {}
        if birthdate:
            delta = relativedelta(datetime.now(), datetime.strptime(str(birthdate), '%Y-%m-%d'))
            res['value'] = {
                'age': delta.years
            }
        return res

    _columns = {
        'use_email': fields.boolean(string='Use Email', help="Use email for logging in"),
        'tmp_name': fields.char(string='Tmp Name', size=128),
    }

    def _get_default_country(self, cr, uid, context=None):
        result = self.pool.get('res.country').search(cr, uid, [('code', '=', 'EC')])
        return result and result[0] or False

    def _get_default_state(self, cr, uid, context=None):
        result = self.pool.get('res.country').search(cr, uid, [('code', '=', 'EC')])
        if result and result[0]:
            res = self.pool.get('res.country.state').search(cr, uid,[('country_id', '=', result[0]), ('code', '=', 'PIC')])
            return res and res[0] or False
        return False

    _defaults = {
        'active': False,
        'is_person': True,
        'tipo_persona':  '6',
        'type_ced_ruc': 'cedula',
        'mobile_operator': 'claro',
        'city': 'Quito',
        'country_id': _get_default_country,
        'state_id': _get_default_state,
        'tz': 'America/Guayaquil',
        'notification_email_send': 'none',
        'groups_id': [],
    }

    def _check_ced_ruc(self, cr, uid, ids, context=None):
        for user in self.browse(cr, uid, ids):
            if user.type_ced_ruc == 'pasaporte':
                return re.match(r'^[a-zA-Z0-9]+$', user.ced_ruc)
            if user.ced_ruc == '9999999999999':
                return True
            if user.type_ced_ruc == 'ruc':
                return _check_ruc(user.ced_ruc, user.property_account_position.name)
            else:
                if user.ced_ruc[:2] == '51':
                    return True
                else:
                    return _check_cedula(user.ced_ruc)
        return True

    def _check_first_name(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.first_name and not re.match(r'^[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]+\D*[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]*$', obj.first_name):
                return False
        return True

    def _check_last_name(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.last_name and not re.match(r'^[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]+$', obj.last_name):
                return False
        return True

    def _check_slast_name(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.slastname and not re.match(r'^[a-zA-ZáÁéÉíÍóÓúÚüÜñÑ]+$', obj.slastname):
                return False
        return True

    def _check_mobile_number(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.mobile and not re.match(r'^[0-9]{9,10}$', obj.mobile):
                return False
        return True

    def _check_phone_number(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.phone and not re.match(r'^[0-9]{7,9}$', obj.phone):
                return False
        return True

    def _check_email(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.email and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', obj.email):
                return False
        return True

    def _check_unique_ced_ruc(self, cr, uid, ids, context=None):
        for user in self.browse(cr, uid, ids):
            if user.ced_ruc:
                counts = self.search(cr, uid, [('id', '!=', user.id), ('ced_ruc', '=', user.ced_ruc)], count= True)
                return counts == 0
        return True

    def _check_unique_email(self, cr, uid, ids, context=None):
        for user in self.browse(cr, uid, ids):
            if user.email:
                counts = self.search(cr, uid, [('id', '!=', user.id), ('email', '=', user.email)], count= True)
                return counts == 0
        return True

    def _check_unique_login(self, cr, uid, ids, context=None):
        for user in self.browse(cr, uid, ids):
            counts = self.search(cr, uid, [('id', '!=', user.id), ('login', '=', user.login)], count= True)
            return counts == 0
        return True

    def _check_password_strength(self, cr, uid, ids, context=None):
        for user in self.browse(cr, uid, ids):
            if user.active and not re.search('[a-z]+', user.password):
                return False
            if user.active and not re.search('[A-Z]+', user.password):
                return False
            if user.active and not re.search('[0-9]+', user.password):
                return False
            if user.active and not re.search('[!@#\$%\^&\*]+', user.password):
                return False
            if user.active and len(user.password) < 8:
                return False
        return True

    def _check_groups(self, cr, uid, ids, context=None):
        patient_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'patient_group')
        doctor_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'doctor_group')
        for user in self.browse(cr, uid, ids):
            if user.id != SUPERUSER_ID and user.groups_id:
                has_patient_group = filter(lambda g: g.id == patient_group[1], user.groups_id)
                has_doctor_group = filter(lambda g: g.id == doctor_group[1], user.groups_id)
                if len(has_patient_group) and len(has_doctor_group):
                    return False
        return True

    def _check_groups_2(self, cr, uid, ids, context=None):
        patient_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'patient_group')
        doctor_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'oemedical', 'doctor_group')
        for user in self.browse(cr, uid, ids):
            if user.id != SUPERUSER_ID and user.groups_id:
                has_patient_group = filter(lambda g: g.id == patient_group[1], user.groups_id)
                has_doctor_group = filter(lambda g: g.id == doctor_group[1], user.groups_id)
                if not len(has_patient_group) and not len(has_doctor_group):
                    return False
        return True

    _constraints = [
        (_check_ced_ruc, 'El número de cédula, ruc o pasaporte esta incorrecto', ['ced_ruc']),
        (_check_first_name, 'El nombre esta incorrecto', ['first_name']),
        (_check_last_name, 'El primer apellido esta incorrecto', ['last_name']),
        (_check_slast_name, 'El segundo apellido esta incorrecto', ['slastname']),
        (_check_mobile_number, 'El número móvil esta incorrecto', ['mobile']),
        (_check_email, 'El correo electrónico esta incorrecto', ['email']),
        (_check_unique_ced_ruc, 'El número de cédula, ruc o pasaporte debe ser unico', ['ced_ruc']),
        (_check_unique_email, 'El correo electrónico debe ser unico', ['email']),
        (_check_unique_login, 'El login de usuario debe ser unico', ['email']),
        (_check_password_strength, 'La contraseña no cumple las políticas de seguridad:\n'
                                   '1-Debe contener al menos 1 letra en minúscula.\n'
                                   '2-Debe contener al menos 1 letra en mayúscula.\n'
                                   '3-Debe contener al menos 1 dígito.\n'
                                   '4-Debe contener al menos un caracter especial.\n'
                                   '5-Su longitud mínima debe ser de 8 caracteres.', ['password']),
        (_check_groups, 'El usuario no puede tener los roles de doctor y paciente a la misma vez.', ['groups_id']),
        (_check_groups_2, 'El usuario tiene que tener el rol de doctor o de paciente.', ['groups_id']),
    ]

res_users()

class res_partner(osv.Model):
    _inherit = 'res.partner'

    def _get_activation_link(self, cr, uid, ids, name, arg, context=None):
        res = {}.fromkeys(ids, '')
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
        for element in self.browse(cr, uid, ids, context=context):
            if element.signup_token:
                res[element.id] = urljoin(base_url, "/validate?db=%(db)s&token=%(token)s" % {
                    'db': cr.dbname,
                    'token': element.signup_token
                })
        return res

    def _get_password_reset_link(self, cr, uid, ids, name, arg, context=None):
        res = {}.fromkeys(ids, '')
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
        for element in self.browse(cr, uid, ids, context=context):
            if element.signup_token:
                res[element.id] = urljoin(base_url, "?db=%(db)s#token=%(token)s&type=reset" % {
                    'db': cr.dbname,
                    'token': element.signup_token
                })
        return res

    _columns = {
        'activation_link': fields.function(_get_activation_link, type='char', string='Activation Link'),
        'password_reset_link': fields.function(_get_password_reset_link, type='char', string='Password Reset Link'),
    }

    def signup_retrieve_info(self, cr, uid, token, context=None):
        partner = self._signup_retrieve_partner(cr, uid, token, raise_exception=True, context=None)
        res = {'db': cr.dbname}
        if partner.signup_valid:
            res['token'] = token
            res['name'] = partner.name
        if partner.user_ids:
            res['login'] = partner.user_ids[0].login
        elif partner.user_id:
            res['login'] = partner.user_id.login
        else:
            res['email'] = partner.email or ''
        return res

res_partner()