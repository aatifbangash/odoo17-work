from odoo import models, fields, api
import re


class Lot(models.Model):
    _name = 'community_module.lot'
    _description = 'Lot'
    _rec_name = 'name'

    name = fields.Char(string='Name', size=128)
    description = fields.Char(string='Description', size=255)
    lot_number = fields.Char("Lot Number")
    is_active = fields.Boolean(string='Status', default=True)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    company_id = fields.Many2one('res.company', 'Company',
                                 readonly=True,
                                 default=lambda self: self.env.company)
    section_id = fields.Many2one('community_module.section', 'Section')

    @api.model_create_multi
    def create(self, vals_list):
        # Create the new records
        records = super(Lot, self).create(vals_list)

        # Loop through the newly created records and print their data
        for record in records:
            print(record.read())  # This prints all fields for the created record

        return records

    @api.model
    def get_lot_by_id(self, lot_id):
        return self.search([('id', '=', lot_id)]).read([])

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
