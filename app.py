from flask import Flask, render_template, redirect, request
from prop import get_search_data, search_props, get_url
from search import save_search, get_entities, get_entity, load_props, update_prop, get_sources, get_search

app = Flask(__name__)

def get_list_template(name, source, can_search, **options):
    entity = get_entity(name)
    search = get_search_data(entity)
    url = get_url(source, entity)
    props = load_props(source, name, **options)
    return render_template('list.html', name=name, source=source, props_url=url, search=search, props=props, can_search=can_search)

def perform_request(name, source, update_field, extra_path=""):
    if request.method == 'POST':
        prop = request.form.get("prop", "")
        list_id = request.form.get("list_id", "")
        field_name, field_value = update_field
        value = request.form.get(field_name, field_value)
        update_prop(source, name, prop, {field_name: value})
        return redirect(f"/{name}/{source}{extra_path}#{list_id}")
    return redirect("/")

@app.route('/')
def home():
    searches = {name: get_search_data(entity) for name, entity in get_entities().items()}
    sources = get_sources()
    return render_template('index.html', searches=searches, sources=sources, can_create=is_local)

@app.route('/new', methods=["GET", "POST"])
def new():
    if request.method == 'POST':
        save_search(request.form.to_dict())
        return redirect("/")
    
    search = get_search()
    return render_template('new.html', search=search)

@app.route('/<name>/<source>/search')
def search(name, source):
    search_props(source, name)
    return redirect(f"/{name}/{source}")

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

@app.route('/<name>/<source>')
def list(name, source):
    return get_list_template(name, source, can_search=is_local, filter_key="rejected", filter_value=False)

@app.route('/<name>/<source>/rejected')
def list_rejected(name, source):
    return get_list_template(name, source, can_search=is_local, filter_key="rejected", filter_value=True)

DEBUG = True
is_local = False
if __name__ == '__main__':
    is_local = True
    app.run(debug=DEBUG) if DEBUG else app.run(debug=False, host="0.0.0.0")
