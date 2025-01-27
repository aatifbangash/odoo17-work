from odoo import models, fields, api


class Gallery(models.Model):
    _name = 'module_sb.gallery'
    _description = 'Gallery'

    name = fields.Char(string='Gallery Name', required=True)
    gallery_item_ids = fields.One2many('module_sb.gallery_item', 'gallery_id', string='Images/Videos')
