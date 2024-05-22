from odoo import models, fields, api


class SBUsers(models.Model):
    _inherit = "res.users"

    is_franchisor = fields.Boolean(string='Is Franchisor', default=False)
