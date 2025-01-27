import json
from pprint import pprint

from odoo import http
from odoo.http import request


class CommunityOptionsController(http.Controller):
    @http.route("/community/home_plan/options", methods=["POST"], type="http", auth="public", csrf=False,
                save_session=False,
                cors="*")
    def community_home_plan_options_store(self):
        request_body = json.loads(request.httprequest.data)
        if not request_body:
            return request.make_json_response({'data': 'Not found'}, status=404)

        for option in request_body:
            home_plan_option = request.env['community_module.community_homeplans_options'].sudo().search([
                ('community_homeplan_id', '=', option['community_homeplan_id']),
                ('homeplan_option_id', '=', option['homeplan_option_id']),
            ])

            if not home_plan_option:
                request.env['community_module.community_homeplans_options'].sudo().create({
                    'community_homeplan_id': option['community_homeplan_id'],
                    'homeplan_option_id': option['homeplan_option_id'],
                    'is_active': option['is_active'],
                    # 'is_base': option['is_base'],
                })
            else:
                home_plan_option.sudo().write({
                    'is_active': option['is_active']
                })

        return request.make_json_response({'data': "Success"}, status=200)

    @http.route("/community/home_plan/<int:community_homeplan_id>/options", methods=["GET"], type="http", auth="public")
    def community_home_plan_options_by_id(self, community_homeplan_id):
        community_home_plan_options = request.env['community_module.community_homeplans_options'].sudo().search([
            ('community_homeplan_id', '=', community_homeplan_id)
        ])

        if not community_home_plan_options:
            return request.make_json_response({'data': 'Not found'}, status=404)

        response = [{
            'community_homeplan_id': option.community_homeplan_id.id,
            'homeplan_option_id': option.homeplan_option_id.id,
            'is_active': option.is_active,
            'is_base': option.is_base
        }
            for option in community_home_plan_options]
        return request.make_json_response({'data': response}, status=200)

    @http.route("/community/home_plan/option_value_set_base", methods=["POST"], type="http", auth="public", csrf=False,
                save_session=False,
                cors="*")
    def community_home_plan_option_value_set_base(self):
        request_body = json.loads(request.httprequest.data)
        if not request_body:
            return request.make_json_response({'data': 'Not found'}, status=404)

        company_id = request_body.get('company_id') or request.env.company.id
        community_homeplan_option = request.env['community_module.community_homeplans_options'].sudo().search([
            ('community_homeplan_id', '=', request_body['community_homeplan_id']),
            ('homeplan_option_id', '=', request_body['homeplan_option_id'])
        ], limit=1)

        if community_homeplan_option:
            community_homeplan_option.write({
                'is_base': True,
                'is_active': True
            })

            sibling_master_plan_records = request.env['module_sb.master_plan_options'].sudo().search([
                ('id', '!=', community_homeplan_option.homeplan_option_id.master_plan_options_id.id),
                ('options_id', '=', community_homeplan_option.homeplan_option_id.master_plan_options_id.options_id.id),
                ('homeplan_id', '=', community_homeplan_option.homeplan_option_id.master_plan_options_id.homeplan_id.id)
            ])
            if sibling_master_plan_records:
                sibling_home_plan_records = request.env['module_sb.home_plan_options'].sudo().search([
                    ('master_plan_options_id', 'in', sibling_master_plan_records.ids),
                    ('homeplan_id', '=',
                     community_homeplan_option.homeplan_option_id.master_plan_options_id.homeplan_id.id),
                    ('company_id', '=', company_id),
                ])
                if sibling_home_plan_records:
                    sibling_records = request.env['community_module.community_homeplans_options'].sudo().search([
                        ('homeplan_option_id', 'in', sibling_home_plan_records.ids),
                        ('community_homeplan_id', '=', request_body['community_homeplan_id'])
                    ])

                    if sibling_records:
                        sibling_records.write({
                            'is_base': False
                        })

            return request.make_json_response({'data': "Record updated"}, status=200)
