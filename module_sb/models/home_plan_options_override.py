from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HomePlanOptionsOverride(models.Model):
    _name = "module_sb.home_plan_options_override"
    _description = "Home Plan Options Override"

    masterplan_option_id = fields.Many2one('module_sb.master_plan_options')
    name = fields.Char(string='Name')
    price = fields.Float(string='Price', default=0.0)
    quantity = fields.Integer(string='Qantity', default=0)
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    type = fields.Selection([('option', 'Option'), ('option_value', 'Option Value')], string='Type', default='option')
    image = fields.Image("Image", max_width=1920, max_height=1920)
    # is_base = fields.Boolean(string='Base', default=False)