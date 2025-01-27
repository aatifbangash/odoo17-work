from odoo import models, fields


class Amenities(models.Model):
    _name = 'community_module.amenities'
    _description = 'Amenities'

    name = fields.Char(string='Name', size=128, required=True)
    description = fields.Text(string='Description')
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920, store=True, required=True)
    category_id = fields.Many2one('community_module.amenities_categories', string='Category', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    community_ids = fields.Many2many(
        'community_module.community',
        'community_amenities_rel',
        'amenities_id',
        'community_id'
    )
