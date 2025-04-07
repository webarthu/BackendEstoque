from flask import Blueprint, jsonify, request
from connection import get_connection

clientes_bp = Blueprint('clientes', __name__)


#GET
@clientes_bp.route('/Clientes', methods=['GET'])
def get_table():
    con = get_connection()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT id, nome FROM Clientes")
        clientes = cursor.fetchall()

        clientes = [{"id cliente": cliente[0], "nome cliente": cliente[1]} for cliente in clientes]

        return jsonify({"clientes": clientes}),200

    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()


#POST
@clientes_bp.route('/registerClientes', methods=['POST'])
def post_clientes():
    con = get_connection()
    try:
        cursor = con.cursor()
        nome = request.json.get('nome')
        telefone = request.json.get('Telefone')

        if not nome or not telefone:
            return jsonify({"error": "Nome e Telefone são obrigatórios"}),400

        cursor.execute("INSERT INTO Clientes (nome, Telefone) VALUES (%s, %s)", (nome, telefone))

        cliente_id = cursor.lastrowid
        con.commit()

        return jsonify({"Cliente": "created", "Nome": nome, "Telefone": telefone, "ID": cliente_id}),200
    
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()


#PATCH
@clientes_bp.route('/changeClientes/<int:id>', methods=['PATCH'])
def changeClientes(id):
    con = get_connection()
    try:
        cursor = con.cursor()
        
        change = request.get_json()
        if not change:
            return jsonify({"menasgem": "Nenhum dado enviado para o PATCH"}),400

        campos = ', '.join([f"{key} = %s" for key in change.keys()])

        valores = list(change.values())
        valores.append(id)

        query = f"UPDATE Clientes SET {campos} WHERE id=%s"

        cursor.execute(query, valores)
        con.commit()
        return jsonify({"UPDATED":"Dados atualizados com sucesso!"}),200

    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()
        

#DELETE
@clientes_bp.route('/delete/<int:id>', methods=['DELETE'])
def deleteClientes(id):
    con = get_connection()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT nome FROM Clientes WHERE id=%s", (id,))

        result = cursor.fetchone()
        if not result:
            return jsonify({"Error": "Cliente não encontrado"}),400

        nome = result[0]
        
        cursor.execute("DELETE FROM Clientes WHERE id=%s", (id,))
        con.commit()

        return jsonify({"Message": "Cliente deletado", "Nome do cliente": nome, "ID do cliente": id}),200
    
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()
