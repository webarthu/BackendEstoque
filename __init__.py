from flask import Flask  # Importa a classe Flask do pacote Flask, que é usada para criar a aplicação.
from routes.clientes import clientes_bp  # Importa o blueprint 'clientes_bp' do módulo 'clientes' na pasta 'routes'.
from routes.produtos import produtos_bp  # Importa o blueprint 'produtos_bp' do módulo 'produtos' na pasta 'routes'.
from routes.vendas import vendas_bp  # Importa o blueprint 'vendas_bp' do módulo 'vendas' na pasta 'routes'.

def create_app():  # Função para criar e configurar a aplicação Flask.
    app = Flask(__name__)  # Cria uma instância da aplicação Flask.

    app.register_blueprint(clientes_bp, produtos_bp, vendas_bp)


    return app  # Retorna a instância da aplicação configurada com os blueprints registrados.
