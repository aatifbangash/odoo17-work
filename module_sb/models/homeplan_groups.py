from odoo import models, fields


class HomePlanGroups(models.Model):
    _name = 'module_sb.homeplan.groups'
    _description = 'Home Plan Groups'

    type = fields.Many2one("product.category", string='Type')
    style = fields.Many2one("product.category", string='Style')
    homeplan_id = fields.Many2one('product.template', string='Home Plans')
