from odoo import fields, models, _
from odoo.exceptions import UserError


class RecruitmentRequest(models.Model):
    _name = 'recruitment.request'
    _description = 'Recruitment Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Request Title', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', tracking=True)
    job_position = fields.Char(string='Job Position', required=True, tracking=True)
    quantity = fields.Integer(string='Quantity', default=1, tracking=True)
    reason = fields.Text(string='Recruitment Reason')
    requirement = fields.Text(string='Job Requirements')
    expected_date = fields.Date(string='Expected Hiring Date')

    hm_id = fields.Many2one('res.users', string='Hiring Manager', default=lambda self: self.env.user, tracking=True)
    hr_id = fields.Many2one('res.users', string='HR Responsible', tracking=True)
    ceo_id = fields.Many2one('res.users', string='CEO', tracking=True)

    budget_amount = fields.Float(string='Recruitment Budget', tracking=True)
    budget_note = fields.Text(string='Budget Note')

    hr_feedback = fields.Text(string='HR Feedback')
    ceo_feedback = fields.Text(string='CEO Feedback')
    ceo_reject_reason = fields.Text(string='CEO Rejection Reason')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent_hr', 'Sent to HR'),
         ('need_revision', 'Need Revision'),
        ('hr_feedback', 'HR Feedback'),
        ('sent_ceo', 'Sent to CEO'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)

    def _show_success_and_redirect(self, message, action_xmlid):
        action = self.env.ref(action_xmlid).read()[0]
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': message,
                'type': 'success',
                'sticky': False,
                'next': action,
            }
        }

    def action_send_to_hr(self):
        for rec in self:
            rec.state = 'sent_hr'
            if rec.hr_id:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary='Review recruitment request',
                    note='Please review this recruitment request.',
                    user_id=rec.hr_id.id
                )
        return self._show_success_and_redirect(
            _('The recruitment request has been sent to HR successfully.'),
            'recruitment_request_approval.recruitment_request_action'
        )

    def action_hr_feedback(self):
        self.ensure_one()
        return {
            'name': 'Send Feedback to Hiring Manager',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.feedback.wizard',
            'view_mode': 'form',
            'target': 'new',
        'context': {
            'default_request_id': self.id,
            'default_hr_feedback': self.hr_feedback,
        }
    }

    def action_send_to_ceo(self):
        self.ensure_one()
        return {
        'name': 'Send to CEO',
        'type': 'ir.actions.act_window',
        'res_model': 'send.to.ceo.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'default_request_id': self.id,
            'default_budget_amount': self.budget_amount,
            'default_budget_note': self.budget_note,
            'default_hr_feedback': self.hr_feedback,
        }
    }

    def action_ceo_approve(self):
        for rec in self:
            rec.state = 'approved'

        if rec.hr_id:
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                summary='Recruitment Request Approved',
                note='The recruitment request has been approved by CEO. You can proceed with recruitment.',
                user_id=rec.hr_id.id
            )

        if rec.hm_id:
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                summary='Recruitment Request Approved',
                note='Your recruitment request has been approved by CEO.',
                user_id=rec.hm_id.id
            )
            
        return self._show_success_and_redirect(
        _('The recruitment request has been approved successfully.'),
        'recruitment_request_approval.action_ceo_approval_requests'
    )

    def action_ceo_reject(self):
         self.ensure_one()
         return {
        'name': 'Reject Request',
        'type': 'ir.actions.act_window',
        'res_model': 'ceo.reject.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'default_request_id': self.id,
        }
    }

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'
        return self._show_success_and_redirect(
            _('The recruitment request has been reset to draft.'),
           'recruitment_request_approval.recruitment_request_action'
        )