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
        # 'data/option_categories_data.xml',
        # 'data/option_classes_data.xml',

        'security/ir.model.access.csv',
        'security/security.xml',
        'views/home_plan.xml',
        'views/partners.xml',
        'views/users.xml',
        'views/categories_group.xml',
        'views/options_group.xml',
        'views/options.xml',
        'views/option_values.xml',
        'views/categories.xml',
        'views/option_classes.xml',
        'views/option_locations.xml',
        'views/option_categories.xml',
        'views/website_content.xml',
        # 'views/dashboard.xml',
        'views/franchise_homeplans.xml',
        'views/gallery.xml',
        'views/gallery_item.xml',
        'views/res_config_settings.xml',
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
