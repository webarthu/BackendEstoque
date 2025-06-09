from flask import Blueprint, jsonify, request  # Importa as funções necessárias do Flask para criar rotas, enviar respostas JSON e receber dados da requisição.
from connection import get_connection  # Importa a função get_connection para estabelecer a conexão com o banco de dados.

produtos_bp = Blueprint('produtos', __name__)  # Cria um Blueprint para as rotas de produtos.

# GET - Rota para obter todos os produtos
@produtos_bp.route('/Produtos', methods=['GET'])
def getProducts():
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        cursor.execute("SELECT * FROM Produtos")  # Executa a consulta para buscar todos os produtos.
        produtos = cursor.fetchall()  # Obtém todos os resultados da consulta.

        if not produtos:
            return jsonify({"status": "error", 
                            "message": "Produtos não encontrados"
                            }), 404
        
        # Cria uma lista de dicionários com os dados dos produtos.
        produtos = [{"id_produto": produto[0], "nome_produto": produto[1], "descricao": produto[2], "valor": produto[3], "quantidade": produto[4]} for produto in produtos]

        return jsonify({
                        "status": "success", 
                        "Produtos": [produtos]
                        }), 200  # Retorna os produtos como resposta JSON.
    
    except Exception as e:
        return jsonify({"status": "error", 
                        "message": str(e)
                        }), 500  # Caso ocorra algum erro, retorna a mensagem de erro.
    
    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.


@produtos_bp.route('/Produtosnome', methods=['GET'])
def get_produto_nome():
    con = get_connection()
    try:
        cursor = con.cursor()
        nome_produto = request.args.get('nome')

        if not nome_produto:
            return jsonify({"status": "error", "message": "Parâmetro 'nome' não fornecido"}), 400

        like_pattern = f"%{nome_produto}%"
        cursor.execute("SELECT * FROM Produtos WHERE nome LIKE %s", (like_pattern,))
        produtos = cursor.fetchall()

        print('produtos:', produtos)

        if not produtos:
            return jsonify({"status": "error", "message": "Produto não encontrado"}), 404

        if len(produtos) > 1:
            print("produtos", produtos)

            return jsonify({
            "status": "success",
            "message": "Produtos encontrados com sucesso",
            "data": produtos
        }), 200
        
        else:
            linha = produtos[0]
            produto_dict = {
                "id": linha[0],
                "name": linha[1],
                "description": linha[2]
            }

            print("produto_dict:", produto_dict)

            return jsonify({
                "status": "success",
                "message": "Produto encontrado com sucesso",
                "data": produto_dict
            }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cursor.close()
        con.close()


#GET WITH ID
@produtos_bp.route('/Produtos/<int:id_produto>', methods=['GET'])
def getProdutoID(id_produto):
    con = get_connection()
    try:
        cursor = con.cursor()

        cursor.execute("SELECT * FROM Produtos WHERE id=%s", (id_produto,))
        produto = cursor.fetchone()

        if not produto:
            return jsonify({"status": "error", "message": "Produto não encontrado"}), 404

        produto_dict = {"id": produto[0],
                    "name": produto[1],
                    "description": produto[2]
                    }

        return jsonify({"status": "success",
                        "message": "produto encontrado com sucesso",
                        "data": produto_dict
                        }),200

    except Exception as e:
        return jsonify({"status": "Error",
                         "message":str(e)
                         }),500

    finally:
        cursor.close()
        con.close()


# POST - Rota para registrar um novo produto
@produtos_bp.route('/registerProducts', methods=['POST'])
def registerProduct():
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        
        nome = request.json.get('nome')  # Obtém o nome do produto da requisição JSON.
        descricao = request.json.get('descricao')  # Obtém a descrição do produto da requisição JSON.
        valor = request.json.get('valor')  # Obtém o valor do produto da requisição JSON.
        quantidade = request.json.get('quantidade')  # Obtém a quantidade do produto da requisição JSON.
        
        # Valida os dados obrigatórios para o cadastro.
        if not nome: 
            return jsonify({
                "error": "Nome do produto é obrigatório"
                }),400
        if not descricao: 
            descricao = ''  # Se não houver descrição, define uma descrição vazia.
        if not valor or valor <= 0: 
            return jsonify({
                "error": "Valor obrigatório"
                }),400
        if not quantidade or quantidade < 0: 
            return jsonify({
                "error": "Quantidade de produtos obrigatória"
                }),400

        # Insere o produto no banco de dados.
        cursor.execute("INSERT INTO Produtos (nome, descricao, valor, quantidade) VALUES (%s, %s, %s, %s)", 
                       (nome, descricao, valor, quantidade))

        produto_id = cursor.lastrowid  # Obtém o ID do produto recém-criado.
        con.commit()  # Commit para salvar as mudanças no banco de dados.
        
        # Retorna uma resposta com os dados do produto cadastrado.
        return jsonify({"status": "success",
                        "message": "Product successfully registered",
                        "product": {
                        "id": produto_id,
                        "name": nome,
                        "description": descricao,
                        "price": valor,
                        "quantity": quantidade
                    }}), 200
    
    except Exception as e:
        return jsonify({'Error': str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.
    
    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.


# PATCH - Rota para atualizar dados de um produto
@produtos_bp.route('/changeProdutos/<int:id>', methods=['PATCH'])
def changeProdutos(id):
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.

        change = request.get_json()  # Obtém os dados da requisição JSON.
        
        if not change:
            return jsonify({
                "message": "Nenhum dado enviado para o PATCH"
                }), 400  # Caso não haja dados na requisição.

        # Cria uma string com os campos a serem atualizados.
        campos = ', '.join([f"{key} = %s" for key in change.keys()])

        valores = list(change.values())  # Obtém os valores a serem atualizados.
        valores.append(id)  # Adiciona o ID do produto à lista de valores.

        # Monta a query para atualizar o produto.
        query = f"UPDATE Produtos SET {campos} WHERE id=%s"

        cursor.execute(query, valores)  # Executa a consulta de atualização.
        con.commit()  # Commit para salvar as mudanças no banco de dados.

        return jsonify({  
                        "status": "success",
                        "message": "Product updated successfully"  
                        }), 200  # Retorna uma mensagem de sucesso.
    
    except Exception as e:
        return jsonify({"status": "error", 
                        "message": str(e)
                        }), 500  # Caso ocorra algum erro, retorna a mensagem de erro.
    
    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.


# DELETE - Rota para deletar um produto
@produtos_bp.route('/deleteProduct/<int:id>', methods=['DELETE'])
def deleteProduct(id):
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        cursor.execute("SELECT nome FROM Produtos WHERE id=%s", (id,))  # Executa a consulta para buscar o produto pelo ID.

        result = cursor.fetchone()  # Obtém o resultado da consulta.
        if not result:
            return jsonify({
                "Error": "Produto não encontrado"
                }), 404  # Caso o produto não seja encontrado, retorna erro.
        
        nome_produto = result[0]  # Obtém o nome do produto.

        cursor.execute("DELETE FROM Produtos WHERE id=%s", (id,))  # Deleta o produto do banco de dados.
        con.commit()  # Commit para salvar as mudanças no banco de dados.

        return jsonify({
            "Message": "Produto deletado", 
            "Nome do produto": nome_produto, 
            "ID do produto": id
            }), 200  # Retorna uma mensagem de sucesso.
    
    except Exception as e:
        return jsonify({"status": "error",
                        "message": str(e)
                        }), 500  # Caso ocorra algum erro, retorna a mensagem de erro.
    
    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.
