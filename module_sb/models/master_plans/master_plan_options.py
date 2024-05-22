from odoo import models, fields, api


class MasterPlanOptions(models.Model):
    _name = "module_sb.master_plan_options"
    _description = "Master Plan Options"

    options_id = fields.Many2one('module_sb.options', string='Options')
    options_related_category_id = fields.Integer(related='options_id.option_categories_id.id', store=False, string="")
    option_values_id = fields.Many2one('module_sb.option_values', string='Option Values')
    homeplan_id = fields.Many2one('product.template', string='Home Plans')

    @api.depends('options_id', 'option_values_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.options_id.name} / {record.option_values_id.name}"
