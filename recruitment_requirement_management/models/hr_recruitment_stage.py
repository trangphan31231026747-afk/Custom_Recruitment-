from odoo import fields, models


class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'

    overdue_limit_days = fields.Integer(
        string='Overdue Limit Days',
        default=7,
        help='Maximum number of days an applicant can stay in this stage before being marked as overdue.'
    )