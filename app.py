from flask import Flask, render_template, redirect, request

import prop as p

from search import SEARCH, ZONAPROP, ARGENPROP

DEBUG = False

app = Flask(__name__)
@app.route('/')
def home():
    names = SEARCH.keys()
    return render_template('index.html', names=names)

# =========
# ZONAPROP

@app.route('/<name>/zonaprop')
def zonaprop(name):
    entity = SEARCH[name]
    locations = entity.get("locations")
    ambs = entity.get("ambs").get("zonaprop")
    zonaprop_file = "./static/json/zonaprop_" + name + ".json"

    url = p.get_url(locations, ambs, ZONAPROP)

    props = p.load_props(zonaprop_file)
    props = {key:value for key,value in sorted(props.items(), key=lambda item: item[1]["date"], reverse=True) if not value["rejected"]}

    return render_template('list.html', source="zonaprop", props=props, props_url=url, locations=locations, ambs=ambs, name=name)

@app.route('/<name>/zonaprop/rejected')
def zonaprop_rejected(name):
    entity = SEARCH[name]
    locations = entity.get("locations")
    ambs = entity.get("ambs").get("zonaprop")
    zonaprop_file = "./static/json/zonaprop_" + name + ".json"

    url = p.get_url(locations, ambs, ZONAPROP)

    props = p.load_props(zonaprop_file)
    props = {key:value for key,value in sorted(props.items(), key=lambda item: item[1]["date"], reverse=True) if value["rejected"]}
    return render_template('list.html', source="zonaprop", props=props, props_url=url, locations=locations, ambs=ambs, name=name)

@app.route('/<name>/zonaprop/search')
def zonaprop_search(name):
    entity = SEARCH[name]
    locations = entity.get("locations")
    ambs = entity.get("ambs").get("zonaprop")
    zonaprop_file = "./static/json/zonaprop_" + name + ".json"
    min_meters = entity.get("min_meters")
    max_value = entity.get("max_value")
    p.search_props(locations, ambs, zonaprop_file, min_meters, max_value, ZONAPROP)

    return redirect("/" + name + "/zonaprop")

@app.route('/<name>/zonaprop/comment', methods=["POST"])
def zonaprop_comment(name):
    if request.method == 'POST':
        zonaprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        comment = request.form.get("comment", "")
        list_id = request.form.get("list_id", "")
        p.add_comment(prop, comment, zonaprop_file)
        return redirect("/" + name + "/zonaprop#"+list_id)
    return redirect("/")

@app.route('/<name>/zonaprop/unrevise', methods=["POST"])
def zonaprop_unrevise(name):
    if request.method == 'POST':
        zonaprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        p.unrevise_prop(prop, zonaprop_file)
        return redirect("/" + name + "/zonaprop#"+list_id)
    return redirect("/")

@app.route('/<name>/zonaprop/revise', methods=["POST"])
def zonaprop_revise(name):
    if request.method == 'POST':
        zonaprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        p.revise_prop(prop, zonaprop_file)
        return redirect("/" + name + "/zonaprop#"+list_id)
    return redirect("/")

@app.route('/<name>/zonaprop/unreject', methods=["POST"])
def zonaprop_unreject(name):
    if request.method == 'POST':
        zonaprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        p.unreject_prop(prop, zonaprop_file)
        return redirect("/" + name + "/zonaprop/rejected#"+list_id)
    return redirect("/")

@app.route('/<name>/zonaprop/reject', methods=["POST"])
def zonaprop_reject(name):
    if request.method == 'POST':
        zonaprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        p.reject_prop(prop, zonaprop_file)
        return redirect("/" + name + "/zonaprop#"+list_id)
    return redirect("/")

# =========
# ARGENPROP

@app.route('/<name>/argenprop')
def argenprop(name):
    entity = SEARCH[name]
    locations = entity.get("locations")
    ambs = entity.get("ambs").get("argenprop")
    argenprop_file = "./static/json/argenprop_" + name + ".json"

    url = p.get_url(locations, ambs, ARGENPROP)

    props = p.load_props(argenprop_file)
    props = {key:value for key,value in sorted(props.items(), key=lambda item: item[1]["date"], reverse=True) if not value["rejected"]}
    return render_template('list.html', source="argenprop", props=props, props_url=url, locations=locations, ambs=ambs, name=name)

@app.route('/<name>/argenprop/rejected')
def argenprop_rejected(name):
    entity = SEARCH[name]
    locations = entity.get("locations")
    ambs = entity.get("ambs").get("argenprop")
    argenprop_file = "./static/json/zonaprop_" + name + ".json"

    url = p.get_url(locations, ambs, ARGENPROP)

    props = p.load_props(argenprop_file)
    props = {key:value for key,value in sorted(props.items(), key=lambda item: item[1]["date"], reverse=True) if value["rejected"]}
    return render_template('list.html', source="argenprop", props=props, props_url=url, locations=locations, ambs=ambs, name=name)

@app.route('/<name>/argenprop/search')
def argenprop_search(name):
    entity = SEARCH[name]
    locations = entity.get("locations")
    ambs = entity.get("ambs").get("argenprop")
    argenprop_file = "./static/json/zonaprop_" + name + ".json"
    min_meters = entity.get("min_meters")
    max_value = entity.get("max_value")
    p.search_props(locations, ambs, argenprop_file, min_meters, max_value, ARGENPROP)

    return redirect("/" + name + "/argenprop")

@app.route('/<name>/argenprop/comment', methods=["POST"])
def argenprop_comment(name):
    if request.method == 'POST':
        argenprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        comment = request.form.get("comment", "")
        list_id = request.form.get("list_id", "")
        p.add_comment(prop, comment, argenprop_file)
        return redirect("/" + name + "/argenprop#"+list_id)
    return redirect("/")

@app.route('/<name>/argenprop/unrevise', methods=["POST"])
def argenprop_unrevise(name):
    if request.method == 'POST':
        argenprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        p.unrevise_prop(prop, argenprop_file)
        return redirect("/" + name + "/argenprop#"+list_id)
    return redirect("/")

@app.route('/<name>/argenprop/revise', methods=["POST"])
def argenprop_revise(name):
    if request.method == 'POST':
        argenprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        p.revise_prop(prop, argenprop_file)
        return redirect("/" + name + "/argenprop#"+list_id)
    return redirect("/")

@app.route('/<name>/argenprop/unreject', methods=["POST"])
def argenprop_unreject(name):
    if request.method == 'POST':
        argenprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        p.unreject_prop(prop, argenprop_file)
        return redirect("/" + name + "/argenprop/rejected#"+list_id)
    return redirect("/")

@app.route('/<name>/argenprop/reject', methods=["POST"])
def argenprop_reject(name):
    if request.method == 'POST':
        argenprop_file = "./static/json/zonaprop_" + name + ".json"
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        p.reject_prop(prop, argenprop_file)
        return redirect("/" + name + "/argenprop#"+list_id)
    return redirect("/")

if __name__ == '__main__':
    if DEBUG:
        app.run(debug=True)
    else:
        app.run(debug=False, host="0.0.0.0")