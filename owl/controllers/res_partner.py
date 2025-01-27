from odoo import http
from pprint import pprint
import json

class ResPartner(http.Controller):
    @http.route('/owl/rpc_service', type='json', auth='user')
    def get_customers(self, limit):
        return http.request.env['product.template'].search_read([], ['name'], limit=limit)

    @http.route('/owl/fetch_api', type='http', auth='public', methods=['GET'])
    def get_customers_fetch_api(self):
        data = http.request.env['product.template'].sudo().search_read([], ['name'])
        return json.dumps(data)

    @http.route('/v1/api', type='http', auth='none')
    def get_customers_api(self, limit=10):
        # response = http.request.env['res.partner'].sudo().search_read([], ['name', 'email'], limit=limit)
        env = http.request.env
        cr = env.cr
        cr.execute("SELECT name, email FROM res_partner ORDER BY id desc LIMIT %s", (limit,))
        # response = cr.fetchall()
        response = cr.dictfetchall()
        return http.Response(json.dumps(response), content_type='application/json', status=200)

    # @http.route('/owl/dashboard_service', type='json', auth='user')
    # def dashboard_service(self):
    #     partner = http.request.env['res.partner']
    #     return {
    #         "partners": partner.search_count([]),
    #         "customers": partner.search_count([('is_company', '=', True)]),
    #         "individuals": partner.search_count([('is_company', '=', False)]),
    #         "locations": len(partner.read_group([], ['state_id'], ['state_id'])),
    #     }
