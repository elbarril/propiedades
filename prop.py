import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import search


def get_ambs_with_format(source: str, ambs_id: str) -> str:
    format_str = search.get_ambs_format(source)
    ambs = search.get_ambs(ambs_id)
    return format_str % (ambs, "s" if int(ambs) > 1 else "")

def get_rooms_with_format(source: str, rooms_id: str) -> str:
    format_str = search.get_rooms_format(source)
    rooms = search.get_rooms(rooms_id)
    return format_str % (rooms, "es" if int(rooms) > 1 else "")

def get_locations(source: str, locations_ids: int) -> str:
    locations_list = search.get_locations_list(locations_ids)
    locations_join = search.get_locations_join(source)
    return locations_join.join(locations_list)

def get_url(source: str, entity: dict) -> str:
    base_url = search.get_base_url(source)
    price = search.get_price(entity["price"])
    ambs = get_ambs_with_format(source, entity["ambs"])
    rooms = get_rooms_with_format(source, entity["rooms"])
    locations = get_locations(source, entity["locations"])
    return base_url % (locations, rooms, ambs, price)

def get_search_data(entity) -> dict:
    return {
        "locations": [loc.replace("-", " ").title() for loc in search.get_locations_list(entity["locations"])],
        "ambs": search.get_ambs(entity["ambs"]).replace("-", " ").title(),
        "rooms": search.get_rooms(entity["rooms"]).replace("-", " ").title(),
        "price": search.get_price(entity["price"]).replace("-", " ").title(),
        "meters": entity["meters"]
    }

def find_props(url: str, prop_xpath: str, wait_xpath: str, next_xpath: str, path_attr: str, id_attr: str, prop_data_xpath: dict, prop_image_xpath: str):
    driver = webdriver.Chrome()
    driver.get(url)

    props_list = []
    next_page = None

    try:
        WebDriverWait(driver, 5).until(
            lambda d: driver.find_element(By.XPATH, wait_xpath).is_displayed()
        )

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        for prop in driver.find_elements(By.XPATH, prop_xpath):
            prop_item = {
                "path": prop.get_attribute(path_attr),
                "content": prop.text,
                "data": {}
            }

            for key, xpath in prop_data_xpath.items():
                try:
                    prop_item["data"][key] = prop.find_element(By.XPATH, xpath).text
                except:
                    continue

            try:
                image = prop.find_element(By.XPATH, prop_image_xpath)
                prop_item.update({
                    "title": image.get_attribute("alt"),
                    "image": image.get_attribute("src")
                })
            except:
                prop_item.update({"title": "", "image": ""})

            props_list.append(prop_item)

        try:
            next_page = driver.find_element(By.XPATH, next_xpath).get_property("href")
        except:
            next_page = None

    except Exception as error:
        print("Errors ocurrs.")

    driver.close()
    return props_list, next_page

def get_prop_meters(prop_content):
    match = re.search(r'([0-9]{2,4})(?:,|.)*m²', prop_content)
    return int(match.group(1)) if match else 0

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

            if path and get_prop_meters(content) >= int(entity["meters"]):
                index += 1
                path = path if "http" in path else base_url[:-1] + path

                if path not in props:
                    props[path] = {
                        "date": time.strftime("%d-%m-%Y"),
                        "index": index,
                        "content": content,
                        "revised": False,
                        "rejected": False,
                        "data": new_prop["data"],
                        "image": new_prop["image"],
                        "title": new_prop["title"]
                    }
                else:
                    props[path].update({key: new_prop[key] for key in ["image", "title", "data"] if not props[path].get(key)})

        keep_looking = page <= len(entity["locations"]) and next_page
        if keep_looking:
            page += 1
            url = next_page
    
    search.save_props(source, name, props)
