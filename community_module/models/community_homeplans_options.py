from pprint import pprint

from odoo import models, fields


class CommunityHomePlanOptions(models.Model):
    _name = 'community_module.community_homeplans_options'
    _description = 'Community Home Plans options'

    community_homeplan_id = fields.Many2one('community_module.community_homeplans', string='Community Home Plans',
                                            ondelete='cascade', required=True)
    homeplan_option_id = fields.Many2one('module_sb.home_plan_options', string='Home Plans Options',
                                         domain="[('homeplan_id', '=', community_homeplan_id_related)]",
                                         )
    community_homeplan_id_related = fields.Integer(related='community_homeplan_id.homeplan_id.id', store=False,
                                                   string="")
    is_active = fields.Boolean(string='Active', default=True)
    is_base = fields.Boolean(string='Base', default=False)

    options_id = fields.Many2one(related="homeplan_option_id.options_id", store=False, string="Options")
    option_values_id = fields.Many2one(related="homeplan_option_id.option_values_id", store=False,
                                       string="Option Value")


    # domain_check = fields.Integer(compute='_compute_domain_check')
    # @api.depends('community_homeplan_id')
    # def _compute_domain_check(self):
    #     for record in self:
    #         record.domain_check = record.community_homeplan_id.homeplan_id.id
