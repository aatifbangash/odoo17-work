from odoo import models, fields, api
import re


class Section(models.Model):
    _name = 'community_module.section'
    _description = 'Section'
    _rec_name = 'name'

    name = fields.Char(string='Name', size=128)

    description = fields.Char(string='Description', size=255)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    company_id = fields.Many2one('res.company', 'Company',
                                 readonly=True,
                                 default=lambda self: self.env.company)
    community_id = fields.Many2one('community_module.community', 'Community')

    @api.model_create_multi
    def create(self, vals_list):
        return super(Section, self).create(vals_list)

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

    @api.model
    def get_sections_by_community(self, community_id):
        """
        Retrieves all sections associated with the given community_id.

        :param community_id: ID of the community
        :return: recordset of sections
        """
        if not community_id:
            raise ValueError("Community ID must be provided.")
        return self.search([('community_id', '=', community_id)]).read([])
