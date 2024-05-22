# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ModuleSBHomePlans(models.Model):
    _inherit = "product.template"

    kova_model_rid = fields.Integer(string='Kova Model Rid')
    legal_name = fields.Char(string='Legal Name', size=128)
    is_published = fields.Boolean(string='Published', default=True)
    category_groups = fields.Many2many('product.category', string="Category Groups")

    # attributes
    homeplan_groups = fields.One2many('module_sb.homeplan.groups', 'homeplan_id', string='Groups')

    # base options (replaced with master_plan_option_ids)
    # homeplan_options = fields.One2many('module_sb.homeplan.options', 'homeplan_id', string='Options')

    # master plan options
    master_plan_options_ids = fields.One2many('module_sb.master_plan_options', 'homeplan_id',
                                              string='Master Plan Options')
    home_plan_options_ids = fields.One2many('module_sb.home_plan_options', 'homeplan_id',
                                              string='Home Plan Options')
    # checkbox to enable home plan for franchise
    enable = fields.Boolean(string='Enable', default=False, store=False, compute='_compute_enable')
    # franchise enabled home plans
    franchise_homeplans_ids = fields.One2many('module_sb.franchise_homeplans', 'homeplan_id',
                                              string='Franchise Home plans')
    is_franchise_admin = fields.Boolean(string='Is Franchise Admin', store=False, compute='_compute_franchise_admin')

    # franchise selected home plan options (based on base selected options) (replaced with home_plan_options_ids)
    # homeplan_franchise_options = fields.One2many('module_sb.franchise.options', 'homeplan_id',
    #                                              string='Franchise Options')
    base_price = fields.Float(string='Base Price', default=0.00)
    incentive_price = fields.Float(string='Incentive Price', default=0.00)
    price = fields.Float(string='Price', default=0.00)

    min_bedrooms = fields.Integer(string='Min Bedrooms', default=0)
    max_bedrooms = fields.Integer(string='Max Bedrooms', default=0)
    min_bathrooms = fields.Integer(string='Min Bathrooms', default=0)
    max_bathrooms = fields.Integer(string='Max Bathrooms', default=0)
    base_heated_square_feet = fields.Integer(string='Base Heated Square Feet', default=0)
    max_heated_square_feet = fields.Integer(string='Max Heated Square Feet', default=0)
    base_total_square_feet = fields.Integer(string='Base Total Square Feet', default=0)
    max_total_square_feet = fields.Integer(string='Max Total Square Feet', default=0)

    def _compute_franchise_admin(self):
        self.is_franchise_admin = self.env.user.has_group('module_sb.franchise_admin')

    @api.depends('franchise_homeplans_ids')
    def _compute_enable(self):
        self.enable = False
        for row in self.franchise_homeplans_ids:
            if row.company_id == self.env.company:
                self.enable = True
                break

    @api.onchange('enable')
    def changed_enable(self):
        if self.enable:
            # Check if record with matching company_id exists
            existing_record = self.franchise_homeplans_ids.filtered(
                lambda record: record.company_id == self.env.company
            )
            if not existing_record:
                # Create new record if none exists # [(0, 0, value)]
                self.update({
                    'franchise_homeplans_ids': [(fields.Command.create({'company_id': self.env.company.id}))]
                })
        else:
            # Clear all existing records [(5,0,0)]
            for record in self.franchise_homeplans_ids:
                if record.company_id == self.env.company:
                    self.update({
                        'franchise_homeplans_ids': [(fields.Command.delete(record.id))]
                    })

    # @api.onchange('is_published')
    # def changed_published(self):
    #     company_name = [company.name for company in self.env.user.company_ids]
    #     print(self.env)
    #     pass


class HomePlanGroups(models.Model):
    _name = 'module_sb.homeplan.groups'
    _description = 'Home Plan Groups'

    type = fields.Many2one("product.category", string='Type')
    style = fields.Many2one("product.category", string='Style')
    homeplan_id = fields.Many2one('product.template', string='Home Plans')


# model to hold base options for master plan
class HomePlanOptions(models.Model):
    _name = 'module_sb.homeplan.options' # replaced with module_sb.master_plan_options
    _description = 'Home Plan Options'
    _rec_name = 'option_group_name'

    option_group_id = fields.Many2one("module_sb.options_group", string='Option Group',
                                      domain="[('parent_id', '=', False), ('enabled', '=', True)]")
    option_group_name = fields.Char(string="Option Group Name", related='option_group_id.name', store=True,
                                    readonly=False)

    option_name_id = fields.Many2one("module_sb.options_group", string='Option Name')
    option_set_name = fields.Char(string="Option Set Name", related='option_name_id.name', store=True, readonly=False)
    homeplan_id = fields.Many2one('product.template', string='Home Plans')
    domain_check = fields.Char(compute='_compute_domain_check')

    @api.depends('option_group_id')
    def _compute_domain_check(self):
        for record in self:
            record.domain_check = "[(0, '=', 1)]"
            if record.option_group_id:
                record.domain_check = f"[('parent_id', '=', {record.option_group_id.id})]"

    @api.depends('option_group_id', 'option_name_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.option_group_name} / {record.option_set_name}"


class HomePlanFranchiseOptions(models.Model):
    _name = 'module_sb.franchise.options' # replaced with module_sb.home_plan_options
    _description = 'Home Plan Franchise Options'
    _rec_name = 'option_group_id'
    _check_company_auto = True

    option_group_id = fields.Many2one("module_sb.homeplan.options", string='Option Group')
    # display_name = fields.Char(string="Display Name", related='option_group.option_set_name', store=True)
    # option_group_name = fields.Char(string="Option Group Name", related='option_group_id.option_group_name', store=True,
    #                                 readonly=False)
    homeplan_id = fields.Many2one('product.template', string='Home Plans')
    company_id = fields.Many2one('res.company', 'Company',
                                 readonly=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('company_option_group_unique', 'unique (company_id, option_group)', 'The record already exists!'),
    ]


class FranchiseHomePlan(models.Model):
    _name = 'module_sb.franchise_homeplans'
    _description = 'Franchise Home Plans'
    _check_company_auto = True

    homeplan_id = fields.Many2one('product.template', string='Home Plans')
    company_id = fields.Many2one('res.company', 'Company',
                                 readonly=True,
                                 default=lambda self: self.env.company)
