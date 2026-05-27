# -*- coding: utf-8 -*-
{
    'name': 'Custom Recruitment BrightVision',
    'summary': 'Module import du lieu va tuy chinh tuyen dung',
    'version': '1.0',
    'category': 'Human Resources',
    'depends': ['base', 'hr', 'hr_recruitment'], 
    'data': [
        'data/res.company.csv',
        'data/res.users.csv',           
        'data/hr.department.csv',       
        'data/hr.employee.csv',         
        'data/hr.job.csv',              
        'data/hr.applicant.csv',        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
