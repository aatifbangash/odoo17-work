# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MySchoolWizard(models.TransientModel):
    _name = 'school.school_wizard'
    _description = 'Custom School Model'

    name = fields.Char(string="School Name")
    # student_ids = fields.One2many('school.student', 'school_id', string="Students")
    student_ids = fields.Many2many('school.student', string="Students")

    # @api.model
    def create_new_school(self):
        self.ensure_one()
        print(self.env.context)
        self.env['school.school'].create({'name': self.name, 'student_ids': [(6, 0, self.student_ids.ids)]})

    def update_new_school(self):
        self.ensure_one()
        print(self.env.context)
        (self.env['school.school'].search([('id', '=', self.env.context.get('active_id'))])
         .write({'name': self.name, 'student_ids': [(6, 0, self.student_ids.ids)]}))


class MyStudentWizard(models.TransientModel):
    _name = 'school.student_wizard'
    _description = 'Custom Student Wizard Model'

    name = fields.Char(string="School Name Char", required=True)
    school_id = fields.Many2one('school.school_wizard', string="School Name M2o", required=True)
