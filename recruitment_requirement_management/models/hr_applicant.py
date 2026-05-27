from odoo import models, fields, api


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    matching_score = fields.Float(
        string='Matching Score',
        compute='_compute_matching'
    )

    matching_result = fields.Selection([
        ('suitable', 'Suitable'),
        ('review', 'Need Review'),
        ('unsuitable', 'Unsuitable')
    ],
        string='Matching Result',
        compute='_compute_matching'
    )

    @api.depends(
        'job_id',
        'job_id.requirement_ids',
        'job_id.requirement_ids.skill_id',
        'job_id.requirement_ids.weight',
        'skill_ids'
    )
    def _compute_matching(self):

        for rec in self:

            score = 0

            if rec.job_id and rec.job_id.requirement_ids:

                applicant_skill_ids = rec.skill_ids.ids

                for requirement in rec.job_id.requirement_ids:

                    if requirement.skill_id.id in applicant_skill_ids:

                        score += requirement.weight

            rec.matching_score = score

            if score >= 80:

                rec.matching_result = 'suitable'

            elif score >= 50:

                rec.matching_result = 'review'

            else:

                rec.matching_result = 'unsuitable'