# -*- coding: utf-8 -*-

from odoo import models, fields


class MapItemStatus(models.Model):
    _name = 'map.item.status'
    _description = 'Map.item.state'

    name = fields.Char(required=1)
    fillColor = fields.Char()
    fillOpacity = fields.Float(default=1)
    strokeWeight = fields.Integer()
    strokeColor = fields.Char()
    strokeOpacity = fields.Float(default=0.8)
    zIndex = fields.Integer()
