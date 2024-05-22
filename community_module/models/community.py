from odoo import models, fields, api


class Community(models.Model):
    _name = 'community_module.community'
    _description = 'Community'

    kova_community_rid = fields.Integer(string='Kova Community RID')
    # partner_id = fields.Many2one('res.partner', string='Partner')
    code = fields.Char(string='Code', size=8)
    legal_name = fields.Char(string='Legal Name', size=128)
    display_name = fields.Char(string='Display Name', size=128)
    email = fields.Char(string='Email', size=128)
    phone = fields.Char(string='Phone', size=128)
    address = fields.Char(string='Address', size=128)
    # address2 = fields.Char(string='Address2', size=128)
    city = fields.Char(string='City', size=80)
    state_code = fields.Char(string='State Code', size=2)
    zip_code = fields.Char(string='Zip Code', size=10)
    description = fields.Char(string='Description', size=255)
    latitude = fields.Char(string='Latitude', size=12, default='0')
    longitude = fields.Char(string='Longitude', size=12, default='0')
    is_active = fields.Boolean(string='Active', default=True)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)

    # community associated home plans
    community_homeplan_ids = fields.One2many('community_module.community_homeplans', 'community_id',
                                             string='Community Home Plans')

    def test(self):
        print(self._context.get('homeplan_id'))
        pass


# model that hold community associated home plans and their options set ID.
class CommunityHomePlans(models.Model):
    _name = 'community_module.community_homeplans'
    _description = 'Community Home Plans'

    community_id = fields.Many2one('community_module.community', string='Community')
    homeplan_id = fields.Many2one('product.template', string='Home Plans')
    community_homeplan_options_ids = fields.One2many('community_module.community_homeplan_options',
                                                     'community_homeplan_id',
                                                     string='Home Plans Options')
    current_company = fields.Integer('Current Company', store=False, default=lambda self: self.env.company.id)
    @api.onchange('homeplan_id')
    def homeplan_changed(self):
        if self.community_homeplan_options_ids:
            self.community_homeplan_options_ids = [(5, 0, 0)]
    def test(self):
        print(self._context.get('homeplan_id'))
        pass


class CommunityHomePlanOptions(models.Model):
    _name = 'community_module.community_homeplan_options'
    _description = 'Community Home Plans options'

    community_homeplan_id = fields.Many2one('community_module.community_homeplans', string='Community Home Plans')
    homeplan_option_id = fields.Many2one('module_sb.home_plan_options', string='Home Plans Options',
                                         domain="[('homeplan_id', '=', community_homeplan_id_related)]",
                                         )
    community_homeplan_id_related = fields.Integer(related='community_homeplan_id.homeplan_id.id', store=False, string="")

    # domain_check = fields.Integer(compute='_compute_domain_check')
    # @api.depends('community_homeplan_id')
    # def _compute_domain_check(self):
    #     for record in self:
    #         record.domain_check = record.community_homeplan_id.homeplan_id.id
