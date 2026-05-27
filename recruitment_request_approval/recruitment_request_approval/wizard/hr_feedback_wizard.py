from odoo import fields, models, _


class HrFeedbackWizard(models.TransientModel):
    _name = 'hr.feedback.wizard'
    _description = 'HR Feedback Wizard'

    request_id = fields.Many2one('recruitment.request', required=True)
    hr_feedback = fields.Text(string='HR Feedback', required=True)

    def action_confirm_feedback(self):
        self.ensure_one()

        request = self.request_id
        request.write({
            'hr_feedback': self.hr_feedback,
            'state': 'need_revision',
        })

        if request.hm_id:
            request.activity_schedule(
                'mail.mail_activity_data_todo',
                summary='Recruitment Request Needs Revision',
                note='HR has sent feedback. Please review and update the recruitment request.',
                user_id=request.hm_id.id
            )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Feedback has been sent to the Hiring Manager.'),
                'type': 'success',
                'sticky': False,
                'next': self.env.ref('recruitment_request_approval.action_hr_review_requests').read()[0],
            }
        }