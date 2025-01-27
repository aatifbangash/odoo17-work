import base64
import json
from pprint import pprint

from odoo import http
from odoo.http import request


class HomePlansOptionsOverrideController(http.Controller):

    @http.route("/home_plan/option_override", methods=["POST"], type="http", auth="public", csrf=False,
                save_session=False,
                cors="*")
    def home_plan_option_override(self):

        option_request = request.httprequest.form
        plan_image_encoded = None

        if not option_request:
            option_request = json.loads(request.httprequest.data)

        plan_image = request.httprequest.files.getlist('image')
        if plan_image:
            plan_image = plan_image[0]
            plan_image_encoded = base64.b64encode(plan_image.read())

        if not option_request:
            return request.make_json_response({'data': 'Not found'}, status=404)

        company_id = int(option_request.get('company_id', request.env.company.id))

        search_query = [('id', '=', option_request['master_plan_option_id'])]
        master_plan_option = request.env['module_sb.master_plan_options'].sudo().search(search_query, limit=1)

        if not master_plan_option:
            return request.make_json_response({'data': "Record not found"}, status=404)

        if (not master_plan_option.homeplan_option_override_ids or
                (master_plan_option.homeplan_option_override_ids and
                 not master_plan_option.homeplan_option_override_ids.filtered(
                     lambda op: op.company_id.id == company_id and op.type == option_request['type'])
                )
        ):
            record = {
                'name': option_request['name'],
                'company_id': company_id,
                'price': option_request['price']
            }
            if option_request['type'] == 'option_value':

                record['description'] = option_request['description']
                record['quantity'] = option_request['quantity']
                record['type'] = option_request['type']
                if plan_image_encoded:
                    record['image'] = plan_image_encoded

            master_plan_option.homeplan_option_override_ids = [(0, 0, record)]
        else:
            record = {
                'name': option_request['name'],
                'price': option_request['price']
            }

            if option_request['type'] == 'option_value':
                record['description'] = option_request['description']
                record['quantity'] = option_request['quantity']
                if plan_image_encoded:
                    record['image'] = plan_image_encoded

            (master_plan_option.homeplan_option_override_ids
             .filtered(lambda op: op.company_id.id == company_id and op.type == option_request['type'])
             .write(record))

        return request.make_json_response({'data': "Record saved"}, status=200)

    # @http.route("/home_plan/option_override", methods=["POST"], type="http", auth="public", csrf=False,
    #             save_session=False,
    #             cors="*")
    # def home_plan_option_override(self):
    #
    #     option_request = json.loads(request.httprequest.data)
    #     if not option_request:
    #         return request.make_json_response({'data': 'Not found'}, status=404)
    #
    #     company_id = option_request.get('company_id') or request.env.company.id
    #
    #     search_query = [('id', '=', option_request['master_plan_option_id'])]
    #     master_plan_option = request.env['module_sb.master_plan_options'].sudo().search(search_query, limit=1)
    #
    #     if not master_plan_option:
    #         return request.make_json_response({'data': "Record not found"}, status=404)
    #
    #     if (not master_plan_option.homeplan_option_override_ids or
    #             (master_plan_option.homeplan_option_override_ids and
    #              not master_plan_option.homeplan_option_override_ids.filtered(
    #                  lambda op: op.company_id.id == company_id and op.type == option_request['type'])
    #             )
    #     ):
    #         record = {
    #             'name': option_request['name'],
    #             'company_id': company_id
    #         }
    #         if option_request['type'] == 'option_value':
    #             record['price'] = option_request['price']
    #             record['description'] = option_request['description']
    #             record['type'] = option_request['type']
    #
    #         master_plan_option.homeplan_option_override_ids = [(0, 0, record)]
    #     else:
    #         record = {
    #             'name': option_request['name']
    #         }
    #         if option_request['type'] == 'option_value':
    #             record['price'] = option_request['price']
    #             record['description'] = option_request['description']
    #
    #         (master_plan_option.homeplan_option_override_ids
    #          .filtered(lambda op: op.company_id.id == company_id and op.type == option_request['type'])
    #          .write(record))
    #
    #     return request.make_json_response({'data': "Record saved"}, status=200)

    # @http.route("/home_plan/option_value_override", methods=["POST"], type="http", auth="public", csrf=False,
    #             save_session=False,
    #             cors="*")
    # def home_plan_option_value_override(self):
    #     option_request = json.loads(request.httprequest.data)
    #     if not option_request:
    #         return request.make_json_response({'data': 'Not found'}, status=404)
    #
    #     company_id = option_request.get('company_id') or request.env.company.id
    #     master_plan_option = request.env['module_sb.master_plan_options'].sudo().search([
    #         ('id', '=', option_request['master_plan_option_id'])
    #     ], limit=1)
    #
    #     if (not master_plan_option.homeplan_option_override_ids or
    #             (master_plan_option.homeplan_option_override_ids and
    #              not master_plan_option.homeplan_option_override_ids.filtered(
    #                  lambda op: op.company_id.id == company_id and op.type == 'option_value')
    #             )
    #     ):
    #         master_plan_option.homeplan_option_override_ids = [(0, 0, {
    #             'name': option_request['name'],
    #             'description': option_request['description'],
    #             'price': option_request['price'],
    #             'company_id': company_id,
    #             'type': 'option_value'
    #         })]
    #     else:
    #         (master_plan_option.homeplan_option_override_ids
    #         .filtered(lambda op: op.company_id.id == company_id and op.type == 'option_value')
    #         .write({
    #             'name': option_request['name'],
    #             'description': option_request['description'],
    #             'price': option_request['price'],
    #         }))
    #
    #     return request.make_json_response({'data': "Record saved"}, status=200)
