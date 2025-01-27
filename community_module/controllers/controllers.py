from odoo import http


class CommunityController(http.Controller):
    @http.route('/community', auth='public')
    def index(self, **kw):
        return "hello world"


