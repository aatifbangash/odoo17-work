import json
import math
from pprint import pprint

from odoo import http
from odoo.http import request


class MasterPlansController(http.Controller):

    @http.route("/master_plan/options", methods=["POST"], type="http", auth="public", csrf=False, save_session=False,
                cors="*")
    def master_plan_options_store(self):
        request_body = json.loads(request.httprequest.data)
        if not request_body:
            return request.make_json_response({'data': 'Not found'}, status=404)

        master_plan_options = []
        for option in request_body:
            if option and option['option_values']:
                for i, option_value in enumerate(option['option_values']):

                    existing_option = False
                    is_title = True if i == 0 else False

                    if 'master_plan_option_id' in option_value:
                        existing_option = request.env['module_sb.master_plan_options'].sudo().search([
                            ('id', '=', option_value['master_plan_option_id'])
                        ], limit=1)

                    if existing_option:
                        existing_option.sudo().write({
                            'is_active': False if option['is_active'] == False else option_value['is_active']
                        })
                    else:
                        master_plan_options.append({
                            'homeplan_id': option['homeplan_id'],
                            'options_id': option['option_id'],
                            'is_title': is_title,
                            'option_values_id': option_value['option_value_id'],
                            'is_active': False if option['is_active'] == False else option_value['is_active'],
                            'quantity': option_value['quantity'],
                        })
            else:
                master_plan_options.append({
                    'homeplan_id': option['homeplan_id'],
                    'options_id': option['option_id'],
                    'is_title': True,
                    'is_active': option['is_active']
                })
        if master_plan_options:
            request.env['module_sb.master_plan_options'].sudo().create(master_plan_options)

        return request.make_json_response({'data': "Record created"}, status=201)

    @http.route("/master_plan/<int:homeplan_id>/options", methods=["GET"], type="http", auth="public")
    def master_plan_options_by_id(self, homeplan_id):

        query_params = request.httprequest.args

        search_term = query_params.get('search_term', False)
        status = query_params.get('status', None)
        page_no = int(query_params.get('page_no', 1))  # Default to page 1 if not provided
        page_size = int(query_params.get('page_size', 10))

        domain = [('homeplan_id', '=', homeplan_id)]
        optional_filters = {
            'category_id': 'options_id.option_categories_id',
            'class_id': 'options_id.option_classes_id',
            'location_id': 'options_id.option_locations_id'
        }

        for param, field in optional_filters.items():
            param_value = query_params.get(param)
            if param_value:
                domain.append((field, '=', int(param_value)))

        if status in ['active', 'inactive']:
            status_domain = domain + [('is_active', '=', True)]
            records = (request.env['module_sb.master_plan_options'].sudo()
                       .read_group(status_domain, fields=['options_id'], groupby=['options_id']))

            active_options_ids = [record['options_id'][0] for record in records]

            domain_operator = 'in' if status == 'active' else 'not in'
            domain.append(('options_id', domain_operator, active_options_ids))

        if search_term:
            records = request.env['module_sb.master_plan_options'].sudo().search(domain, order='id desc')
            unique_option_ids = self._get_matching_option_ids(records, search_term)
        else:
            unique_option_ids = (request.env['module_sb.master_plan_options']
                                 .sudo().search(domain, order='id desc').exists().mapped('options_id').ids)

        total_records = len(unique_option_ids)
        offset = (page_no - 1) * page_size
        paginated_option_ids = unique_option_ids[offset:offset + page_size]

        domain.append(('options_id', 'in', paginated_option_ids))
        master_plan_options = request.env['module_sb.master_plan_options'].sudo().search(domain, order='id desc')

        if not master_plan_options:
            return request.make_json_response({'data': 'Not found'}, status=404)

        pagination_response = {
            'page_no': page_no,
            'page_size': page_size,
            'total_records': total_records,
            'total_pages': math.ceil(total_records / page_size)
        }
        final_response = []
        for master_plan_option in master_plan_options:
            if not any(fr['option_id'] == master_plan_option.options_id.id for fr in
                       final_response):  # Ignore if option already exists (unique records in final response)
                # if master_plan_option.is_title:
                name = master_plan_option.options_id.name
                inherited_name = None
                is_override = False
                if master_plan_option.option_override_id and master_plan_option.option_override_id.name:
                    name = master_plan_option.option_override_id.name
                    inherited_name = master_plan_option.options_id.name
                    is_override = True

                final_response.append({
                    "id": master_plan_option.id,
                    "option_id": master_plan_option.options_id.id,
                    "homeplan_id": homeplan_id,
                    "name": name,
                    "inherited_name": inherited_name,
                    "is_active": master_plan_option.is_active,
                    "is_title": master_plan_option.is_title,
                    "is_override": is_override,
                    "price_type": master_plan_option.options_id.price_type,
                    "option_type": master_plan_option.options_id.option_type,
                    "units": master_plan_option.options_id.units,
                    "option_categories_id": [
                        master_plan_option.options_id.option_categories_id.id,
                        master_plan_option.options_id.option_categories_id.name
                    ],
                    "option_classes_id": [
                        master_plan_option.options_id.option_classes_id.id,
                        master_plan_option.options_id.option_classes_id.name
                    ],
                    "option_locations_id": [
                        master_plan_option.options_id.option_locations_id.id,
                        master_plan_option.options_id.option_locations_id.name
                    ],
                    'option_values': []
                }, )

        for master_plan_option_values in master_plan_options:
            target_index = next((index for index, fr in enumerate(final_response) if
                                 fr['option_id'] == master_plan_option_values.options_id.id), -1)
            if target_index == -1:
                continue

            name = master_plan_option_values.option_values_id.name
            inherited_name = None
            description = None
            is_override = False

            image = None
            if master_plan_option_values.option_values_id.default_image:
                image = master_plan_option_values.option_values_id.default_image

            if master_plan_option_values.option_value_override_id:
                if master_plan_option_values.option_value_override_id.name:
                    name = master_plan_option_values.option_value_override_id.name
                    inherited_name = master_plan_option_values.option_values_id.name
                    is_override = True
                description = master_plan_option_values.option_value_override_id.description
                if master_plan_option_values.option_value_override_id.image:
                    image = master_plan_option_values.option_value_override_id.image

            final_response[target_index]['option_values'].append({
                "master_plan_option_id": master_plan_option_values.id,
                "option_set_id": master_plan_option_values.option_values_id.option_id,
                "option_value_id": master_plan_option_values.option_values_id.id,
                "name": name,
                "inherited_name": inherited_name,
                "description": description,
                "is_active": master_plan_option_values.is_active,
                "is_title": master_plan_option_values.is_title,
                "is_override": is_override,
                "is_base": master_plan_option_values.is_base,
                # "price_type": master_plan_option_values.option_values_id.price_type,
                # "units": master_plan_option_values.option_values_id.units,
                "quantity": master_plan_option_values.quantity,
                "image": image,
                "option_categories_id": [
                    master_plan_option_values.option_values_id.option_categories_id.id,
                    master_plan_option_values.option_values_id.option_categories_id.name
                ],
                "option_classes_id": [
                    master_plan_option_values.option_values_id.option_classes_id.id,
                    master_plan_option_values.option_values_id.option_classes_id.name
                ]
            }, )

        return request.make_json_response({'pagination': pagination_response, 'data': final_response}, status=200)

    @http.route("/master_plan_active/<int:homeplan_id>/options", methods=["GET"], type="http", auth="public")
    def master_plan_active_options_by_id(self, homeplan_id):

        query_params = request.httprequest.args

        search_term = query_params.get('search_term', False)
        status = query_params.get('status', None)
        page_no = int(query_params.get('page_no', 1))  # Default to page 1 if not provided
        page_size = int(query_params.get('page_size', 10))
        company_id = int(query_params.get('company_id', request.env.company.id))

        domain = [
            ('is_active', '=', True), ('homeplan_id', '=', homeplan_id)
        ]

        optional_filters = {
            'category_id': 'options_id.option_categories_id',
            'class_id': 'options_id.option_classes_id',
            'location_id': 'options_id.option_locations_id'
        }

        for param, field in optional_filters.items():
            param_value = query_params.get(param)
            if param_value:
                domain.append((field, '=', int(param_value)))

        if status in ['active', 'inactive']:
            active_options_ids = request.env['module_sb.home_plan_options'].sudo().search([
                ('homeplan_id', '=', homeplan_id),
                ('company_id', '=', company_id),
                ('is_active', '=', True)
            ]).mapped('master_plan_options_id.options_id').ids

            domain_operator = 'in' if status == 'active' else 'not in'
            domain.append(('options_id', domain_operator, active_options_ids))

        if search_term:
            records = request.env['module_sb.master_plan_options'].sudo().search(domain, order='id desc')
            unique_option_ids = self._get_matching_option_ids(records, search_term, company_id,
                                                              is_homeplan_override=True)
        else:
            unique_option_ids = request.env['module_sb.master_plan_options'].sudo().search(domain,
                                                                                           order='id desc').exists().mapped(
                'options_id').ids

        total_records = len(unique_option_ids)
        offset = (page_no - 1) * page_size
        paginated_option_ids = unique_option_ids[offset:offset + page_size]

        domain.append(('options_id', 'in', paginated_option_ids))

        master_plan_active_options = request.env['module_sb.master_plan_options'].sudo().search(domain)

        if not master_plan_active_options:
            return request.make_json_response({'data': 'Not found'}, status=404)

        pagination_response = {
            'page_no': page_no,
            'page_size': page_size,
            'total_records': total_records,
            'total_pages': math.ceil(total_records / page_size)
        }

        final_response = []
        for master_plan_option in master_plan_active_options:
            if not any(fr['option_id'] == master_plan_option.options_id.id for fr in
                       final_response):  # Ignore if option already exists
                # if master_plan_option.is_title:

                name = master_plan_option.options_id.name  # default
                price = 0.00
                inherited_name = None
                is_override = False
                override_home_plan_record_exists = master_plan_option.homeplan_option_override_ids.filtered(
                    lambda r: r.company_id.id == company_id and r.type == 'option'
                )
                override_master_plan_record_exists = master_plan_option.option_override_id

                if override_home_plan_record_exists and override_home_plan_record_exists.name:  # name from home plan override
                    name = override_home_plan_record_exists.name
                    is_override = True
                    if override_master_plan_record_exists and override_master_plan_record_exists.name:
                        inherited_name = override_master_plan_record_exists.name
                elif override_master_plan_record_exists and override_master_plan_record_exists.name:  # name from master plan override
                    name = override_master_plan_record_exists.name
                    inherited_name = master_plan_option.options_id.name

                if override_home_plan_record_exists and override_home_plan_record_exists.price:
                    price = override_home_plan_record_exists.price

                final_response.append({
                    "id": master_plan_option.id,
                    "option_id": master_plan_option.options_id.id,
                    "homeplan_id": homeplan_id,
                    "name": name,
                    "inherited_name": inherited_name,
                    "price": price,
                    "is_active": False,
                    "is_title": master_plan_option.is_title,
                    "is_override": is_override,
                    "price_type": master_plan_option.options_id.price_type,
                    "option_type": master_plan_option.options_id.option_type,
                    "units": master_plan_option.options_id.units,
                    "option_categories_id": [
                        master_plan_option.options_id.option_categories_id.id,
                        master_plan_option.options_id.option_categories_id.name
                    ],
                    "option_classes_id": [
                        master_plan_option.options_id.option_classes_id.id,
                        master_plan_option.options_id.option_classes_id.name
                    ],
                    "option_locations_id": [
                        master_plan_option.options_id.option_locations_id.id,
                        master_plan_option.options_id.option_locations_id.name
                    ],
                    'option_values': []
                }, )

        for master_plan_option_values in master_plan_active_options:
            target_index = next((index for index, fr in enumerate(final_response) if
                                 fr['option_id'] == master_plan_option_values.options_id.id), -1)
            if target_index == -1:
                continue

            name = master_plan_option_values.option_values_id.name  # default
            inherited_name = None
            description = master_plan_option_values.option_value_override_id.description
            price = 0.0
            is_override = False
            is_base = master_plan_option_values.is_base
            override_home_plan_record_exists = master_plan_option_values.homeplan_option_override_ids.filtered(
                lambda r: r.company_id.id == company_id and r.type == 'option_value'
            )
            override_master_plan_record_exists = master_plan_option_values.option_value_override_id

            if override_home_plan_record_exists and override_home_plan_record_exists.name:  # name from home plan override
                name = override_home_plan_record_exists.name
                is_override = True
                if override_master_plan_record_exists:
                    inherited_name = override_master_plan_record_exists.name
            elif override_master_plan_record_exists and override_master_plan_record_exists.name:  # name from master plan override
                name = override_master_plan_record_exists.name
                inherited_name = master_plan_option_values.option_values_id.name

            # check for image only
            image = master_plan_option_values.option_values_id.default_image
            if override_home_plan_record_exists and override_home_plan_record_exists.image:
                image = override_home_plan_record_exists.image
            elif override_master_plan_record_exists and override_master_plan_record_exists.image:
                image = override_master_plan_record_exists.image

            # check for description and price only
            if override_home_plan_record_exists:
                description = override_home_plan_record_exists.description
                price = override_home_plan_record_exists.price

            quantity = master_plan_option_values.quantity
            if override_home_plan_record_exists and override_home_plan_record_exists.quantity:
                quantity = override_home_plan_record_exists.quantity

            final_response[target_index]['option_values'].append({
                "master_plan_option_id": master_plan_option_values.id,
                "option_set_id": master_plan_option_values.option_values_id.option_id,
                "option_value_id": master_plan_option_values.option_values_id.id,
                "name": name,
                "inherited_name": inherited_name,
                "description": description,
                "price": price,
                "is_active": False,
                "is_override": is_override,
                "is_title": master_plan_option_values.is_title,
                "is_base": is_base,
                # "price_type": master_plan_option_values.option_values_id.price_type,
                # "units": master_plan_option_values.option_values_id.units,
                "image": image,
                "quantity": quantity,
                "option_categories_id": [
                    master_plan_option_values.option_values_id.option_categories_id.id,
                    master_plan_option_values.option_values_id.option_categories_id.name
                ],
                "option_classes_id": [
                    master_plan_option_values.option_values_id.option_classes_id.id,
                    master_plan_option_values.option_values_id.option_classes_id.name
                ]
            }, )

        # check for base option value
        if final_response:
            for option in final_response:
                if option['option_values']:
                    master_plan_option_ids = [option_value['master_plan_option_id'] for option_value in
                                              option['option_values']]
                    if master_plan_option_ids:
                        base_home_plan_option_value_exists = request.env['module_sb.home_plan_options'].sudo().search([
                            ('master_plan_options_id', 'in', master_plan_option_ids),
                            ('company_id', '=', company_id),
                            ('homeplan_id', '=', homeplan_id),
                            ('is_base', '=', True)
                        ], limit=1)
                        if base_home_plan_option_value_exists:
                            for option_val in option['option_values']:
                                if option_val[
                                    'master_plan_option_id'] == base_home_plan_option_value_exists.master_plan_options_id.id:
                                    option_val['is_base'] = True
                                else:
                                    option_val['is_base'] = False
        return request.make_json_response({'pagination': pagination_response, 'data': final_response}, status=200)

    @http.route("/master_plan/option_value_set_base", methods=["POST"], type="http", auth="public", csrf=False,
                save_session=False,
                cors="*")
    def master_plan_option_value_set_base(self):
        request_body = json.loads(request.httprequest.data)
        if not request_body:
            return request.make_json_response({'data': 'Not found'}, status=404)

        masterplan_option = request.env['module_sb.master_plan_options'].sudo().search([
            ('id', '=', request_body['master_plan_option_id'])
        ], limit=1)

        if masterplan_option:
            masterplan_option.write({
                'is_base': True,
                'is_active': True
            })

            sibling_records = request.env['module_sb.master_plan_options'].sudo().search([
                ('id', '!=', request_body['master_plan_option_id']),
                ('options_id', '=', masterplan_option.options_id.id),
                ('homeplan_id', '=', masterplan_option.homeplan_id.id)
            ])

            if sibling_records:
                sibling_records.write({
                    'is_base': False
                })

        return request.make_json_response({'data': "Record updated"}, status=200)

    def _get_matching_option_ids(self, records, search_term, company_id=None, is_homeplan_override=False):
        matched_ids = []
        for record in records:
            if not any(fr['option_id'] == record.options_id.id for fr in
                       matched_ids):
                name = record.options_id.name

                if company_id and is_homeplan_override:
                    override_home_plan_record_exists = record.homeplan_option_override_ids.filtered(
                        lambda r: r.company_id.id == company_id and r.type == 'option'
                    )
                    override_master_plan_record_exists = record.option_override_id
                    if override_home_plan_record_exists and override_home_plan_record_exists.name:
                        name = override_home_plan_record_exists.name

                    elif override_master_plan_record_exists and override_master_plan_record_exists.name:
                        name = override_master_plan_record_exists.name
                else:
                    if record.option_override_id and record.option_override_id.name:
                        name = record.option_override_id.name

                matched_ids.append({
                    "option_id": record.options_id.id,
                    "name": name
                })
        for record in records:

            name = record.option_values_id.name
            if company_id and is_homeplan_override:
                override_home_plan_record_exists = record.homeplan_option_override_ids.filtered(
                    lambda r: r.company_id.id == company_id and r.type == 'option_value'
                )
                override_master_plan_record_exists = record.option_value_override_id

                if override_home_plan_record_exists and override_home_plan_record_exists.name:
                    name = override_home_plan_record_exists.name

                elif override_master_plan_record_exists and override_master_plan_record_exists.name:
                    name = override_master_plan_record_exists.name
            else:
                if record.option_value_override_id:
                    if record.option_value_override_id.name:
                        name = record.option_value_override_id.name

            matched_ids.append({
                "option_id": record.options_id.id,
                "name": name
            })

        matching_option_ids = [
            item['option_id'] for item in matched_ids if search_term.lower() in item['name'].lower()
        ]
        return list(set(matching_option_ids))
