from odoo import http
from odoo.http import request
from pprint import pprint


class WebsiteController(http.Controller):

    # @http.route('/', auth='public', website=True)
    # def index(self, **kw):
    #     is_franchisor = request.env.company.is_franchisor
    #     if not is_franchisor:
    #         home_plans = http.request.env['product.template'].sudo().search([
    #             ('is_published', '=', True),
    #             ('active', '=', True),
    #             ('franchise_homeplans_ids.company_id', '=', request.env.company.id),
    #             ('homeplan_community_ids', '!=', False),
    #             ('homeplan_community_ids.community_id.create_uid', '=', request.env.user.id),
    #         ])
    #
    #         ### check if module is installed
    #         # module_installed = request.env['ir.module.module'].sudo().search_count([
    #         #     ('name', '=', 'your_module_name'),
    #         #     ('state', '=', 'installed')
    #         # ]) > 0
    #
    #         # pprint(home_plans.read(['name', 'legal_name', 'default_code']))
    #         communities = http.request.env['community_module.community'].sudo().search([
    #             ('is_active', '=', True),
    #             ('create_uid', '=', request.env.user.id),
    #         ])
    #         return http.request.render('theme_sb.custom_homepage', {
    #             'communities': communities,
    #             'home_plans': home_plans
    #         })
    #     else:
    #         return http.request.render('franchisor_theme.franchisor_homepage', {})

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

    # @http.route('/community_plan/<int:community_id>', type="http", auth="public", website=True)
    # def community_plan(self, community_id, **kw):
    #     community_home_plan = http.request.env['community_module.community'].sudo().search([
    #         ('id', '=', community_id),
    #         ('is_active', '=', True),
    #         ('create_uid', '=', request.env.user.id),
    #     ], limit=1)
    #     print(community_home_plan)
    #     return http.request.render('theme_sb.community_plan', {
    #         'community_home_plan': community_home_plan
    #     })
