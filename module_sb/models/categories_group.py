from odoo import models, fields


class CategoriesGroup(models.Model):
    _name = 'module_sb.categories_group'
    _description = 'Categories Group'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
