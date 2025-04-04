from flask import Flask
from routes.clientes import clientes_bp  # importa seus blueprints
from routes.produtos import produtos_bp

def create_app():
    app = Flask(__name__)

    # aqui você registra os blueprints
    app.register_blueprint(clientes_bp, produtos_bp)

    return app