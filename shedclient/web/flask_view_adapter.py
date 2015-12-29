import json
import os
try:
    from flask import (
        Flask,
        send_from_directory,
        request,
    )
except ImportError:
    Flask = None
    send_from_directory = None
    request = None

web_folder = os.path.abspath(os.path.join(os.path.dirname(__file__)))
packed_folder = os.path.join(web_folder, "packed")

if Flask:
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder=packed_folder,
    )
else:
    app = None

from galaxy.tools.toolbox import managed_conf
managed_tool_conf = managed_conf.ManagedConf("./shed_tools.json")
managed_tool_conf_view = managed_conf.ManagedConfView(managed_tool_conf)


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(web_folder, 'index.html')


@app.route('/shed_tool_conf', methods=['GET', 'PUT'])
def shed_tool_conf():
    if request.method == 'PUT':
        return_json = managed_tool_conf_view.put(request.form_data)
    else:
        return_json = managed_tool_conf_view.get()
    return json.dumps(return_json)


if __name__ == '__main__':
    app.run(debug=True)
