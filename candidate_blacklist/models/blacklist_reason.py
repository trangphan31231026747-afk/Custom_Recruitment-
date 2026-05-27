from odoo import fields, models


class RecruitmentBlacklistReason(models.Model):
    _name = "recruitment.blacklist.reason"
    _description = "Candidate Blacklist Reason"

    name = fields.Char(string="Reason", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)