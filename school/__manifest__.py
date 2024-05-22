# -*- coding: utf-8 -*-
{
    'name': 'school',
    'version': '1.0',
    'summary': 'Example school module for Odoo',
    'sequence': 100,
    'description': """School""",
    'category': 'Custom',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/school.xml',
        'views/student.xml',
        'wizard/school_wizard.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    # 'assets': {
    #     'web.assets_backend': [
    #         'owl/static/css/style.css',
    #         'owl/static/src/components/*/*.js',
    #         'owl/static/src/components/*/*.xml',
    #         'owl/static/src/components/*/*.scss',
    #     ],
    # },
    'license': 'LGPL-3'
}
