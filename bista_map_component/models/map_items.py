# -*- coding: utf-8 -*-
import base64
from collections import defaultdict

import pygeoif.geometry
from fastkml import kml
from odoo import models, fields, api
from odoo.tools import json


class MapItem(models.Model):
    _name = 'google.map.item'
    _description = 'Google Maps Item'

    sequence = fields.Integer(default=1)
    google_map_id = fields.Many2one('google.map', string='Google Maps Map')
    status_id = fields.Many2one('map.item.status')
    name = fields.Char()
    type = fields.Selection([('community', 'Community'), ('home', 'Lot')], default="community")
    active = fields.Boolean(default=True)

    community_id = fields.Many2one("google.map.item")
    section_id = fields.Many2one("google.map.item")
    home_plan_ids = fields.One2many('google.map.item', 'section_id')
    section_ids = fields.One2many('google.map.item', 'community_id')

    # Individual Click Event
    click_event = fields.Selection([('html', 'HTML'), ('url', 'URL')])
    content_html = fields.Text()
    content_url = fields.Char()

    # Coordinates Json and ids
    coordinate_ids = fields.One2many('google.map.coordinate', 'map_item_id')
    coordinates = fields.Text(compute="_get_coordinates")

    content_ids = fields.One2many('map.item.content', 'map_item_id')
    zoom_content = fields.Text(compute="_get_zoom_content")

    # KML
    kml_file = fields.Binary()
    reload_home_plans = fields.Boolean()
    group_name = fields.Char()

    # Shape
    shape_type = fields.Selection([
        ('polygon', 'Polygon'),
        ('polyline', 'polyline'),
        ('circle', 'Circle'),
        ('rectangle', 'Rectangle'),
        ('marker', "Marker")
    ], default="polygon")
    shape_css = fields.Text()

    fill_type = fields.Selection([
        ('color', 'Color'),
        ('image', 'Image')
    ], default="color")
    fillColor = fields.Char()
    fillOpacity = fields.Char()
    background_image = fields.Binary()
    file_type = fields.Char()

    strokeWeight = fields.Integer()
    strokeColor = fields.Char()

    # Marker
    marker_icon = fields.Binary()
    marker_content = fields.Text()
    marker_header = fields.Text()
    marker_footer = fields.Text()
    marker_zoom = fields.Integer(default=15)
    marker_lat = fields.Float()
    marker_lng = fields.Float()

    # Circle
    radius = fields.Float()

    def write(self, vals):
        background_image = vals.get("background_image", "")
        if background_image and "," in background_image:
            image_data = background_image.split(",")
            vals['background_image'] = image_data[1]
            vals['file_type'] = image_data[0]
        return super().write(vals)

    @api.model
    def _get_field_list(self):
        field_list = self.env['ir.model.fields'].search([('model_id.model', '=', 'google.map.item')])
        return field_list.mapped("name")

    @api.model
    def parseCoordinates(self, coordinates):
        return [(0, 0, rec) for rec in coordinates]

    @api.depends('coordinate_ids.lat', 'coordinate_ids.lng')
    def _get_coordinates(self):
        for record in self:
            record.coordinates = json.dumps([[cord.lat, cord.lng] for cord in record.coordinate_ids])

    @api.depends("content_ids")
    def _get_zoom_content(self):
        for record in self:
            contents = defaultdict(dict)
            for zoom in record.content_ids:
                if zoom.name == 'html':
                    content = zoom.html_content
                elif zoom.name == 'css':
                    content = zoom.css_content
                else:
                    content = zoom.image_url
                contents[zoom.zoom_level] = {
                    'type': zoom.name,
                    'content': content,
                }
            record.zoom_content = json.dumps(contents)

    def create_shapes(self):
        feature_list = []
        if self.reload_home_plans:
            self.home_plan_ids.unlink()
            self.coordinate_ids.unlink()

        if self.kml_file:
            raw_data = base64.b64decode(self.kml_file).decode('utf-8')
            raw_data = raw_data.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
            raw_data = raw_data.replace('http://earth.google.com/kml/2.1', 'http://www.opengis.net/kml/2.2')

            k = kml.KML.class_from_string(raw_data)
            features = k.features[0].features if len(k.features) > 0 else []
            for item in features:
                for feature in item.features:
                    if isinstance(feature.geometry, pygeoif.geometry.MultiPolygon):
                        continue
                    feature_list.append({
                        'name': feature.name,
                        'type': 'home',
                        'coordinate_ids': [(0, 0, {'lat': rec[1], 'lng': rec[0]}) for rec in
                                           feature.geometry.coords[0]],
                        'group_name': 'A',
                        'section_id': self.id,
                        'google_map_id': self.google_map_id.id,
                        'status_id': self.community_id.status_id.id
                    })

        self.create(feature_list)

    @api.onchange("type")
    def _get_order(self):
        if self.sequence:
            return
        if self.type == 'community':
            self.sequence = 1
        else:
            self.sequence = 2

    def unlink(self):
        for x in self:
            if x.type == 'community':
                x.home_plan_ids.unlink()
        return super(MapItem, self).unlink()

    def get_data(self):
        items = []
        blocklisted_fields = ['write_uid', 'write_date', 'create_uid', 'create_date', 'kml_file']
        fields_list = self.env['ir.model.fields'].search([('model_id.model', '=', self._name,),
                                                          ('name', 'not in', blocklisted_fields)]).mapped('name')
        for item in self:
            data = item.read(fields=fields_list)[0]
            if item.status_id:
                data['fillColor'] = item.status_id.fillColor
                data['fillOpacity'] = item.status_id.fillOpacity
                data['strokeWeight'] = item.status_id.strokeWeight
                data['strokeColor'] = item.status_id.strokeColor
                data['status_id'] = item.status_id.id
                data['status_name'] = item.status_id.name
            if item.community_id:
                data['community_id'] = item.community_id.id
            if item.background_image:
                data['background_image'] = item.background_image.decode('utf-8', errors='ignore')
            data['coordinates'] = json.loads(item.coordinates)
            data['zoom_content'] = json.loads(item.zoom_content)
            items.append(data)
        return items


class MapItemContent(models.Model):
    _name = 'map.item.content'
    _description = 'Google Maps Item Content'

    name = fields.Selection([
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('image_url', 'Image URL'),
        ('image', 'Image'),
        ("marker", "Marker"),
        ('hide', 'Hide Content')
    ], string="Content Type")
    description = fields.Char()
    html_content = fields.Text()
    css_content = fields.Text()
    image_url = fields.Char()
    zoom_level = fields.Integer()
    map_item_id = fields.Many2one('google.map.item', 'Google Maps Item ID')
