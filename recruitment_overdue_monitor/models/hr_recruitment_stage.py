from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'

    overdue_limit_days = fields.Integer(
        string='Overdue Limit Days',
        default=7,
        help='Maximum number of days an applicant can stay in this stage before being marked as overdue.'
    )

    @api.constrains('overdue_limit_days')
    def _check_overdue_limit_days(self):

        for record in self:

            if record.overdue_limit_days <= 0:

                raise ValidationError(
                    "Please enter a value greater than 0"
                )