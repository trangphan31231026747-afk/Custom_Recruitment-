from odoo import api, fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    overdue_days = fields.Integer(
        string='Overdue Days',
        compute='_compute_overdue',
        store=True
    )

    is_overdue = fields.Boolean(
        string='Is Overdue',
        compute='_compute_overdue',
        store=True
    )

    @api.depends(
        'date_last_stage_update',
        'stage_id',
        'stage_id.overdue_limit_days',
        'active',
        'date_closed',
        'refuse_reason_id'
    )
    def _compute_overdue(self):
        now = fields.Datetime.now()

        for applicant in self:
            limit_days = applicant.stage_id.overdue_limit_days or 0

            if (
                applicant.active
                and not applicant.date_closed
                and not applicant.refuse_reason_id
                and applicant.date_last_stage_update
                and limit_days > 0
            ):
                days = (now - applicant.date_last_stage_update).days

                applicant.overdue_days = days
                applicant.is_overdue = days > limit_days

            else:
                applicant.overdue_days = 0
                applicant.is_overdue = False

    def cron_check_overdue_applicants(self):
        applicants = self.search([
            ('active', '=', True),
            ('date_closed', '=', False),
            ('refuse_reason_id', '=', False),
        ])

        applicants._compute_overdue()

    def cron_create_overdue_activities(self):
        overdue_applicants = self.search([
            ('is_overdue', '=', True),
            ('user_id', '!=', False),
        ])

        activity_type = self.env.ref('mail.mail_activity_data_todo')

        for applicant in overdue_applicants:
            existing_activity = self.env['mail.activity'].search([
                ('res_model', '=', 'hr.applicant'),
                ('res_id', '=', applicant.id),
                ('user_id', '=', applicant.user_id.id),
                ('activity_type_id', '=', activity_type.id),
                ('summary', '=', 'Overdue Recruitment Application'),
            ], limit=1)

            if existing_activity:
                continue

            applicant.activity_schedule(
                activity_type_id=activity_type.id,
                summary='Overdue Recruitment Application',
                note='This application has exceeded the allowed processing time. Please review and process it.',
                user_id=applicant.user_id.id,
            )