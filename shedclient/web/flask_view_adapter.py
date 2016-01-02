import json
import os
import sys
import functools

try:
    from flask import (
        Flask,
        send_from_directory,
        request,
        Markup,
        url_for,
    )
except ImportError:
    Flask = None
    send_from_directory = None
    request = None
    Markup = None
    url_for = None

web_folder = os.path.abspath(os.path.join(os.path.dirname(__file__)))
shedclient_lib_folder = os.path.join(web_folder, os.path.pardir)
static_folder = os.path.join(web_folder, "static")
packed_folder = os.path.join(static_folder, "packed")
vendor_folder = os.path.join(static_folder, "vendor")

if Flask:
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder=static_folder,
    )
else:
    app = None


def jsonify(func):

    @functools.wraps(func)
    def func_to_json(*args, **kwargs):
        rval = func(*args, **kwargs)
        return json.dumps(rval)

    return func_to_json


try:
    from shedclient.toolbox import ShedClientApp
except ImportError:
    sys.path[1:1] = shedclient_lib_folder
    from shedclient.toolbox import ShedClientApp

from galaxy.tools.deps.views import DependencyResolversView

config_ini_path = os.getenv("SHEDCLIENT_CONFIG_INI")
shed_client_app = ShedClientApp(config_ini_path)


def toolbox():
    return shed_client_app.toolbox


def managed_tool_conf_view():
    return toolbox().managed_tool_conf_view


def dependency_resolvers_view():
    return DependencyResolversView(shed_client_app)


def consumes_dependencies_view(func):

    @functools.wraps(func)
    def func_to_json(*args, **kwargs):
        kwargs["view"] = dependency_resolvers_view()
        return func(*args, **kwargs)

    return func_to_json


@app.route('/', methods=['GET'])
def index():
    index = os.path.join(web_folder, "index.html")
    with open(index, "r") as f:
        index_contents = f.read()
    index_contents = index_contents.replace('ROOT_URL', request.url_root)
    return index_contents


@app.route('/api/shed_tool_conf', methods=['GET', 'PUT'])
@jsonify
def shed_tool_conf():
    view = managed_tool_conf_view()
    if request.method == 'PUT':
        view.update(json.loads(request.data))

    return view.get()


@app.route('/api/dependency_resolvers', methods=['GET', 'PUT'])
@jsonify
@consumes_dependencies_view
def dependency_resolvers(view):
    if request.method == 'PUT':
        view.reload()
    return view.index()


@app.route('/api/dependency_resolvers/dependency', methods=['GET'])
@jsonify
@consumes_dependencies_view
def get_manager_dependency(view):
    return view.manager_dependency(**request.args)


@app.route('/api/dependency_resolvers/toolbox', methods=['GET'])
@jsonify
@consumes_dependencies_view
def toolbox_summary(view):
    return view.toolbox_summary(**request.args)


@app.route('/api/dependency_resolvers/<index>/dependency', methods=['GET'])
@jsonify
@consumes_dependencies_view
def get_resolver_dependency(view, index):
    view = dependency_resolvers_view()
    return view.manager_dependency(index, **request.args)


@app.route('/api/dependency_resolvers/<index>', methods=['GET'])
@jsonify
@consumes_dependencies_view
def show_dependency_resolver(view, index):
    return view.show(index)


if __name__ == '__main__':
    app.run(debug=True)
