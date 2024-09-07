from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import json
import re
import time

from search import SEARCH, JSON_PATH, SEARCH_PATH

import json
from os import walk

#FIXME once create another search server needs to be rebooted to update SEARCH_ENTITIES
SEARCH_ENTITIES:dict[str, dict] = {}
for search_file in next(walk(SEARCH_PATH), (None, None, []))[2]:
    with open(SEARCH_PATH / search_file, "r", encoding="utf-8") as file:
        SEARCH_ENTITIES.setdefault(search_file.split(".")[0], json.load(file))

def save_search(search):
    try:
        entity = {
            "locations": search.getlist("locations"),
            "meters": search.get("meters"),
            "price": search.get("price"),
            "ambs": search.get("ambs"),
            "rooms": search.get("rooms")
        }
        file_name = search.get("name").replace(" ", "") + ".json"
        with open(SEARCH_PATH / file_name, "w", encoding='utf-8') as f:
            json.dump(entity, f)
    except Exception as e:
        print(e)

def get_file_path(source, name):
    return  JSON_PATH / f"{source}_{name}.json"

def get_url(source, entity):
    web_options = SEARCH["sources"][source]

    base = web_options.get("base_url")
    rooms_format = web_options.get("rooms_format")
    ambs_format = web_options.get("ambs_format")

    locations_list = [SEARCH["locations"][int(location)] for location in entity.get("locations")]
    ambs_int = int(SEARCH["ambs"][int(entity.get("ambs"))])
    rooms_int = int(SEARCH["rooms"][int(entity.get("rooms"))])
    price_str = SEARCH["prices"][int(entity.get("price"))]

    ambs_str = ambs_format % (ambs_int, "s" if ambs_int > 1 else "")
    rooms_str = rooms_format % (rooms_int, "es" if rooms_int > 1 else "")
    locations_join = web_options.get("locations_join")
    locations_str = locations_join.join(locations_list)

    return base % (locations_str, rooms_str, ambs_str, price_str)

def load_props(file, filter_key=None, filter_value=True):
    props = {}

    try:
        with open(file, "r") as f:
            props = json.load(f)
    except Exception as e:
        print(e)
    else:
        if filter_key is not None:
            props = {key: value for key, value in props.items() if value.get(filter_key) == filter_value}

    return props

def save_props(props, file):
    try:
        with open(file, "w", encoding='utf-8') as f:
            json.dump(props, f)
    except Exception as e:
        print(e)

def update_prop(prop, update, file):
    props = load_props(file)
    if prop in props:
        props[prop].update(update)
    save_props(props, file)

def find_props(url, prop_xpath, wait_xpath, next_xpath, path_attr, id_attr, prop_data_xpath, prop_image_xpath):
    driver = webdriver.Chrome()
    driver.get(url)

    element_to_wait_for = driver.find_element(By.XPATH, wait_xpath)
    wait = WebDriverWait(driver, timeout=5)
    wait.until(lambda d : element_to_wait_for.is_displayed())
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    props = driver.find_elements(By.XPATH, prop_xpath)
    props_list = []

    for prop in props:
        prop_list_item = {
            "id": prop.get_attribute(id_attr),
            "path": prop.get_attribute(path_attr),
            "content": prop.text,
            "data": {}
        }
        
        for key in prop_data_xpath:
            try:
                value = prop.find_element(By.XPATH, prop_data_xpath[key])
                prop_list_item["data"].update({key: value.text})
            except: continue

        try:
            image = prop.find_element(By.XPATH, prop_image_xpath)
            image_title = image.get_attribute("alt")
            image_src = image.get_attribute("src")
        except: 
            image_src = image_title = ""

        prop_list_item.update({
            "title": image_title,
            "image": image_src
        })
        props_list.append(prop_list_item)

    try:
        next_page:str = driver.find_element(By.XPATH, next_xpath).get_property("href")
    except:
        next_page = None
    driver.close()

    return (props_list, next_page)

def get_prop_price(prop_content):
    price = 0
    regex = r'USD.([0-9]{1,3}\.[0-9]{3}\.([0-9]{3}))'
    price_match = re.search(regex, prop_content)
    if price_match:
        price = int(price_match.groups()[0])
    return price

def get_prop_meters(prop_content):
    meters = 0
    meters_match = re.search(r'([0-9]{3}|[0-9]{2})\s*m²', prop_content)
    if meters_match: meters = int(meters_match.groups()[0])
    return meters

def search_props(source, entity_name):
    entity = SEARCH_ENTITIES.get(entity_name)
    locations = [SEARCH["locations"][int(location)] for location in entity["locations"]]
    file = get_file_path(source, entity_name)
    min_meters = entity["meters"]
    max_value = entity["price"]
    web_options = SEARCH["sources"][source]
    date = time.strftime("%d-%m-%Y") + "\n"
    url = get_url(source, entity)
    props = load_props(file)

    base = web_options.get("base_url")

    keep_looking = True
    page = 1
    index = 0
    while keep_looking:
        xpaths = dict(web_options.get("xpaths"))
        xpaths["next_xpath"] = str(xpaths["next_xpath"] % str(page+1))

        new_props, next_page = find_props(url, **xpaths)

        for new_prop in new_props:
            index += 1
            path = new_prop["path"]
            if not path: continue
            content = new_prop["content"]
            path = path if "http" in path else base[:-1] + path
            meters = get_prop_meters(content)
            price = get_prop_price(content)
            if int(meters) < int(min_meters) or int(price) > int(max_value): continue
            
            id = new_prop["id"]
            data = new_prop["data"]
            image = new_prop["image"]
            title = new_prop["title"]

            if not path in props:
                prop = {
                    "id": id,
                    "date": date,
                    "index": index,
                    "content": content,
                    "revised": False,
                    "rejected": False,
                    "data": data,
                    "image": image,
                    "title": title
                }

                props.update({path: prop})
            elif "image" not in props[path] or not bool(props[path]["image"]):
                props[path].update({"image": image})
            elif "title" not in props[path] or not bool(props[path]["title"]):
                props[path].update({"title": title})
            elif "data" not in props[path] or not bool(props[path]["data"]):
                props[path].update({"data": data})

        if page > len(locations) // 2 or next_page is None:
            keep_looking = False

        if keep_looking:
            page += 1
            url = next_page
    
    save_props(props, file)
