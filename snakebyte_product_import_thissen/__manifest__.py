{
    'name': 'Snakebyte Product Import Thissen',
    'version': '15.0.1.0.0',
    'author': 'Snakebyte',
    'license': 'OPL-1',  # Gebruik een toegestane waarde zoals OPL-1
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/thissen_security.xml',
        'security/ir.model.access.csv',
        'views/thissen_crawl_action.xml',
        'views/thissen_product_view.xml',
        'views/thissen_menu.xml',
    ],
    'installable': True,
    'application': True,
}
