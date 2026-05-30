from odoo import models, fields

class AssetPackage(models.Model):
    _name = 'asset.package'
    _description = 'Onboarding Asset Package'

    name = fields.Char(string='Asset Package Name', required=True)
    max_budget = fields.Float(string='Maximum Budget (VND)', help='The maximum budget allowed for this package.')
    description = fields.Text(string='General Notes')
    
    line_ids = fields.One2many('asset.package.line', 'package_id', string='Asset Lines')

class AssetPackageLine(models.Model):
    _name = 'asset.package.line'
    _description = 'Asset Package Line'

    package_id = fields.Many2one('asset.package', string='Asset Package')
    product_id = fields.Many2one('product.product', string='Asset / Equipment', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    is_mandatory = fields.Boolean(string='Is Mandatory?', default=True)