import json
import math
from pprint import pprint

from odoo import http
from odoo.http import request


class PartnerController(http.Controller):

    @http.route('/get/partners', auth="public", type='json', website=True, csrf=False)
    def get_partners(self, **args):

        partner_data = {}
        partners = request.env['res.company'].sudo().search(
            [("is_franchisor", "=", False)]
        )
        if partners:
            for partner in partners:
                community_count = http.request.env['community_module.community'].sudo().search_count([
                    ('is_active', '=', True),
                    ('create_uid.company_id.id', '=', partner.id),
                ])
                partner_data[str(partner.id)] = {
                    "id": str(partner.id),
                    "title": partner.display_name + ", " + (partner.state_id.code if partner.state_id else ''),
                    "icon": partner.state_id.code,
                    "count": community_count if community_count else 0,
                }

        return partner_data

    @http.route('/get/community', auth="public", type='json', website=True, csrf=False)
    def get_partner_community(self, community_id):
        community = request.env['community_module.community'].sudo().browse(int(community_id))
        if community:
            return {
                "id": str(community.id),
                "name": community.display_name
            }
        else:
            return {}

    @http.route('/get/company', auth="public", type='json', website=True, csrf=False)
    def get_partner_company(self, company_id):
        company = request.env['res.company'].sudo().browse(int(company_id))
        if company:
            return {
                "id": str(company.id),
                "name": company.display_name
            }
        else:
            return {}
