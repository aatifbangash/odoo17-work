from odoo import models, fields


class Options(models.Model):
    _name = "module_sb.options"
    _description = "Options"
    # _table = "module_sb_options_group"
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char('Name', index='trigram', required=True)
    enabled = fields.Boolean(string='Enabled', default=True)
    option_classes_id = fields.Many2one('module_sb.option_classes', 'Class')
    option_categories_id = fields.Many2one('module_sb.option_categories', 'Category')
    option_locations_id = fields.Many2one('module_sb.option_locations', 'Location')
    option_id = fields.Char('Opt Sel ID')

    option_type = fields.Selection([
        ('attribute', 'Attribute'),
        ('binary', 'Binary'),
        ('quantity', 'Quantity'),
    ], string='Option Type', required=True, default='attribute')

    price_type = fields.Selection([('fixed', 'Fixed Price'), ('dynamic', 'Dynamic')], string='Price Type',
                                  default='fixed', required=True)
    units = fields.Selection([
        ('square_foot', 'Square Foot'),
        ('square', 'Square'),
        ('linear_foot', 'Linear Foot'),
        ('each', 'Each'),
        ('square', 'Square')
    ], string='Unit of Measure', default=None)
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The record already exists!'),
    ]
