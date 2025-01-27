from odoo import models, fields, api


class OptionsGroup(models.Model):
    _name = "module_sb.options_group"
    _description = "Options Group"
    # _table = "module_sb_options_group"
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char('Name', index='trigram', required=True)
    enabled = fields.Boolean(string='Enabled', default=True)
    parent_id = fields.Many2one('module_sb.options_group', 'Option Group', ondelete='cascade')
    option_category = fields.Many2one('module_sb.option_categories', 'Category')
    option_class = fields.Many2one('module_sb.option_classes', 'Class')

    location = fields.Many2one('module_sb.option_locations', 'Location')
    option_id = fields.Char('Opt Sel ID')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    # @api.model
    # def search(self, domain, offset=0, limit=None, order=None):
    #     print('search method')
    #     return super().search(domain, offset=offset, limit=limit, order=order)
    #
    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     print(self)
    #     print('name_search')
    #     return super().name_search(name=name, args=args, operator=operator, limit=limit)
    # #
    # @api.model
    # def browse(self, ids=None):
    #     # print('browse')
    #     # print(ids)
    #     return super().browse(ids=ids)
    #
    # @api.model
    # def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
    #     print('search fetch')
    #     print(domain)
    #     print(field_names)
    #
    #     return super().search_fetch(domain=domain, field_names=field_names, offset=offset, limit=limit, order=order)

    # @api.model
    # def fetch(self, field_names):
    #     # print('fetch')
    #     # print(field_names)
    #     return super().fetch(field_names=field_names)
    # @api.model
    # def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
    #     print('web search read')
    #     print(domain)
    #     print(specification)
    #     #
    #     # records = self.search_fetch(domain, ['name'], offset=offset, limit=limit, order=order)
    #     # values_records = records.web_read({"name":{}})
    #     # print(values_records)
    #     return super().web_search_read(domain=domain, specification=specification, offset=offset, limit=limit, order=order, count_limit=count_limit)
    #
    # @api.model
    # def _format_web_search_read_results(self, domain, records, offset, limit, count_limit):
    #     # print('format web search read results')
    #     # newRecords = [{'name': record['name'] + ' - testing'} for record in records]
    #     # print(newRecords)
    #
    #     # newRecords = []
    #     # for record in records:
    #     #     record['name'] = record['name'] + ' - ' + "testing"
    #     #     newRecords.append(record)
    #     # print(newRecords)
    #     # records = [records[0]]
    #     return super()._format_web_search_read_results(domain=domain, records=newRecords, offset=offset, limit=limit, count_limit=count_limit)
    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     print('search read')
    #     return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
    #

    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     print('_search')
    #     print(domain)
    #     return super()._search(domain=domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)

    # def write(self, vals):
    #     print('write')
    #     return super().write(vals)
    #
    # @api.model
    # def create(self, vals_list):
    #     print('create')
    #     return super().create(vals_list)
    #
    # def unlink(self):
    #     print('delete')
    #     return super().unlink()
    # @api.model
    # def default_get(self, fields):
    #     res = super(OptionsGroup, self).default_get(fields)
    #
    #     company_text = self.get_company_text()
    #     if company_text:
    #         res.update({'name': company_text.name })
    #     return res
    #
    # def get_company_text(self):
    #     return self.search([('company_id', '=', self.env.company.id)], limit=1)
