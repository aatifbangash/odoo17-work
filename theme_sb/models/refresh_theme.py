from odoo import models, api


# class RefreshTheme(models.Model):
#     _name = 'theme_sb.refresh.my.theme'
#     _description = "Refresh My Theme"
#     def refresh_my_theme(self, **kwargs):
#
#         for key, value in kwargs.items():
#             print(f"{key}: {value}")
#         website = self.env['website'].search([('id', '=', 5)], limit=1)
#         print(website)
#         # for field_name, field_value in website.read()[0].items():
#         #     print(f"{field_name}: {field_value}")
#         # website.theme_id._theme_upgrade_upstream()
#         return True