{
    'name': 'Recruitment Request Approval',
    'version': '1.0',
    'depends': ['hr_recruitment', 'mail'],
    'data': [
        'security/recruitment_request_groups.xml',
        'security/ir.model.access.csv',
        'views/recruitment_request_views.xml',
        'views/recruitment_request_wizard_views.xml',
        'views/menuitems.xml',
],
    'installable': True,
    'application': False,
}