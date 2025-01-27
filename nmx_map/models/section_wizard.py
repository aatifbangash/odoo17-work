from pprint import pprint

from odoo import models, fields, api


class SectionWizard(models.TransientModel):
    _name = 'nmx_map.section_wizard'
    _description = 'Action Wizard'

    name = fields.Char()
    community_id = fields.Many2one('community_module.community', string='Community')

    def action_apply_category(self):
        pprint(self.read())
        pprint('action applhy')
        # active_ids = self.env.context.get('active_ids', [])
        # communities = self.env['community_module.community'].browse(active_ids)
        # for community in communities:
        #     community.category_id = self.category_id
        # return {'type': 'ir.actions.act_window_close'}

    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'nmx_map.section_wizard',
            'view_mode': 'form',
            'target': 'new',
        }
