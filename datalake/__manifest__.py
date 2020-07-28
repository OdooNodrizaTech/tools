# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Datalake",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base"
    ],
    "external_dependencies": {
        "python": [
            "boto3"
        ],
    },
    "data": [
        "data/ir_configparameter_data.xml",
        "data/ir_cron.xml",
    ],
    "installable": True
}
