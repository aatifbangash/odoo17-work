# -*- coding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2021 (https://www.bistasolutions.com)
#
##############################################################################
{
    'name': 'Bista Web Form',
    'version': '17.0',
    'category': 'misc',
    'license': 'LGPL-3',
    'description': '''Dynamic Contact Forms''',
    'author': 'Omid Totakhel',
    'maintainer': 'Bista Solutions Pvt. Ltd.',
    'website': 'http://www.bistasolutions.com',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/web_form.xml',
        'views/contact_form.xml',
    ],
    'assets': {
        'web.assets_backend': [],
        'web.assets_frontend': [
            'bista_web_form/static/src/**/*',
        ],

    },
    'installable': True,
    'auto_install': False,
}
