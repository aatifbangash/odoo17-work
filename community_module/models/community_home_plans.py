from odoo import models, fields, api


class CommunityHomePlans(models.Model):
    _inherit = 'product.template'
    _description = 'Community inherited Home Plans'

    def _compute_domain_homeplan_community(self):
        current_user = self.env.user

        if not current_user.is_franchisor:
            return [('community_id.create_uid', '=', self.env.user.id)]

        return [(1, '=', 1)]

    homeplan_community_ids = fields.One2many('community_module.community_homeplans', 'homeplan_id',
                                             string='Community Home Plans',
                                             domain=_compute_domain_homeplan_community,
                                             )
