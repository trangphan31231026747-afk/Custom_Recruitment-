from odoo import fields, models, _


class SendToCeoWizard(models.TransientModel):
    _name = 'send.to.ceo.wizard'
    _description = 'Send Recruitment Request to CEO'

    request_id = fields.Many2one('recruitment.request', required=True)
    budget_amount = fields.Float(string='Recruitment Budget', required=True)
    budget_note = fields.Text(string='Budget Note')

    def action_confirm_send_to_ceo(self):
        self.ensure_one()

        request = self.request_id
        request.write({
    'budget_amount': self.budget_amount,
    'budget_note': self.budget_note,
    'state': 'sent_ceo',
})

        if request.ceo_id:
            request.activity_schedule(
                'mail.mail_activity_data_todo',
                summary='Approve Recruitment Request',
                note='Please review and approve or reject this recruitment request.',
                user_id=request.ceo_id.id
            )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('The request has been sent to CEO successfully.'),
                'type': 'success',
                'sticky': False,
                'next': self.env.ref('recruitment_request_approval.action_hr_review_requests').read()[0],
            }
        }