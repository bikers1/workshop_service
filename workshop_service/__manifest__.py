{
    'name': 'Workshop Service Management',
    'version': '17.0.1.0.0',
    'category': 'Services/Workshop',
    'summary': 'Manage workshop and service orders for vehicles or equipment',
    'description': """
Workshop Service Management
===========================
Modul untuk mengelola service order di bengkel.
Fitur:
- Pencatatan service order lengkap
- Manajemen spare part dan jasa
- Integrasi dengan Sales Order
- Integrasi dengan Stock Picking
    """,
    'author': 'Test Candidate',
    'website': '',
    'depends': ['base', 'sale', 'stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/workshop_service_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
