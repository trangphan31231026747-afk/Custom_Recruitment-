from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.osv import expression


class RecruitmentCandidateBlacklist(models.Model):
    _name = "recruitment.candidate.blacklist"
    _description = "Candidate Blacklist"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "candidate_name"
    _order = "blacklisted_date desc"

    applicant_id = fields.Many2one(
        "hr.applicant",
        string="Source Applicant",
        ondelete="set null",
        tracking=True,
    )

    candidate_name = fields.Char(
        string="Candidate Name",
        required=True,
        tracking=True,
    )

    email = fields.Char(
        string="Email",
        index=True,
        tracking=True,
    )

    phone = fields.Char(
        string="Phone",
        index=True,
    )

    mobile = fields.Char(
        string="Mobile",
        index=True,
    )

    job_id = fields.Many2one(
        "hr.job",
        string="Applied Job",
    )

    stage_id = fields.Many2one(
        "hr.recruitment.stage",
        string="Recruitment Stage",
    )

    reason_ids = fields.Many2many(
        "recruitment.blacklist.reason",
        "candidate_blacklist_reason_rel",
        "blacklist_id",
        "reason_id",
        string="Blacklist Reasons",
    )

    other_reason = fields.Text(
        string="Other Reason / Reason Note",
    )

    note = fields.Text(
        string="Internal Note",
    )

    state = fields.Selection(
        [
            ("active", "Active Blacklist"),
            ("removed", "Removed"),
        ],
        string="Status",
        default="active",
        tracking=True,
    )

    blacklisted_by = fields.Many2one(
        "res.users",
        string="Blacklisted By",
        default=lambda self: self.env.user,
        readonly=True,
    )

    blacklisted_date = fields.Datetime(
        string="Blacklisted Date",
        default=fields.Datetime.now,
        readonly=True,
    )

    removed_by = fields.Many2one(
        "res.users",
        string="Removed By",
        readonly=True,
    )

    removed_date = fields.Datetime(
        string="Removed Date",
        readonly=True,
    )

    remove_reason = fields.Text(
        string="Removal Reason",
        readonly=True,
    )

    @api.constrains("email", "phone", "mobile", "state")
    def _check_duplicate_active_blacklist(self):
        for record in self:
            if record.state != "active":
                continue

            domains = []

            if record.email:
                domains.append([("email", "=ilike", record.email.strip())])

            if record.phone:
                phone = record.phone.strip()
                domains.append([("phone", "=", phone)])
                domains.append([("mobile", "=", phone)])

            if record.mobile:
                mobile = record.mobile.strip()
                domains.append([("phone", "=", mobile)])
                domains.append([("mobile", "=", mobile)])

            if not domains:
                continue

            duplicate_domain = expression.AND([
                [("id", "!=", record.id), ("state", "=", "active")],
                expression.OR(domains),
            ])

            duplicate = self.search(duplicate_domain, limit=1)

            if duplicate:
                raise ValidationError(
                    _("This candidate already exists in the active blacklist.")
                )

    def action_remove_blacklist(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Remove Blacklist"),
            "res_model": "recruitment.remove.blacklist.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_blacklist_id": self.id,
            },
        }