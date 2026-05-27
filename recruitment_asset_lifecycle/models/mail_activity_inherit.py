from odoo import models, api

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    @api.model_create_multi
    def create(self, vals_list):
        activities = super().create(vals_list)
        
        for activity in activities:
            if activity.res_model == 'hr.employee' and activity.res_id:
                employee = self.env['hr.employee'].browse(activity.res_id)
                
                if employee.exists() and employee.job_id and employee.job_id.asset_package_id:
        
                        
                        existing_ticket = self.env['asset.handover'].sudo().search([
                            ('employee_id', '=', employee.id)
                        ], limit=1)
                        
                        if not existing_ticket:
                            self.env['asset.handover'].sudo().create({
                                'employee_id': employee.id,
                                'package_id': employee.job_id.asset_package_id.id,
                            })
        return activities