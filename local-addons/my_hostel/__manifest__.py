{
    'name': 'Hostel Management',
    'version': '16.0.1.0.0',
    'category': 'Hospitality',
    'summary': 'Manage hostel rooms, students, and allocations',
    'description': """
        Hostel Management System
        ========================
        This module helps manage hostel operations including:
        - Room Management
        - Student Registration
        - Room Allocation
        - Hostel Services
        - Fee Management
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/hostel_security.xml',
        'security/ir.model.access.csv',
        'data/hostel_data.xml',
        # Wizards
        'wizards/hostel_change_room_wizard_views.xml',
        'wizards/hostel_fee_payment_wizard_views.xml',
        # Views
        'views/hostel_hostel_views.xml',
        'views/hostel_room_views.xml',
        'views/hostel_student_views.xml',
        'views/hostel_allocation_views.xml',
        'views/hostel_service_views.xml',
        'views/hostel_fee_views.xml',
        # Reports
        'reports/hostel_reports.xml',
        # Menu - comes after all views and wizards
        'views/hostel_menu.xml',
    ],
    'demo': [
        'demo/hostel_demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'my_hostel/static/src/js/hostel_dashboard.js',
            'my_hostel/static/src/scss/hostel_style.scss',
            'my_hostel/static/src/css/hostel_style.css',
            'my_hostel/static/src/xml/hostel_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
