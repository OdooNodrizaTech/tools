# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Pipedrive",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "crm",
        "mail",
        "mail_activity_done"
    ],
    "external_dependencies": {
        "python": [
            "pipedrive-python-lib",
            # "pipedrive",
            "boto3"
        ],
    },
    "data": [
        "data/ir_configparameter_data.xml",
        "data/ir_cron.xml",
        "views/pipedrive_menu.xml",
        "views/pipedrive_activity_view.xml",
        "views/pipedrive_activity_type_view.xml",
        "views/pipedrive_currency_view.xml",
        "views/pipedrive_deal_view.xml",
        "views/pipedrive_organization_view.xml",
        "views/pipedrive_person_view.xml",
        "views/pipedrive_pipeline_view.xml",
        "views/pipedrive_product_view.xml",
        "views/pipedrive_stage_view.xml",
        "views/pipedrive_user_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True
}
