import base64
from pprint import pprint

import requests

from odoo import models, fields, api


class OptionValues(models.Model):
    _name = "module_sb.option_values"
    _description = "Option Values"
    # _table = "module_sb_options_group"
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char('Name', index='trigram', required=True)
    enabled = fields.Boolean(string='Enabled', default=True)
    option_classes_id = fields.Many2one('module_sb.option_classes', 'Class')
    option_categories_id = fields.Many2one('module_sb.option_categories', 'Category')
    option_locations_id = fields.Many2one('module_sb.option_locations', 'Location')
    option_id = fields.Char('Opt Val ID')

    style = fields.Char(string='Style', default=None)
    color = fields.Char(string='Color', default=None)
    internal_id = fields.Char(string='Internal ID', default=None)
    external_id = fields.Char(string='External ID', default=None)
    manufacturer = fields.Char(string='Manufacturer', default=None)
    model = fields.Char(string='Model', default=None)

    def do_action(self):
        pprint("hheeer")
    # @api.depends('internal_id')
    def compute_option_default_image(self):
        api_url = "https://api.prod.bundle.build/purchasing-api/v1/products/variants"
        bearer_token = self.env['ir.config_parameter'].sudo().get_param('module_sb.bundled_bearer_token')

        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        for record in self:
            payload = {
                "builder_ids": [record.internal_id],
            }

            try:
                response = requests.post(api_url, json=payload, headers=headers)
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data and response_data[0].get('default_image'):
                        image_binary = requests.get(response_data[0].get('default_image'))
                        record.default_image = base64.b64encode(image_binary.content)
                    else:
                        record.default_image = None

                else:
                    record.default_image = None

            except requests.exceptions.RequestException as e:
                record.default_image = None

    default_image = fields.Image(string='Default Image', default=None, store=True)


    _sql_constraints = [
        ('name_uniq_option_value', 'unique (name)', 'The record already exists!'),
    ]
