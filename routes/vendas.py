from flask import Blueprint, jsonify, request  # Importa as funções necessárias do Flask para criar rotas, enviar respostas JSON e receber dados da requisição.
from connection import get_connection  # Importa a função get_connection para estabelecer a conexão com o banco de dados.

vendas_bp = Blueprint('vendas', __name__)  # Cria um Blueprint para as rotas de vendas.

# GET - Rota para obter todas as vendas
@vendas_bp.route('/Vendas', methods=['GET'])
def getVendas():
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        
        cursor.execute("SELECT * FROM Vendas")  # Executa a consulta para buscar todas as vendas.
        vendas = cursor.fetchall()  # Obtém todos os resultados da consulta.
        resultado = []  # Lista para armazenar os dados das vendas no formato desejado.

        # Loop para formatar os dados das vendas e retornar como JSON.
        for venda in vendas:
            resultado.append({
                "Venda_ID": venda[0],
                "Data_Venda": venda[1].isoformat(),  # Converte a data para o formato ISO.
                "Cliente_ID": venda[2],
                "Valor_Total": float(venda[3])  # Converte o valor total para float.
            })
        return jsonify(resultado), 200  # Retorna os dados das vendas como resposta JSON.
        
        con.commit()  # Commit (não necessário aqui, já que estamos apenas consultando).

    except Exception as e:
        return jsonify({"Error": str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.
    
    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.


# POST - Rota para registrar uma nova venda
@vendas_bp.route('/registerVendas', methods=['POST'])
def registerVendas():
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.
        nome_cliente = request.json.get('nome')  # Obtém o nome do cliente da requisição JSON.
        id_cliente = request.json.get('id')  # Obtém o ID do cliente da requisição JSON.
        produtos = request.json.get('produtos')  # Obtém a lista de produtos da requisição JSON.
        valor_total = 0  # Inicializa o valor total da venda.

        # Valida se foi informado nome ou ID do cliente.
        if not nome_cliente and not id_cliente:
            return jsonify({"Error": "É necessário informar um nome ou id para cadastrar uma venda"}), 400
        
        if not produtos:
            return jsonify({"Error": "Não tem produtos"}), 400

        # Se o nome do cliente for informado, busca o cliente no banco de dados.
        if nome_cliente:
            cursor.execute("SELECT * FROM Clientes WHERE nome = %s", (nome_cliente,))
            clientes = cursor.fetchall()  # Obtém todos os clientes com o nome informado.

            # Caso mais de um cliente seja encontrado, retorna uma mensagem de erro.
            if len(clientes) > 1:
                return jsonify({"Options": clientes, "Message": "Mais de um cliente encontrado com esse nome"}), 400
            
            id_cliente = clientes[0][0]  # Atribui o ID do cliente encontrado.

        # Se o ID do cliente for informado, registra a venda no banco de dados.
        if id_cliente:
            cursor.execute("INSERT INTO Vendas (id_cliente) VALUES (%s)", (id_cliente,))
            id_venda = cursor.lastrowid  # Obtém o ID da venda recém-criada.

        # Para cada produto na lista de produtos, registra os itens de venda.
        for produto in produtos:
            cursor.execute("SELECT valor FROM Produtos WHERE id=%s", (produto['id_produto'],))  # Obtém o valor do produto.
            resultado = cursor.fetchone()  # Obtém o resultado da consulta.

            if resultado:  # Se o produto existir, registra o item de venda.
                valor_unitario = resultado[0]  # Obtém o valor unitário do produto.
                quantidade = produto['quantidade']  # Obtém a quantidade do produto.
                valor_total += valor_unitario * quantidade  # Calcula o valor total.

                cursor.execute("INSERT INTO ItensVenda (id_venda, id_produto, quantidade, valor_unitario) VALUES (%s, %s, %s, %s)",
                               (id_venda, produto["id_produto"], quantidade, valor_unitario))  # Registra o item de venda.

        # Atualiza o valor total da venda.
        cursor.execute("UPDATE Vendas SET valor_total = %s WHERE id = %s", (valor_total, id_venda))

        con.commit()  # Commit para salvar as mudanças no banco de dados.

        return jsonify({"Message": "Venda realizada!", "ID venda": id_venda, "Valor total": valor_total, "ID_Cliente": id_cliente, "Nome Cliente": nome_cliente}), 200

    except Exception as e:
        return jsonify({"Error": str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.
 
    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.


# DELETE - Rota para deletar uma venda
@vendas_bp.route('/deleteVendas/<int:id>', methods=['DELETE'])
def deleteVendas(id):
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.

        cursor.execute("SELECT id_cliente FROM Vendas WHERE id=%s", (id,))  # Obtém o ID do cliente da venda.
        result = cursor.fetchone()  # Obtém o resultado da consulta.
        
        if not result:
            return jsonify({'Error': "Venda não encontrada"}), 400  # Se a venda não for encontrada, retorna erro.

        id_cliente = result[0]  # Obtém o ID do cliente da venda.

        cursor.execute("SELECT nome FROM Clientes WHERE id=%s", (id_cliente,))  # Obtém o nome do cliente.
        res = cursor.fetchone()  # Obtém o resultado da consulta.

        if not res:
            return jsonify({'Error': "Cliente não encontrado"}), 400  # Se o cliente não for encontrado, retorna erro.

        nome = res[0]  # Obtém o nome do cliente.

        # Deleta os itens da venda e a venda em si.
        cursor.execute("DELETE FROM ItensVenda WHERE id_venda=%s", (id,))
        cursor.execute("DELETE FROM Vendas WHERE id=%s", (id,))
        con.commit()  # Commit para salvar as mudanças no banco de dados.

        return jsonify({"Message": "Venda deletada", "Nome Cliente": nome, "ID Cliente": id_cliente}), 200

    except Exception as e:
        return jsonify({"Error": str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.
    
    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.
