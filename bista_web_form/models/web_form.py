# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licens

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class WebForm(models.Model):
    _name = 'bista.web.form'
    _description = "Web Form"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    model_id = fields.Many2one('ir.model', required=True, ondelete='cascade')
    field_ids = fields.One2many('web.form.field', 'form_id')
    active = fields.Boolean(default=True)
    post_action = fields.Selection([('confirmation', "Show Confirmation Message"),
                                    ('redirect', "Redirect to Another URL")])
    redirect_url = fields.Char()
    confirmation_message = fields.Html()

    @api.model
    def get_form_data(self, ref):
        form = self.search([('code', '=', ref)], limit=1)
        if not form:
            return {'error': "Form with code '%s' not found" % ref}

        data = {
            'name': form.name,
            'code': form.code,
            'model': form.model_id.model,
            'active': form.active,
            'post_action': form.post_action,
            'redirect_url': form.redirect_url,
            'confirmation_message': form.confirmation_message,
            'sections': {}
        }
        section = False
        for field in form.field_ids.sorted(lambda f: f.sequence):
            if field.display_type == 'line_section':
                section = field.name
                data['sections'][section] = {'name': section, 'fields': {}}
                continue
            else:
                if not section:
                    section = 'Other'
                    data['sections'][section] = {'name': section, 'fields': {}}
            data['sections'][section]['fields'][field.id] = field._get_field_vals()
        return data


class FormFields(models.Model):
    _name = 'web.form.field'
    _description = 'Form Field'

    def _get_field_vals(self):
        self = self.sudo()
        data = self.read(['sequence', 'name', 'field_id', 'required',
                          'invisible', 'value_source', 'field_type',
                          'field_description', 'css_class',
                          'field_relation', 'domain', 'display_type'])[0]
        if self.field_type in ['many2one', 'many2many']:
            data['records'] = self.env[self.field_relation].search_read(safe_eval(self.domain or '[]'),
                                                                        ['id', 'display_name'])
        elif self.field_type == 'selection':
            data['records'] = [{'id': option.value, 'display_name': option.name} for option in self.selection_ids]
        return data

    sequence = fields.Integer(required=True, default=1)
    name = fields.Char(required=True)
    field_id = fields.Many2one('ir.model.fields')
    field_description = fields.Char(related="field_id.name")
    required = fields.Boolean()
    invisible = fields.Boolean()
    value_source = fields.Selection([
        ('param', 'Parameter')
    ])
    selection_ids = fields.One2many(related="field_id.selection_ids")
    field_type = fields.Selection(related="field_id.ttype")
    field_relation = fields.Char(related="field_id.relation")
    domain = fields.Text()
    form_id = fields.Many2one('bista.web.form')
    model_id = fields.Many2one('ir.model', related="form_id.model_id")
    model = fields.Char(related="model_id.model")
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")],
        default=False,
        help="Technical field for UX purpose.")
    css_class = fields.Char()

    @api.onchange("field_id")
    def _get_field_configs(self):
        if not self.field_id:
            return
        if not self.name:
            self.name = self.field_id.field_description
        if self.field_id.required:
            self.required = True

    @api.onchange("required")
    def _validate_required(self):
        if self.field_id and self.field_id.required and not self.required:
            raise UserError("This field is required by the model and cannot be left blank")

    @api.model
    def create(self, vals):
        form_id = vals.get('form_id')
        sequence_exists = self.search([('form_id', '=', form_id)])
        vals['sequence'] = max(line.sequence for line in sequence_exists) + 1 if sequence_exists else 1
        return super(FormFields, self).create(vals)
