import json
import math
from pprint import pprint

from odoo import http
from odoo.http import request


class HomePlansController(http.Controller):

    @http.route("/home_plan/options", methods=["POST"], type="http", auth="public", csrf=False, save_session=False,
                cors="*")
    def home_plan_options_store(self):
        options = json.loads(request.httprequest.data)
        if not options:
            return request.make_json_response({'data': 'Not found'}, status=404)

        for option in options:
            home_plan_option = request.env['module_sb.home_plan_options'].sudo().search([
                ('homeplan_id', '=', option['homeplan_id']),
                ('master_plan_options_id', '=', option['master_plan_option_id']),
                ('company_id', '=', request.env.company.id),
            ])

            if not home_plan_option:
                request.env['module_sb.home_plan_options'].sudo().create({
                    'homeplan_id': option['homeplan_id'],
                    'master_plan_options_id': option['master_plan_option_id'],
                    'company_id': request.env.company.id,
                    'is_active': option['is_active'],
                    # 'is_base': option['is_base']
                })
            else:
                home_plan_option.write({
                    'is_active': option['is_active']
                })

        return request.make_json_response({'data': "Success"}, status=200)

    @http.route("/home_plan/<int:homeplan_id>/options", methods=["GET"], type="http", auth="public")
    def home_plan_options_by_id(self, homeplan_id):
        home_plan_options = request.env['module_sb.home_plan_options'].sudo().search([
            ('homeplan_id', '=', homeplan_id),
            ('company_id', '=', request.env.company.id)
        ])

        if not home_plan_options:
            return request.make_json_response({'data': 'Not found'}, status=404)

        response = [{
            'homeplan_id': option.homeplan_id.id,
            'master_plan_option_id': option.master_plan_options_id.id,
            'is_active': option.is_active,
            # 'is_base': option.is_base
        }
            for option in home_plan_options]
        return request.make_json_response({'data': response}, status=200)

    @http.route(['/home_plans'], type='json', auth="public", website=True)
    def home_plans(self, limit=4):
        response = []
        # print(request.website)
        # print(request.env.user)
        home_plans = request.env['product.template'].search([])
        for home_plan in home_plans:
            data = {
                "id": home_plan.id,
                "name": home_plan.name,
                "legal_name": home_plan.legal_name,
                "default_code": home_plan.default_code,
                "status": home_plan.active,
                # "image": home_plan.image_1920,
            }
            response.append(data)

        return response

    @http.route(["/home_plan_active/<int:homeplan_id>/options/<int:community_homeplan_id>",
                 "/home_plan_active/<int:homeplan_id>/options"], methods=["GET"], type="http", auth="public")
    def home_plan_active_options_by_id(self, homeplan_id, community_homeplan_id=None):

        query_params = request.httprequest.args
        status = query_params.get('status', None)
        search_term = query_params.get('search_term', False)
        page_no = int(query_params.get('page_no', 1))  # Default to page 1 if not provided
        page_size = int(query_params.get('page_size', 10))

        company_id = request.env.company.id
        if query_params.get('company_id'):
            company_id = int(query_params.get('company_id'))

        domain = [
            ('homeplan_id', '=', homeplan_id),
            ('company_id', '=', company_id),
            ('is_active', '=', True)
        ]

        optional_filters = {
            'category_id': 'master_plan_options_id.options_id.option_categories_id',
            'class_id': 'master_plan_options_id.options_id.option_classes_id',
            'location_id': 'master_plan_options_id.options_id.option_locations_id'
        }

        for param, field in optional_filters.items():
            param_value = query_params.get(param)
            if param_value:
                domain.append((field, '=', int(param_value)))

        if status in ['active', 'inactive']:
            active_options_ids = (request.env['community_module.community_homeplans_options']
            .sudo().search([
                ('community_homeplan_id', '=', community_homeplan_id),
                ('is_active', '=', True)
            ])).mapped('homeplan_option_id.master_plan_options_id.options_id').ids

            domain_operator = 'in' if status == 'active' else 'not in'
            domain.append(('options_id', domain_operator, active_options_ids))

        if search_term:
            records = request.env['module_sb.home_plan_options'].sudo().search(domain)
            unique_option_ids = self._get_matching_option_ids(records, search_term, company_id, community_homeplan_id)

        else:
            unique_option_ids = request.env['module_sb.home_plan_options'].sudo().search(domain).exists().mapped(
                'master_plan_options_id.options_id').ids

        total_records = len(unique_option_ids)
        offset = (page_no - 1) * page_size
        paginated_option_ids = unique_option_ids[offset:offset + page_size]

        domain.append(('master_plan_options_id.options_id', 'in', paginated_option_ids))

        home_plan_active_options = request.env['module_sb.home_plan_options'].sudo().search(domain)

        if not home_plan_active_options:
            return request.make_json_response({'data': 'Not found'}, status=404)

        pagination_response = {
            'page_no': page_no,
            'page_size': page_size,
            'total_records': total_records,
            'total_pages': math.ceil(total_records / page_size)
        }
        final_response = []
        for home_plan_option in home_plan_active_options:
            if not any(fr['option_id'] == home_plan_option.master_plan_options_id.options_id.id for fr in
                       final_response):  # Ignore if option already exists

                name = home_plan_option.master_plan_options_id.options_id.name
                inherited_name = False
                is_override = False
                override_community_home_plan_record_exists = home_plan_option.community_homeplan_option_override_ids.filtered(
                    lambda r: r.community_homeplan_id.id == community_homeplan_id and r.type == 'option'
                )


                override_home_plan_record_exists = home_plan_option.computed_homeplan_option_override

                price = override_community_home_plan_record_exists.price if override_community_home_plan_record_exists and override_community_home_plan_record_exists.price else 0.0
                if not price and override_home_plan_record_exists and override_home_plan_record_exists.price:
                    price = override_home_plan_record_exists.price
                # op = home_plan_option.options_id
                # r = (request.env['module_sb.home_plan_options_override']
                #      .sudo().search([('options_id', '=', op.id)]))
                # pprint(r)

                if override_community_home_plan_record_exists and override_community_home_plan_record_exists.name:
                    name = override_community_home_plan_record_exists.name
                    is_override = True
                    if override_home_plan_record_exists and override_home_plan_record_exists.name:
                        inherited_name = override_home_plan_record_exists.name
                    else:
                        override_master_plan_record_exists = home_plan_option.master_plan_options_id.option_override_id
                        if override_master_plan_record_exists and override_master_plan_record_exists.name:
                            inherited_name = override_master_plan_record_exists.name
                        else:
                            inherited_name = home_plan_option.master_plan_options_id.options_id.name
                else:
                    override_master_plan_record_exists = home_plan_option.master_plan_options_id.option_override_id
                    if override_home_plan_record_exists and override_home_plan_record_exists.name:  # name from home plan override
                        name = override_home_plan_record_exists.name
                        if override_master_plan_record_exists and override_master_plan_record_exists.name:
                            inherited_name = override_master_plan_record_exists.name
                        else:
                            inherited_name = home_plan_option.master_plan_options_id.options_id.name
                    elif override_master_plan_record_exists and override_master_plan_record_exists.name:  # name from master plan override
                        name = override_master_plan_record_exists.name
                        inherited_name = home_plan_option.master_plan_options_id.options_id.name

                final_response.append({
                    "id": home_plan_option.id,
                    "option_id": home_plan_option.master_plan_options_id.options_id.id,
                    "option_type": home_plan_option.options_id.option_type,
                    "homeplan_id": homeplan_id,
                    "name": name,
                    "inherited_name": inherited_name,
                    "price": price,
                    "is_active": False,
                    "is_title": home_plan_option.master_plan_options_id.is_title,
                    "is_override": is_override,
                    "price_type": home_plan_option.master_plan_options_id.options_id.price_type,
                    "option_type": home_plan_option.master_plan_options_id.options_id.option_type,
                    "units": home_plan_option.master_plan_options_id.options_id.units,
                    "option_categories_id": [
                        home_plan_option.master_plan_options_id.options_id.option_categories_id.id,
                        home_plan_option.master_plan_options_id.options_id.option_categories_id.name
                    ],
                    "option_classes_id": [
                        home_plan_option.master_plan_options_id.options_id.option_classes_id.id,
                        home_plan_option.master_plan_options_id.options_id.option_classes_id.name
                    ],
                    "option_locations_id": [
                        home_plan_option.master_plan_options_id.options_id.option_locations_id.id,
                        home_plan_option.master_plan_options_id.options_id.option_locations_id.name
                    ],
                    'option_values': []
                }, )

        for home_plan_option_values in home_plan_active_options:
            target_index = next((index for index, fr in enumerate(final_response) if
                                 fr['option_id'] == home_plan_option_values.master_plan_options_id.options_id.id), -1)
            if target_index == -1:
                continue

            name = home_plan_option_values.master_plan_options_id.option_values_id.name  # default
            inherited_name = False
            description = None
            price = 0.0
            is_override = False
            is_base = home_plan_option_values.master_plan_options_id.is_base
            overrite_community_home_plan_record_exists = home_plan_option_values.community_homeplan_option_override_ids.filtered(
                lambda r: r.community_homeplan_id.id == community_homeplan_id and r.type == 'option_value'
            )

            override_home_plan_record_exists = home_plan_option_values.master_plan_options_id.homeplan_option_override_ids.filtered(
                lambda r: r.company_id.id == company_id and r.type == 'option_value'
            )

            if overrite_community_home_plan_record_exists and overrite_community_home_plan_record_exists.name:
                if overrite_community_home_plan_record_exists.name:
                    name = overrite_community_home_plan_record_exists.name
                    is_override = True
                    if override_home_plan_record_exists and override_home_plan_record_exists.name:
                        inherited_name = override_home_plan_record_exists.name
            else:
                override_master_plan_record_exists = home_plan_option_values.master_plan_options_id.option_value_override_id
                if override_home_plan_record_exists and override_home_plan_record_exists.name:  # name from home plan override
                    if override_home_plan_record_exists.name:
                        name = override_home_plan_record_exists.name
                        if override_master_plan_record_exists and override_master_plan_record_exists.name:  # name from master plan override
                            inherited_name = override_master_plan_record_exists.name
                elif override_master_plan_record_exists and override_master_plan_record_exists.name:  # name from master plan override
                    name = override_master_plan_record_exists.name
                    inherited_name = home_plan_option_values.master_plan_options_id.option_values_id.name

            # check for price and description only
            if overrite_community_home_plan_record_exists:
                description = overrite_community_home_plan_record_exists.description
                price = overrite_community_home_plan_record_exists.price
            else:
                override_master_plan_record_exists = home_plan_option_values.master_plan_options_id.option_value_override_id
                if override_home_plan_record_exists:
                    description = override_home_plan_record_exists.description
                    price = override_home_plan_record_exists.price
                elif override_master_plan_record_exists:
                    description = home_plan_option_values.master_plan_options_id.option_value_override_id.description

            # check for image only
            image = home_plan_option_values.master_plan_options_id.option_values_id.default_image
            if overrite_community_home_plan_record_exists and overrite_community_home_plan_record_exists.image:
                image = overrite_community_home_plan_record_exists.image
            else:
                override_master_plan_record_exists = home_plan_option_values.master_plan_options_id.option_value_override_id
                if override_home_plan_record_exists and override_home_plan_record_exists.image:
                    image = override_home_plan_record_exists.image
                elif override_master_plan_record_exists and override_master_plan_record_exists.image:
                    image = override_master_plan_record_exists.image

            quantity = home_plan_option_values.master_plan_options_id.quantity
            if overrite_community_home_plan_record_exists and overrite_community_home_plan_record_exists.quantity:
                quantity = overrite_community_home_plan_record_exists.quantity
            else:
                if override_home_plan_record_exists and override_home_plan_record_exists.quantity:
                    quantity = override_home_plan_record_exists.quantity

            final_response[target_index]['option_values'].append({
                # "community_homeplan_id": request.context.get('active_id'),
                "master_plan_option_id": home_plan_option_values.master_plan_options_id.id,
                "home_plan_option_id": home_plan_option_values.id,
                "option_set_id": home_plan_option_values.master_plan_options_id.option_values_id.option_id,
                "option_value_id": home_plan_option_values.master_plan_options_id.option_values_id.id,
                "name": name,
                "inherited_name": inherited_name,
                "description": description,
                "price": price,
                "is_active": False,
                "is_override": is_override,
                "is_title": home_plan_option_values.master_plan_options_id.is_title,
                "is_base": is_base,
                "home_plan_option_value_is_base": home_plan_option_values.is_base,
                # "price_type": home_plan_option_values.master_plan_options_id.option_values_id.price_type,
                # "units": home_plan_option_values.master_plan_options_id.option_values_id.units,
                "quantity": quantity,
                "image": image,
                "option_categories_id": [
                    home_plan_option_values.master_plan_options_id.option_values_id.option_categories_id.id,
                    home_plan_option_values.master_plan_options_id.option_values_id.option_categories_id.name
                ],
                "option_classes_id": [
                    home_plan_option_values.master_plan_options_id.option_values_id.option_classes_id.id,
                    home_plan_option_values.master_plan_options_id.option_values_id.option_classes_id.name
                ]
            }, )

        if final_response:
            for option in final_response:
                home_plan_option_ids = [option_value['home_plan_option_id'] for option_value in option['option_values']]
                base_community_option_value_exists_id = False
                if home_plan_option_ids:
                    base_community_option_value_exists_id = request.env[
                        'community_module.community_homeplans_options'].sudo().search([
                        ('homeplan_option_id', 'in', home_plan_option_ids),
                        ('is_base', '=', True),
                        ('community_homeplan_id', '=', community_homeplan_id)
                    ])
                if base_community_option_value_exists_id:
                    for option_val in option['option_values']:
                        if option_val[
                            'home_plan_option_id'] == base_community_option_value_exists_id.homeplan_option_id.id:
                            option_val['is_base'] = True
                        else:
                            option_val['is_base'] = False
                else:
                    base_home_plan_option_value_exists_ids = [option_value['master_plan_option_id'] for option_value in
                                                              option['option_values'] if
                                                              option_value['home_plan_option_value_is_base']]

                    if base_home_plan_option_value_exists_ids:
                        for option_val in option['option_values']:
                            if option_val['master_plan_option_id'] in base_home_plan_option_value_exists_ids:
                                option_val['is_base'] = True
                            else:
                                option_val['is_base'] = False

        return request.make_json_response({'pagination': pagination_response, 'data': final_response}, status=200)

    @http.route("/home_plan/option_value_set_base", methods=["POST"], type="http", auth="public", csrf=False,
                save_session=False,
                cors="*")
    def home_plan_option_value_set_base(self):
        request_body = json.loads(request.httprequest.data)
        if not request_body:
            return request.make_json_response({'data': 'Not found'}, status=404)

        company_id = request_body.get('company_id') or request.env.company.id
        homeplan_option = request.env['module_sb.home_plan_options'].sudo().search([
            ('homeplan_id', '=', request_body['homeplan_id']),
            ('master_plan_options_id', '=', request_body['master_plan_option_id']),
            ('company_id', '=', company_id),
        ], limit=1)

        if homeplan_option:
            homeplan_option.write({
                'is_base': True,
                'is_active': True
            })

            sibling_records = request.env['module_sb.master_plan_options'].sudo().search([
                ('id', '!=', request_body['master_plan_option_id']),
                ('options_id', '=', homeplan_option.master_plan_options_id.options_id.id),
                ('homeplan_id', '=', homeplan_option.master_plan_options_id.homeplan_id.id)
            ])

            if sibling_records:
                (request.env['module_sb.home_plan_options']
                .sudo()
                .search([('master_plan_options_id', 'in', sibling_records.ids)])
                .filtered(lambda r: r.company_id.id == company_id)
                .write({
                    'is_base': False
                }))

        return request.make_json_response({'data': "Record updated"}, status=200)

    def _get_matching_option_ids(self, records, search_term, company_id=None, community_homeplan_id=False):
        matched_ids = []
        for record in records:
            if not any(fr['option_id'] == record.master_plan_options_id.options_id.id for fr in
                       matched_ids):

                name = record.master_plan_options_id.options_id.name
                override_community_home_plan_record_exists = record.community_homeplan_option_override_ids.filtered(
                    lambda r: r.community_homeplan_id.id == community_homeplan_id and r.type == 'option'
                )
                override_home_plan_record_exists = record.master_plan_options_id.homeplan_option_override_ids.filtered(
                    lambda r: r.company_id.id == company_id and r.type == 'option'
                )
                if override_community_home_plan_record_exists:
                    if override_community_home_plan_record_exists.name:
                        name = override_community_home_plan_record_exists.name
                else:
                    override_master_plan_record_exists = record.master_plan_options_id.option_override_id
                    if override_home_plan_record_exists:
                        name = override_home_plan_record_exists.name

                    elif override_master_plan_record_exists:
                        name = override_master_plan_record_exists.name

                matched_ids.append({
                    'option_id': record.master_plan_options_id.options_id.id,
                    'name': name
                })
        for record in records:
            name = record.master_plan_options_id.option_values_id.name  # default
            overrite_community_home_plan_record_exists = record.community_homeplan_option_override_ids.filtered(
                lambda r: r.community_homeplan_id.id == community_homeplan_id and r.type == 'option_value'
            )
            override_home_plan_record_exists = record.master_plan_options_id.homeplan_option_override_ids.filtered(
                lambda r: r.company_id.id == company_id and r.type == 'option_value'
            )
            if overrite_community_home_plan_record_exists and overrite_community_home_plan_record_exists.name:
                if overrite_community_home_plan_record_exists.name:
                    name = overrite_community_home_plan_record_exists.name
            else:
                override_master_plan_record_exists = record.master_plan_options_id.option_value_override_id
                if override_home_plan_record_exists and override_home_plan_record_exists.name:
                    if override_home_plan_record_exists.name:
                        name = override_home_plan_record_exists.name

                elif override_master_plan_record_exists and override_master_plan_record_exists.name:
                    name = override_master_plan_record_exists.name

            matched_ids.append({
                'option_id': record.master_plan_options_id.options_id.id,
                'name': name
            })
        matching_option_ids = [
            item['option_id'] for item in matched_ids if search_term.lower() in item['name'].lower()
        ]

        return list(set(matching_option_ids))
