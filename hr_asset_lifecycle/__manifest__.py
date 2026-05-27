{
    'name': 'HR Asset Lifecycle Management',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Quản lý Gói tài sản và Bàn giao tài sản vật lý cho nhân sự (Odoo 17)',
    'description': """
        Module hỗ trợ:
        - Thiết lập gói tài sản theo chức danh (Asset Package).
        - Ghi nhận trạng thái bàn giao tài sản vật lý có cam kết chữ ký.
    """,
    'author': 'Your Name',
    'depends': ['base', 'hr', 'hr_recruitment', 'product','mail'],
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