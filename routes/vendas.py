from flask import Blueprint, jsonify, request
from connection import get_connection

vendas_bp = Blueprint('vendas', __name__)

#GET
@vendas_bp.route('/Vendas', methods=['GET'])
def getVendas():
    con = get_connection()
    try:
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM Vendas")
        vendas = cursor.fetchall()
        resultado = []
        for venda in vendas:
            resultado.append({
                "Venda_ID": venda[0],
                "Data_Venda": venda[1].isoformat(),
                "Cliente_ID": venda[2],
                "Valor_Total": float(venda[3])
            })
        return jsonify(resultado),200
        
        con.commit()
    
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()


#POST
@vendas_bp.route('/registerVendas', methods=['POST'])
def registerVendas():
    con = get_connection()
    try:
        cursor = con.cursor()
        nome_cliente = request.json.get('nome')
        id_cliente = request.json.get('id')
        produtos = request.json.get('produtos')
        valor_total = 0

        if not nome_cliente and not id_cliente:
            return jsonify({"Error": "É necessário informar um nome ou id para cadastrar uma venda"}),400
        
        if not produtos:
            return jsonify({"Error": "nao tem produtos"}),400

        if nome_cliente:
            cursor.execute("SELECT * FROM Clientes WHERE nome = %s", (nome_cliente,))
            clientes = cursor.fetchall()


            if len(clientes) > 1: #{
                    return jsonify({"Options": clientes, "Message": "Mais de um cliente encontrado com esse nome"}),400
            #}
            id_cliente = clientes[0][0]
            
            
        if id_cliente:
            cursor.execute("INSERT INTO Vendas (id_cliente) VALUES (%s)", (id_cliente,))
            id_venda = cursor.lastrowid

        for produto in produtos:
            cursor.execute("SELECT valor FROM Produtos WHERE id=%s", (produto['id_produto'],))
            resultado = cursor.fetchone()
            
            if resultado: 
                valor_unitario = resultado[0]
                quantidade = produto['quantidade']
                valor_total += valor_unitario * quantidade
                
                cursor.execute("INSERT INTO ItensVenda (id_venda, id_produto, quantidade, valor_unitario) VALUES (%s, %s, %s, %s)",(id_venda, produto["id_produto"], quantidade, valor_unitario))

        cursor.execute("UPDATE Vendas SET valor_total = %s WHERE id = %s", (valor_total, id_venda))
        
        con.commit()
        
        return jsonify({"Message": "Venda realizada!", "ID venda": id_venda, "Valor total": valor_total, "ID_Cliente": id_cliente, "Nome Cliente":nome_cliente}), 200

    except Exception as e:
        return jsonify({"Error": str(e)}), 500
 
    finally:
        cursor.close()
        con.close()


#DELETE
@vendas_bp.route('/deleteVendas/<int:id>', methods=['DELETE'])
def deleteVendas(id):
    con = get_connection()
    try:
        cursor = con.cursor()

        cursor.execute("SELECT id_cliente FROM Vendas WHERE id=%s", (id,))
        
        result = cursor.fetchone()
        if not result:
            return jsonify({'Error': "Venda nao encontrada"}),400

        id_cliente = result[0]

        cursor.execute("SELECT nome FROM Clientes WHERE id=%s", (id_cliente,))
        
        res = cursor.fetchone()
        if not res:
            return jsonify({'Error': "Cliente nao encontrado"}),400

        nome = res[0]

        cursor.execute("DELETE FROM ItensVenda WHERE id_venda=%s", (id,))
        cursor.execute("DELETE FROM Vendas WHERE id=%s", (id,))
        con.commit()

        return jsonify({"Message": "Venda Deleteada", "Nome Cliente": nome, "ID Cliente": id_cliente}),200

        
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()