from pprint import pprint

from odoo import http
from odoo.http import request


class OptionsController(http.Controller):

    @http.route("/options", methods=["GET"], type="http", auth="public")
    def options(self):

        query_params = request.httprequest.args
        domain = []
        homeplan_id = query_params.get('homeplan_id')
        if homeplan_id:
            added_options_ids = request.env['module_sb.master_plan_options'].sudo().search(
                [('homeplan_id', '=', int(homeplan_id))]).mapped('options_id').ids
            domain.append(('id', 'not in', added_options_ids))

        options = request.env['module_sb.options'].search_read(domain, ['name', 'enabled', 'option_categories_id',
                                                                        'option_classes_id', 'option_type', 'price_type',
                                                                        'units'])
        if not options:
            return request.make_json_response([], status=200)

        return request.make_json_response(options)

    @http.route("/option_values", methods=["GET"], type="http", auth="public")
    def option_values(self):
        option_values = request.env['module_sb.option_values'].search_read([],
                                                                           ['name', 'enabled', 'option_categories_id',
                                                                            'option_classes_id', 'price_type', 'units'])
        if not option_values:
            return request.make_json_response({'data': 'Not found'}, status=404)

        return request.make_json_response(option_values)

    @http.route("/option_values/categories/<int:category_id>", methods=["GET"], type="http", auth="public")
    def option_values_by_category_id(self, category_id):
        option_values = request.env['module_sb.option_values'].search_read([('option_categories_id', '=', category_id)],
                                                                           ['name', 'enabled', 'option_categories_id',
                                                                            'option_classes_id', 'price_type', 'units'])
        if not option_values:
            return request.make_json_response({'data': 'Not found'}, status=404)

        return request.make_json_response(option_values)

    @http.route("/option_values/categories/<int:category_id>/classes/<int:class_id>", methods=["GET"], type="http",
                auth="public")
    def option_values_by_category_and_class_id(self, category_id, class_id):
        option_values = request.env['module_sb.option_values'].search_read([
            ('option_classes_id', '=', class_id),
            ('option_categories_id', '=', category_id)
        ],
            ['name', 'enabled', 'option_categories_id', 'option_classes_id']
        )
        if not option_values:
            return request.make_json_response({'data': 'Not found'}, status=404)

        return request.make_json_response(option_values)

    @http.route("/option_categories", methods=["GET"], type="http", auth="public")
    def option_categories(self):
        option_categories = request.env['module_sb.option_categories'].search_read([], ['id', 'name', 'display_name'])
        if not option_categories:
            return request.make_json_response({'data': 'Not found'}, status=404)

        return request.make_json_response(option_categories)

    @http.route("/option_classes", methods=["GET"], type="http", auth="public")
    def option_classes(self):
        option_classes = request.env['module_sb.option_classes'].search_read([], ['id', 'name', 'display_name'])
        if not option_classes:
            return request.make_json_response({'data': 'Not found'}, status=404)

        return request.make_json_response(option_classes)

    @http.route("/option_locations", methods=["GET"], type="http", auth="public")
    def option_locations(self):
        option_locations = request.env['module_sb.option_locations'].search_read([], ['id', 'name', 'display_name'])
        if not option_locations:
            return request.make_json_response({'data': 'Not found'}, status=404)

        return request.make_json_response(option_locations)
