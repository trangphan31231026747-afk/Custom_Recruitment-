from odoo import models, fields

class HrJob(models.Model):
    _inherit = 'hr.job'

   
    asset_package_id = fields.Many2one('asset.package', string='Gói Tài Sản Mặc Định')