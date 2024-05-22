from odoo import models, fields


class OptionLocations(models.Model):
    _name = 'module_sb.option_locations'
    _description = 'Option Locations For Option Groups'
    _rec_name = 'name'

    name = fields.Char(string='Location', required=True)
