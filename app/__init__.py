from flask import Flask
from app.routes import routes_bp

def create_app():
    app = Flask(__name__)


    app.register_blueprint(routes_bp, url_prefix="/scraper")

    return app
