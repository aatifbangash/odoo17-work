from odoo import models, fields, api
from pprint import pprint


class Lot_inherited(models.Model):
    _inherit = 'community_module.lot'

    def _compute_domain_map_item(self):
        current_user = self.env.user
        if not current_user.is_franchisor:
            return [('type', 'in', ['home']), ('create_uid.company_id.id', '=', current_user.company_id.id)]
        return [('type', 'in', ['home'])]

    google_map_item_id = fields.Many2one('google.map.item', string='Google Map Item',
                                         domain=_compute_domain_map_item)

    @api.model_create_multi
    def create(self, vals_list):
        ret = super(Lot_inherited, self).create(vals_list)
        for rec in ret:
            rec.google_map_item_id = self._create_map_item(rec)
        return ret

    def _create_map_item(self, rec):
        # self.env['community_module.section'].search([('id', '=', community_id)]).read([])
        return self.env['google.map.item'].create({
            'name': rec.name,
            'type': 'home',
            'lot_number': rec.lot_number,
            'section_id': rec.section_id.google_map_item_id.id
        })

    def unlink(self):
        self.google_map_item_id.unlink()
        return super(Lot_inherited, self).unlink()

    def map_lot_action(self):
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
