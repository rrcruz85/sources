# -*- coding: utf-8 -*-
{

    'name': 'Odontological Exams',
    'version': '1.0',
    'author': "Easys Dev Solutions",
    'category': 'Generic Modules/Others',
    'depends': ['oemedical'],
    'application': True,
    'description': """
Allows to manage odontological exams for patients
""",
    "website": "https://www.easysdev.com",
    "licence": "AGPL v3",
    "data": [
        'odontology_exam_view.xml',
        'odontology_exam_menu.xml',
        'report/odontogram.xml',
    ],
    "demo": [
    ],
    'test':[
    ],
    'css': [        
        'static/src/css/odontogram.css',
    ],
    'js': [
        'static/src/js/lib/jspdf.debug.js',
        'static/src/js/view_form.js',
        'static/src/js/boot.js',        
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
