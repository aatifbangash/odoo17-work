from pprint import pprint

import requests

from odoo import models, fields, api
import re

from odoo.exceptions import ValidationError
from ..kova_api.kova_api import KovaAPI


class SBPartner(models.Model):
    _inherit = "res.company"

    slug = fields.Char(string='Territory', size=128)
    kova_bunit_rid = fields.Integer(string='Kova BUnit RID')
    code = fields.Char(string='Code', size=8)
    legal_name = fields.Char(string='Legal Name', size=128)
    description = fields.Text(string='Description')
    latitude = fields.Char(string='Latitude', size=128, default='0')
    longitude = fields.Char(string='Longitude', size=128, default='0')
    is_franchisor = fields.Boolean(string='Is Franchisor', default=False)
    state_code = fields.Char(compute='_compute_state_code', store=False, string='State Code')
    tax_id = fields.Char(string='Tax ID')

    # web content fields
    header_text = fields.Text('Header Text')
    why_us_html = fields.Html('Why Us Text')
    builder_image = fields.Image('Builder Image')
    about_the_builder = fields.Html('About The Builder')

    @api.depends('state_id')
    def _compute_state_code(self):
        if self.state_id:
            self.state_code = self.state_id.code
        else:
            self.state_code = ''

    # @api.onchange('name')
    # def _name_changed(self):
    #     if not self.slug:
    #         self.slug = self.name

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:

            existing_partner = self.env['res.users'].search([('email', '=', values.get('email'))], limit=1)
            if existing_partner:
                raise ValidationError("This email is already registered. Please use a different email address.")

            if not values.get('slug'):
                values['slug'] = self._generate_slug(values['name'])

        company = super(SBPartner, self).create(vals_list)

        # Create internal user for the company
        franchisee_admin_group = self.env.ref('module_sb.franchise_admin')
        internal_user_group = self.env.ref('base.group_user')  # Internal user group
        user_vals = {
            'name': f'Admin {company.name}',
            'login': company.email,
            'email': company.email,
            'company_id': company.id,
            'company_ids': [company.id],
            'groups_id': [(6, 0, [franchisee_admin_group.id, internal_user_group.id])],
            'password': 'bubblegum'
        }
        # Create the user
        self.env['res.users'].sudo().create(user_vals)

        kova_api = KovaAPI(self.env)
        company.kova_bunit_rid = kova_api.create_franchisee_kova(company)

        return company

    @api.model
    def _generate_slug(self, name):
        slug = re.sub(r'[^\w\s-]', '', name).strip().lower()
        slug = re.sub(r'[-\s]+', '-', slug)
        return self._ensure_unique_slug(slug)

    @api.model
    def _ensure_unique_slug(self, slug):
        original_slug = slug
        counter = 1
        while self.search([('slug', '=', slug)]):
            slug = f"{original_slug}-{counter}"
            counter += 1
        return slug
