import datetime
import secrets

from odoo import models, fields, api

INVALID_AUTH = "Invalid API key or Secret."


class RPCAuth(models.Model):
    _name = "rpc.auth"
    _description = "RPC Auth"


    name = fields.Char(required=True)
    user_id = fields.Many2one('res.users')

    api_key = fields.Char()
    secret = fields.Char()
    active = fields.Boolean(default=True)

    attempts = fields.Integer(default=0)
    expiration_date = fields.Date()

    @api.model
    def create(self, vals_list):
        ret = super(RPCAuth, self).create(vals_list)
        ret.generate_api()
        return ret

    def verify_key(self, api_key, secret_key, ip_address):
        invalid_auth = {"error": True, "message": INVALID_AUTH}
        if not api_key or not secret_key:
            return invalid_auth

        auth_attempts = self.env['rpc.auth.attempts']
        attempts = auth_attempts.search([('api_key', '=', api_key),
                                         ('ip_address', '=', ip_address)])
        if len(attempts) >= 5:
            return {"error": True, "message": f'Too many failed attempts from IP: {ip_address}. API Key is blocked'}

        key = self.search([('api_key', '=', api_key),
                           ('secret', '=', secret_key),
                           ('active', '=', True),
                           '|', ('expiration_date', '>=', datetime.date.today()),
                           ('expiration_date', '=', False)],
                          limit=1)

        if key:
            return {"user": key.user_id}
        else:
            auth_attempts.create({'ip_address': ip_address, 'api_key': api_key,})
            return invalid_auth

    def generate_api(self):
        self.write({
            'api_key': secrets.token_urlsafe(16),
            'secret': secrets.token_urlsafe(32)
        })


class AuthAttempts(models.Model):
    _name = "rpc.auth.attempts"

    ip_address = fields.Char()
    api_key = fields.Char()
