{
    'name': "module_sb",
    'summary': "Custom module for Odoo customization",
    'description': """
Custom module for Odoo customization
    """,
    'author': "Schellbrothers",
    'website': "https://www.schellbrothers.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'sequence': 20,
    'depends': ['base', 'product', 'sale'],
    'data': [
        'data/option_categories_data.xml',
        'data/option_classes_data.xml',

        'security/ir.model.access.csv',
        'security/security.xml',
        'views/home_plan.xml',
        'views/partners.xml',
        'views/users.xml',
        'views/categories_group.xml',
        'views/options_group.xml',
        'views/options/options.xml',
        'views/options/option_values.xml',
        'views/categories.xml',
        'views/options/option_classes.xml',
        'views/options/option_locations.xml',
        'views/options/option_categories.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'module_sb/static/src/scss/theme_style_backend.scss',
        ]
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
