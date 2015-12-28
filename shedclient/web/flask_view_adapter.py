import os
try:
    from flask import Flask
    from flask import send_from_directory
except ImportError:
    Flask = None
    send_from_directory = None

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


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(web_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
