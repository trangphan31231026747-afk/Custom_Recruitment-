{
    'name': 'Requirement Management',

    'version': '1.0',

    'summary': 'Requirement Management for Recruitment',

    'category': 'Human Resources',

    'depends': [
        'hr_recruitment',
        'hr_skills'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_job_views.xml',
        'views/hr_applicant_views.xml',
    ],

    'installable': True,

    'application': True,

    'license': 'LGPL-3',
}