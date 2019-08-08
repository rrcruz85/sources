# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from ast import literal_eval
import random
from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.addons.auth_signup.res_users import SignupError
from openerp.tools.translate import _
from urlparse import urljoin

def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.SystemRandom().choice(chars) for i in xrange(20))

def now(**kwargs):
    dt = datetime.now() + timedelta(**kwargs)
    return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

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
                    values['company_ids'] = [(6,0,[partner.company_id.id])]
                self._signup_create_user(cr, uid, values, context=context)
        else:
            # no token, sign up an external user
            if values.get('use_email_for_logging_in'):
                values['login'] = values.get('email')
            else:
                values['login'] = values.get('name')
            values.pop('use_email_for_logging_in')

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
        user_id = super(res_users, self).create(cr, uid, values, context=context)
        user = self.browse(cr, uid, user_id, context=context)

        if user.partner_id:
            country = self.pool.get('res.country').search(cr, uid, [('code', '=', 'EC')])
            state = self.pool.get('res.country.state').search(cr, uid, [('country_id', '=', country[0]), ('code', '=', 'PIC')])
            token = random_token()
            self.pool.get('res.partner').write(cr, uid, [user.partner_id.id], {
                'name': values['first_name'] + ' ' + values['last_name'] + ' ' + values['slastname'],
                'user_id': user_id,
                'country_id': country[0],
                'state_id': state[0],
                'city': 'Quito',
                'signup_token': token,
                'signup_type': 'signup',
                'signup_expiration': now(days=+1),
                'notification_email_send': 'none'
            }, context=None)

            self.pool.get('oemedical.patient').create(cr, uid, {
                'sex': values.get('sex'),
                'partner_id': user.partner_id.id,
                'dob':   datetime.strptime(values.get('birthdate'), '%d-%m-%Y')
            }, context=None)

            patient_group = self.pool.get('ir.model.data').get_object(cr, uid, 'oemedical', 'patient_group')
            portal_group = self.pool.get('ir.model.data').get_object(cr, uid, 'portal', 'group_portal')

            if patient_group:
                self.write(cr, uid, [user_id], {
                    'groups_id': [(4, patient_group.id)]
                }, context=context)
            if portal_group:
                self.write(cr, uid, [user_id], {
                    'groups_id': [(3, portal_group.id)]
                }, context=context)

            try:
                template = self.pool.get('ir.model.data').get_object(cr, uid, 'oemedical_auth_signup', 'activation_account_email')
                if not user.email:
                    raise osv.except_osv(_("Cannot send email: user has no email address."), user.name)
                mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, user.id, True, context=context)
                mail_obj = self.pool.get('mail.mail')
                mail_state = mail_obj.read(cr, uid, mail_id, ['state'], context=context)
                if mail_state and mail_state['state'] == 'exception':
                    raise osv.except_osv(_("Cannot send email: no outgoing email server configured.\nYou can configure it under Settings/General Settings."), user.name)
            except ValueError:
                pass

        if context and context.get('reset_password') and user.email:
            ctx = dict(context, create_user=True)
            self.action_reset_password(cr, uid, [user.id], context=ctx)
        return user_id

res_users()

class res_partner(osv.Model):
    _inherit = 'res.partner'

    def _get_activation_link(self, cr, uid, ids, name, arg, context=None):
        res = {}.fromkeys(ids, '')
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
        for element in self.browse(cr, uid, ids, context=context):
            if element.signup_token:
                res[element.id] = urljoin(base_url, "/validate?db=%(db)s&token=%(token)s" % {
                    'db' : cr.dbname,
                    'token' : element.signup_token
                })
        return res

    _columns = {
        'activation_link': fields.function(_get_activation_link, type='char', string='Activation Link'),
    }