{
    'name': 'Franchisor Theme',
    'description': 'SB website franchisor theme',
    'category': 'Theme',
    'sequence': 11,
    'version': '1.0',
    'depends': ['base', 'website', 'theme_sb', 'bista_map_component'],
    'images': [
        'static/description/cover.png',
        'static/description/theme_default_screenshot.jpg',
    ],
    'data': [
        'views/header.xml',
        'views/footer.xml',
        'views/menu.xml',
        'views/homepage.xml',
        'views/schellter.xml',
        'views/division.xml',
        'views/community_plan.xml',
        'views/community_details.xml',
        'views/plan-detail.xml',
        'views/find_your_home.xml',
        'views/custom_contactus.xml',
        'views/gallery.xml',
        'views/about_us.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'franchisor_theme/static/css/style.scss',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
            'franchisor_theme/static/src/js/script.js',
            'franchisor_theme/static/src/components/*',
            'franchisor_theme/static/src/templates/*'
        ],
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
        ],
        'web.assets_qweb': [
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
        ],
    },
    'license': 'LGPL-3'
}
