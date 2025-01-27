# -*- coding: utf-8 -*-
import re
from pprint import pprint

from odoo import models, fields, api


class ModuleSBHomePlans(models.Model):
    _inherit = "product.template"

    slug = fields.Char(string='Slug', size=128, tracking=True)

    kova_model_rid = fields.Integer(string='Kova Model Rid')
    legal_name = fields.Char(string='Legal Name', size=128, tracking=True)
    is_published = fields.Boolean(string='Published', default=True)
    category_groups = fields.Many2many('product.category', string="Category Groups")

    # attributes
    homeplan_groups = fields.One2many('module_sb.homeplan.groups', 'homeplan_id', string='Groups')
    master_plan_options_ids = fields.One2many('module_sb.master_plan_options', 'homeplan_id',
                                              string='Master Plan Options')
    home_plan_options_ids = fields.One2many('module_sb.home_plan_options', 'homeplan_id',
                                            string='Home Plan Options')
    # checkbox to enable home plan for franchise
    enable = fields.Boolean(string='Enable', default=False, store=False, compute='_compute_enable')
    franchise_homeplans_ids = fields.One2many('module_sb.franchise_homeplans', 'homeplan_id',
                                              string='Franchise Home plans')
    product_override_ids = fields.One2many('module_sb.product_override', 'product_id',
                                           string='Product Override')
    is_franchise_admin = fields.Boolean(string='Is Franchise Admin', store=False, compute='_compute_franchise_admin')

    def _compute_base_price(self):
        for product in self:

            base_price_record = None
            user_role = 'franchisee' if self.env.user.has_group('module_sb.franchise_admin') else 'franchisor'

            if user_role == 'franchisee':
                base_price_record = product.product_override_ids.filtered(
                    lambda r: r.type == 'plan' and r.company_id == self.env.company)
                if not base_price_record:
                    base_price_record = product.product_override_ids.filtered(lambda r: r.type == 'master_plan')

            if user_role == 'franchisor':
                base_price_record = product.product_override_ids.filtered(lambda r: r.type == 'master_plan')

            product.base_price = base_price_record.base_price if base_price_record else 0.00

    def _inverse_base_price(self):
        for product in self:
            new_price_from_view = product.base_price
            record_type = 'plan' if self.env.user.has_group('module_sb.franchise_admin') else 'master_plan'

            base_price_record = self.env['module_sb.product_override'].search([
                ('product_id', '=', product.id),
                ('company_id', '=', self.env.company.id),
                ('type', '=', record_type)
            ], limit=1)
            if base_price_record and new_price_from_view < 1:
                base_price_record.unlink()
            else:
                if base_price_record:
                    base_price_record.base_price = new_price_from_view  # Store the user-provided price
                else:
                    self.env['module_sb.product_override'].create({
                        'product_id': product.id,
                        'base_price': new_price_from_view,
                        'company_id': self.env.company.id,
                        'type': record_type
                    })

    base_price = fields.Float(string='Base Price', default=0.00, tracking=False, store=False,
                              compute='_compute_base_price',
                              inverse='_inverse_base_price')
    incentive_price = fields.Float(string='Incentive Price', default=0.00, tracking=True)

    @api.depends('base_price', 'incentive_price')
    def _compute_price(self):
        for product in self:
            product.price = product.base_price - product.incentive_price
    price = fields.Float(string='Price', default=0.00, tracking=True,compute='_compute_price', )

    min_bedrooms = fields.Integer(string='Min Bedrooms', default=0)
    max_bedrooms = fields.Integer(string='Max Bedrooms', default=0)
    min_bathrooms = fields.Float(string='Min Bathrooms', default=0)
    max_bathrooms = fields.Float(string='Max Bathrooms', default=0)
    base_heated_square_feet = fields.Integer(string='Base Heated Square Feet', default=0)
    max_heated_square_feet = fields.Integer(string='Max Heated Square Feet', default=0)
    base_total_square_feet = fields.Integer(string='Base Total Square Feet', default=0)
    max_total_square_feet = fields.Integer(string='Max Total Square Feet', default=0)

    def _compute_franchise_admin(self):
        self.is_franchise_admin = self.env.user.has_group('module_sb.franchise_admin')

    @api.depends('franchise_homeplans_ids')
    def _compute_enable(self):
        self.enable = False
        for row in self.franchise_homeplans_ids:
            if row.company_id == self.env.company:
                self.enable = True
                break

    @api.onchange('enable')
    def changed_enable(self):
        if self.enable:
            # Check if record with matching company_id exists
            existing_record = self.franchise_homeplans_ids.filtered(
                lambda record: record.company_id == self.env.company
            )
            if not existing_record:
                # Create new record if none exists # [(0, 0, value)]
                self.update({
                    'franchise_homeplans_ids': [(fields.Command.create({'company_id': self.env.company.id}))]
                })
        else:
            # Clear all existing records [(5,0,0)]
            for record in self.franchise_homeplans_ids:
                if record.company_id == self.env.company:
                    self.update({
                        'franchise_homeplans_ids': [(fields.Command.delete(record.id))]
                    })

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get('slug'):
                values['slug'] = self._generate_slug(values['name'])
        return super(ModuleSBHomePlans, self).create(vals_list)

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

    def write(self, vals):
        if 'is_published' in vals and not vals['is_published']:
            franchise_homeplans = self.env['module_sb.franchise_homeplans'].search([
                ('homeplan_id', 'in', self.ids)
            ])
            if franchise_homeplans:
                franchise_homeplans.unlink()

        return super(ModuleSBHomePlans, self).write(vals)

    def options_action(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({'testing_data': 'test', 'active_id': self.id})

        is_franchise_admin = self.env.user.has_group('module_sb.franchise_admin')
        plan = 'Home plans' if is_franchise_admin else 'Master Plans'

        return {
            'type': 'ir.actions.client',
            'tag': 'owl.master_plan_options',
            "target": "current",
            "context": ctx,
            'params': {
                "homeplan_id": self.id,
                "homeplan_name": self.name,
                "panel": plan,
                'view_type': 'form'
            }
        }