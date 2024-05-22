from odoo import models, fields, api


class SBCategory(models.Model):
    _inherit = "product.category"
    _rec_name = "name"

    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='active', string="Status", required=True)
    read_only = fields.Boolean(string="Read Only", default=False)
    categories_group = fields.Many2one('module_sb.categories_group', string="Categories Group")
