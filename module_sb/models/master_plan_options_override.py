from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MasterPlanOptionsOverride(models.Model):
    _name = "module_sb.master_plan_options_override"
    _description = "Master Plan Options Override"

    name = fields.Char(string='Name')

