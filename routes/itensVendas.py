from flask import Blueprint, jsonify, request  # Importa as funções necessárias do Flask.
from connection import get_connection  # Importa a função get_connection para estabelecer a conexão com o banco de dados.

itensVendas_bp = Blueprint('itensVendas', __name__)  # Cria um Blueprint para as rotas de itens de vendas.

# GET - Rota para obter os itens de uma venda específica
@itensVendas_bp.route('/itensVendas/<int:id_venda>', methods=['GET'])
def itensVendas(id_venda):
    print('chamou funcao')
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    print('entrou na conexao')
    try:
        print('entrou')
        cursor = con.cursor()

        # Consulta os itens da venda com o nome do produto.
        
        cursor.execute("""
            SELECT i.id, i.quantidade, i.valor_unitario, i.id_venda, i.id_produto, p.nome
            FROM ItensVenda i
            JOIN Produtos p ON i.id_produto = p.id
            WHERE i.id_venda = %s
        """, (id_venda,))

        print("id venda:", id_venda)
        itens = cursor.fetchall()

        if not itens:
            return jsonify({"error": "Itens não encontrados nessa venda."}), 404

        lista_itens = []
        for item in itens:
            lista_itens.append({
                "id": item[0],
                "quantidade": item[1],
                "valor_unitario": item[2],
                "id_venda": item[3],
                "id_produto": item[4],
                "nome_produto": item[5]
            })

        print(lista_itens)

        return jsonify(lista_itens), 200  # Retorna a lista como JSON com status 200.

    except Exception as e:
        print("Erro ao buscar itens da venda:", e)
        return jsonify({"Error": "Erro interno no servidor."}), 500

    finally:
        cursor.close()
        con.close()


# DELETE - Rota para deletar um item específico de uma venda
@itensVendas_bp.route('/deleteitensVendas/<int:id_item>', methods=['DELETE'])  # Corrigido para 'DELETE' no lugar de 'DELTE'
def deleteItensVendas(id_item):
    con = get_connection()  # Estabelece a conexão com o banco de dados.
    try:
        cursor = con.cursor()  # Cria um cursor para executar consultas no banco de dados.

        # Executa a consulta para verificar a existência do item na tabela de ItensVendas.
        cursor.execute("SELECT id_venda, id_produto FROM ItensVendas WHERE id_produto=%s", (id_item,))
        dados = cursor.fetchall()  # Obtém todos os dados relacionados ao item.

        if not dados:  # Caso o item não seja encontrado, retorna um erro.
            return jsonify({"Error": "item não encontrado"}), 400

        lista_dados = []  # Lista para armazenar os dados do item.
        for dado in dados:
            id_venda, id_produto = dado

            # Executa uma consulta para obter o nome do produto.
            cursor.execute("SELECT nome FROM Produtos WHERE id=%s", (id_produto,))
            nome_produto = cursor.fetchone()  # Obtém o nome do produto.

            if nome_produto:
                nome_produto = nome_produto[0]  # Obtém o nome do produto.

                lista_dados.append({
                    "id_venda": id_venda,  # ID da venda.
                    "id_produto": id_produto,  # ID do produto.
                    "nome_produto": nome_produto  # Nome do produto.
                })

        if not lista_dados:  # Caso não seja possível encontrar o produto na venda, retorna um erro.
            return jsonify({"Error": "Produto não encontrado na venda"}), 400

        # Deleta o item da tabela de ItensVendas após encontrar o item.
        cursor.execute("DELETE FROM ItensVendas WHERE id_produto=%s", (id_item,))
        con.commit()  # Commit para aplicar as mudanças no banco de dados.

        return jsonify({"Message": "Item deletado com sucesso!"}), 200  # Retorna uma mensagem de sucesso.

    except Exception as e:
        return jsonify({"Error": str(e)}), 500  # Caso ocorra algum erro, retorna a mensagem de erro.

    finally:
        cursor.close()  # Fecha o cursor.
        con.close()  # Fecha a conexão com o banco de dados.
