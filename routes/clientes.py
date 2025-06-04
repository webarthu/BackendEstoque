from flask import Blueprint, jsonify, request  # Importa as funções necessárias do Flask.
from connection import get_connection  # Importa a função get_connection para estabelecer a conexão com o banco de dados.

clientes_bp = Blueprint('clientes', __name__)  # Cria um Blueprint para as rotas de clientes.

# GET - Rota para obter todos os clientes
@clientes_bp.route('/Clientes', methods=['GET'])
def get_table():
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        cursor.execute("SELECT * FROM Clientes")  # Executa a consulta para buscar os clientes.
        clientes = cursor.fetchall()  # Obtém todos os resultados.

        # Formata os resultados em um formato mais amigável
        clientes = [{"id_cliente": cliente[0], "nome_cliente": cliente[1], "telefone": cliente[2]} for cliente in clientes]

        return jsonify({"clientes": clientes}), 200  # Retorna a lista de clientes em formato JSON.

    except Exception as e:
        return jsonify({"Error": str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.

    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.


# POST - Rota para cadastrar um novo cliente
@clientes_bp.route('/registerClientes', methods=['POST'])
def post_clientes():
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        nome = request.json.get('nome')  # Obtém o nome do cliente do corpo da requisição.
        telefone = request.json.get('Telefone')  # Obtém o telefone do cliente do corpo da requisição.

        # Valida se os dados obrigatórios estão presentes
        if not nome or not telefone:
            return jsonify({"error": "Nome e Telefone são obrigatórios"}), 400

        cursor.execute("INSERT INTO Clientes (nome, Telefone) VALUES (%s, %s)", (nome, telefone))  # Insere o novo cliente.

        cliente_id = cursor.lastrowid  # Obtém o ID do cliente recém inserido.
        con.commit()  # Aplica as alterações no banco de dados.

        return jsonify({"Cliente": "created", "Nome": nome, "Telefone": telefone, "ID": cliente_id}), 200  # Retorna o cliente criado.

    except Exception as e:
        return jsonify({"Error": str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.

    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.


# PATCH - Rota para atualizar os dados de um cliente
@clientes_bp.route('/changeClientes/<int:id>', methods=['PATCH'])
def changeClientes(id):
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        
        change = request.get_json()  # Obtém os dados a serem alterados no corpo da requisição.
        if not change:  # Caso nenhum dado seja enviado no PATCH.
            return jsonify({"mensagem": "Nenhum dado enviado para o PATCH"}), 400

        # Cria a parte da query que irá atualizar os campos enviados.
        campos = ', '.join([f"{key} = %s" for key in change.keys()])
        
        valores = list(change.values())  # Obtém os novos valores para atualização.
        valores.append(id)  # Adiciona o ID do cliente no final da lista de valores.

        # Monta a query de atualização.
        query = f"UPDATE Clientes SET {campos} WHERE id=%s"

        cursor.execute(query, valores)  # Executa a query de atualização.
        con.commit()  # Aplica as alterações no banco de dados.
        return jsonify({"UPDATED": "Dados atualizados com sucesso!"}), 200  # Retorna a mensagem de sucesso.

    except Exception as e:
        return jsonify({"Error": str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.

    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.


# DELETE - Rota para deletar um cliente pelo ID
@clientes_bp.route('/delete/<int:id>', methods=['DELETE'])
def deleteClientes(id):
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        cursor.execute("SELECT nome FROM Clientes WHERE id=%s", (id,))  # Verifica se o cliente existe.

        result = cursor.fetchone()  # Obtém o nome do cliente se encontrado.
        if not result:  # Caso o cliente não seja encontrado.
            return jsonify({"Error": "Cliente não encontrado"}), 400

        nome = result[0]  # Obtém o nome do cliente.

        cursor.execute("DELETE FROM Clientes WHERE id=%s", (id,))  # Deleta o cliente.
        con.commit()  # Aplica as alterações no banco de dados.

        return jsonify({"Message": "Cliente deletado", "Nome do cliente": nome, "ID do cliente": id}), 200  # Retorna a mensagem de sucesso.

    except Exception as e:
        return jsonify({"Error": str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.

    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.
