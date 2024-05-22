{
    'name': 'Community Module',
    'version': '1.0',
    'summary': 'Manage communities in Odoo',
    'description': 'A simple module to manage communities in Odoo backend.',
    'category': 'Tools',
    'license': 'LGPL-3',
    'author': 'Rizwan',
    'depends': ['base', 'sale', 'product', 'module_sb'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/heartbeat_groups.xml',
        'views/community.xml',
        'views/templates.xml',
        'views/community_home_plans.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}