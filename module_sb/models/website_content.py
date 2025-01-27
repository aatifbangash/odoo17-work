from odoo import models, fields, api


class WebsiteContent(models.Model):
    _name = "module_sb.website_content"
    _description = "Website Content"
    _rec_name = 'company_id'

    header_text = fields.Text('Header Text')
    why_us_html = fields.Html('Why Us Text')
    builder_image = fields.Image('Builder Image')
    about_the_builder = fields.Html('About The Builder')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, ondelete='cascade')

    def do_action(self):
        res_id = False
        record = self.env['module_sb.website_content'].search([('company_id', '=', self.env.company.id)])
        if record:
            res_id = record.id
        return {
            "name": "Add website content",
            "res_model": "module_sb.website_content",
            "view_mode": "form",
            "target": "current",
            "context": {},
            "res_id": res_id,
            "type": "ir.actions.act_window"
        }
