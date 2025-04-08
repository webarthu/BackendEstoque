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
        id = request.json.get('id')
        
        if not nome or not id:
            return jsonify({"Error": "É necessário informar um nome ou id para cadastrar uma venda"}),400
        
        if nome:
            cursor.execute("SELECT id FROM Clientes WHERE nome = %s", (nome))

        if id:
            cursor.execute("SELECT name FROM Clientes WHERE id = %s", (id))

        cursor.execute()

    except Exception as e:
        return jsonify({"Error", str(e)}),500
    finally:
        cursor.close()
        con.close()