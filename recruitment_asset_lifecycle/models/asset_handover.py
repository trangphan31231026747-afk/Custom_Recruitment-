from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetHandover(models.Model):
    _name = 'asset.handover'
    _description = 'Phiếu Bàn Giao Tài Sản'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Hỗ trợ ghi log Chatter

    name = fields.Char(string='Mã phiếu', default='New', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Nhân viên nhận', required=True, tracking=True)
    package_id = fields.Many2one('asset.package', string='Gói tài sản áp dụng')
    
    handover_date = fields.Date(string='Ngày bàn giao', default=fields.Date.context_today)
    has_physical_signature = fields.Boolean(string='Đã có chữ ký thực tế?', default=False, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Nháp (Chờ chuẩn bị)'),
        ('in_use', 'Đang sử dụng (Hoàn tất)')
    ], string='Trạng thái', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('asset.handover') or 'HO-NEW'
        return super().create(vals_list)

    
    def action_confirm_handover(self):
        for record in self:
            if not record.has_physical_signature:
                raise ValidationError("LỖI BẢO MẬT: Vui lòng đảm bảo nhân viên đã ký nhận vào biên bản thực tế (Tick chọn 'Đã có chữ ký thực tế') trước khi xác nhận trên hệ thống!")
            record.write({'state': 'in_use'})