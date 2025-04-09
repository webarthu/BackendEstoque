from flask import Blueprint, jsonify, request
from connection import get_connection

vendas_bp = Blueprint('vendas', __name__)

#GET

#POST
@vendas_bp.route('/registerVendas', methods=['POST'])
def registerVendas():
    con = get_connection()
    try:
        cursor = con.cursor()
        nome = request.json.get('nome')
        id_cliente = request.json.get('id')
        produtos = request.json.get([{'id_produto', 'quantidade'}])

        if not nome and not id_cliente:
            return jsonify({"Error": "É necessário informar um nome ou id para cadastrar uma venda"}),400
        
        if nome:
            cursor.execute("SELECT * FROM Clientes WHERE nome = %s", (nome))

        if id_cliente:
            cursor.execute("INSERT INTO Vendas (id_cliente, data_venda) VALUES (s%, )", (id_cliente, ))
        
        cursor.execute("SELECT id FROM Vendas WHERE ...")
        id_venda = cursor.fetchone()
        
        cursor.execute("SELECT valor FROM Produtos WHERE id = %s ", (for i in produtos[0]))

        cursor.execute("INSERT INTO ItensVenda (id_produto, quantidade, valor_unitario) VALUES (s%, s%, s%)",(produtos.id_produto, produtos.quantidade, valor_unitario))

        return jsonify({"Venda realizada!": "ID venda":id_venda}),200

    except Exception as e:
        return jsonify({"Error", str(e)}),500
    finally:
        cursor.close()
        con.close()