# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Cesce",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale",
        "account",
        "partner_financial_risk"
    ],
    "data": [
        "data/ir_configparameter_data.xml",
        "data/ir_cron.xml",
        "data/cesce_risk_classification_motive.xml",
        "data/cesce_risk_classification_situation.xml",
        "data/cesce_payment_term.xml",
        "data/cesce_sale_situation.xml",
        "data/cesce_sale_motive_situation.xml",
        "data/cesce_webservice_error.xml",
        "views/account_move_line_view.xml",
        "views/cesce_view.xml",
        "views/res_partner_view.xml",
        "views/cesce_risk_classification_view.xml",
        "security/ir.model.access.csv"
    ],
    "installable": True
}