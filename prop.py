from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import json
import re
import time

from search import SOURCES, LOCATIONS, AMBS, JSON_PATH

import json
from os import walk

def get_search_entities():
    search_files = next(walk(JSON_PATH.joinpath("search/")), (None, None, []))[2]  # [] if no file
    search_entities:dict[str, dict] = {}
    for search_file in search_files:
        filename, extension = tuple(search_file.split("."))
        with open(JSON_PATH.joinpath("search/").joinpath(search_file), "r", encoding="utf-8") as file:
            json_data = json.load(file)
            search_entities.setdefault(filename, json_data)
    return search_entities

def save_search(name:str, locations, price, meters, ambs, dolar):
    try:
        entity = {
            "locations": locations,
            "min_meters": meters,
            "max_value": price,
            "ambs": ambs,
            "dolar": True if dolar else False
        }
        with open(JSON_PATH.joinpath("search/").joinpath(name.replace(" ", "") + ".json"), "w", encoding='utf-8') as f:
            json.dump(entity, f)
    except Exception as e:
        print(e)

def get_locations():
    return LOCATIONS

def get_ambs():
    return AMBS

def get_source_names():
    return SOURCES.keys()

def get_entities_names():
    return get_search_entities().keys()

def get_entity(name):
    return get_search_entities()[name]

def get_source(name):
    return SOURCES[name]

def get_location_names(location_keys):
    return [LOCATIONS[location] for location in location_keys]

def get_amb_names(amb_keys, source):
    return [AMBS[source][amb] for amb in amb_keys[source]]

def get_file_path(source, name):
    return  JSON_PATH.joinpath(source + "_" + name + ".json")

def get_url(location_list, amb_list, source):
    web_options = get_source(source)
    base = web_options.get("base_url")
    url_join:str = web_options.get("url_join")
    separator:str = web_options.get("url_separator")
    types_suffix = web_options.get("prop_types_suffix")
    types = web_options.get("prop_types")
    types_separator = types_suffix + separator if types_suffix else separator
    types = url_join.join(types) + types_separator if url_join else separator.join(types) + types_separator
    locations = url_join.join(location_list) + separator if url_join else separator.join(location_list) + separator
    ambs = url_join.join(amb_list) + separator if url_join else separator.join(amb_list) + separator
    order = web_options.get("list_order")
    return base + types + locations + ambs + order

def load_props(file, sort=None, if_not=None, if_yes=None):
    props:dict[str, dict] = {}
    try:
        with open(file, "r") as f:
            props = json.load(f)
    except Exception as e:
        print(e)

    if sort:
        if if_not:
            props = {key:value for key,value in sorted(props.items(), key=lambda item: item[1][sort], reverse=True) if not value[if_not]}
        elif if_yes:
            props = {key:value for key,value in sorted(props.items(), key=lambda item: item[1][sort], reverse=True) if value[if_yes]}
        else:
            props = {key:value for key,value in sorted(props.items(), key=lambda item: item[1][sort], reverse=True)}

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
        path = prop.get_attribute(path_attr)
        id = prop.get_attribute(id_attr)

        data = {}
        
        for key in prop_data_xpath:
            try:
                value = prop.find_element(By.XPATH, prop_data_xpath[key])
                data.update({key: value.text})
            except: continue

        try:
            image = prop.find_element(By.XPATH, prop_image_xpath)
            title = image.get_attribute("alt")
            image_src = image.get_attribute("src")
        except: 
            image_src = title = ""

        props_list.append({
            "id": id,
            "path": path,
            "content": prop.text,
            "data": data,
            "image": image_src,
            "title": title
        })

    try:
        next_page:str = driver.find_element(By.XPATH, next_xpath).get_property("href")
    except:
        next_page = None
    driver.close()

    return (props_list, next_page)

def get_today():
    return time.strftime("%d-%m-%Y") + "\n"

def get_prop_price(prop_content, dolar):
        price = 0
        if dolar:
            regex = r'USD.([0-9]{3})'
        else:
            regex = r'\$.([0-9]{3})\.([0-9]{3})(?!.Expensas)'
        price_match = re.search(regex, prop_content)
        if price_match: 
            if dolar:
                price = int(price_match.groups()[0])
            else:
                price = int(price_match.groups()[0] + price_match.groups()[1])
        return price

def get_prop_meters(prop_content):
        meters = 0
        meters_match = re.search(r'([0-9]{3}|[0-9]{2})\s*m²', prop_content)
        if meters_match: meters = int(meters_match.groups()[0])
        return meters

def search_props(locations, ambs, file, min_meters, max_value, dolar, source):
    web_options = get_source(source)
    date = get_today()
    url = get_url(locations, ambs, source)
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
            if not dolar and "USD" in content: continue
            if dolar and not "USD" in content: continue
            path = path if "http" in path else base[:-1] + path
            meters = get_prop_meters(content)
            price = get_prop_price(content, dolar)
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
