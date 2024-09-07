from pathlib import Path

PROJECT_PATH = Path(__file__).parent.resolve()
JSON_PATH = PROJECT_PATH / "static/json/"
SEARCH_PATH = JSON_PATH / "search/"

SEARCH = {
    "locations": [
       "agronomia",
       "almagro",
       "balvanera",
       "barracas",
       "belgrano",
       "boedo",
       "caballito",
       "chacarita",
       "coghlan",
       "colegiales",
        "constitucion",
        "flores",
        "floresta",
        "la-boca",
        "la-paternal",
        "liniers",
        "mataderos",
        "monte-castro",
        "monserrat",
        "pompeya",
        "nunez",
        "palermo",
        "parque-avellaneda",
        "parque-chacabuco",
        "parque-chas",
        "parque-patricios",
        "puerto-madero",
        "recoleta",
        "retiro",
        "saavedra",
        "san-cristobal",
        "san-nicolas",
        "san-telmo",
        "versalles",
        "villa-crespo",
        "villa-deboto",
        "villa-general-mitre",
        "villa-lugano",
        "villa-luro",
        "villa-ortuzar",
        "villa-pueyrredon",
        "villa-real",
        "villa-riachuelo",
        "villa-santa-rita",
        "villa-soldati",
        "villa-urquiza",
        "villa-del-parque",
        "velez-sarsfield",
        "once",
        "barrio-norte",
        "congreso",
        "parque-centenario"
    ],
    "rooms": [
        "1",
        "2",
        "3",
        "4",
    ],
    "ambs": [
        "1",
        "2",
        "3",
        "4"
    ],
    "prices": [
        "100000",
        "200000",
        "300000",
        "400000",
        "500000",
        "600000",
        "700000",
        "800000",
        "900000",
        "1000000"
    ],
    "sources": {
        "zonaprop": {
            "base_url": "https://www.zonaprop.com.ar/inmuebles-venta-%s-%s-%s-menos-%s-dolar-orden-publicado-descendente.html",
            "ambs_format":"%s-ambiente%s",
            "rooms_format":"%s-habitacion%s",
            "locations_join":"-",
            "xpaths": {
                "wait_xpath": "//button[@data-qa='cookies-policy-banner']",
                "prop_xpath": "//div[@data-qa='posting PROPERTY']",
                "prop_image_xpath": ".//div[@data-qa='POSTING_CARD_GALLERY']//img[1]",
                "prop_data_xpath": {
                    "precio": ".//div[@data-qa='POSTING_CARD_PRICE']",
                    "expensas": ".//div[@data-qa='expensas']",
                    "direccion": ".//div[contains(@class, 'postingAddress')]",
                    "metros": ".//h3[@data-qa='POSTING_CARD_FEATURES']/span[1]",
                    "habitaciones": ".//h3[@data-qa='POSTING_CARD_FEATURES']/span[2]",
                    "hace": "./div/div[2]/div[2]/div[2]"
                },
                "next_xpath": "//a[@data-qa='PAGING_%s']",
                "path_attr": "data-to-posting",
                "id_attr": "data-id"
            }
        },
        "argenprop": {
            "base_url": "https://www.argenprop.com/casas-o-departamentos-o-ph/venta/%s/%s/%s/dolares-hasta-%s/?solo-ver-dolares&orden-masnuevos",
            "ambs_format":"%s-ambiente%s", #TODO 1-ambiente is set as monoambiente
            "rooms_format":"%s-dormitorio%s",
            "locations_join":"-o-",
            "xpaths": {
                "wait_xpath": "//div[@class='header-widget']",
                "prop_xpath": "//a[@class='card ']",
                "prop_image_xpath": ".//ul[@class='card__photos']/li[1]/img",
                "prop_data_xpath": {
                    "precio": ".//p[@class='card__price']",
                    "direccion": ".//p[@class='card__address']",
                    "metros": ".//ul[@class='card__main-features']/li[1]",
                    "habitaciones": ".//ul[@class='card__main-features']/li[2]",
                    "hace": "./div/div[2]/div[2]/div[2]",
                },
                "next_xpath": "//li[@class='pagination__page']/a[text()='%s']",
                "path_attr": "href",
                "id_attr": "data-item-id-visibilidad"
            }
        }
    }
}