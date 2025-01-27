# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licens

import json
import logging

from odoo import http
from odoo.http import request

logger = logging.getLogger(__name__)


class WebFormController(http.Controller):

    @http.route('/web/contact_form', website=True, type='http', auth='public', csrf=True)
    def render_web_configurator(self):
        return request.render('bista_web_form.contact_form')

    @http.route('/web/form/options', auth="public", type='json', website=True, csrf=False)
    def get_options(self, source):
        data = {}
        return json.dumps(data)

    @http.route('/web/get_form_data', website=True, type='json', auth='public', csrf=False)
    def get_form_data(self, **kwargs):
        if not kwargs:
            return []
        return request.env['bista.web.form'].sudo().get_form_data(kwargs.get('ref'))

    @http.route('/web/set_form_data', website=True, type='json', auth='public', csrf=False)
    def set_form_data(self, **kwargs):
        form_ref = kwargs.get('ref')
        data = kwargs.get('data')
        form_id = request.env['bista.web.form'].sudo().search([('code', '=', form_ref)], limit=1)
        if not form_id:
            return {"error": "Form Not found"}
        return request.env[form_id.model_id.model].sudo().create(data)
