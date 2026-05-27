{
    'name': 'Recruitment Overdue Monitor',
    'version': '1.0',
    'depends': ['hr_recruitment', 'mail'],
    'data': [
        'views/hr_applicant_views.xml',
        'views/hr_recruitment_stage_views.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': False,
}