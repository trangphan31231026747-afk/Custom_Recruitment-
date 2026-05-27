from odoo import api, fields, models
from odoo.exceptions import UserError


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    evaluation_ids = fields.One2many(
        "applicant.interview.evaluation",
        "applicant_id",
        string="Interview Evaluations"
    )

    interview_total_score = fields.Float(
        string="Interview Total Score",
        compute="_compute_interview_score",
        store=True
    )

    interview_average_score = fields.Float(
        string="Interview Average Score",
        compute="_compute_interview_score",
        store=True
    )

    evaluation_count = fields.Integer(
        string="Evaluation Count",
        compute="_compute_interview_score",
        store=True
    )

    @api.depends(
        "evaluation_ids",
        "evaluation_ids.line_ids",
        "evaluation_ids.line_ids.score"
    )
    def _compute_interview_score(self):
        for applicant in self:
            lines = applicant.evaluation_ids.mapped("line_ids")
            scores = lines.mapped("score")

            applicant.evaluation_count = len(applicant.evaluation_ids)
            applicant.interview_total_score = sum(scores)
            applicant.interview_average_score = (
                sum(scores) / len(scores) if scores else 0.0
            )

    def action_create_interview_evaluation(self):
        self.ensure_one()

        if not self.stage_id:
            raise UserError("This applicant does not have a recruitment stage yet.")

        return {
            "type": "ir.actions.act_window",
            "name": "Create Interview Evaluation",
            "res_model": "applicant.interview.evaluation",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_applicant_id": self.id,
                "default_stage_id": self.stage_id.id,
                "default_evaluator_id": self.env.user.id,
            },
        }