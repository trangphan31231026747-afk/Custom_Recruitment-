from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class InterviewChecklistTemplate(models.Model):
    _name = "interview.checklist.template"
    _description = "Interview Checklist Template"

    name = fields.Char(string="Checklist Name", required=True)

    stage_id = fields.Many2one(
        "hr.recruitment.stage",
        string="Interview Stage",
        required=True
    )

    line_ids = fields.One2many(
        "interview.checklist.template.line",
        "template_id",
        string="Checklist Criteria"
    )


class InterviewChecklistTemplateLine(models.Model):
    _name = "interview.checklist.template.line"
    _description = "Interview Checklist Template Line"

    template_id = fields.Many2one(
        "interview.checklist.template",
        string="Checklist Template",
        required=True,
        ondelete="cascade"
    )

    name = fields.Char(string="Criteria", required=True)

    description = fields.Text(string="Description")

    max_score = fields.Float(
        string="Max Score",
        default=10.0
    )


class ApplicantInterviewEvaluation(models.Model):
    _name = "applicant.interview.evaluation"
    _description = "Applicant Interview Evaluation"

    applicant_id = fields.Many2one(
        "hr.applicant",
        string="Applicant",
        required=True,
        ondelete="cascade"
    )

    stage_id = fields.Many2one(
        "hr.recruitment.stage",
        string="Interview Stage",
        required=True
    )

    evaluator_id = fields.Many2one(
        "res.users",
        string="Evaluator",
        default=lambda self: self.env.user
    )

    line_ids = fields.One2many(
        "applicant.interview.evaluation.line",
        "evaluation_id",
        string="Evaluation Lines"
    )

    total_score = fields.Float(
        string="Total Score",
        compute="_compute_score",
        store=True
    )

    average_score = fields.Float(
        string="Average Score",
        compute="_compute_score",
        store=True
    )

    note = fields.Text(string="Overall Comment")

    def _get_checklist_line_commands(self, stage_id):
        template = self.env["interview.checklist.template"].search([
            ("stage_id", "=", stage_id)
        ], limit=1)

        if not template:
            return []

        return [
            (0, 0, {
                "criteria": line.name,
                "max_score": line.max_score,
                "score": 0.0,
                "comment": "",
            })
            for line in template.line_ids
        ]

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        stage_id = res.get("stage_id")
        if stage_id and not res.get("line_ids"):
            res["line_ids"] = self._get_checklist_line_commands(stage_id)

        return res

    @api.onchange("stage_id")
    def _onchange_stage_id_load_checklist(self):
        for rec in self:
            if not rec.stage_id:
                rec.line_ids = [(5, 0, 0)]
                return

            is_not_scored_yet = all(
                not line.score and not line.comment
                for line in rec.line_ids
            )

            if not rec.line_ids or is_not_scored_yet:
                rec.line_ids = [(5, 0, 0)] + rec._get_checklist_line_commands(rec.stage_id.id)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            stage_id = vals.get("stage_id")
            line_ids = vals.get("line_ids")

            if stage_id and not line_ids:
                commands = self._get_checklist_line_commands(stage_id)
                if commands:
                    vals["line_ids"] = commands

        return super().create(vals_list)

    @api.depends("line_ids.score")
    def _compute_score(self):
        for rec in self:
            scores = rec.line_ids.mapped("score")
            rec.total_score = sum(scores)
            rec.average_score = sum(scores) / len(scores) if scores else 0.0

    def action_open_evaluation(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Interview Evaluation",
            "res_model": "applicant.interview.evaluation",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }


class ApplicantInterviewEvaluationLine(models.Model):
    _name = "applicant.interview.evaluation.line"
    _description = "Applicant Interview Evaluation Line"

    evaluation_id = fields.Many2one(
        "applicant.interview.evaluation",
        string="Evaluation",
        required=True,
        ondelete="cascade"
    )

    criteria = fields.Char(string="Criteria", required=True)

    max_score = fields.Float(
        string="Max Score",
        default=10.0
    )

    score = fields.Float(string="Score")

    comment = fields.Text(string="Comment")

    @api.constrains("score", "max_score")
    def _check_score_range(self):
        for rec in self:
            if rec.score < 0:
                raise ValidationError(_("Score cannot be negative."))
            if rec.max_score and rec.score > rec.max_score:
                raise ValidationError(_("Score cannot be greater than Max Score."))