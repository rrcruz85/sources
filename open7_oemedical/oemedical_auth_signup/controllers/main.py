# -*- coding: utf-8 -*-
import simplejson
import urllib
import openerp
import openerp.addons.web.http as openerpweb
import openerp.addons.web.controllers.main as webmain
import re
from openerp.modules.registry import RegistryManager
from datetime import datetime
from openerp.tools.translate import _

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
    # http://hostname:8069/validate?db=kbamed&token=2UqutM23KC8CNWgXF7BA
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

        if not errmsg:
            registry = RegistryManager.get(db)
            with registry.cursor() as cr:
                res_partner = registry.get('res.partner')
                partnerId = res_partner.search(cr, openerp.SUPERUSER_ID,[('signup_token', '=', token)])
                if not partnerId:
                    errmsg = _('Invalid Activation Link')
                else:
                    partner = res_partner.browse(cr, openerp.SUPERUSER_ID, partnerId[0])
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
                'company_name': 'Kubamed',
                'db': db,
                'error': errmsg
            }
        else:
            template = success_html % {
                'company_name': 'Kubamed',
                'db': db,
                'index_url': 'http://localhost:8069?db=kbamed',
                'message': _('User Account Successfully Activated. In order to access our portal you have to go to login screen.'),
                'link_message' : _('Back to Login Screen')
            }
        return template

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
