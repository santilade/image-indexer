from flask import Flask
from flask_bootstrap import Bootstrap
import secrets


# Generate random key:
GENERATED_KEY = secrets.token_urlsafe(30)
API_BASE_URL = "http://127.0.0.1:5000/"


def create_app():
    # Initialize flask:
    app = Flask(__name__, template_folder='templates')
    Bootstrap(app)
    # Encrypt cookies and session data:
    app.config['SECRET_KEY'] = GENERATED_KEY

    # Import and register blueprints:
    from .image_indexer import image_indexer
    app.register_blueprint(image_indexer, url_prefix='/')

    return app
