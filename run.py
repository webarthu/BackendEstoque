from app import create_app  # Importa a função create_app do módulo 'app', que cria a instância da aplicação Flask.

app = create_app()  # Cria a instância da aplicação Flask chamando a função create_app.

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente (não importado como módulo).
    print("connecting to db")  # Exibe uma mensagem indicando que está conectando ao banco de dados.
    app.run(debug=True)  # Executa o servidor Flask em modo de debug, o que permite a recarga automática de código e mostra erros detalhados.
