# -*- coding: utf-8 -*-
import re
from pprint import pprint

from odoo import models, fields, api


class MapItem(models.Model):
    _inherit = 'google.map.item'

    type = fields.Selection(selection_add=[('franchise', 'Franchise'),('section', 'Section')])

    is_not_home = fields.Boolean(compute='_compute_is_home', string='Is Home')

    franchise_id = fields.Many2one("google.map.item")
    community_ids = fields.One2many('google.map.item', 'franchise_id')
    lot_number = fields.Char("Lot Number")
    sequence = fields.Integer(default=1)
    address = fields.Char("Address")
    # community associated home plans
    # community_map_homeplans_ids = fields.One2many('community_module.community_homeplans', 'community_map_id',
    #                                           string='Community Home Plans')
    #
    # header_text = fields.Html(string='Header Text', size=255)
    # why_us_html = fields.Html('Why Us Text')
    #
    # code = fields.Char(string='Code', size=8)
    # slug = fields.Char(string='Slug', size=128)
    # email = fields.Char(string='Email', size=128)
    # phone = fields.Char(string='Phone', size=128)
    # city = fields.Char(string='City', size=80)
    # state_code = fields.Char(string='State Code', size=2)
    # zip_code = fields.Char(string='Zip Code', size=10)

    # amenities_ids = fields.Many2many(
    #     'community_module.amenities',
    #     'community_map_amenities_rel',
    #     'community_map_id',
    #     'amenities_id',
    # )

    @api.model_create_multi
    def create(self, vals_list):
        original_vals_list = [vals.copy() for vals in vals_list]
        for vals in vals_list:
            # if not vals.get('slug'):
            #     vals['slug'] = self._generate_slug(vals['name'])
            vals.pop('core_community_id', None)

        map_items = super(MapItem, self).create(vals_list)

        # Loop through the created records and corresponding vals to associate with Community
        for map_item, vals in zip(map_items, original_vals_list):
            if 'core_community_id' in vals:
                core_community_id = vals.get('core_community_id')
                if core_community_id:
                    community = self.env['community_module.community'].sudo().browse(core_community_id)
                    if community.exists():
                        community.google_map_item_id = map_item.id

        return map_items

    def write(self, vals):
        if 'core_community_id' in vals:
            core_community_id = vals.get('core_community_id')
            if core_community_id:
                community = self.env['community_module.community'].sudo().browse(core_community_id)
                if community.exists():
                    community.google_map_item_id = self.id
        vals.pop('core_community_id', None)
        return super(MapItem, self).write(vals)

    def read(self, fields=None, load='_classic_read'):
        records = super(MapItem, self).read(fields=fields, load=load)

        for record in records:
            community = self.env['community_module.community'].search([
                ('google_map_item_id', '=', record['id'])
            ], limit=1)
            record['core_community_id'] = community.id if community else False

        return records

    def action_owl_community_plans(self):
        # pprint(self.id)
        return {
            "type": "ir.actions.client",
            "tag": "owl.plans",
            "context": {
                "active_id": self.id
            },
            "params": {
                "panel": "Community",
                "community_name": self.name
            },

        }

    @api.depends('type')
    def _compute_is_home(self):
        for record in self:
            record.is_not_home = (record.type != 'home')
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     # Fetch records using the original `search_read` method
    #     pprint('search_read')
    #     records = super(MapItem, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit,
    #                                                  order=order)
    #
    #     # # Add extra data to each record
    #     for record in records:
    #         # Add custom data
    #         record['extra_info2'] = 'Additional info here'  # Customize as needed
    #
    #     return records

