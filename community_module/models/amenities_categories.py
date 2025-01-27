from odoo import models, fields


class AmenitiesCategories(models.Model):
    _name = 'community_module.amenities_categories'
    _description = 'Amenities Categories'

    name = fields.Char(string='Name', size=128, required=True)
    icon = fields.Char(string='Icon', size=128, required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
