from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.osv import expression


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    is_blacklisted = fields.Boolean(
        string="Is Blacklisted",
        compute="_compute_blacklist_info",
        compute_sudo=True,
    )

    blacklist_count = fields.Integer(
        string="Blacklist Records",
        compute="_compute_blacklist_info",
        compute_sudo=True,
    )

    blacklist_warning = fields.Char(
        string="Blacklist Warning",
        compute="_compute_blacklist_info",
        compute_sudo=True,
    )

    def _get_blacklist_match_domain(self):
        self.ensure_one()

        domains = []

        if self.email_from:
            domains.append([("email", "=ilike", self.email_from.strip())])

        if self.partner_phone:
            phone = self.partner_phone.strip()
            domains.append([("phone", "=", phone)])
            domains.append([("mobile", "=", phone)])

        if self.partner_mobile:
            mobile = self.partner_mobile.strip()
            domains.append([("phone", "=", mobile)])
            domains.append([("mobile", "=", mobile)])

        if not domains:
            return [("id", "=", 0)]

        return expression.AND([
            [("state", "=", "active")],
            expression.OR(domains),
        ])

    def _get_blacklist_domain_from_values(self, vals):
        domains = []

        email = vals.get("email_from")
        phone = vals.get("partner_phone")
        mobile = vals.get("partner_mobile")

        if email:
            domains.append([("email", "=ilike", email.strip())])

        if phone:
            phone = phone.strip()
            domains.append([("phone", "=", phone)])
            domains.append([("mobile", "=", phone)])

        if mobile:
            mobile = mobile.strip()
            domains.append([("phone", "=", mobile)])
            domains.append([("mobile", "=", mobile)])

        if not domains:
            return False

        return expression.AND([
            [("state", "=", "active")],
            expression.OR(domains),
        ])

    @api.depends("email_from", "partner_phone", "partner_mobile")
    def _compute_blacklist_info(self):
        Blacklist = self.env["recruitment.candidate.blacklist"].sudo()

        for applicant in self:
            count = Blacklist.search_count(applicant._get_blacklist_match_domain())

            applicant.blacklist_count = count
            applicant.is_blacklisted = count > 0

            if count:
                applicant.blacklist_warning = _(
                    "This candidate matches %s active blacklist record(s)."
                ) % count
            else:
                applicant.blacklist_warning = False

    def action_open_blacklist_wizard(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Add Candidate to Blacklist"),
            "res_model": "recruitment.blacklist.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_applicant_id": self.id,
                "default_candidate_name": self.partner_name or self.name,
                "default_email": self.email_from,
                "default_phone": self.partner_phone,
                "default_mobile": self.partner_mobile,
                "default_job_id": self.job_id.id if self.job_id else False,
                "default_stage_id": self.stage_id.id if self.stage_id else False,
            },
        }

    def action_view_blacklist_records(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Blacklist Records"),
            "res_model": "recruitment.candidate.blacklist",
            "view_mode": "tree,form",
            "domain": self._get_blacklist_match_domain(),
        }

    @api.model_create_multi
    def create(self, vals_list):
        Blacklist = self.env["recruitment.candidate.blacklist"].sudo()

        for vals in vals_list:
            blacklist_domain = self._get_blacklist_domain_from_values(vals)

            if blacklist_domain:
                blacklist_record = Blacklist.search(blacklist_domain, limit=1)

                if blacklist_record:
                    raise ValidationError(
                        _("Sorry, your application has been rejected.")
                    )

        applicants = super().create(vals_list)

        return applicants

    def write(self, vals):
        result = super().write(vals)

        check_fields = {"email_from", "partner_phone", "partner_mobile"}

        if check_fields.intersection(vals.keys()):
            for applicant in self:
                if applicant.is_blacklisted:
                    applicant.message_post(
                        body=_(
                            "Warning: Candidate information matches an active blacklist record."
                        )
                    )

        return result