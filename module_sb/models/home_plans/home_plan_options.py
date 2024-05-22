from odoo import models, fields


class HomePlanOptions(models.Model):
    _name = "module_sb.home_plan_options"
    _description = "Home Plan Options"
    _rec_name = 'option_group_id'
    _check_company_auto = True

    option_group_id = fields.Many2one("module_sb.master_plan_options", string='Master Plan Options')
    company_id = fields.Many2one('res.company', 'Company',
                                 readonly=True,
                                 default=lambda self: self.env.company)
    homeplan_id = fields.Many2one('product.template', string='Home Plans')

    # _sql_constraints = [
    #     ('home_plan_company_option_group_unique', 'unique (company_id, option_group)', 'The record already exists!'),
    # ]
