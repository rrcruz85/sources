# -*- encoding: utf-8 -*-
 
{
    "name": "Oemedical Baritric Evolution",
    "version": "1.0",
    "description": """
        Permite llevar registro de evoluciones de la evaluacion Bariatrica
    """,
    "author": "CoreCloud Team",
    "website": "http://www.corecloud.ec",
    "category": "Info",
    "depends": [
            "oemedical",
            "base",#Este modulo para instalarse debe tener el modulo base y oemedical instalado
                ],
    "data":[
            "oemedical_bariatric_evolution_view.xml", #todos los archivos xml que posea nuestro modulo se debe de agregarse aqui
                ],
    "demo_xml": [
                        ],
    "update_xml": [
                        ],
    "active": False,
    "installable": True,
    "certificate" : "",
}