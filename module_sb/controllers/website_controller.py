from odoo import http
from odoo.http import request
from pprint import pprint


class ModuleSBWebsiteController(http.Controller):

    @http.route('/', auth='public', website=True)
    def index(self, **kw):
        partners = request.env['res.company'].sudo().search([
            ('is_franchisor', '=', False),
            ('slug', '!=', False)
        ], limit=3)

        return http.request.render('franchisor_theme.franchisor_homepage', {'partners': partners})

    @http.route('/community_plan/<int:community_id>', type="http", auth="public", website=True)
    def community_plan(self, community_id, **kw):
        community_home_plan = http.request.env['community_module.community'].sudo().search([
            ('id', '=', community_id),
            ('is_active', '=', True),
            ('create_uid.company_id.id', '=', request.env.company.id),
        ], limit=1)

        return http.request.render('theme_sb.community_plan', {
            'community_home_plan': community_home_plan
        })

    @http.route('/find-your-home/<path:path>', type='http', auth='public', website=True)
    def website_by_directory(self, path):
        """
        Handles incoming requests and routes them to the appropriate website
        based on the directory structure in the URL path.

        Args:
            path (str): The entire path portion of the URL.

        Returns:
            http.request: The response object containing website content.
        """

        # Define your routing logic here
        # This is a basic example, adapt based on your needs

        website_mappings = {
            'website1': '/website/1',  # Map '/website1' to website ID 1
            'website2': '/website/2',  # Map '/website2' to website ID 2
        }

        # Check if the path exists in the website mappings dictionary
        if path in website_mappings:
            # Extract the Odoo website ID from the mapped value
            website_id = website_mappings[path].split('/')[2]
            # print(website_id)
            #     website = request.env['website'].search([('id', '=', website_id)], limit=1)
            #     if website:
            #         request.env['website'].browse(website.id).set_request_website()
            #     return request.render('franchisor_theme.franchisor_homepage', {})
            # #
            # Set the website ID in the request context
            new_context = request.context.copy()
            new_context['website_id'] = website_id
            # Pass the modified context to your rendering function

            return http.request.render('franchisor_theme.franchisor_homepage', {}).with_context(new_context)
        # If the path doesn't match any mapping, return a 404 error
        # return request.not_found(message='Website not found')
        #
