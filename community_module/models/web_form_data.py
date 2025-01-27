from odoo import models, fields, api


class CommunityHomePlans(models.Model):
    _name = 'community_module.web_form_data'
    _description = 'Test Web Form Data'

    name = fields.Char(string='Name', size=128)
    description = fields.Char(string='Description', size=250)
    community_id = fields.Integer(string='Community')

    @api.depends('community_id')
    def _compute_community_name(self):
        for rec in self:
            rec.community_name = self.env['community_module.community'].browse(rec.community_id).display_name

    community_name = fields.Char(compute='_compute_community_name', string='Community Name', store=False)
    company_id = fields.Integer(string='Company')

    @api.depends('company_id')
    def _compute_company_name(self):
        for rec in self:
            rec.company_name = self.env['res.company'].browse(rec.company_id).display_name

    company_name = fields.Char(compute='_compute_company_name', string='Company', store=False)
