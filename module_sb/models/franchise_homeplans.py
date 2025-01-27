# -*- coding: utf-8 -*-
from pprint import pprint

from odoo import models, fields, api


class FranchiseHomePlan(models.Model):
    _name = 'module_sb.franchise_homeplans'
    _description = 'Franchise Home Plans'
    _check_company_auto = True

    homeplan_id = fields.Many2one('product.template', string='Home Plans')
    company_id = fields.Many2one('res.company', 'Company',
                                 readonly=True,
                                 default=lambda self: self.env.company)

    community_id = fields.Integer("Community ID", store=False, readonly=False)
    community_homeplan_id = fields.Integer(store=False, default=0, compute="_is_plan_exist")
    community_name = fields.Char(store=False, default=None, compute="_is_plan_exist")
    enable = fields.Boolean(string="Enable", default=False, store=False, readonly=False)
    homeplan_base_price = fields.Float(related="homeplan_id.base_price", store=False, string="Base Price")
    homeplan_company_id = fields.Many2one(related="homeplan_id.company_id", store=False, string="Company")
    homeplan_legal_name = fields.Char(related="homeplan_id.legal_name", store=False, string="Legal Name")
    homeplan_is_published = fields.Boolean(related="homeplan_id.is_published", store=False, string="Max Price")
    homeplan_detailed_type = fields.Selection(related="homeplan_id.detailed_type", store=False, string="Type")
    homeplan_active = fields.Boolean(related="homeplan_id.active", store=False, string="Active")
    homeplan_default_code = fields.Char(related="homeplan_id.default_code", store=False, string="Code")
    homeplan_standard_price = fields.Float(related="homeplan_id.standard_price", store=False, string="Price")
    homeplan_kova_model_rid = fields.Integer(related="homeplan_id.kova_model_rid", store=False, string="KovaID")

    def unlink(self):
        for record in self:
            homeplan_id = record.homeplan_id.id
            current_company_id = record.company_id.id

            community_homeplans = self.env['community_module.community_homeplans'].sudo().search([
                ('community_id.create_uid.company_id', '=', current_company_id),
                ('homeplan_id', '=', homeplan_id)
            ])
            if community_homeplans:
                community_homeplans.unlink()

            homeplan_options = self.env['module_sb.home_plan_options'].sudo().search([
                ('homeplan_id', '=', homeplan_id),
                ('company_id', '=', current_company_id)
            ])
            if homeplan_options:
                homeplan_options.unlink()

            masterplan_option = self.env['module_sb.master_plan_options'].sudo().search([
                ('homeplan_id', '=', homeplan_id)
            ])
            if masterplan_option:
                for option in masterplan_option:
                    found_records = option.homeplan_option_override_ids.filtered(
                        lambda x: x.company_id.id == current_company_id
                    )
                    if found_records:
                        found_records.unlink()

        return super(FranchiseHomePlan, self).unlink()

    def action_set_community_plan(self):
        community_id = self.community_id
        plan_id = self.homeplan_id.id

        exists_community_homeplan = self.env['community_module.community_homeplans'].search([
            ('community_id', '=', community_id),
            ('homeplan_id', '=', plan_id)
        ])
        if not exists_community_homeplan:
            self.env['community_module.community_homeplans'].create({
                'community_id': community_id,
                'homeplan_id': plan_id
            })
        else:
            exists_community_homeplan.unlink()

    # @api.depends('homeplan_id', 'community_id')
    def _is_plan_exist(self):
        for record in self:
            record.community_homeplan_id = 0
            record.community_name = None
            exists_community_homeplan = self.env['community_module.community_homeplans'].search([
                ('community_id', '=', record.community_id),
                ('homeplan_id', '=', record.homeplan_id.id)
            ])
            if exists_community_homeplan:
                record.community_homeplan_id = exists_community_homeplan.id
                record.community_name = exists_community_homeplan.community_id.display_name

    def action_set_options(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({'testing_data': 'test', 'active_id': self._context.get('community_homeplan_id')})
        return {
            'type': 'ir.actions.client',
            'tag': 'owl.master_plan_options',
            "target": "current",
            "context": ctx,
            'params': {
                "homeplan_id": self._context.get('homeplan_id'),
                "homeplan_name": self._context.get('homeplan_name'),
                "panel": self._context.get('panel'),
            }
        }
