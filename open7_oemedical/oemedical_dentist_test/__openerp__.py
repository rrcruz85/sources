# -*- coding: utf-8 -*-
{

    'name': 'Examen Odontológico',
    'version': '1.0',
    'author': "OeMEdical Team",
    'category': 'Generic Modules/Others',
    'depends': ['oemedical'],
    'application': True,
    'description': """
Permite gestionar exámenes odontológicos para los pacientes
""",
    "website": "http://launchpad.net/oemedical",
    "licence": "AGPL v3",
    "data": [
        'oemedical_dentist_test_view.xml',
        'oemedical_dentist_test_menu.xml',
        'report/oemedical_dentist_test.xml',
    ],
    "demo": [
    ],
    'test':[
    ],
    'css': [
        'static/src/css/styles.css',
        'static/src/css/odontograma.css',
    ],
    'js': [
        'static/src/js/lib/jspdf.debug.js',
        'static/src/js/view_form.js',
        'static/src/js/boot.js',        
    ],
    'qweb': [
        'static/src/xml/base.xml',
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
