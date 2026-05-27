from odoo import models, fields

class AssetPackage(models.Model):
    _name = 'asset.package'
    _description = 'Gói Tài Sản Onboarding'

    name = fields.Char(string='Tên Gói Tài Sản', required=True)
    max_budget = fields.Float(string='Ngân sách tối đa (VND)', help='Mức ngân sách tối đa quy định cho gói này.')
    description = fields.Text(string='Ghi chú chung')
    
    
    line_ids = fields.One2many('asset.package.line', 'package_id', string='Chi tiết tài sản')

class AssetPackageLine(models.Model):
    _name = 'asset.package.line'
    _description = 'Chi tiết Gói Tài Sản'

    package_id = fields.Many2one('asset.package', string='Gói tài sản')
    product_id = fields.Many2one('product.product', string='Tài sản / Thiết bị', required=True)
    quantity = fields.Integer(string='Số lượng', default=1)
    is_mandatory = fields.Boolean(string='Bắt buộc?', default=True)