{
    'name': 'HR Asset Lifecycle Management',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Manage Asset Packages and Physical Asset Handover for employees (Odoo 17)',
    'description': """
        Module features:
        - Configure asset packages by job position (Asset Package).
        - Record physical asset handover status with physical signature verification.
    """,
    'author': 'Your Name',
    'depends': ['base', 'hr', 'hr_recruitment', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/asset_package_views.xml',
        'views/asset_handover_views.xml',
        'views/hr_job_views_inherit.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}