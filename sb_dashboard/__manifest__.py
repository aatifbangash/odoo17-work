# -*- coding: utf-8 -*-
{
    'name': "Dashboard",
    'summary': "This is custom Dashboard",
    'description': """
This is custom Dashboard, that will display all kpis.
    """,
    'author': "NMX",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'product', 'community_module', 'owl'],
    'data': [
        'views/sb_dashboard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sb_dashboard/static/src/components/**/*.js',
            'sb_dashboard/static/src/components/**/*.xml',
            # 'sb_dashboard/static/src/components/**/*.scss',
        ],
    },
    'installable': True,
    'application': True,
}
