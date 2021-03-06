# -*- coding: utf-8 -*-
import openerp
import openerp.addons.web.http as openerpweb
import openerp.addons.web.controllers.main as webmain
import re
from openerp.modules.registry import RegistryManager
from datetime import datetime
from openerp.tools.translate import _
from urlparse import urljoin
import operator
import logging

_logger = logging.getLogger(__name__)

error_html = """
<!DOCTYPE html>
<html style="height: 100%%">
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>%(company_name)s</title>
        <link rel="shortcut icon" href="/web_customization/static/src/img/favicon/tooth.ico" type="image/x-icon"/>
        <link rel="stylesheet" href="/web/static/src/css/full.css" />
        <link rel="stylesheet" href="/web/webclient/css?db=%(db)s">
        <script type="text/javascript" src="/web/webclient/js?db=%(db)s"></script>
    </head>
    <body>
        <!--[if lte IE 8]>
        <script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>
        <script>CFInstall.check({mode: "overlay"});</script>
        <![endif]-->
        
        <div class="openerp openerp_webclient_container">
            <table class="oe_webclient">
                <tbody>
                    <tr>
                        <td class="oe_application">
				            <div>
                                <div class="oe_login">
                                    <div class="oe_login_bottom"></div>  
                                    <div style="top: 10px" class="oe_login_logo">
                                        <img src="/web/static/src/img/logo2.png">
                                    </div>                                  
                                    <div style="display: inline-block;margin-top:80px" class="oe_login_error_message">
                                        <span>%(error)s</span>
                                    </div>                                     
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>		
    </body>
</html>
"""

success_html = """
<!DOCTYPE html>
<html style="height: 100%%">
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>%(company_name)s</title>
        <link rel="shortcut icon" href="/web_customization/static/src/img/favicon/tooth.ico" type="image/x-icon"/>
        <link rel="stylesheet" href="/web/static/src/css/full.css" />
        <link rel="stylesheet" href="/web/webclient/css?db=%(db)s">
        <script type="text/javascript" src="/web/webclient/js?db=%(db)s"></script>
    </head>
    <body>
        <!--[if lte IE 8]>
        <script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>
        <script>CFInstall.check({mode: "overlay"});</script>
        <![endif]-->

        <div class="openerp openerp_webclient_container">
            <table class="oe_webclient">
                <tbody>
                    <tr>
                        <td class="oe_application">
				            <div>
                                <div class="oe_login">
                                    <div class="oe_login_bottom"></div>  
                                    <div style="top: 10px" class="oe_login_logo">
                                        <img src="/web/static/src/img/logo2.png">
                                    </div>                                  
                                    <div style="display: inline-block; margin-top:80px; background-color:darkgreen" class="oe_login_error_message">
                                        <span>%(message)s</span>
                                    </div>
                                    <br><br>
                                    <div style="display: inline-block;">                                        
                                        <a style="font-size: 16px; font-weight: bold;" href="%(index_url)s">%(link_message)s</a>
                                    </div>                                       
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>		
    </body>
</html>
"""

class ValidateToken(openerpweb.Controller):
    # http://hostname:8069/validate?db=kbamed&token=12345
    _cp_path = "/validate"

    @openerpweb.httprequest
    def index(self, req, db, token):
        errmsg = ''
        db_list = webmain.db_list(req)
        if not db:
            errmsg = _('No database provided')
        elif db not in db_list:
            errmsg = _('Invalid database name')
        elif not token:
            errmsg = _('No token provided')
        elif len(token) != 20:
            errmsg = _('Invalid token')
        elif not re.match(r'^[a-zA-Z0-9]+$', token):
            errmsg = _('Invalid token format')

        base_url = ''
        company_name = ''
        if not errmsg:
            registry = RegistryManager.get(db)
            with registry.cursor() as cr:
                base_url = registry.get('ir.config_parameter').get_param(cr, openerp.SUPERUSER_ID, 'web.base.url')
                res_partner = registry.get('res.partner')
                partnerId = res_partner.search(cr, openerp.SUPERUSER_ID, [('signup_token', '=', token)])
                if not partnerId:
                    errmsg = _('Invalid Activation Link')
                else:
                    partner = res_partner.browse(cr, openerp.SUPERUSER_ID, partnerId[0])
                    company_name = partner.company_id.name
                    if not partner.signup_expiration or datetime.strptime(partner.signup_expiration, '%Y-%m-%d %H:%M:%S') <= datetime.now():
                        errmsg = _('Activation Link Expired. You have to request a new one by clicking reset password option on login screen.')
                    else:
                        res_partner.write(cr, openerp.SUPERUSER_ID, partnerId, {
                            'signup_type': False,
                            'signup_expiration': False,
                            'signup_token': False
                        })

                        if partner.user_id:
                            registry.get('res.users').write(cr, openerp.SUPERUSER_ID, [partner.user_id.id], {
                                'active': True
                            })

        if errmsg:
            template = error_html % {
                'company_name': company_name,
                'db': db,
                'error': errmsg
            }
        else:
            base_url = urljoin(base_url, "?db=%(db)s" % {'db': db})
            template = success_html % {
                'company_name': company_name,
                'db': db,
                'index_url': base_url,
                'message': _('User Account Successfully Activated. In order to access our portal you have to go to login screen.'),
                'link_message': _('Back to Login Screen')
            }
        return template

