# -*- coding: utf-8 -*-
from odoo import api, fields, models
import random
from datetime import datetime


class MySchool(models.Model):
    _name = 'school.school'
    _description = 'Custom School Model'

    name = fields.Char(string="School Name")
    student_ids = fields.One2many('school.student', 'school_id', string="Students")

    def replace_all(self):
        students = self.env['school.student'].search([], [], limit=2)
        if students:
            student_ids = [std.id for std in students]
            if student_ids:
                self.student_ids = [(6, 0, student_ids)]

    def unlink_all_relation(self):
        if self.student_ids:
            self.student_ids = [(5, 0, 0)]

    def add_existing(self):
        students = self.env['school.student'].search([], [], limit=2)
        self.student_ids = [(4, student.id) for student in students]
        # for std in students:
        #     self.student_ids = [(4, std.id, False)]

    def edit_existing_student(self):
        if self.student_ids:
            student = self.student_ids[:1]
            self.student_ids = [
                (1, student.id, {'name': 'Edited Name-' + str(random.randint(0, 100)) + '-' + str(datetime.now())})]

    def unlink_relation_student(self):
        if self.student_ids:
            students = self.student_ids
            for student in students[:2]:
                self.student_ids = [(3, student.id, False)]

    def delete_student(self):
        students = self.student_ids
        for student in students:
            self.student_ids = [(2, student.id, False)]
        print('here')

    def add_student(self):
        print(self)
        self.student_ids = [(0, 0, {'name': 'New Student dynamically'}), (0, 0, {'name': 'New Student dynamically 2'})]

    def new_school_wizard(self):
        return {
            "name": "Create new school",
            "res_model": "school.school_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"mode": 'create'},
            "type": "ir.actions.act_window"
        }

    def edit_school(self):
        print(self.env.context)
        print(self.student_ids.ids)
        return {
            "name": "Edit school",
            "res_model": "school.school_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"mode": 'edit', 'default_name': self.name,
                        'default_student_ids': self.student_ids.ids
                        },
            # "res_id": self.id, # used for real models
            "type": "ir.actions.act_window"
        }

    def delete_school(self):
        self.unlink()

    def server_action(self):
        records = self.env['school.school'].search([('id', 'in', self._context.get('active_ids'))])
        if records:
            records.write({'name': 'New Name'})

    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     # print('name_search')
    #     return super(MySchool, self).name_search(name, args, operator, limit)

    # @api.model
    # def name_create(self, name):
    #     print('name_create')
    #     print(name)
    #     return super(MySchool, self).name_create(name)
    # @api.model
    # def default_get(self, fields_list):
    #     print('default_get')
    #     print(fields_list)
    #     return super(MySchool, self).default_get(fields_list)
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     print(self.env.context.get('name'))
    #     # print('_search in school class')
    #     # print(domain)
    #     domain = [('id', 'in', [1, 2])]
    #     return super(MySchool, self)._search(domain, offset=offset, limit=limit, order=order,
    #                                           access_rights_uid=access_rights_uid)


class MyStudent(models.Model):
    _name = 'school.student'
    _description = 'Custom Student Model'

    name = fields.Char(string="Student Name")
    school_id = fields.Many2one('school.school', string="School Name")

    # @api.model
    # def create(self, vals_list):
    #     print('created')
    #     print(vals_list)
    #     return super(MyStudent, self).create(vals_list)
    #
    # @api.model
    # def write(self, vals_list):
    #     print('written')
    #     print(vals_list)
    #     return super(MyStudent, self).write(vals_list)
    #
    # def unlink(self):
    #     print('unlinked')
    #     return super(MyStudent, self).unlink()
    #
    # @api.model
    # def default_get(self, fields_list):
    #     print('default_get in student class')
    #     # print(fields_list)
    #     res = super(MyStudent, self).default_get(fields_list)
    #     res['name'] = 'test'
    #     res['school_id'] = self.env['school.school'].search([], limit=1).id
    #     print(res)
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     print('_search in student class')
    #     return super(MyStudent, self)._search(domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)
    #
