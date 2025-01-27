from odoo import models, fields, api
from pprint import pprint
import re
from ..kova_api.kova_api import KovaAPI


class Community(models.Model):
    _name = 'community_module.community'
    _description = 'Community'
    _rec_name = 'display_name'

    kova_community_rid = fields.Integer(string='Kova Community RID')
    # partner_id = fields.Many2one('res.partner', string='Partner')
    code = fields.Char(string='Code', size=8)
    legal_name = fields.Char(string='Legal Name', size=128)
    display_name = fields.Char(string='Display Name', size=128)
    slug = fields.Char(string='Slug', size=128)
    email = fields.Char(string='Email', size=128)
    phone = fields.Char(string='Phone', size=128)
    address = fields.Char(string='Address', size=128)
    # address2 = fields.Char(string='Address2', size=128)
    city = fields.Char(string='City', size=80)
    state_code = fields.Char(string='State Code', size=2)
    zip_code = fields.Char(string='Zip Code', size=10)
    header_text = fields.Html(string='Header Text', size=255)
    why_us_html = fields.Html('Why Us Text')
    description = fields.Char(string='Description', size=255)
    latitude = fields.Char(string='Latitude', size=12, default='0')
    longitude = fields.Char(string='Longitude', size=12, default='0')
    is_active = fields.Boolean(string='Active', default=True)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    company_id = fields.Many2one('res.company', 'Company',
                                 readonly=True,
                                 default=lambda self: self.env.company)
    json_data = fields.Text('data')

    # community associated home plans
    community_homeplans_ids = fields.One2many('community_module.community_homeplans', 'community_id',
                                              string='Community Home Plans')

    amenities_ids = fields.Many2many(
        'community_module.amenities',
        'community_amenities_rel',
        'community_id',
        'amenities_id',
    )

    # def _compute_community_homeplans_inactive_ids(self):
    #     for record in self:
    #         related_products = self.env['module_sb.franchise_homeplans'].search([
    #             ('company_id', '=', self.env.company.id),
    #             ('homeplan_id', 'not in', self.community_homeplans_ids.homeplan_id.ids)
    #         ])
    #         record.community_homeplans_inactive_ids = [(6, 0, related_products.ids)]
    #
    # community_homeplans_inactive_ids = fields.One2many("module_sb.franchise_homeplans", 'homeplan_id',
    #                                                    string='Related Products',
    #                                                    compute='_compute_community_homeplans_inactive_ids'
    #                                                    )

    # def test(self):
    #     print(self._context.get('homeplan_id'))
    #     pass

    # def write(self, vals):
    #     pprint(vals)
    #     return super(Community, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get('slug'):
                values['slug'] = self._generate_slug(values['display_name'])
        community = super(Community, self).create(vals_list)

        kova_api = KovaAPI(self.env)
        community.kova_community_rid = kova_api.create_community_kova(community)
        return community

    @api.model
    def get_community_by_id(self, community_id):
        return self.search([('id', '=', community_id)]).read([])
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

    def action_option_community_plans(self):
        # pprint(self.env.company.id)
        return {
            "type": "ir.actions.act_window",
            "res_model": "module_sb.franchise_homeplans",
            "views": [[False, "kanban"], [False, "tree"],
                      [False, "form"]],
            'view_mode': 'kanban,tree,form',
            "domain": [('company_id.id', '=', self.env.company.id)],
            "name": "Active Plans",
            # "search_view_id": [self.env.ref('hr_presence.hr_employee_view_presence_search').id, 'search'],
            "context": {'default_community_id': self.id},
        }

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
                "community_name": self.display_name
            },

        }

    @api.model
    def get_all_communities(self):
        return self.search([]).read()
    # def action_option_community_plans(self):
    #     return {
    #         "type": "ir.actions.act_window",
    #         "res_model": "community_module.community_homeplans",
    #         "views": [[False, "kanban"], [False, "tree"],
    #                   [False, "form"]],
    #         'view_mode': 'kanban,tree,form',
    #         "domain": [('community_id.id', '=', self.id)],
    #         "name": "Community Plans",
    #         # "search_view_id": [self.env.ref('hr_presence.hr_employee_view_presence_search').id, 'search'],
    #         "context": {'default_community_id': self.id},
    #     }

    # res_id = False
    # record = self.env['module_sb.website_content'].search([('company_id', '=', self.env.company.id)])
    # if record:
    #     res_id = record.id
    # return {
    #     "name": "Add website content",
    #     "res_model": "module_sb.website_content",
    #     "view_mode": "form",
    #     "target": "current",
    #     "context": {},
    #     # "res_id": res_id,
    #     "type": "ir.actions.act_window"
    # }
