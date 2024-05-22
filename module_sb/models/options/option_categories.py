from odoo import models, fields


class OptionCategories(models.Model):
    _name = 'module_sb.option_categories'
    _description = 'Option Categories For Option Groups'
    _rec_name = 'name'

    name = fields.Char(string='Category', required=True)
