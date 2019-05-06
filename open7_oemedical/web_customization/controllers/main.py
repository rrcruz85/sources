# -*- coding: utf-8 -*-
import logging
import simplejson
import os
import openerp
#import openerp.addons.web.http as openerpweb
#import openerp.addons.web.controllers.main as webmain
#import urllib
#from openerp.addons.web.controllers.main import manifest_list, module_boot, html_template, db_monodb_redirect, redirect_with_hash

openerp.addons.web.controllers.main.html_template = """<!DOCTYPE html>
<html style="height: 100%%">
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>Kubamed</title>
        <link rel="shortcut icon" href="/web_customization/static/src/img/favicon/tooth.ico" type="image/x-icon"/>
        <link rel="stylesheet" href="/web/static/src/css/full.css" />
        %(css)s
        %(js)s
        <script type="text/javascript">
            $(function() {
                var s = new openerp.init(%(modules)s);
                %(init)s
            });
        </script>
    </head>
    <body>
        <!--[if lte IE 8]>
        <script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>
        <script>CFInstall.check({mode: "overlay"});</script>
        <![endif]-->
    </body>
</html>
"""

'''
class WebCustomizationController(#.Controller):    
   
    @openerpweb.httprequest
    def index(self, req, s_action=None, db=None, **kw):
        
        db, redir = db_monodb_redirect(req)
        if redir:
            return redirect_with_hash(req, redir)

        js = "\n        ".join('<script type="text/javascript" src="%s"></script>' % i for i in manifest_list(req, 'js', db=db))
        css = "\n        ".join('<link rel="stylesheet" href="%s">' % i for i in manifest_list(req, 'css', db=db))

        r = html_template % {
            'js': js,
            'css': css,
            'modules': simplejson.dumps(module_boot(req, db=db)),
            'init': 'var wc = new s.web.WebClient();wc.appendTo($(document.body));'
        }
        return r
'''

