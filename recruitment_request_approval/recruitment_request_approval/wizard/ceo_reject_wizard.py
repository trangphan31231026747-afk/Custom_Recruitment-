from odoo import fields, models, _


class CeoRejectWizard(models.TransientModel):
    _name = 'ceo.reject.wizard'
    _description = 'CEO Reject Recruitment Request'

    request_id = fields.Many2one('recruitment.request', required=True)
    ceo_reject_reason = fields.Text(string='Rejection Reason', required=True)

    def action_confirm_reject(self):
        self.ensure_one()

        request = self.request_id
        request.write({
            'ceo_reject_reason': self.ceo_reject_reason,
            'state': 'rejected',
        })

        if request.hm_id:
            request.activity_schedule(
                'mail.mail_activity_data_todo',
                summary='Recruitment Request Rejected',
                note='Your recruitment request has been rejected by CEO.',
                user_id=request.hm_id.id
            )

        if request.hr_id:
            request.activity_schedule(
                'mail.mail_activity_data_todo',
                summary='Recruitment Request Rejected',
                note='The recruitment request has been rejected by CEO.',
                user_id=request.hr_id.id
            )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Rejected'),
                'message': _('The request has been rejected successfully.'),
                'type': 'warning',
                'sticky': False,
                'next': self.env.ref('recruitment_request_approval.action_ceo_approval_requests').read()[0],
            }
        }