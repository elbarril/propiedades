from flask import Flask, render_template, redirect, request

import prop as p

DEBUG = True

def get_list_template(name, source, **options):
    entity = p.get_entity(name)
    locations = p.get_location_names(entity["locations"])
    ambs = p.get_amb_names(entity["ambs"], source)
    file = p.get_file_path(source, name)
    url = p.get_url(locations, ambs, source)
    props = p.load_props(file, **options)
    return render_template('list.html', source=source, props=props, props_url=url, locations=locations, ambs=ambs, name=name)

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
@app.route('/')
def home():
    names = p.get_entities_names()
    sources = p.get_source_names()
    return render_template('index.html', names=names, sources=sources)

@app.route('/<name>/<source>')
def list(name, source):
    return get_list_template(name, source, sort="date", if_not="rejected")

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
    p.search_props(locations, ambs, file, min_meters, max_value, source)
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
    if DEBUG:
        app.run(debug=True)
    else:
        app.run(debug=False, host="0.0.0.0")