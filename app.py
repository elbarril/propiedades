from flask import Flask, render_template, redirect, request

import prop as p

DEBUG = True

def get_list_template(name, source, can_search, **options):
    entity = p.get_entity(name)
    locations = p.get_location_names(entity["locations"])
    ambs = p.get_amb_names(entity["ambs"], source)
    file = p.get_file_path(source, name)
    url = p.get_url(locations, ambs, source)
    props = p.load_props(file, **options)
    return render_template('list.html', source=source, props=props, props_url=url, locations=locations, ambs=ambs, name=name, can_search=can_search)

def perform_request(name, source, update_field, extra_path=""):
    if request.method == 'POST':
        file = p.get_file_path(source, name)
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        field_name, field_value = update_field
        value = request.form.get(field_name, field_value)
        p.update_prop(prop, {field_name: value}, file)
        return redirect("/" + name + "/" + source + extra_path + "#"+list_id)
    return redirect("/")

app = Flask(__name__)
@app.route('/new', methods=["GET", "POST"])
def new():
    locations = p.get_locations()
    ambs = p.get_ambs()
    if request.method == 'POST':
        locations_selected = request.form.getlist("locations")
        ambs_zonaprop = request.form.getlist("amb-zonaprop")
        ambs_argenprop = request.form.getlist("amb-argenprop")
        ambs_selected = {
            "zonaprop": ambs_zonaprop,
            "argenprop": ambs_argenprop
        }
        name = request.form.get("name", "")
        meters = request.form.get("meters", "")
        price = request.form.get("price", "")
        dolar = request.form.get("dolar", "")

        p.save_search(name, locations_selected, price, meters, ambs_selected, dolar)

        return redirect("/")

    return render_template('new.html', locations=locations, ambs=ambs)

@app.route('/<name>/<source>/rejected')
def list_rejected(name, source):
    return get_list_template(name, source, sort="date", if_yes="rejected")

@app.route('/<name>/<source>/search')
def search(name, source):
    entity = p.get_entity(name)
    locations = p.get_location_names(entity["locations"])
    ambs = p.get_amb_names(entity["ambs"], source)
    file = p.get_file_path(source, name)
    min_meters = entity["min_meters"]
    max_value = entity["max_value"]
    dolar = entity["dolar"]
    p.search_props(locations, ambs, file, min_meters, max_value, dolar, source)
    return redirect("/" + name + "/" + source)

@app.route('/<name>/<source>/comment', methods=["POST"])
def comment(name, source):
    return perform_request(name, source, ("comment", ""))

@app.route('/<name>/<source>/unrevise', methods=["POST"])
def unrevise(name, source):
    return perform_request(name, source, ("revised", False))

@app.route('/<name>/<source>/revise', methods=["POST"])
def revise(name, source):
    return perform_request(name, source, ("revised", True))

@app.route('/<name>/<source>/unreject', methods=["POST"])
def unreject(name, source):
    return perform_request(name, source, ("rejected", False), extra_path="/rejected")

@app.route('/<name>/<source>/reject', methods=["POST"])
def reject(name, source):
    return perform_request(name, source, ("rejected", True))

if __name__ == '__main__':
    @app.route('/<name>/<source>')
    def list(name, source):
        return get_list_template(name, source, can_search=True, sort="date", if_not="rejected")

    @app.route('/')
    def home():
        entities = p.get_search_entities()
        sources = p.get_source_names()
        location_names = p.get_locations()
        amb_names = p.get_ambs()
        return render_template('index.html', entities=entities, sources=sources, location_names=location_names, amb_names=amb_names, can_create=True)

    if DEBUG:
        app.run(debug=True)
    else:
        app.run(debug=False, host="0.0.0.0")

else:
    @app.route('/<name>/<source>')
    def list(name, source):
        return get_list_template(name, source, can_search=False, sort="date", if_not="rejected")

    @app.route('/')
    def home():
        entities = p.get_search_entities()
        sources = p.get_source_names()
        location_names = p.get_locations()
        amb_names = p.get_ambs()
        return render_template('index.html', entities=entities, sources=sources, location_names=location_names, amb_names=amb_names, can_create=False)