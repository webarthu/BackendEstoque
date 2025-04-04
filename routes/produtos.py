from flask import Blueprint, jsonify, request
from connection import get_connection

produtos_bp = Blueprint('produtos', __name__)

#GET
@produtos_bp.route('/Produtos', methods=['GET'])
def getProducts():
    con = get_connection()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT id, nome FROM Produtos")
        produtos = cursor.fetchall()

        produtos = [{"id produto": produto[0], "nome produto": produto[1]} for produto in produtos]

        return jsonify({"Produtos": produtos}),200
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()


#POST
@produtos_bp.route('/registerProducts', methods=['POST'])
def registerProduct():
    con = get_connection()
    try:
        cursor = con.cursor()
        
        nome = request.json.get('nome')
        descricao = request.json.get('descricao')
        valor = request.json.get('valor')
        quantidade = request.json.get('quantidade')
        
        if not nome: return jsonify({"error": "Nome do produto é obrigatório"})
        if not descricao: descricao = ('')
        if not valor or valor <= 0 : return jsonify({"error": "Valor obrigatório"})
        if not quantidade or quantidade < 0: return jsonify({"error": "Quantidade de produtos obrigatória"})

        cursor.execute("INSERT INTO Produtos (nome, descricao, valor, quantidade) VALUES (%s, %s, %s, %s)", (nome, descricao, valor, quantidade))

        produto_id = cursor.lastrowid
        con.commit()
        
        return jsonify({"Produto cadastrado": "Produto criado", 
                        "ID Produto": produto_id, 
                        "Nome produto": nome, 
                        "Descriçao produto": descricao, 
                        "Valor do produto": valor, 
                        "Qtd": quantidade}),200
    
    except Exception as e:
        return jsonify({'Error': str(e)}),500
    
    finally:
        cursor.close()
        con.close()


#DELETE
@produtos_bp.route('/deleteProduct/<int:id>', methods=['DELETE'])
def deleteProduct(id):
    con = get_connection()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT nome FROM Produtos WHERE id=%s", (id,))

        result = cursor.fetchone()
        if not result:
            return jsonify({"Error":"Produto nao encontrado"}),400
        
        nome_produto = result[0]

        cursor.execute("DELETE FROM Produtos WHERE id=%s", (id,))
        con.commit()

        return jsonify({"Message": "Produto deleteado", "Nome do produto": nome_produto, "ID do produto": id}),200
    
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()
