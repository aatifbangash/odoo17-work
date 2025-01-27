# -*- coding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2021 (https://www.bistasolutions.com)
#
##############################################################################
{
    'name': 'Bista Lead Stages',
    'version': '17.0',
    'category': 'CRM',
    'license': 'LGPL-3',
    'summary': 'Bista Lead Stages',
    'description': '''Bista Lead Stages''',
    'author': 'Bista Solutions Pvt. Ltd',
    'maintainer': 'Bista Solutions Pvt. Ltd.',
    'website': 'http://www.bistasolutions.com',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_stage_visible.xml',
    ],
    'installable': True,
    'auto_install': False,
}