class OemedicalSession(webmain.Session):

    @openerpweb.jsonrequest
    def set_password(self, req, fields):

        if not fields:
            return {'error': _('Invalid url, no params provided')}

        if 'dbname' not in fields or not fields['dbname']:
            return {'error': _('Invalid url, db param not found')}
        else:
            db_list = webmain.db_list(req)
            if fields['dbname'] not in db_list:
                return {'error': _('Invalid database name')}

        if 'token' not in fields or not fields['token']:
            return {'error': _('Invalid url, token param not found')}
        elif len(fields['token']) != 20:
            return {'error': _('Invalid url, token param is incorrect')}
        elif not re.match(r'^[a-zA-Z0-9]+$', fields['token']):
            return {'error': _('Invalid url, token format is incorrect')}

        if 'password' not in fields or not fields['password']:
            return {'error': _('Invalid url, password param not found')}

        registry = RegistryManager.get(fields['dbname'])
        with registry.cursor() as cr:
            base_url = registry.get('ir.config_parameter').get_param(cr, openerp.SUPERUSER_ID, 'web.base.url')
            res_partner = registry.get('res.partner')
            partner_id = res_partner.search(cr, openerp.SUPERUSER_ID, [('signup_token', '=', fields.get('token'))])
            if not partner_id:
                return {'error': _('Invalid Reset Password Link')}
            else:
                partner = res_partner.browse(cr, openerp.SUPERUSER_ID, partner_id[0])

                if partner.name != fields['name']:
                    return {'error': _('Incorrect UserName')}

                if partner.user_id.login != fields['login']:
                    return {'error': _('Incorrect Login Name')}

                if not partner.signup_expiration or datetime.strptime(partner.signup_expiration, '%Y-%m-%d %H:%M:%S') <= datetime.now():
                    return {'error': _('Reset Password Link Expired. You have to request a new one by clicking reset password option on login screen.')}
                else:
                    res_partner.write(cr, openerp.SUPERUSER_ID, partner_id, {
                        'signup_type': False,
                        'signup_expiration': False,
                        'signup_token': False
                    })

                    if partner.user_id:
                        registry.get('res.users').write(cr, openerp.SUPERUSER_ID, [partner.user_id.id], {
                            'active': True,
                            'password': fields['password']
                        })

                    return {'error': False, 'base_url': urljoin(base_url, "?db=%(db)s" % {'db': fields['dbname']})}

    @openerpweb.jsonrequest
    def change_password(self, req, fields):
        old_password, new_password, confirm_password = operator.itemgetter('old_pwd', 'new_password', 'confirm_pwd')(
            dict(map(operator.itemgetter('name', 'value'), fields)))
        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            return {'error': _('You cannot leave any password empty.'), 'title': _('Change Password')}
        if new_password != confirm_password:
            return {'error': _('The new password and its confirmation must be identical.'),
                    'title': _('Change Password')}
        if old_password.strip() == new_password.strip():
            return {'error': _('The new password can not be the same of the old password.'),
                    'title': _('Change Password')}
        if new_password.strip().find(old_password.strip()) != -1:
            return {'error': _('The new password can not be contained in the old password.'),
                    'title': _('Change Password')}
        if old_password.strip().find(new_password.strip()) != -1:
            return {'error': _('The new password can not contains the old password.'),
                    'title': _('Change Password')}
        try:
            if req.session.model('res.users').change_password(
                    old_password, new_password):
                return {'new_password': new_password}
        except Exception as e:
            msg = e.faultCode[e.faultCode.find(':')+2:]
            msg = msg.replace('\n', '<br/>')
            return {'error': _(msg),
                    'title': _('Change Password')}
        return {'error': _('Error, password not changed !'), 'title': _('Change Password')}

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
