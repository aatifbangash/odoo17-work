import base64
import json
from pprint import pprint

from odoo import http
from odoo.http import request


class CommunityHomePlansOptionsOverride(http.Controller):

    @http.route("/community/home_plan/option_override", methods=["POST"], type="http", auth="public", csrf=False,
                save_session=False,
                cors="*")
    def community_home_plan_option_override(self):
        option_request = request.httprequest.form

        if not option_request:
            option_request = json.loads(request.httprequest.data)

        if not option_request:
            return request.make_json_response({'data': 'Not found'}, status=404)

        home_plan_option = request.env['module_sb.home_plan_options'].sudo().search([
            ('id', '=', option_request['homeplan_option_id'])
        ], limit=1)

        if not home_plan_option:
            return request.make_json_response({'data': "Record not found"}, status=404)

        plan_image_encoded = None
        plan_image = request.httprequest.files.getlist('image')
        if plan_image:
            plan_image = plan_image[0]
            plan_image_encoded = base64.b64encode(plan_image.read())

        if (not home_plan_option.community_homeplan_option_override_ids or
                (home_plan_option.community_homeplan_option_override_ids and
                 not home_plan_option.community_homeplan_option_override_ids.filtered(
                     lambda op: op.community_homeplan_id.id == int(option_request[
                                                                       'community_homeplan_id']) and op.type ==
                                option_request['type'])
                )
        ):
            record = {
                'name': option_request['name'] or None,
                'community_homeplan_id': option_request['community_homeplan_id'],
            }

            new_price = 0.00
            if option_request.get('price') and float(option_request.get('price')) > 0:
                new_price = option_request.get('price')
            record['price'] = new_price

            if option_request['type'] == 'option_value':
                record['description'] = option_request['description']
                record['quantity'] = option_request['quantity']
                record['type'] = option_request['type']
                if plan_image_encoded:
                    record['image'] = plan_image_encoded

            home_plan_option.community_homeplan_option_override_ids = [(0, 0, record)]
        else:
            record = {
                'name': option_request['name'] or None,
            }

            new_price = 0.00
            if option_request.get('price') and float(option_request.get('price')) > 0:
                new_price = option_request.get('price')

            record['price'] = float(new_price)

            if option_request['type'] == 'option_value':
                record['description'] = option_request['description']
                record['quantity'] = option_request['quantity']
                if plan_image_encoded:
                    record['image'] = plan_image_encoded

            (home_plan_option.community_homeplan_option_override_ids
             .filtered(lambda op: op.community_homeplan_id.id == int(option_request[
                                                                         'community_homeplan_id']) and op.type ==
                                  option_request['type'])
             .write(record))

        return request.make_json_response({'data': "Record saved"}, status=200)
    # Before Image
    # def community_home_plan_option_override(self):
    #     option_request = json.loads(request.httprequest.data)
    #     if not option_request:
    #         return request.make_json_response({'data': 'Not found'}, status=404)
    #
    #     home_plan_option = request.env['module_sb.home_plan_options'].sudo().search([
    #         ('id', '=', option_request['homeplan_option_id'])
    #     ], limit=1)
    #
    #     if not home_plan_option:
    #         return request.make_json_response({'data': "Record not found"}, status=404)
    #
    #     if (not home_plan_option.community_homeplan_option_override_ids or
    #             (home_plan_option.community_homeplan_option_override_ids and
    #              not home_plan_option.community_homeplan_option_override_ids.filtered(
    #                  lambda op: op.community_homeplan_id.id == option_request[
    #                      'community_homeplan_id'] and op.type == option_request['type'])
    #             )
    #     ):
    #         record = {
    #             'name': option_request['name'] or None,
    #             'community_homeplan_id': option_request['community_homeplan_id'],
    #         }
    #         if option_request.get('price'):
    #             record['price'] = option_request['price']
    #         if option_request['type'] == 'option_value':
    #             record['description'] = option_request['description']
    #             record['type'] = option_request['type']
    #
    #         home_plan_option.community_homeplan_option_override_ids = [(0, 0, record)]
    #     else:
    #         record = {
    #             'name': option_request['name'] or None,
    #         }
    #         if option_request.get('price'):
    #             record['price'] = option_request['price']
    #         if option_request['type'] == 'option_value':
    #             record['description'] = option_request['description']
    #
    #         (home_plan_option.community_homeplan_option_override_ids
    #          .filtered(lambda op: op.community_homeplan_id.id == option_request[
    #             'community_homeplan_id'] and op.type == option_request['type'])
    #          .write(record))
    #
    #     return request.make_json_response({'data': "Record saved"}, status=200)
