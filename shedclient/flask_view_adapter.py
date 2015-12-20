try:
    from flask import Flask
except ImportError:
    Flask = None

if Flask:
    app = Flask(
        __name__,
        static_url_path='/static',
    )
else:
    app = None

if __name__ == '__main__':
    app.run(debug=True)
