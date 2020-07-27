# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Tr Oniad",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "crm",
        "sale"
    ],
    "data": [
        "data/ir_cron.xml",
        "views/crm_lead_view.xml",
        "views/sale_order_view.xml",
        "views/res_partner_view.xml"
    ],
    "installable": True
}
