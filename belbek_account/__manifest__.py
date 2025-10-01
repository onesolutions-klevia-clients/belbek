{
    'name': "Belbek - Account",
    'category': "Accounting",
    'version': "18.0.0.0.2",
    'installable': True,
    'sequence': 1,

    'license': "OPL-1",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['l10n_ch'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        'reports/swissqr_report.xml',

        'views/res_company.xml',
        'views/res_partner.xml',
    ],

    'qweb': [],
}
