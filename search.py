LUI = {
    "locations": [
        "balvanera",
        "san-cristobal",
        "once",
        "barrio-norte",
        "san-nicolas",
        "monserrat",
        "almagro",
        "boedo",
        "parque-patricios",
        "congreso",
        "villa-crespo",
        "parque-centenario"
    ],
    "min_meters": 60,
    "max_value": 750000,
    "zonaprop_file": "./static/json/zonaprop_lui.json",
    "argenprop_file": "./static/json/argenprop_lui.json",
    "ambs": {
        "zonaprop": [
            "mas-de-2-habitaciones",
            "mas-de-3-ambientes"
        ],
        "argenprop": [
            "3-ambientes",
            "4-ambientes"
        ]
    }
}

EMI = {
    "locations": [
        "balvanera",
        "san-cristobal",
        "once",
        "barrio-norte",
        "san-nicolas",
        "monserrat",
        "almagro",
        "boedo",
        "parque-patricios",
        "congreso",
        "villa-crespo",
        "parque-centenario"
    ],
    "min_meters": 30,
    "max_value": 350000,
    "zonaprop_file": "./static/json/zonaprop_emi.json",
    "argenprop_file": "./static/json/argenprop_emi.json",
    "ambs": {
        "zonaprop": [
            "1-habitacion",
            "2-ambientes"
        ],
        "argenprop": [
            "monoambiente",
            "2-ambientes"
        ]
    }
}

SEARCH = {
    "lui": LUI,
    "emi": EMI
}

ZONAPROP = {
    "base_url": "https://www.zonaprop.com.ar/",
    "prop_types": "inmuebles-alquiler",
    "url_separator": "-",
    "list_order": "orden-publicado-descendente.html",
    "xpaths": {
        "wait_xpath": "//button[@data-qa='cookies-policy-banner']",
        "prop_xpath": "//div[@data-qa='posting PROPERTY']",
        "prop_data_xpath": {
            "precio": ".//div[@data-qa='POSTING_CARD_PRICE']",
            "expensas": ".//div[@data-qa='expensas']",
            "direccion": ".//div[contains(@class, 'postingAddress')]",
            "metros": ".//h3[@data-qa='POSTING_CARD_FEATURES']/span[1]",
            "habitaciones": ".//h3[@data-qa='POSTING_CARD_FEATURES']/span[2]",
            "hace": "./div/div[2]/div[2]/div[2]"
        },
        "next_xpath": "//a[@data-qa='PAGING_%s']",
        "path_attr": "data-to-posting"
    }
}

ARGENPROP = {
    "base_url": "https://www.argenprop.com/",
    "prop_types": "casas-o-departamentos-o-ph/alquiler",
    "url_join": "-o-",
    "url_separator": "/",
    "list_order": "?orden-masnuevos",
    "xpaths": {
        "wait_xpath": "//div[@class='header-widget']",
        "prop_xpath": "//a[@class='card ']",
        "prop_data_xpath": {
            "precio": ".//p[@class='card__price']",
            "expensas": ".//span[@class='card__expenses']",
            "direccion": ".//p[@class='card__address']",
            "metros": ".//ul[@class='card__main-features']/li[1]",
            "habitaciones": ".//ul[@class='card__main-features']/li[2]",
            "hace": "./div/div[2]/div[2]/div[2]"
        },
        "next_xpath": "//li[@class='pagination__page']/a",
        "path_attr": "href"
    }
}