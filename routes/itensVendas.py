from flask import Blueprint, jsonify, request
from connection import get_connection

itensVendas_bp = Blueprint('itensVendas', __name__)

#GET
@itensVendas_bp.route('/itensVendas/<int:id_venda>', methods=['GET'])
def itensVendas(id_venda):
    con = get_connection()
    try:
        cursor = con.cursor()

        cursor.execute("""
            SELECT i.id, i.quantidade, i.valor_unitario, i.id_venda, i.id_produto, p.nome
            FROM ItensVenda i
            JOIN Produtos p ON i.id_produto = p.id
            WHERE i.id_venda = %s
        """, (id_venda,))

        itens = cursor.fetchall()

        if not itens:
            return jsonify({"Error": "itens nao encontrados nessa venda"})

        lista_itens = []
        for item in itens:
            lista_itens.append({
                "id": item[0],
                "quantidade": item[1],
                "valor_produto": item[2],
                "id_venda": item[3],
                "id_produto": item[4],
                "nome_produto": item[5]
            })

        return jsonify(lista_itens), 200

    
    except Exception as e:
        return jsonify({"Error": str(e)})

    finally:
        cursor.close()
        con.close()

#DELETE
@itensVendas_bp.route('/deleteitensVendas/<int:id_iten>', methods=['DELTE'])
def deleteItensVendas(id_iten):
    con = get_connection()
    try:
        cursor = con.cursor()

        cursor.execute("SELECT id_venda, id_produto FROM ItensVendas WHERE id_produto=%s", (id_iten,))
        dados = cursor.fetchall()
        
        if not dados:
            return jsonify({"Error": "item nao encontrado"}), 400
        

        lista_dados = []
        for dado in dados:
            id_venda, id_produto = dado
            
            cursor.execute("SELECT nome FROM Produtos WHERE id=%s", (id_produto,))
            nome_produto = cursor.fetchone()

            if nome_produto:
                nome_produto = nome_produto[0]

                lista_dados.append({
                    "id_venda": id_venda,
                    "id_produto": id_produto,
                    "nome_produto": nome_produto
                })

        if not lista_dados:
            return jsonify({"Error": "Produto não encontrado na venda"}), 400


    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()