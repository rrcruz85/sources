# -*- coding: utf-8 -*-

{

    'name': 'OeMedical. Patient Surgery Notifications',
    'description': """To include notifications to patient's surgeries""",
    'version': '1.0',

    'author': "OeMEdical Team",
    "website": "http://launchpad.net/oemedical",
    "licence": "AGPL v3",

    'category': 'Generic Modules/Others',
    'depends': ['oemedical_bariatric_evaluation'],

    "data": [
        # Views...
        'views/oemedical_patient_surgery_notification_view.xml',
    ],

    "demo": [

    ],

    'css': [
        'static/src/css/widget.css',
    ],

    'js': [
        'static/src/js/scripts.js',        
    ],

    'qweb': [
        'static/src/xml/templates.xml',
    ],

    'application': False,
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
