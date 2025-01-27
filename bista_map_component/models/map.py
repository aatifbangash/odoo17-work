from odoo import fields, models


class Map(models.Model):
    _name = 'google.map'
    _description = 'Google Maps'

    name = fields.Char(required=True)
    map_id = fields.Char()
    init_zoom = fields.Integer()
    center_lat = fields.Float()
    center_lng = fields.Float()
    search = fields.Boolean(string='Search Bar', default=True)
