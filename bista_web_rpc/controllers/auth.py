import json

from odoo import http
from odoo.http import request


class APIController(http.Controller):

    @http.route('/rpc/resource', type='json', auth='public', methods=['POST', "GET"], csrf=False)
    def get_resource(self, **kwargs):
        data = json.loads(request.httprequest.data.decode('utf-8')) or {}
        header = request.httprequest.headers
        api_key = header.get('api_key')
        secret_key = header.get('secret')

        ip_address = request.httprequest.remote_addr
        if not api_key or not secret_key:
            return json.dumps({"error": 'Missing API key or Secret key'})

        # Verify the API key and Secret key
        api_key_model = request.env['rpc.auth'].sudo()
        result = api_key_model.verify_key(api_key, secret_key, ip_address)
        if result.get("error", False):
            return json.dumps({"error": result.get("message")})

        method = data.get("method")
        object = data.get("object")
        domain = data.get("domain", [])
        order = data.get("order")
        limit = data.get("limit")
        fields = data.get("fields", ['id', 'display_name'])
        args = data.get("args", [])
        res_id = data.get("res_id", 0)
        vals = data.get("vals", {})
        user = result.get("user")
        object_method = data.get("function", False)

        print("Object ", object)
        print("Domain ", domain)
        print("Order ", order)
        print("MEthod ", method)

        if not method or not object:
            return json.dumps({"error": "Invalid method or object"})

        object_env = request.env[object].with_user(user)
        if method == "search":
            return object_env.search(domain,
                                     order=order or "create_date desc",
                                     limit=limit or False).ids
        elif method == "search_read":
            return object_env.search_read(domain,
                                          fields=fields,
                                          order=order or "create_date desc",
                                          limit=limit or False)
        elif method == "create":
            return object_env.create(vals).id

        elif method == "write":
            record = object_env.browse(res_id)
            return record.with_user(user).write(vals)

        elif method == "unlink":
            record = object_env.browse(res_id)
            return record.with_user(user).unlink()
        elif method == 'method':
            if not object_method:
                return json.dumps({"error": "Missing the method name to call."})

            record = object_env
            if res_id:
                record = object_env.browse(res_id)
            method = getattr(record, object_method)
            if args:
                return method(*args)
            else:
                return method()

        return json.dumps({"code": "Green"})
