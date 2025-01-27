from odoo import models, fields, api
from pprint import pprint


class Partner_inherited(models.Model):
    _inherit = "res.company"

    def _compute_domain_map_item(self):
        current_user = self.env.user
        if not current_user.is_franchisor:
            return [('type', 'in', ['franchise']), ('id', '=', current_user.company_id.id)]
        return [('type', 'in', ['franchise'])]

    google_map_item_id = fields.Many2one('google.map.item', string='Google Map Item',
                                         domain=_compute_domain_map_item)

    @api.model_create_multi
    def create(self, vals_list):
        ret = super(Partner_inherited, self).create(vals_list)
        for rec in ret:
            rec.google_map_item_id = self._create_map_item(rec)
        return ret

    def write(self, vals):
        if self.google_map_item_id:
            data = {}
            if 'latitude' in vals:
                data['marker_lat'] = vals['latitude']

            if 'longitude' in vals:
                data['marker_lng'] = vals['longitude']

            if data:
                self.google_map_item_id.write(data)

        return super(Partner_inherited, self).write(vals)

    def _create_map_item(self, rec):
        return self.env['google.map.item'].create({
            'name': rec.display_name,
            'type': 'franchise',
            'marker_zoom': 4,
            'marker_lat': rec.latitude,
            'marker_lng': rec.longitude,
            'marker_content': rec.description
        })

    def unlink(self):
        self.google_map_item_id.unlink()
        return super(Partner_inherited, self).unlink()
