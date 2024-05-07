JSON_PATH = "./static/json/"

LOCATIONS = {
    0: "agronomia",
    1: "almagro",
    2: "balvanera",
    3: "barracas",
    4: "belgrano",
    5: "boedo",
    6: "caballito",
    7: "chacarita",
    8: "coghlan",
    9: "colegiales",
    10: "constitucion",
    11: "flores",
    12: "floresta",
    13: "la-boca",
    14: "la-paternal",
    15: "liniers",
    16: "mataderos",
    17: "monte-castro",
    18: "monserrat",
    19: "pompeya",
    20: "nunez",
    21: "palermo",
    22: "parque-avellaneda",
    23: "parque-chacabuco",
    24: "parque-chas",
    25: "parque-patricios",
    26: "puerto-madero",
    27: "recoleta",
    28: "retiro",
    29: "saavedra",
    30: "san-cristobal",
    31: "san-nicolas",
    32: "san-telmo",
    33: "versalles",
    34: "villa-crespo",
    35: "villa-deboto",
    36: "villa-general-mitre",
    37: "villa-lugano",
    38: "villa-luro",
    39: "villa-ortuzar",
    40: "villa-pueyrredon",
    41: "villa-real",
    42: "villa-riachuelo",
    43: "villa-santa-rita",
    44: "villa-soldati",
    45: "villa-urquiza",
    46: "villa-del-parque",
    47: "velez-sarsfield",
    48: "once",
    49: "barrio-norte",
    50: "congreso",
    51: "parque-centenario"
}

AMBS = {
    "zonaprop": {
        0: "1-habitacion",
        1: "2-habitaciones",
        2: "3-habitaciones",
        3: "4-habitaciones",
        4: "1-ambiente",
        5: "2-ambientes",
        6: "3-ambientes",
        7: "4-ambientes",
        8: "mas-de-1-habitacion",
        9: "mas-de-2-habitaciones",
        10: "mas-de-3-habitaciones",
        11: "mas-de-4-habitaciones",
        12: "mas-de-1-ambiente",
        13: "mas-de-2-ambientes",
        14: "mas-de-3-ambientes",
        15: "mas-de-4-ambientes"
    },
    "argenprop": {
        0:"monoambiente",
        1:"2-ambientes",
        2:"3-ambientes",
        3:"4-ambientes"
    }
}

ZONAPROP = {
    "base_url": "https://www.zonaprop.com.ar/",
    "prop_types": ["inmuebles", "alquiler"],
    "url_separator": "-",
    "list_order": "orden-publicado-descendente.html",
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
}

ARGENPROP = {
    "base_url": "https://www.argenprop.com/",
    "prop_types": "casas-o-departamentos-o-ph/alquiler",
    "prop_types": ["casas", "departamentos", "ph"],
    "prop_types_suffix": "/alquiler",
    "url_join": "-o-",
    "url_separator": "/",
    "list_order": "?orden-masnuevos",
    "xpaths": {
        "wait_xpath": "//div[@class='header-widget']",
        "prop_xpath": "//a[@class='card ']",
        "prop_image_xpath": ".//ul[@class='card__photos']/li[1]/img",
        "prop_data_xpath": {
            "precio": ".//p[@class='card__price']",
            "expensas": ".//span[@class='card__expenses']",
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

SOURCES = {
    "zonaprop": ZONAPROP,
    "argenprop": ARGENPROP
}