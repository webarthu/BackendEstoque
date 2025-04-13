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
        produtos = request.json.get('produtos')

        print("nome:", nome)
        print("\nid:", id_cliente)
        print("\nprodutos:", produtos)

        if not nome and not id_cliente:
            return jsonify({"Error": "É necessário informar um nome ou id para cadastrar uma venda"}),400
        
        if nome:
            cursor.execute("SELECT * FROM Clientes WHERE nome = %s", (nome,))
            clientes = cursor.fetchall()
            
            print("\nclientes:", clientes)

            if len(clientes) > 1: #{
                    return jsonify({"Options": clientes, "Message": "Mais de um cliente encontrado com esse nome"}), 400
            #}
            id_cliente = clientes[0][0]
            
            print("\nid_cliente:", id_cliente)
            
        if id_cliente:
            cursor.execute("INSERT INTO Vendas (id_cliente) VALUES (%s)", (id_cliente,))
            id_venda = cursor.lastrowid
            
            print("\nid_venda:", id_venda)

        for produto in produtos:
            print("entrou no loop")
            print("aparente erro:", produto["id_produto"])
            print(produto)
            print(produto["id_produto"])
            print(produto["quantidade"])
            print("---------")
            cursor.execute("SELECT valor FROM Produtos WHERE id=%s", (produto['id_produto'],))
            print("executou a query")

            valor_unitario = cursor.fetchone()[0]
            
            print("\nvalor_unitario", valor_unitario)
            

            cursor.execute("INSERT INTO ItensVenda (id_venda, id_produto, quantidade, valor_unitario) VALUES (%s, %s, %s, %s)",(id_venda, produto["id_produto"], produto["quantidade"], valor_unitario))

            print("segunda query do loop")


        con.commit()

        return jsonify({"Message": "Venda realizada!", "ID venda": id_venda}),200

    except Exception as e:
        return jsonify({"Error": str(e)}), 500
 
    finally:
        cursor.close()
        con.close()