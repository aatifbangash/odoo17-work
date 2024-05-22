# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(Http, self).session_info()

        res['session_testing_item'] = True  # self.env.user.odoobot_state not in [False, 'not_initialized']
        res['is_franchisor'] = self.env.user.is_franchisor
        return res
