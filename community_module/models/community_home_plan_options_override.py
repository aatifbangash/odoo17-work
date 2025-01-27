from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CommunityHomePlanOptionsOverride(models.Model):
    _name = "community_module.community_home_plan_options_override"
    _description = "Community Home Plan Options Override"

    homeplan_option_id = fields.Many2one('module_sb.home_plan_options')
    community_homeplan_id = fields.Many2one('community_module.community_homeplans', ondelete='cascade')
    name = fields.Char(string='Name')
    price = fields.Float(string='Price', default=0.0)
    quantity = fields.Integer(string='Quantity', default=0)
    description = fields.Text(string='Description')
    image = fields.Image("Image", max_width=1920, max_height=1920)
    type = fields.Selection([('option', 'Option'), ('option_value', 'Option Value')], string='Type', default='option')
