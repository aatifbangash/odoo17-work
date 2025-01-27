import re

from odoo import models, fields, api
from odoo.tools import image_data_uri


class GalleryItems(models.Model):
    _name = 'module_sb.gallery_item'
    _description = 'Gallery Image/Video'

    gallery_id = fields.Many2one('module_sb.gallery', string='Gallery', required=True, ondelete='cascade')
    name = fields.Char(string='Title')
    image = fields.Binary(string='Image')
    video_code = fields.Text(string='Video Code')
    media_type = fields.Selection([
        ('image', 'Image'),
        ('video', 'Video')
    ], string='Media Type', required=True, default='image')

    media_display = fields.Html(
        string="Media Display",
        compute="_compute_media_display",
        sanitize=False,
        store=False  # Don't store this field in the database
    )

    video_id = fields.Char(
        string="Video ID",
        compute="_compute_video_id",
        store=False
    )

    @api.depends('media_type', 'image', 'video_code')
    def _compute_media_display(self):
        for record in self:
            if record.media_type == 'image' and record.image:
                record.media_display = f'<img src="/web/image?model=module_sb.gallery_item&id={record.id}&field=image" style="max-width:70px; max-height:70px;"/>'
            elif record.media_type == 'video' and record.video_code:
                record.media_display = f'<img src="/module_sb/static/img/youtube-icon.jpeg" style="max-width:70px; max-height:70px;"/>'
            else:
                record.media_display = ''

    @api.depends('media_type', 'image', 'video_code')
    def _compute_video_id(self):
        for record in self:
            if record.media_type == 'video' and record.video_code:
                video_id = self._extract_youtube_id(record.video_code)
                if video_id:
                    record.video_id = video_id
                else:
                    record.video_id = None
            else:
                record.video_id = None

    def _extract_youtube_id(self, video_code):
        match = re.search(r'(?:v=|\/embed\/|\/1\/|\/v\/|youtu\.be\/|\/watch\?v=|\/watch\?vi=)([A-Za-z0-9_-]{11})',
                          video_code)
        return match.group(1) if match else None