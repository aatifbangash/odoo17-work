from odoo import models, fields


class OptionClasses(models.Model):
    _name = 'module_sb.option_classes'
    _description = 'Option Classes For Option Groups'
    _rec_name = 'name'

    name = fields.Char(string='Class Name', required=True)
