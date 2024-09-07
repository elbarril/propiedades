from flask import Flask, render_template, redirect, request

from prop import SEARCH_ENTITIES, SEARCH, save_search
from prop import search_props, load_props, update_prop
from prop import get_file_path, get_url

def get_list_template(name, source, can_search, **options):
    entity = SEARCH_ENTITIES.get(name)
    file = get_file_path(source, name)
    url = get_url(source, entity)
    props = load_props(file, **options)
    return render_template('list.html', entity=entity, search=SEARCH, source=source, props=props, props_url=url, name=name, can_search=can_search)

def perform_request(name, source, update_field, extra_path=""):
    if request.method == 'POST':
        file = get_file_path(source, name)
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        field_name, field_value = update_field
        value = request.form.get(field_name, field_value)
        update_prop(prop, {field_name: value}, file)
        return redirect("/" + name + "/" + source + extra_path + "#"+list_id)
    return redirect("/")

app = Flask(__name__)

@app.route('/new', methods=["GET", "POST"])
def new():
    if request.method == 'POST':
        save_search(request.form)
        return redirect("/")
    return render_template('new.html', search=SEARCH)

@app.route('/<name>/<source>/search')
def search(name, source):
    search_props(source, name)
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


DEBUG = True
is_local = False
if __name__ == '__main__':
    is_local = True

@app.route('/<name>/<source>')
def list(name, source):
    return get_list_template(name, source, can_search=is_local, filter_key="rejected", filter_value=False)

@app.route('/<name>/<source>/rejected')
def list_rejected(name, source):
    return get_list_template(name, source, can_search=is_local, filter_key="rejected", filter_value=True)

@app.route('/')
def home():
    return render_template('index.html', entities=SEARCH_ENTITIES, search=SEARCH, can_create=is_local)

if is_local:
    if DEBUG:
        app.run(debug=True)
    else:
        app.run(debug=False, host="0.0.0.0")
