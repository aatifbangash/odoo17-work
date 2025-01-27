# -*- coding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2021 (https://www.bistasolutions.com)
#
##############################################################################
{
    'name': 'NMX Map',
    'version': '17.0',
    'category': 'CRM',
    'license': 'LGPL-3',
    'description': '''Bista Google Map Component Inherited''',
    'author': 'NMX',
    'maintainer': 'Numetrics',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'community_module', 'bista_map_component'],
    'data': [
        'security/ir.model.access.csv',
        'views/community_inherited.xml',
        'views/map_items_inherited.xml',
        'views/map_lots.xml',
        'views/partner_inherited.xml',
        'views/section_wizard.xml'
    ],
    'assets': {
        'web.assets_backend': [

        ],
        'web.assets_frontend': [

        ],

    },
    'installable': True,
    'auto_install': False,
}
