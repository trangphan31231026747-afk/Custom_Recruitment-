from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RecruitmentRequirement(models.Model):

    _name = 'recruitment.requirement'

    _description = 'Recruitment Requirement'

    _rec_name = 'skill_id'


    skill_id = fields.Many2one(
        'hr.skill',
        string='Skill',
        required=True
    )

    skill_level = fields.Selection([
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], string='Required Level')

    weight = fields.Float(
        string='Weight (%)',
        required=True
    )

    description = fields.Text(
        string='Description'
    )

    job_id = fields.Many2one(
        'hr.job',
        string='Job Position'
    )


    @api.constrains('weight')
    def _check_weight(self):

        for record in self:

            if record.weight < 0:

                raise ValidationError(
                    "Weight must be greater than or equal to 0"
                )