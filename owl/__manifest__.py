# -*- coding: utf-8 -*-
{
    'name': 'Backend OWL',
    'version': '1.0',
    'summary': 'OWL Tutorial',
    'sequence': 100,
    'description': """OWL Backend""",
    'category': 'OWL',
    'depends': ['base', 'web', 'sale', 'community_module', 'module_sb'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml',
        'views/odoo_services.xml',
        'views/community.xml',
        'views/master_plan_options.xml',
        'views/home_plan.xml',
        'views/owl_plans.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl/static/css/style.css',
            'owl/static/src/components/*/*.js',
            'owl/static/src/components/*/*.xml',
            'owl/static/src/components/*/*.scss',
        ],
    },
    'license': 'LGPL-3'
}
