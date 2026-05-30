from odoo import fields, models, _
from odoo.exceptions import UserError


class RecruitmentRemoveBlacklistWizard(models.TransientModel):
    _name = "recruitment.remove.blacklist.wizard"
    _description = "Remove Candidate from Blacklist Popup"

    blacklist_id = fields.Many2one(
        "recruitment.candidate.blacklist",
        string="Blacklist Record",
        required=True,
        readonly=True,
    )

    remove_reason = fields.Text(
        string="Remove Reason",
        required=True,
    )

    def action_confirm_remove_blacklist(self):
        self.ensure_one()

        if not self.remove_reason:
            raise UserError(_("Please enter the reason for removing this blacklist record."))

        self.blacklist_id.write({
            "state": "removed",
            "remove_reason": self.remove_reason,
            "removed_by": self.env.user.id,
            "removed_date": fields.Datetime.now(),
        })

        if self.blacklist_id.applicant_id:
            self.blacklist_id.applicant_id.message_post(
                body=_("Blacklist has been removed.<br/>Reason: %s") % self.remove_reason
            )

        return {
            "type": "ir.actions.act_window_close",
        }