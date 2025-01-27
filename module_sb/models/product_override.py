# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductOverride(models.Model):
    _name = 'module_sb.product_override'
    _description = 'Product Template Override'

    base_price = fields.Float(string='Base Price')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    product_id = fields.Many2one('product.template', string='Product', required=True)
    type = fields.Selection([('master_plan', 'Master Plan'), ('plan', 'Plan'), ('community', 'Community')],
                            string='Type',
                            default='master_plan')
