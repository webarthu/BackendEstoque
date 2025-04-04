from flask import Flask
from routes.clientes import clientes_bp
from routes.produtos import produtos_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(produtos_bp)
    return app
