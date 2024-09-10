from pathlib import Path
from os import walk
import json

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
        "5"
    ],
    "ambs": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
    ],
    "prices": [
        "100000",
        "150000",
        "200000",
        "250000",
        "300000",
        "350000",
        "400000",
        "450000",
        "500000",
        "550000",
        "600000",
        "650000",
        "700000",
        "750000",
        "800000",
        "850000",
        "900000",
        "950000",
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

def get_search() -> dict:
    return SEARCH

def get_sources() -> list:
    return list(SEARCH["sources"].keys())

def get_entities() -> dict:
    search_entities:dict[str, dict] = {}
    for search_file in next(walk(SEARCH_PATH), (None, None, []))[2]:
        with open(SEARCH_PATH / search_file, "r", encoding="utf-8") as file:
            search_entities.setdefault(search_file.split(".")[0], json.load(file))
    return search_entities

def save_search(entity:dict):
    try:
        file_name = entity["name"].replace(" ", "") + ".json"
        with open(SEARCH_PATH / file_name, "w", encoding='utf-8') as f:
            json.dump(entity, f)
    except Exception as e:
        print(e)

def filter_props(props:dict, filter_key:str, filter_value) -> dict:
    return {key: value for key, value in props.items() if value.get(filter_key) == filter_value}

def load_props(source:str, name:str, filter_key=None, filter_value=True) -> dict:
    file = get_file_path(source, name)
    props = {}
    try:
        with open(file, "r") as f:
            props:dict = json.load(f)
    except Exception as e:
        print(e)
    else:
        if filter_key is not None:
            props = filter_props(props, filter_key, filter_value)
    return props

def save_props(source:str, name:str, props:dict):
    file = get_file_path(source, name)
    try:
        with open(file, "w", encoding='utf-8') as f:
            json.dump(props, f)
    except Exception as e:
        print(e)

def update_prop(source:str, name:str, prop:str, update:dict):
    props = load_props(source, name)
    if prop in props:
        props[prop].update(update)
    save_props(source, name, props)

def get_entity(name:str):
    return get_entities().get(name)

def get_file_path(source:str, name:str):
    return  JSON_PATH / f"{source}_{name}.json"

def get_base_url(source:str) -> str:
    return SEARCH["sources"][source]["base_url"]

def get_locations_join(source:str) -> str:
    return SEARCH["sources"][source]["locations_join"]

def get_locations_list(locations_ids:list) -> list:
    return [SEARCH["locations"][int(location)] for location in locations_ids]

def get_xpaths(source:str) -> dict:
    return SEARCH["sources"][source]["xpaths"]

def get_ambs(ambs_id:str) -> str:
    return SEARCH["ambs"][int(ambs_id)]

def get_ambs_format(source:str) -> str:
    return SEARCH["sources"][source]["ambs_format"]

def get_rooms(rooms_id:str) -> str:
    return SEARCH["rooms"][int(rooms_id)]

def get_rooms_format(source:str) -> str:
    return SEARCH["sources"][source]["rooms_format"]

def get_price(price_id:str) -> str:
    return SEARCH["prices"][int(price_id)]
