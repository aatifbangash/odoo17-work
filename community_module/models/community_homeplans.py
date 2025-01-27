from pprint import pprint

from odoo import models, fields, api


class CommunityHomePlans(models.Model):
    _name = 'community_module.community_homeplans'
    _description = 'Community Home Plans'
    _rec_name = 'homeplan_id'

    community_id = fields.Many2one('community_module.community', string='Community', ondelete='cascade', required=False)
    community_display_name = fields.Char(related="community_id.display_name", store=False, string="Community Name")
    homeplan_id = fields.Many2one('product.template', string='Plans', readonly=True)
    community_homeplan_options_ids = fields.One2many('community_module.community_homeplans_options',
                                                     'community_homeplan_id',
                                                     string='Plans Options')
    latitude = fields.Char(string='Latitude', size=12, default='0')
    longitude = fields.Char(string='Longitude', size=12, default='0')

    product_override_ids = fields.One2many('module_sb.product_override',
                                                     'community_homeplan_id',
                                                     string='Product Override')

    base_price = fields.Float(string='Base Price', default=0.00, store=False,
                              compute='_compute_base_price',
                              inverse='_inverse_base_price'
                              )

    def _compute_base_price(self):
        for product in self:
            record = None

            base_price_record = self.env['module_sb.product_override'].search([
                ('product_id', '=', product.homeplan_id.id),
                ('community_homeplan_id', '=', product.id),
            ])
            if base_price_record:
                record = base_price_record.filtered(lambda r: r.type == 'community' and r.company_id == self.env.company)
                if not record:
                    record = base_price_record.filtered(lambda r: r.type == 'plan' and r.company_id == self.env.company)
                    if not record:
                        record = base_price_record.filtered(lambda r: r.type == 'master_plan')

            product.base_price = record.base_price if record else 0.00

    def _inverse_base_price(self):
        for product in self:
            new_price_from_view = product.base_price

            base_price_record = self.env['module_sb.product_override'].search([
                ('product_id', '=', product.homeplan_id.id),
                ('company_id', '=', self.env.company.id),
                ('community_homeplan_id', '=', product.id),
                ('type', '=', 'community')
            ], limit=1)
            if base_price_record and new_price_from_view < 1:
                base_price_record.unlink()
            else:
                if base_price_record:
                    base_price_record.base_price = new_price_from_view
                else:
                    self.env['module_sb.product_override'].create({
                        'product_id': product.homeplan_id.id,
                        'base_price': new_price_from_view,
                        'company_id': self.env.company.id,
                        'community_homeplan_id': product.id,
                        'type': 'community'
                    })
    def _compute_partner_active_plans(self):
        self.partner_active_plans = [
            {
                'name': 'name',
                'field1': 'field1',
                'field2': 'field2',
            },
            {
                'name': 'name',
                'field1': 'field1',
                'field2': 'field2',
            }
        ]

        # print(self)


    partner_active_plans = fields.Json(string='Other Model Data', store=False, compute='_compute_partner_active_plans')
    current_company = fields.Integer('Current Company', store=False, default=lambda self: self.env.company.id)

    homeplan_base_price = fields.Float(related="homeplan_id.base_price", store=False, string="Base Price")
    homeplan_incentive_price = fields.Float(related="homeplan_id.incentive_price", store=False, string="Base Price")
    homeplan_company_id = fields.Many2one(related="homeplan_id.company_id", store=False, string="Company")
    homeplan_legal_name = fields.Char(related="homeplan_id.legal_name", store=False, string="Legal Name")
    homeplan_is_published = fields.Boolean(related="homeplan_id.is_published", store=False, string="Max Price")
    homeplan_detailed_type = fields.Selection(related="homeplan_id.detailed_type", store=False, string="Type")
    homeplan_active = fields.Boolean(related="homeplan_id.active", store=False, string="Active")
    homeplan_default_code = fields.Char(related="homeplan_id.default_code", store=False, string="Code")
    homeplan_standard_price = fields.Float(related="homeplan_id.standard_price", store=False, string="Price")
    homeplan_kova_model_rid = fields.Integer(related="homeplan_id.kova_model_rid", store=False, string="KovaID")

    @api.depends('base_price', 'homeplan_incentive_price')
    def _compute_price(self):
        for product in self:
            product.price = product.base_price - product.homeplan_incentive_price
    price = fields.Float(string='Price', default=0.00, store=False, tracking=True,compute='_compute_price', )
    @api.onchange('homeplan_id')
    def homeplan_changed(self):
        home_plan_options = self.env['module_sb.home_plan_options'].search([('homeplan_id', '=', self.homeplan_id.id)])
        if self.community_homeplan_options_ids:
            self.community_homeplan_options_ids = [(5, 0, 0)]
        # self.update({
        #     'community_homeplan_options_ids': [(0, 0, {'homeplan_option_id': x.id}) for x in home_plan_options]
        # })
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
