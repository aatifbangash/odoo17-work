# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bundled_bearer_token = fields.Char("Bundle Bearer Token", readonly=False,
                                       config_parameter='module_sb.bundled_bearer_token'
                                       )

    kova_api_token = fields.Char("KOVA API Token", readonly=False,
                                       config_parameter='module_sb.kova_api_token'
                                       )
