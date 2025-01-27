# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class MapController(http.Controller):

    @http.route('/website_editor_right', type='json', auth='public', website=True, csrf=False)
    def check_map_access_right(self):
        return request.env.user.has_group('website.group_website_restricted_editor')

    @http.route('/get_communities', type='json', auth='public', website=True, csrf=False)
    def get_communities(self):
        community_ids = request.env['google.map.item'].sudo().search_read([('type', '=', 'community')],
                                                                          fields=['id', 'name', 'coordinates'])
        return community_ids

    @http.route('/get_core_communities', type='json', auth='public', website=True, csrf=False)
    def get_core_communities(self):
        community_ids = request.env['community_module.community'].sudo().search_read([('google_map_item_id', '=', False)],
                                                                          fields=['id', 'display_name'])
        return community_ids

    @http.route('/get_item_status', type='json', auth='public', website=True, csrf=False)
    def get_item_status(self):
        status_ids = (request.env['map.item.status'].sudo()
                      .search_read([], fields=['id', 'name',
                                               'fillColor', 'fillOpacity',
                                               'strokeWeight', 'strokeColor', 'strokeOpacity']))
        return status_ids

    @http.route('/map/api_key', auth="public", type='json', website=True, csrf=False)
    def get_map_api_key(self, **args):
        return request.env.company.google_places_api

    @http.route('/map/playground', auth="user", type='http', website=True, csrf=False)
    def render_playground(self, **args):
        return request.render("bista_map_component.map_playground", {"data": self.get_sample_data()})

    def get_sample_data(self):
        google_map = request.env['google.map'].search_read([],
                                                           fields=['name', 'map_id', 'init_zoom', 'center_lat',
                                                                   'search',
                                                                   'center_lng'], limit=1)
        map_data = google_map[0]
        google_map_items = request.env['google.map.item'].sudo().search(
            [('google_map_id', '=', map_data.get('id'))])
        item_data = google_map_items.get_data()
        for rec in google_map_items:
            print("Rec " , rec.name)
        return {
            'map': map_data,
            'item_data': item_data,
        }
