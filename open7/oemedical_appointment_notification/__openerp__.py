# -*- coding: utf-8 -*-

{

    'name': 'OeMedical. Appointment Notifications',
    'description': """To include notifications to patients...""",
    'version': '1.0',

    'author': "OeMEdical Team",
    "website": "http://launchpad.net/oemedical",
    "licence": "AGPL v3",

    'category': 'Generic Modules/Others',
    'depends': ['oemedical', 'web'],

    "data": [
        # Views...
        'views/oemedical_appointment_view_inherit.xml',

        # Wizards...
        'wizards/send_notification_wizard_view.xml',
        'data/scheduler.xml',
    ],

    "demo": [

    ],

    'css': [
        'static/src/css/widget.css',
    ],

    'js': [
        'static/src/js/scripts.js',
        'static/src/js/widget.js',
    ],

    'qweb': [
        'static/src/xml/templates.xml',
    ],

    'application': False,
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
