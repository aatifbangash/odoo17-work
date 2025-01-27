import copy
import json
from pprint import pprint

from odoo import http
from odoo.http import request


class FranchiserWebsiteController(http.Controller):

    # @http.route('/home', auth='public', website=True)
    # def franchisor_index(self, **kw):
    #     is_franchisor = request.env.company.is_franchisor
    #     if is_franchisor:
    #         return http.request.render('franchisor_theme.franchisor_homepage', {})

    # @http.route('/division', auth='public', website=True)
    # def division(self, **kw):
    #
    #     is_franchisor = request.env.company.is_franchisor
    #     if not is_franchisor:
    #         return request.redirect('/404')
    #
    #     return http.request.render('franchisor_theme.divisions', {})

    @http.route('/schellter-technology', auth='public', website=True)
    def division(self, **kw):
        return http.request.render('franchisor_theme.schellter-technology', {})

    @http.route('/about-us', auth='public', website=True)
    def about_us(self, **kw):
        partner = request.env['res.company']._get_main_company()
        return http.request.render('franchisor_theme.about-us', {
            'partner': partner
        })

    @http.route('/gallery', auth='public', website=True)
    def gallery(self, **kw):
        galleries = request.env['module_sb.gallery'].sudo().search([])
        return http.request.render('franchisor_theme.gallery', {
            "galleries": galleries
        })

    @http.route('/find-your-home', auth='public', website=True)
    def find_your_home(self, **kw):
        partners_domain = [
            ('is_franchisor', '=', False)
        ]

        if request.httprequest.args.get('partner_id'):
            partners_domain.append(('id', '=', int(request.httprequest.args.get('partner_id'))))

        partners = request.env['res.company'].sudo().search(partners_domain)
        if not partners:
            return request.redirect('/404')

        google_map_object = {}
        if self.is_module_installed('bista_map_component'):
            google_map_object = self.get_sample_data()

        return http.request.render('franchisor_theme.find_your_home', {
            'partners': partners,
            'google_map_object': google_map_object
        })

    def get_sample_data(self, google_map_item_id=None, type=None):
        google_map = request.env['google.map'].sudo().search_read([],
                                                                  fields=['name', 'map_id', 'init_zoom', 'center_lat',
                                                                          'search',
                                                                          'center_lng'], limit=1)
        map_data = google_map[0]
        domain = [
            ('google_map_id', '=', map_data.get('id'))
        ]

        if type == 'partner':
            # Get communities associated with the partner (franchise)
            community_domain = domain[:]
            community_domain.append(('franchise_id', '=', google_map_item_id.id))
            community_domain.append(('type', '=', 'community'))

            community_ids = request.env['google.map.item'].sudo().search(community_domain).ids
            pprint(community_ids)
            # Get sections under the communities
            section_domain = domain[:]
            section_domain.append(('community_id', 'in', community_ids))
            section_domain.append(('type', '=', 'section'))

            section_ids = request.env['google.map.item'].sudo().search(section_domain).ids
            # Get lots under the sections
            domain.append(('section_id', 'in', section_ids))
            domain.append(('type', '=', 'home'))

        elif type == 'community':
            # Get sections under the specific community
            section_domain = copy.copy(domain)
            section_domain.append(('community_id', '=', google_map_item_id.id))
            section_domain.append(('type', '=', 'section'))

            section_ids = request.env['google.map.item'].sudo().search(section_domain).ids

            # Get lots under the sections
            domain.append(('section_id', 'in', section_ids))
            domain.append(('type', '=', 'home'))

        google_map_items = request.env['google.map.item'].sudo().search(domain)
        item_data = google_map_items.get_data()
        return {
            'map': map_data,
            'item_data': item_data,
        }

    def is_module_installed(self, module_name):
        module = request.env['ir.module.module'].sudo().search(
            [('name', '=', module_name), ('state', '=', 'installed')], limit=1)
        return bool(module)

    @http.route('/find-your-home/<string:state>/<string:partner_slug>/plan/<string:homeplan_slug>', methods=["GET"],
                type="http",
                auth='public', website=True)
    def partner_plain_detail(self, partner_slug, homeplan_slug):
        # Partner validation
        partner = request.env['res.company'].sudo().search([
            ('slug', '=', partner_slug),
            ('is_franchisor', '=', False)
        ])
        if not partner:
            return request.redirect('/404')

        # Home Plan validation
        home_plan = http.request.env['product.template'].sudo().search([
            ('slug', '=', homeplan_slug),
            ('is_published', '=', True),
            ('active', '=', True),
            ('franchise_homeplans_ids.company_id', '=', partner.id)  # this is for enable on a partner plan
        ])

        if not home_plan:
            return request.redirect('/404')

        # Get the current home plan options.
        home_plan_options = request.env['module_sb.home_plan_options'].sudo().search([
            ('homeplan_id', '=', home_plan.id),
            ('company_id', '=', partner.id),
            # ('is_active', '=', True)
        ])

        final_response_list = False

        if home_plan_options:
            home_plan_options_active = home_plan_options.filtered(lambda x: x.is_active == True).ids

            # Prepare options in home Plan
            final_response = {}
            for homeplan_option in home_plan_options:
                # Option Data
                option_id = homeplan_option.master_plan_options_id.options_id.id

                override_option_homeplan = homeplan_option.master_plan_options_id.homeplan_option_override_ids.filtered(
                    lambda r: r.company_id.id == partner.id and r.type == 'option'
                )

                if override_option_homeplan and override_option_homeplan.name:
                    option_name = override_option_homeplan.name
                elif homeplan_option.master_plan_options_id.option_override_id.name:
                    option_name = homeplan_option.master_plan_options_id.option_override_id.name
                else:
                    option_name = homeplan_option.master_plan_options_id.options_id.name

                # Option Value Data
                override_optionvalue_homeplan = homeplan_option.master_plan_options_id.homeplan_option_override_ids.filtered(
                    lambda r: r.company_id.id == partner.id and r.type == 'option_value'
                )

                if override_optionvalue_homeplan and override_optionvalue_homeplan.name:
                    option_value_name = override_optionvalue_homeplan.name
                elif homeplan_option.master_plan_options_id.option_value_override_id.name:
                    option_value_name = homeplan_option.master_plan_options_id.option_value_override_id.name
                else:
                    option_value_name = homeplan_option.master_plan_options_id.option_values_id.name

                option_value_price = 0.00
                if override_optionvalue_homeplan and override_optionvalue_homeplan.price:
                    option_value_price = override_optionvalue_homeplan.price

                # Option value Image
                option_value_image = homeplan_option.master_plan_options_id.option_values_id.default_image
                if override_optionvalue_homeplan and override_optionvalue_homeplan.image:
                    option_value_image = override_optionvalue_homeplan.image
                elif homeplan_option.master_plan_options_id.option_value_override_id.image:
                    option_value_image = homeplan_option.master_plan_options_id.option_value_override_id.image

                # Add the options and option values to the dictionary
                if option_id not in final_response:
                    final_response[option_id] = {
                        "id": homeplan_option.id,
                        "option_id": option_id,
                        "option_type": homeplan_option.options_id.option_type,
                        "name": option_name,
                        'option_values': []
                    }

                final_response[option_id]['option_values'].append({
                    "name": option_value_name,
                    "option_value_price": None,
                    "image": option_value_image,
                    "is_active": True if homeplan_option.id in home_plan_options_active else False
                })
            # Convert the dictionary to a list
            final_response_list = list(final_response.values())

            # Filter out inactive option values and remove options with no active values
        filtered_options = []
        if final_response_list:
            for option in final_response_list:
                if option['option_type'] == 'binary':
                    option['option_values'] = []
                    filtered_options.append(option)
                else:
                    active_values = [value for value in option['option_values'] if value['is_active']]
                    if active_values:
                        option['option_values'] = active_values
                        filtered_options.append(option)

        # Grab the elevation options
        elevation_options = []
        if filtered_options:
            for option in filtered_options:
                if option['name']:
                    if "Elevation" in option['name']:
                        elevation_options.append(option)

        return http.request.render('franchisor_theme.plan_detail', {
            'home_plan': home_plan,
            'final_response_list': filtered_options,
            'elevation_options': elevation_options
        })

    @http.route('/find-your-home/<string:state>/<string:partner_slug>/<string:community_slug>/<string:homeplan_slug>',
                methods=["GET"], type="http", auth='public', website=True)
    def community_plan_detail(self, partner_slug, community_slug, homeplan_slug):
        # Partner validation
        partner = request.env['res.company'].sudo().search([
            ('slug', '=', partner_slug),
            ('is_franchisor', '=', False)
        ], limit=1)
        if not partner:
            return request.redirect('/404')

        # Home Plan validation
        home_plan = http.request.env['product.template'].sudo().search([
            ('slug', '=', homeplan_slug),
            ('is_published', '=', True),
            ('active', '=', True),
            ('franchise_homeplans_ids.company_id', '=', partner.id)
        ], limit=1)

        if not home_plan:
            return request.redirect('/404')

        # Community validation
        community = http.request.env['google.map.item'].sudo().search([
            ('slug', '=', community_slug)
        ], limit=1)

        if not community:
            return request.redirect('/404')

        # check if home plan is attached with current comunity
        if home_plan not in community.community_map_homeplans_ids.homeplan_id:
            return request.redirect('/404')

        comunity_homeplan = community.community_map_homeplans_ids.filtered(lambda x: x.homeplan_id.id == home_plan.id)
        final_response = {}
        if comunity_homeplan:
            community_homeplan_options_active = comunity_homeplan.community_homeplan_options_ids.filtered(
                lambda x: x.is_active).homeplan_option_id.ids

            community_homeplan_options = comunity_homeplan.community_homeplan_options_ids
            if community_homeplan_options:
                # Prepare options in home Plan

                for homeplan_option in community_homeplan_options.homeplan_option_id:

                    # Option Data
                    option_id = homeplan_option.master_plan_options_id.options_id.id

                    override_option_community_homeplan = homeplan_option.community_homeplan_option_override_ids.filtered(
                        lambda r: r.community_homeplan_id.id == comunity_homeplan.id and r.type == 'option'
                    )
                    override_option_homeplan = homeplan_option.master_plan_options_id.homeplan_option_override_ids.filtered(
                        lambda r: r.company_id.id == partner.id and r.type == 'option'
                    )

                    if override_option_community_homeplan and override_option_community_homeplan.name:
                        option_name = override_option_community_homeplan.name
                    elif override_option_homeplan and override_option_homeplan.name:
                        option_name = override_option_homeplan.name
                    elif homeplan_option.master_plan_options_id.option_override_id.name:
                        option_name = homeplan_option.master_plan_options_id.option_override_id.name
                    else:
                        option_name = homeplan_option.master_plan_options_id.options_id.name

                    # Option Value Data
                    override_optionvalue_community_homeplan = homeplan_option.community_homeplan_option_override_ids.filtered(
                        lambda r: r.community_homeplan_id.id == comunity_homeplan.id and r.type == 'option_value'
                    )
                    override_optionvalue_homeplan = homeplan_option.master_plan_options_id.homeplan_option_override_ids.filtered(
                        lambda r: r.company_id.id == partner.id and r.type == 'option_value'
                    )

                    if override_optionvalue_community_homeplan and override_optionvalue_community_homeplan.name:
                        option_value_name = override_optionvalue_community_homeplan.name
                    elif override_optionvalue_homeplan and override_optionvalue_homeplan.name:
                        option_value_name = override_optionvalue_homeplan.name
                    elif homeplan_option.master_plan_options_id.option_value_override_id.name:
                        option_value_name = homeplan_option.master_plan_options_id.option_value_override_id.name
                    else:
                        option_value_name = homeplan_option.master_plan_options_id.option_values_id.name

                    option_value_price = 0.00
                    if override_optionvalue_community_homeplan and override_optionvalue_community_homeplan.price:
                        option_value_price = override_optionvalue_community_homeplan.price
                    elif override_optionvalue_homeplan and override_optionvalue_homeplan.price:
                        option_value_price = override_optionvalue_homeplan.price

                    # Option Value Image Data
                    option_value_image = None
                    if override_optionvalue_community_homeplan and override_optionvalue_community_homeplan.image:
                        option_value_image = override_optionvalue_community_homeplan.image
                    elif override_optionvalue_homeplan and override_optionvalue_homeplan.image:
                        option_value_image = override_optionvalue_homeplan.image
                    elif homeplan_option.master_plan_options_id.option_value_override_id.image:
                        option_value_image = homeplan_option.master_plan_options_id.option_value_override_id.image

                    # Add the options and option values to the dictionary
                    if option_id not in final_response:
                        final_response[option_id] = {
                            "id": homeplan_option.id,
                            "option_id": option_id,
                            "option_type": homeplan_option.options_id.option_type,
                            "name": option_name,
                            'option_values': []
                        }

                    final_response[option_id]['option_values'].append({
                        "name": option_value_name,
                        "option_value_price": option_value_price,
                        "image": option_value_image,
                        "is_active": True if homeplan_option.id in community_homeplan_options_active else False
                    })
        # Convert the dictionary to a list
        final_response_list = list(final_response.values())

        # Filter out inactive option values and remove options with no active values
        filtered_options = []
        for option in final_response_list:
            if option['option_type'] == 'binary':
                option['option_values'] = []
                filtered_options.append(option)
            else:
                active_values = [value for value in option['option_values'] if value['is_active']]
                if active_values:
                    option['option_values'] = active_values
                    filtered_options.append(option)

        # Grab the elevation options
        elevation_options = []
        if filtered_options:
            for option in filtered_options:
                if option['name']:
                    if "Elevation" in option['name']:
                        elevation_options.append(option)

        return http.request.render('franchisor_theme.plan_detail', {
            'home_plan': home_plan,
            'final_response_list': filtered_options,
            'elevation_options': elevation_options
        })

    @http.route('/find-your-home/<string:state>/<string:partner_slug>', auth='public', type="http", website=True)
    def partner_landing_page(self, partner_slug):
        partner = request.env['res.company'].sudo().search([
            ('slug', '=', partner_slug),
            ('is_franchisor', '=', False)
        ])

        if not partner:
            return request.redirect('/404')

        home_plans = http.request.env['product.template'].sudo().search([
            ('is_published', '=', True),
            ('active', '=', True),
            ('franchise_homeplans_ids.company_id', '=', partner.id),
            # ('homeplan_community_ids', '!=', False),
            # ('homeplan_community_ids.community_id.create_uid.company_id.id', '=', partner.id),
        ])

        communities = http.request.env['community_module.community'].sudo().search([
            ('is_active', '=', True),
            ('create_uid.company_id.id', '=', partner.id),
        ])

        website_content = http.request.env['module_sb.website_content'].sudo().search([
            ('company_id', '=', partner.id),
        ])

        # google_map_object = {}
        # default_zoom_level = None
        # if communities:
        #     map_data = []
        #     for community in communities:
        #         if community.google_map_item_id:
        #             map_item = community.google_map_item_id
        #             default_zoom_level = map_item.marker_zoom if map_item.marker_zoom else 15
        #             if map_item.marker_lat and map_item.marker_lng and map_item.marker_lat != '0' and map_item.marker_lng != '0':
        #                 marker = {
        #                     "name": community.display_name,
        #                     "content_header": community.display_name,
        #                     "content_body": "This is a great community",
        #                     "content_footer": f"Coordinates {map_item.marker_lat}/{map_item.marker_lng}",
        #                     "coordinates": [
        #                         map_item.marker_lat,
        #                         map_item.marker_lng
        #                     ],
        #                     "type": "marker",
        #                     "zoomMax": 16,
        #                     "zoomMin": 15,
        #                 }
        #                 map_data.append(marker)
        #
        #     # Create the full map object
        #     google_map_object = {
        #         "initZoom": default_zoom_level,
        #         "data": map_data,
        #     }
        def plan_to_dict(plan):
            return {
                'id': plan.id,
                'name': plan.name,
                'slug': plan.slug,
                'image_1920': plan.image_1920.decode('utf-8', errors='ignore'),
                'product_override_ids': [id.id for id in plan.product_override_ids],
                'incentive_price': plan.incentive_price,
                'min_bedrooms': plan.min_bedrooms,
                'max_bedrooms': plan.max_bedrooms,
                'min_bathrooms': plan.min_bathrooms,
                'max_bathrooms': plan.max_bathrooms,
                'base_heated_square_feet': plan.base_heated_square_feet,
                'max_heated_square_feet': plan.max_heated_square_feet,
                'base_total_square_feet': plan.base_total_square_feet,
                'max_total_square_feet': plan.max_total_square_feet,
                # 'image': base64.b64encode(plan.image_1920).decode('utf-8') if plan.image_1920 else None,
                # Convert binary field to Base64
            }

        home_plans_data = [plan_to_dict(plan) for plan in home_plans]
        google_map_object = {}
        if self.is_module_installed('bista_map_component'):
            google_map_object = self.get_sample_data(partner.google_map_item_id, 'partner')
        google_map_object['partner_slug'] = partner_slug
        return http.request.render('franchisor_theme.division', {
            'partner': partner,
            'communities': communities,
            'home_plans': home_plans,
            'json_data': {
                'partner_slug': partner_slug,
            },
            'website_content': website_content,
            'google_map_object': google_map_object
        })

    @http.route('/find-your-home/<string:state>/<string:partner_slug>/<string:community_slug>', type="http",
                auth="public",
                website=True)
    def community_plan(self, partner_slug, community_slug, **kw):
        partner = request.env['res.company'].sudo().search([
            ('slug', '=', partner_slug),
            ('is_franchisor', '=', False)
        ])
        if not partner:
            return request.redirect('/404')

        # community_home_plan = http.request.env['google.map.item'].sudo().search([
        #     ('slug', '=', community_slug)
        # ], limit=1)

        community_home_plan = http.request.env['community_module.community'].sudo().search([
            ('slug', '=', community_slug),
            ('is_active', '=', True),
            ('create_uid.company_id.id', '=', partner.id),
        ], limit=1)

        if not community_home_plan:
            return request.redirect('/404')

        google_map_object = {}
        if self.is_module_installed('bista_map_component'):
            # google_map_object = self.get_sample_data(community_home_plan, 'community')
            google_map_object = self.get_sample_data(community_home_plan.google_map_item_id, 'community')

        amenities_ids = community_home_plan.amenities_ids
        categories = []
        for x in amenities_ids:
            category = x.category_id.read()
            if category not in categories:
                categories.append(category[0])

        # Use frozenset to create a set of unique dictionaries
        categories = [dict(t) for t in {frozenset(d.items()) for d in categories}]
        google_map_object['partner_slug'] = partner_slug
        google_map_object['community_slug'] = community_slug
        return http.request.render('franchisor_theme.community_details', {
            'partner': partner,
            'community_home_plan': community_home_plan,
            'google_map_object': google_map_object,
            'categories': categories,
            'json_data': {
                'partner_slug': partner_slug,
                'community': community_slug
            },
        })

    @http.route('/get/partners/plans', auth='public', type="json", website=True)
    def community_page(self, community_slug, partner_slug):
        partner = request.env['res.company'].sudo().search([
            ('slug', '=', partner_slug),
            ('is_franchisor', '=', False)
        ])
        result_array = []
        if not community_slug:
            result_array = http.request.env['product.template'].sudo().search([
                ('is_published', '=', True),
                ('active', '=', True),
                ('franchise_homeplans_ids.company_id', '=', partner.id)
            ]).read()
        else:
            community_homeplan = http.request.env['community_module.community'].sudo().search([
                ('slug', '=', community_slug),
                ('is_active', '=', True),
                ('create_uid.company_id.id', '=', partner.id),
            ], limit=1)
            home_plans = community_homeplan.community_homeplans_ids

            # Iterate through the array
            for plan in home_plans:
                # Read the fields from the `homeplan_id` object
                homeplan_data = plan.homeplan_id.read(
                    ['id', 'display_name', 'incentive_price', 'max_bathrooms', 'max_bedrooms', 'min_bedrooms',
                     'min_bathrooms', 'name', 'price', 'base_price', 'product_override_ids', 'slug', 'image_1920',
                     'max_total_square_feet', 'base_total_square_feet', 'max_heated_square_feet',
                     'base_heated_square_feet'])[0]  # Read specific fields
                id = homeplan_data.get('id')
                display_name = homeplan_data.get('display_name')
                incentive_price = homeplan_data.get('incentive_price')
                max_bathrooms = homeplan_data.get('max_bathrooms')
                max_bedrooms = homeplan_data.get('max_bedrooms')
                min_bedrooms = homeplan_data.get('min_bedrooms')
                min_bathrooms = homeplan_data.get('min_bathrooms')
                name = homeplan_data.get('name')
                price = homeplan_data.get('price')
                base_price = homeplan_data.get('base_price')
                product_override_ids = homeplan_data.get('product_override_ids')
                slug = homeplan_data.get('slug')
                image_1920 = homeplan_data.get('image_1920')
                max_total_square_feet = homeplan_data.get('max_total_square_feet')
                base_total_square_feet = homeplan_data.get('base_total_square_feet')
                max_heated_square_feet = homeplan_data.get('max_heated_square_feet')
                base_heated_square_feet = homeplan_data.get('base_heated_square_feet')

                # Create an object and append it to the result array
                result_array.append({
                    'id': id,
                    'display_name': display_name,
                    'incentive_price': incentive_price,
                    'max_bathrooms': max_bathrooms,
                    'max_bedrooms': max_bedrooms,
                    'min_bedrooms': min_bedrooms,
                    'min_bathrooms': min_bathrooms,
                    'name': name,
                    'price': price,
                    'base_price': base_price,
                    'product_override_ids': product_override_ids,
                    'slug': slug,
                    'image_1920': image_1920,
                    'max_total_square_feet': max_total_square_feet,
                    'base_total_square_feet': base_total_square_feet,
                    'max_heated_square_feet': max_heated_square_feet,
                    'base_heated_square_feet': base_heated_square_feet,
                })
        return_data = {'home_plans': result_array, 'partner': {
            'id': partner.id, 'name': partner.name,
            'state_id': {'code': partner.state_code},
            'slug': partner.slug
        }}
        return return_data
