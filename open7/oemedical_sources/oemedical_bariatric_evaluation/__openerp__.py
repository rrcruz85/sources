# -*- encoding: utf-8 -*-
 
{
    "name": "Oemedical Baritric Evaluation",
    "version": "1.0",
    "description": """
        Permite llevar registro de evaluaciones de la ficha Bariatrica
    """,
    "author": "CoreCloud Team",
    "website": "http://www.corecloud.ec",
    "category": "Info",
    "depends": [
            "oemedical",
            "base",#Este modulo para instalarse debe tener el modulo base y oemedical instalado
                ],
    "data":[
            "oemedical_bariatric_evaluation_view.xml", #todos los archivos xml que posea nuestro modulo se debe de agregarse aqui
            "report/oemedical_bariatric_report.xml", 
           ],
    "demo_xml": [
                        ],
    "update_xml": [
                        ],
    "active": False,
    "installable": True,
    "certificate" : "",
}