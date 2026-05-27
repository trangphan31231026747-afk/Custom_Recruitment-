from odoo import fields, models, _
from odoo.exceptions import UserError


class RecruitmentBlacklistWizard(models.TransientModel):
    _name = "recruitment.blacklist.wizard"
    _description = "Add Candidate to Blacklist Popup"

    applicant_id = fields.Many2one(
        "hr.applicant",
        string="Applicant",
        readonly=True,
    )

    candidate_name = fields.Char(
        string="Candidate Name",
        readonly=True,
    )

    email = fields.Char(
        string="Email",
        readonly=True,
    )

    phone = fields.Char(
        string="Phone",
        readonly=True,
    )

    mobile = fields.Char(
        string="Mobile",
        readonly=True,
    )

    job_id = fields.Many2one(
        "hr.job",
        string="Applied Job",
        readonly=True,
    )

    stage_id = fields.Many2one(
        "hr.recruitment.stage",
        string="Current Recruitment Stage",
        readonly=True,
    )

    reason_ids = fields.Many2many(
        "recruitment.blacklist.reason",
        string="Blacklist Reasons",
    )

    other_reason = fields.Text(
        string="Other Reason / Reason Note",
    )

    note = fields.Text(
        string="Internal Note",
    )

    def action_confirm_blacklist(self):
        self.ensure_one()

        if not self.reason_ids and not self.other_reason:
            raise UserError(
                _("Please select at least one blacklist reason or enter another reason.")
            )

        blacklist = self.env["recruitment.candidate.blacklist"].sudo().create({
            "applicant_id": self.applicant_id.id if self.applicant_id else False,
            "candidate_name": self.candidate_name or self.applicant_id.name,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "job_id": self.job_id.id if self.job_id else False,
            "stage_id": self.stage_id.id if self.stage_id else False,
            "reason_ids": [(6, 0, self.reason_ids.ids)],
            "other_reason": self.other_reason,
            "note": self.note,
            "state": "active",
        })

        if self.applicant_id:
            reason_names = ", ".join(self.reason_ids.mapped("name"))

            message = _("Candidate has been added to the blacklist.")
            message += _("<br/>Applicant has been removed from the active application list.")

            if reason_names:
                message += _("<br/>Reasons: %s") % reason_names

            if self.other_reason:
                message += _("<br/>Other Reason / Note: %s") % self.other_reason

            self.applicant_id.message_post(body=message)

            self.applicant_id.sudo().with_context(active_test=False).write({
                "active": False,
            })

        return {
            "type": "ir.actions.act_window",
            "name": _("Blacklist Record"),
            "res_model": "recruitment.candidate.blacklist",
            "res_id": blacklist.id,
            "view_mode": "form",
            "target": "current",
        }