from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetHandover(models.Model):
    _name = 'asset.handover'
    _description = 'Asset Handover Record'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char(string='Handover Reference', default='New', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Receiving Employee', required=True, tracking=True)
    package_id = fields.Many2one('asset.package', string='Applied Asset Package')
    
    handover_date = fields.Date(string='Handover Date', default=fields.Date.context_today)
    has_physical_signature = fields.Boolean(string='Has Physical Signature?', default=False, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft (Pending)'),
        ('in_use', 'In Use (Completed)')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('asset.handover') or 'HO-NEW'
        return super().create(vals_list)

    def action_confirm_handover(self):
        for record in self:
            if not record.has_physical_signature:
                raise ValidationError("SECURITY ERROR: Please ensure the employee has signed the physical handover protocol (Tick 'Has Physical Signature?') before confirming on the system!")
            record.write({'state': 'in_use'})