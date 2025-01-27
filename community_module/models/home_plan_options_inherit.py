from odoo import models, fields


class CommunityHomePlanOptionsInherit(models.Model):
    _inherit = "module_sb.home_plan_options"
    _description = "Community Home Plan Options Inherit"

    community_homeplan_option_override_ids = fields.One2many('community_module.community_home_plan_options_override',
                                                             'homeplan_option_id',
                                                             string='Override Community Home Plan Option Name')
