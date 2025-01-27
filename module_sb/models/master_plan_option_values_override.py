from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MasterPlanOptionValuesOverride(models.Model):
    _name = "module_sb.master_plan_option_values_override"
    _description = "Master Plan Option Values Override"

    name = fields.Char(string='Name')
    image = fields.Image("Image", max_width=1920, max_height=1920)
    description = fields.Text(string='Description')

