from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import json
import re
import time

def get_url(location_list, amb_list, web_options:dict):
    base = web_options.get("base_url")
    url_join:str = web_options.get("url_join")
    separator:str = web_options.get("url_separator")
    types = web_options.get("prop_types") + separator
    locations = url_join.join(location_list) + separator if url_join else separator.join(location_list) + separator
    ambs = url_join.join(amb_list) + separator if url_join else separator.join(amb_list) + separator
    order = web_options.get("list_order")
    return base + types + locations + ambs + order

def load_props(file):
    props:dict[str, dict] = {}
    try:
        with open(file, "r") as f:
            props = json.load(f)
    except Exception as e:
        print(e)
    return props

def save_props(props, file):
    try:
        with open(file, "w", encoding='utf-8') as f:
            json.dump(props, f)
    except Exception as e:
        print(e)

def add_comment(prop, comment, file):
    props = load_props(file)
    if prop in props:
        props[prop].update({"comment": comment})
    save_props(props, file)

def unrevise_prop(prop, file):
    props = load_props(file)
    if prop in props:
        props[prop]["revised"] = False
    save_props(props, file)

def revise_prop(prop, file):
    props = load_props(file)
    if prop in props:
        props[prop]["revised"] = True
    save_props(props, file)

def unreject_prop(prop, file):
    props = load_props(file)
    if prop in props:
        props[prop]["rejected"] = False
    save_props(props, file)

def reject_prop(prop, file):
    props = load_props(file)
    if prop in props:
        props[prop]["rejected"] = True
    save_props(props, file)

def find_props(url, prop_xpath, wait_xpath, next_xpath, path_attr, prop_data_xpath):
    driver = webdriver.Chrome()
    driver.get(url)

    element_to_wait_for = driver.find_element(By.XPATH, wait_xpath)
    wait = WebDriverWait(driver, timeout=5)
    wait.until(lambda d : element_to_wait_for.is_displayed())

    props = driver.find_elements(By.XPATH, prop_xpath)
    props_list = []

    for prop in props:
        path = prop.get_attribute(path_attr)

        data = {}
        if prop_data_xpath:
            for key in prop_data_xpath:
                try:
                    value = prop.find_element(By.XPATH, prop_data_xpath[key])
                    data.update({key: value.text})
                except: continue

        props_list.append({
            "path": path,
            "content": prop.text,
            "data": data
        })

    try:
        next_page:str = driver.find_element(By.XPATH, next_xpath).get_property("href")
        response = (props_list, next_page)
    except:
        response = props_list

    driver.close()
    return response

def get_today():
    return time.strftime("%d-%m-%Y") + "\n"

def get_prop_price(prop_content):
        price = 0
        price_match = re.search(r'\$.([0-9]{3})\.([0-9]{3})(?!.Expensas)', prop_content)
        if price_match: price = int(price_match.groups()[0] + price_match.groups()[1])
        return price

def get_prop_meters(prop_content):
        meters = 0
        meters_match = re.search(r'([0-9]{3}|[0-9]{2})\s*m²', prop_content)
        if meters_match: meters = int(meters_match.groups()[0])
        return meters

def search_props(locations, ambs, file, min_meters, max_value, web_options):
    date = get_today()
    url = get_url(locations, ambs, web_options)
    props = load_props(file)

    base = web_options.get("base_url")
    xpaths = web_options.get("xpaths")

    keep_looking = True
    page = 1

    while keep_looking:
        new_props, next_page = find_props(url, prop_xpath=xpaths["prop_xpath"], wait_xpath=xpaths["wait_xpath"], next_xpath=xpaths["next_xpath"] % str(page+1) if "%" in xpaths["next_xpath"] else xpaths["next_xpath"], path_attr=xpaths["path_attr"], prop_data_xpath=xpaths["prop_data_xpath"])

        for prop in new_props:
            path = prop["path"]
            if not path: continue
            content = prop["content"]
            if "USD" in content: continue
            path = path if "http" in path else base[:-1] + path
            meters = get_prop_meters(content)
            price = get_prop_price(content)
            if meters < min_meters or price > max_value: continue
            
            data = prop["data"]

            if path not in props:
                props.update({path: {
                    "date": date,
                    "content": content,
                    "revised": False,
                    "rejected": False,
                    "data": data
                }})

        if page > 8:
            keep_looking = False

        if keep_looking:
            page += 1
            url = next_page
    
    save_props(props, file)
