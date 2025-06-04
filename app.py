from flask import Flask  # Importa a classe Flask do pacote Flask, que é usada para criar a aplicação.
from flask_cors import CORS

from routes.clientes import clientes_bp  # Importa o blueprint 'clientes_bp' do módulo 'clientes' na pasta 'routes'.
from routes.produtos import produtos_bp  # Importa o blueprint 'produtos_bp' do módulo 'produtos' na pasta 'routes'.
from routes.vendas import vendas_bp  # Importa o blueprint 'vendas_bp' do módulo 'vendas' na pasta 'routes'.
from routes.itensVendas import itensVendas_bp

def create_app():  # Função para criar e configurar a aplicação Flask.
    app = Flask(__name__)  # Cria uma instância da aplicação Flask.
    CORS(app)

    app.register_blueprint(clientes_bp)  # Registra o blueprint de clientes na aplicação.
    app.register_blueprint(produtos_bp)  # Registra o blueprint de produtos na aplicação.
    app.register_blueprint(vendas_bp)  # Registra o blueprint de vendas na aplicação.

    app.register_blueprint(itensVendas_bp)
    return app  # Retorna a instância da aplicação configurada com os blueprints registrados.
