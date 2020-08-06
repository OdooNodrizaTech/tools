# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Googleanalytics Api",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [
            "oauth2client",
            "apiclient"
        ],
    },
    "depends": [
        "base"
    ],
    "data": [
        "data/ir_cron.xml",
        "data/ir_configparameter_data.xml",
        "security/ir.model.access.csv"
    ],
    "installable": True
}
