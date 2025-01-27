from pprint import pprint

from odoo import models, fields, api


class HomePlanOptions(models.Model):
    _name = "module_sb.home_plan_options"
    _description = "Home Plan Options"
    _rec_name = 'master_plan_options_id'
    _check_company_auto = True

    master_plan_options_id = fields.Many2one("module_sb.master_plan_options", string='Master Plan Options')
    company_id = fields.Many2one('res.company', 'Company',
                                 readonly=True,
                                 default=lambda self: self.env.company)
    homeplan_id = fields.Many2one('product.template', string='Home Plans')
    is_active = fields.Boolean(string='Active', default=True)
    is_base = fields.Boolean(string='Base', default=None)

    options_id = fields.Many2one(related="master_plan_options_id.options_id", store=False, string="Options")
    option_values_id = fields.Many2one(related="master_plan_options_id.option_values_id", store=False,
                                       string="Option Value")

    computed_homeplan_option_override = fields.Many2one('module_sb.home_plan_options_override', string='Override',
                                                        compute='_compute_override', store=False)

    # transient_field = fields.Many2one('module_sb.home_plan_options_transient',
    #                                   string='Transient Field',
    #                                   compute="_compute_override_info"
    #                                   )

    @api.depends('options_id')
    def _compute_override_info(self):
        for record in self:
            # Create an instance of the transient model
            override_info = self.env['module_sb.home_plan_options_transient'].create({})

            override_info.name = 'test'
            override_info.price = 123
            override_info.is_override = True

            record.transient_field = override_info

    @api.depends('options_id')
    def _compute_override(self):
        for record in self:
            override = self.env['module_sb.home_plan_options_override'].search([
                ('masterplan_option_id.options_id', '=', record.options_id.id),
                ('company_id', '=', record.company_id.id),
                ('type', '=', 'option')
            ], limit=1)
            record.computed_homeplan_option_override = override if override else False

    # WIll test later
    def write(self, vals):
        if 'is_active' in vals and not vals['is_active']:
            (self.env['community_module.community_homeplans_options']
             .search([('homeplan_option_id', 'in', self.ids)])
             .write({'is_active': False}))

        return super(HomePlanOptions, self).write(vals)

    # @api.autovacuum
    # def _clean_old_records(self):
    #     pprint('heeer clean')
    #     self.env['module_sb.home_plan_options_transient'].search([]).unlink()


# class HomePlanOptionsTransient(models.TransientModel):
#     _name = 'module_sb.home_plan_options_transient'
#     _description = 'Home plan options transient'
#     _transient_max_hours = 0.016666666666667
#     _transient_max_count = 5
#
#     name = fields.Char(string='Name')
#     price = fields.Float(string='Price')
#     is_override = fields.Boolean(string='Override')
