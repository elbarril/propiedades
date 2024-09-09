import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import search


def get_ambs_with_format(source:str, ambs_id:str) -> str:
    format = search.get_ambs_format(source)
    ambs = search.get_ambs(ambs_id)
    return format % (ambs, "s" if int(ambs) > 1 else "")

def get_rooms_with_format(source:str, rooms_id:str) -> int:
    format = search.get_rooms_format(source)
    rooms = search.get_rooms(rooms_id)
    return format % (rooms, "es" if int(rooms) > 1 else "")

def get_locations(source:str, locations_ids:int) -> str:
    locations_list = search.get_locations_list(locations_ids)
    locations_join = search.get_locations_join(source)
    return locations_join.join(locations_list)

def get_url(source:str, entity:dict):
    base_url = search.get_base_url(source)
    price = search.get_price(entity["price"])
    ambs = get_ambs_with_format(source, entity["ambs"])
    rooms = get_rooms_with_format(source, entity["rooms"])
    locations = get_locations(source, entity["locations"])
    return base_url % (locations, rooms, ambs, price)

def get_search_data(entity) -> dict:
    search_data = {
        "locations": [location.replace("-", " ").title() for location in search.get_locations_list(entity["locations"])],
        "ambs": search.get_ambs(entity["ambs"]).replace("-", " ").title(),
        "rooms": search.get_rooms(entity["rooms"]).replace("-", " ").title(),
        "price": search.get_price(entity["price"]).replace("-", " ").title(),
        "meters": entity["meters"]
    }
    return search_data

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

def validate_price_and_meters(max_price:str, min_meters:str, content:str):
    meters = get_prop_meters(content)
    price = get_prop_price(content)
    return int(meters) >= int(min_meters) and int(price) <= int(max_price)

def search_props(source, name):
    entity = search.get_entity(name)
    url = get_url(source, entity)
    props = search.load_props(source, name)
    base_url = search.get_base_url(source)

    page = 1
    index = 0
    keep_looking = True
    while keep_looking:
        xpaths = dict(search.get_xpaths(source))
        xpaths["next_xpath"] = str(xpaths["next_xpath"] % str(page+1))

        new_props, next_page = find_props(url, **xpaths)
        for new_prop in new_props:
            path = new_prop["path"]
            content = new_prop["content"]
            if path and validate_price_and_meters(search.get_price(entity["price"]), entity["meters"], content):
                index += 1
                path = path if "http" in path else base_url[:-1] + path
                data = new_prop["data"]
                image = new_prop["image"]
                title = new_prop["title"]

                if not path in props:
                    prop = {
                        "date": time.strftime("%d-%m-%Y") + "\n",
                        "index": index,
                        "content": content,
                        "revised": False,
                        "rejected": False,
                        "data": data,
                        "image": image,
                        "title": title
                    }

                    props.update({path: prop})
                else:
                    if "image" not in props[path] or not bool(props[path]["image"]):
                        props[path].update({"image": image})
                    if "title" not in props[path] or not bool(props[path]["title"]):
                        props[path].update({"title": title})
                    if "data" not in props[path] or not bool(props[path]["data"]):
                        props[path].update({"data": data})

        keep_looking = page <= len(entity["locations"]) and next_page

        if keep_looking:
            page += 1
            url = next_page
    
    search.save_props(source, name, props)
