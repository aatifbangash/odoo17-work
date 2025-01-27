from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MasterPlanOptions(models.Model):
    _name = "module_sb.master_plan_options"
    _description = "Master Plan Options"

    options_id = fields.Many2one('module_sb.options', string='Options')
    options_related_category_id = fields.Integer(related='options_id.option_categories_id.id', store=False, string="")
    option_values_id = fields.Many2one('module_sb.option_values', string='Option Values')
    homeplan_id = fields.Many2one('product.template', string='Home Plans')
    is_active = fields.Boolean(string='Active', default=True)
    is_base = fields.Boolean(string='Base', default=False)
    is_title = fields.Boolean(string='Title Option', default=False)
    quantity = fields.Integer(string='Quantity', default=None)
    option_override_id = fields.Many2one('module_sb.master_plan_options_override', string='Override Option Name',
                                         default=False)
    option_value_override_id = fields.Many2one('module_sb.master_plan_option_values_override',
                                               string='Override Option Value Name', default=False)
    homeplan_option_override_ids = fields.One2many('module_sb.home_plan_options_override', 'masterplan_option_id',
                                                   string='Override Home Plan Option Name')

    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.options_id.name} / {record.option_values_id.name}"

    @api.onchange('option_values_id')
    def _rest_option_values(self):
        for l in self.homeplan_id.master_plan_options_ids:
            print(l.option_values_id)
        # self.option_values_id = False

    @api.constrains('option_values_id')
    def _check_for_unique_records(self):
        pass
        # print(self.option_values_id)
        # for record in self:
        #     print(record)
        # print(self.option_values_id)
        # self.option_values_id = False
        # print(record)
        # if existing_record:
        #     raise ValidationError("The combination of Options and Option Values must be unique.")
    # WIll test later
    def write(self, vals):
        if 'is_active' in vals and not vals['is_active']:
            (self.env['module_sb.home_plan_options']
             .search([('master_plan_options_id', 'in', self.ids)])
             .write({'is_active': False}))

        return super(MasterPlanOptions, self).write(vals)
