# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OwlHomePlans(models.Model):
    _inherit = "product.template"

    def action_set_options(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'owl.master_plan_options',
            "target": "current",
            "context": {"mode": 'create'},
            'params': {
                "homeplan_id": self._context.get('homeplan_id'),
                "homeplan_name": self._context.get('homeplan_name'),
                "panel": self._context.get('panel')
            }
        }
