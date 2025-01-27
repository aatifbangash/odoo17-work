from odoo import models, fields


class ProductOverrideInherit(models.Model):
    _inherit = "module_sb.product_override"
    _description = "Product Override Inherit"

    community_homeplan_id = fields.Many2one('community_module.community_homeplans', string='Community Home Plan')
