from odoo import models, fields, api
from pprint import pprint


class Community_inherited(models.Model):
    _inherit = 'community_module.community'

    def _compute_domain_map_item(self):
        current_user = self.env.user
        if not current_user.is_franchisor:
            return [('type', 'in', ['community']), ('create_uid.company_id.id', '=', current_user.company_id.id)]
        return [('type', 'in', ['community'])]

    google_map_item_id = fields.Many2one('google.map.item', string='Google Map Item',
                                         domain=_compute_domain_map_item)

    @api.model_create_multi
    def create(self, vals_list):
        ret = super(Community_inherited, self).create(vals_list)
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

        return super(Community_inherited, self).write(vals)

    def _create_map_item(self, rec):
        return self.env['google.map.item'].create({
            'franchise_id': rec.company_id.google_map_item_id.id,
            'name': rec.display_name,
            'type': 'community',
            'marker_zoom': 15,
            'marker_lat': rec.latitude,
            'marker_lng': rec.longitude,
            'marker_content': rec.description
        })

    def unlink(self):
        self.google_map_item_id.unlink()
        return super(Community_inherited, self).unlink()

    def map_community_action(self):
        self.ensure_one()
        record = self.google_map_item_id
        if record:
            return {
                "name": "Map Item",
                "res_model": "google.map.item",
                "view_mode": "form",
                "target": "current",
                "context": {},
                "res_id": record.id,
                "type": "ir.actions.act_window"
            }
        return False
