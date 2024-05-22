from odoo import models, fields, api


class SBPartner(models.Model):
    _inherit = "res.company"

    kova_bunit_rid = fields.Integer(string='Kova BUnit RID')
    code = fields.Char(string='Code', size=8)
    legal_name = fields.Char(string='Legal Name', size=128)
    description = fields.Text(string='Description')
    latitude = fields.Char(string='Latitude', size=128, default='0')
    longitude = fields.Char(string='Longitude', size=128, default='0')
    is_franchisor = fields.Boolean(string='Is Franchisor', default=False)
