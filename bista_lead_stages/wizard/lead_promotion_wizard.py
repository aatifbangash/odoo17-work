from odoo import models
from odoo.exceptions import UserError


class LeadPromotionWizard(models.TransientModel):
    _inherit = "crm.lead2opportunity.partner"

    def action_apply(self):
        stage_id = self.lead_id.stage_id
        team_id = self.env['crm.team'].search([('id', '!=', stage_id.team_id.id),
                                               ('member_ids', '=', self.user_id.id)])
        if not team_id:
            raise UserError("The user is not assigned to any of the qualified team.")
        next_stage = self.env['crm.stage'].search(
            [('team_id', 'in', team_id.ids),
             ('sequence', '>', stage_id.sequence)], limit=1)

        self.lead_id.write({'stage_id': next_stage.id})

        if self.name == 'merge':
            result_opportunity = self._action_merge()
        else:
            result_opportunity = self._action_convert()

        return result_opportunity.redirect_lead_opportunity_view()
