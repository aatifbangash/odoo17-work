from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError


class Lead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def _get_stage_domain(self):
        team_ids = self._get_user_team_ids()
        domain = ['|', ('team_id', '=', False), ('team_id', 'in', team_ids)]
        return domain

    stage_id = fields.Many2one(
        'crm.stage', string='Stage', index=True, tracking=True,
        compute='_compute_stage_id', readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids', ondelete='restrict',
        domain=_get_stage_domain)

    team_ids = fields.Many2many(
        'crm.team', string="Teams",
        compute='_compute_team_ids'
    )

    @api.model
    def default_get(self, fields):
        ret = super().default_get(fields)

        crm_stages_env = self.env['crm.stage']
        team_ids = self._get_user_team_ids()
        stage_id = False
        if team_ids:
            # Prioritize stages assigned to the team
            stage_domain = [('team_id.use_leads', '=', True),
                            ('team_id', 'in', team_ids)]
            stage_id = crm_stages_env.search(stage_domain, limit=1, order="sequence").id

        if not stage_id:
            # If team stage was not available, search all stages and make an attempt to assign the one without team_id
            stage_domain = [('team_id.use_leads', '=', True)]
            stage_id = crm_stages_env.search(stage_domain, order="sequence")
            stage_without_team = stage_id.filtered(lambda t: not t.team_id)
            if stage_without_team:
                stage_id = stage_without_team[0].id
            elif stage_id:
                stage_id = stage_id[0].id
            else:
                raise UserError("Odoo could not find a default stage for type lead.")

        ret['stage_id'] = stage_id
        ret['type'] = 'lead'
        ret['team_id'] = team_ids[0] if team_ids else False

        # IF user has access to opportunity stage promote the lead
        opportunity_stage = crm_stages_env.search([('team_id.use_opportunities', '=', True),
                                                   ('team_id', 'in', team_ids)],
                                                  order="sequence", limit=1)
        if opportunity_stage:
            ret['team_id'] = opportunity_stage.team_id.id
            ret['stage_id'] = opportunity_stage.id
            ret['type'] = 'opportunity'

        # Do not set sales person if its public user
        user = ret.get("user_id", False)
        if user:
            public_user_id = self.env.ref("base.public_user").id
            default_user_id = self.env['res.users'].browse(user).id
            if default_user_id and default_user_id == public_user_id:
                ret['user_id'] = False
        return ret

    def _compute_team_ids(self):
        for lead in self:
            lead.team_ids = self._get_user_team_ids()

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        team_ids = self._get_user_team_ids()
        if team_ids:
            search_domain = ['|', ('id', 'in', stages.ids), '|', ('team_id', '=', False), ('team_id', 'in', team_ids)]
        else:
            search_domain = ['|', ('id', 'in', stages.ids), ('team_id', '=', False)]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID) or []
        return stages.browse(stage_ids)

    def read(self, fields=None, load='_classic_read'):
        result = super(Lead, self).read(fields, load=load)
        filtered = []
        team_ids = self._get_user_team_ids()
        for record in result:
            team_id = record.get('team_id', False)
            if team_id and team_id not in team_ids:
                continue
            filtered.append(record)
        return filtered

    def _get_user_team_ids(self):
        super_groups = ['sales_team.group_sale_salesman_all_leads',
                        'sales_team.group_sale_manager',
                        'base.group_erp_manager',
                        'base.group_system']
        is_super_user = False
        for group in super_groups:
            if self.env.user.has_group(group):
                is_super_user = True
                break
        if not is_super_user:
            return self.env['crm.team'].search([('member_ids', '=', self.env.user.id)]).ids
        else:
            return self.env['crm.team'].search([]).ids

