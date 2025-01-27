from odoo import models


class Community(models.Model):
    _inherit = 'community_module.community'
    _description = 'Community'

    def options_page(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'owl.master_plan_options',
            "target": "new",
            "context": {"mode": 'create'},
            'params': {}
        }
