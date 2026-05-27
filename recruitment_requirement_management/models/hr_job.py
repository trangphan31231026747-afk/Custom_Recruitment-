from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrJob(models.Model):

    _inherit = 'hr.job'


    requirement_ids = fields.One2many(
        'recruitment.requirement',
        'job_id',
        string='Requirements'
    )


    total_weight = fields.Float(
        string='Total Weight',
        compute='_compute_total_weight',
        store=True
    )


    @api.depends('requirement_ids.weight')
    def _compute_total_weight(self):

        for rec in self:

            total = 0

            for requirement in rec.requirement_ids:

                total += requirement.weight

            rec.total_weight = total


    @api.constrains('requirement_ids')
    def _check_total_weight(self):

        for rec in self:

            if rec.requirement_ids and rec.total_weight != 100:

                raise ValidationError(
                    'Total weight must equal 100%'
                )


    def action_save_requirements(self):

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Requirements saved successfully',
                'type': 'success',
                'sticky': False,
            }
        }