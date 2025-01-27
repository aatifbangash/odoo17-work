from odoo import models, fields


class CommunityCrmLead(models.Model):
    _inherit = 'crm.lead'

    community_id = fields.Many2one(
        'community_module.community', string='Community'
    )
