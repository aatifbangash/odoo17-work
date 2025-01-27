{
    'name': 'SB Theme 2',
    'description': 'SB website theme',
    'category': 'Theme',
    'sequence': 10,
    'version': '1.0',
    'depends': ['base','website','module_sb'],
    'images': [
        'static/description/cover.png',
        'static/description/theme_default_screenshot.jpg',
    ],
    'data': [
        'views/snippets/block_1.xml',
        'views/snippets/block_2.xml',
        'views/snippets/block_3.xml',
        'views/community.xml',
        'views/homepage.xml',
        'views/community_plan.xml',
        'views/snippets/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_sb/static/css/style.scss',
            'theme_sb/static/src/js/script.js',
            'theme_sb/static/src/js/front.js',
            'theme_sb/static/src/js/home_plans.js',
        ],
        'web.assets_backend': [
            'theme_sb/static/src/scss/theme_style_backend.scss',
        ]
    },
    'license': 'LGPL-3'
}
