from odoo import http


class CommunityController(http.Controller):
    @http.route('/community', auth='public')
    def index(self, **kw):
        return "hello world"

    @http.route('/community/objects', auth='public', website=True)
    def list(self, **kw):
        return http.request.render('community_module.listing', {
            'root': '/community',
            'objects': http.request.env['community_module.community'].search([]),
        })

    @http.route('/community/objects/<model("community_module.community"):obj>', auth='public', website=True)
    def object(self, obj, **kw):
        return http.request.render('community_module.single', {
            'object': obj
        })

    # @http.route('/division', auth='public', website=True)
    # def index(self, **kw):
    #     # communities = http.request.env['community_module.community'].sudo().search([])
    #     # print(communities)
    #     return http.request.render('community_module.custom_division', {
    #         'name': 'Divisions',
    #         # 'communities': communities
    #     })
