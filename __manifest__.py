{
    "name": "Controle de Combustível",
    "version": "19.0.1.0.0",
    "category": "Operations",
    "summary": "Registro de abastecimentos e controle simples de estoque de combustível.",
    "author": "Alexandre Jacques",
    "license": "LGPL-3",
    "depends": ["base", "fleet"],
    "data": [
    "security/security.xml",
    "security/ir.model.access.csv",

    # dashboards primeiro 
    "dashboards/dashboard_views.xml",

    # menus 
    "views/menu.xml",

    # views das telas
    "views/abastecimento_views.xml",
    "views/tanque_views.xml",
    "views/compra_views.xml",
    
    # Reports

    "reports/abastecimento_report.xml",
    "reports/abastecimento_report_template.xml",

    ],

    "application": True,
    "installable": True,
}
