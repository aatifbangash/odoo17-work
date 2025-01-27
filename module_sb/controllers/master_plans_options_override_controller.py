import base64
import json
import math
from pprint import pprint

from odoo import http
from odoo.http import request


class MasterPlansOptionsOverrideController(http.Controller):

    @http.route("/master_plan/option_override", methods=["POST"], type="http", auth="public", csrf=False,
                save_session=False,
                cors="*")
    def master_plan_option_override(self):
        option_request = json.loads(request.httprequest.data)
        if not option_request:
            return request.make_json_response({'data': 'Not found'}, status=404)

        options = request.env['module_sb.master_plan_options'].sudo().search([
            ('options_id', '=', option_request['option_id']),
            ('homeplan_id', '=', option_request['homeplan_id'])
        ])

        if not options:
            return request.make_json_response({'data': "Record not found"}, status=404)

        masterplan_options = None
        for option in options:
            if option.option_override_id:
                masterplan_options = option
                break

        if not masterplan_options:  # create
            masterplan_options = options[0]
            new_option_override_id = masterplan_options.option_override_id.create({
                'name': option_request['name']
            })

            if new_option_override_id:
                options.write({
                    'option_override_id': new_option_override_id.id
                })
        else:  # update
            masterplan_options.option_override_id.write({
                'name': option_request['name']
            })

            options.filtered(lambda op: not op.option_override_id).write({
                'option_override_id': masterplan_options.option_override_id
            })

        return request.make_json_response({'data': "Record saved"}, status=200)

    # @http.route("/master_plan/option_value_override/backup", methods=["POST"], type="http", auth="public", csrf=False,
    #             save_session=False,
    #             cors="*")
    # def master_plan_option_value_override_BACKUP(self):
    #     option_value_request = json.loads(request.httprequest.data)
    #     if not option_value_request:
    #         return request.make_json_response({'data': 'Not found'}, status=404)
    #
    #     masterplan_option = request.env['module_sb.master_plan_options'].sudo().search([
    #         ('id', '=', option_value_request.get('master_plan_option_id'))
    #     ])
    #
    #     if not masterplan_option.option_value_override_id:  # create
    #         new_option_value_override_id = masterplan_option.option_value_override_id.create({
    #             'name': option_value_request.get('name'),
    #             'description': option_value_request.get('description')
    #         })
    #
    #         if new_option_value_override_id:
    #             masterplan_option.write({
    #                 'option_value_override_id': new_option_value_override_id.id
    #             })
    #     else:  # update
    #         masterplan_option.option_value_override_id.write({
    #             'name': option_value_request.get('name'),
    #             'description': option_value_request.get('description')
    #         })
    #
    #     quantity = option_value_request.get('quantity')
    #     if masterplan_option and quantity:
    #         masterplan_option.quantity = quantity
    #
    #     return request.make_json_response({'data': "Record saved"}, status=200)


    @http.route("/master_plan/option_value_override", methods=["POST"], type="http", auth="public", csrf=False,
                save_session=False,
                cors="*")
    def master_plan_option_value_override(self):
        option_value_request = request.httprequest.form
        if not option_value_request:
            return request.make_json_response({'data': 'Not found'}, status=404)

        plan_image_encoded = None
        plan_image = request.httprequest.files.getlist('image')
        if plan_image:
            plan_image = plan_image[0]
            plan_image_encoded = base64.b64encode(plan_image.read())

        masterplan_option = request.env['module_sb.master_plan_options'].sudo().search([
            ('id', '=', option_value_request['master_plan_option_id'])
        ])

        if not masterplan_option.option_value_override_id:  # create
            override_record = {
                'name': option_value_request['name'],
                'description': option_value_request['description'],
            }
            if plan_image_encoded:
                override_record['image'] = plan_image_encoded

            new_option_value_override_id = masterplan_option.option_value_override_id.create(override_record)

            if new_option_value_override_id:
                masterplan_option.write({
                    'option_value_override_id': new_option_value_override_id.id
                })
        else:  # update
            override_record = {
                'name': option_value_request['name'],
                'description': option_value_request['description']
            }
            if plan_image_encoded:
                override_record['image'] = plan_image_encoded

            masterplan_option.option_value_override_id.write(override_record)

        quantity = option_value_request.get('quantity')
        quantity_value_check = float(quantity)
        if masterplan_option and quantity is not None and not math.isnan(quantity_value_check):
            masterplan_option.quantity = quantity

        return request.make_json_response({'data': "Record saved"}, status=200)

    # @http.route("/v2/master_plan/option_override", methods=["POST"], type="http", auth="public", csrf=False,
    #             save_session=False,
    #             cors="*")
    # def master_plan_option_override_v2(self):
    #     option_request = json.loads(request.httprequest.data)
    #     if not option_request:
    #         return request.make_json_response({'data': 'Not found'}, status=404)
    #
    #     master_plan_option = request.env['module_sb.master_plan_options'].sudo().search([
    #         ('id', '=', option_request['master_plan_option_id']),
    #         ('is_title', '=', True)
    #     ])
    #
    #     if not master_plan_option:
    #         return request.make_json_response({'data': "Record not found"}, status=404)
    #
    #     if not master_plan_option.option_override_id:  # create
    #         new_option_override_id = request.env['module_sb.master_plan_options_override'].create(
    #             {'name': option_request['name']}
    #         )
    #         master_plan_option.option_override_id = new_option_override_id
    #     else:
    #         master_plan_option.option_override_id.write({
    #             'name': option_request['name']
    #         })
    #
    #     return request.make_json_response({'data': "Record saved"}, status=200)
