# -*- coding: utf-8 -*-
from odoo import models, fields


class MapCoordinate(models.Model):
    _name = 'google.map.coordinate'
    _description = 'Google Maps Coordinates'

    lat = fields.Char()
    lng = fields.Char()
    map_item_id = fields.Many2one('google.map.item', 'Google Maps Item')
