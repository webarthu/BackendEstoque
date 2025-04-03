from flask import Flask
from flask import jsonify
from flask import request
import mysql.connector

app=Flask(__name__)



#Get
@app.route('/getTlabes', methods=['GET'])
def get_table():
    cursor=con.cursor()
    cursor.execute("SHOW TABLES")
    tables=cursor.fetchall()
    cursor.close()
    con.close()
    table_names=[table[0] for table in tables]
    return jsonify({"tables": table_names}),200

#Post
@app.route('/register', methods=['POST'])
def post_clientes():
    try:
        cursor=con.cursor()
        nome = request.json.get('nome')
        Telefone = request.json.get('Telefone')
        if not nome or not Telefone:
            return jsonify({"error": "Nome e Telefone são obrigatórios"}),400

        cursor.execute("INSERT INTO Clientes (nome, Telefone) VALUES (%s, %s)", (nome, Telefone))
        cliente_id = cursor.lastrowid
        con.commit()

        return jsonify({"Cliente": "created", "Nome": nome, "Telefone": Telefone, "ID": cliente_id}), 200
    
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()

#Delete
@app.route(f'/delete/<int:id>', methods=['DELETE'])
def delete_clientes(id,):
    print("porra", id)
    try:
        cursor=con.cursor()
        if not id:
            return jsonify({"error": "Id obrigátorio"}),400
        
        cursor.execute("SELECT nome FROM Clientes WHERE id=%s", (id,))

        result = cursor.fetchone()

        if not result:
            return jsonify({"Error": "Cliente nao encontrado"}),400

        nome = result[0]

        cursor.execute("DELETE FROM Clientes WHERE id=%s", (id,))
        con.commit()

        return jsonify({"Message": "Cliente deletado", "Nome do cliente": nome, "ID do cliente": id}), 200

    
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    
    finally:
        cursor.close()
        con.close()


if __name__=="__main__":
    print("connecting to db")
    app.run(debug=True)