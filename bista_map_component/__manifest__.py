# -*- coding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2021 (https://www.bistasolutions.com)
#
##############################################################################
{
    'name': 'Bista Interactive Google Map',
    'version': '17.0',
    'category': 'CRM',
    'license': 'LGPL-3',
    'description': '''Interactive Google Map Component''',
    'author': 'Omid Totakhel',
    'maintainer': 'Bista Solutions Pvt. Ltd.',
    'website': 'http://www.bistasolutions.com',
    'depends': ['base', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/map.xml',
        'views/map_items.xml',
        'views/map_item_status.xml',
        'views/res_config_settings.xml',
        'views/map_playground.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [

        ],
        'web.assets_frontend': [
            'https://unpkg.com/@googlemaps/js-api-loader@1.x/dist/index.min.js',
            'bista_map_component/static/lib/*.js',
            'bista_map_component/static/src/scss/*.scss',
            'bista_map_component/static/src/**/*',
            'bista_map_component/static/src/components/*',
            'bista_map_component/static/src/template/*'
        ],

    },
    'external_dependencies': {
        'python': ['fastkml'],
    },
    'installable': True,
    'auto_install': False,
}
