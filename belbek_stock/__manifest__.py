{
    'name': "Belbek - Stock",
    'category': "Inventory",
    'version': "18.0.1.0.1",
    'installable': True,
    'sequence': 1,

    'license': "OPL-1",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['sale_stock', 'shopify_ept'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Reports
        'reports/report_deliveryslip.xml',
    ],
}
