from odoo import models, fields

class HrJob(models.Model):
    _inherit = 'hr.job'

    # Cho phép 1 chức danh chọn 1 gói tài sản mặc định
    asset_package_id = fields.Many2one('asset.package', string='Gói Tài Sản Mặc Định')