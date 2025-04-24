# 🛍️ Sistema de Gerenciamento de Vendas com Flask + MySQL

 🚀 Um sistema de API RESTful feito com Flask para gerenciamento de Clientes, Produtos, Vendas e Itens de Venda.<br> 💾 Banco de dados MySQL para persistência dos dados.<br> 🧰 Ideal para pequenos sistemas de controle de estoque ou registro de vendas.<br><br>

## 🧩 Como instalar o projeto:
Instale o Python: https://www.python.org/downloads/<br>

Instale o pip (caso não venha com sua instalação do Python):<br> python -m ensurepip --upgrade<br>

Clone este repositório:<br> git clone https://github.com/seuusuario/seurepositorio.git<br>

Entre no diretório do projeto:<br> cd seurepositorio<br>

Instale as bibliotecas:<br> pip install flask mysql-connector-python<br><br>

## 🛠️ Bibliotecas utilizadas:
Flask: Framework web para construir a API.<br>

MySQL Connector: Conecta o Python ao banco de dados MySQL.<br><br>

## 🚀 Como rodar o projeto:
Certifique-se de que o MySQL está rodando.<br>

Crie um banco de dados chamado vendas com as tabelas necessárias.<br>

Configure a função get_connection() no arquivo connection.py com seus dados de conexão.<br>

Execute o servidor com o comando:<br> python app.py<br>

Acesse os endpoints via Postman, Insomnia ou qualquer cliente HTTP:<br> http://localhost:5000<br><br>

---

# 📡 Endpoints da API

---

## 📋 Produtos
### [GET] /Produtos
Retorna todos os produtos cadastrados.<br>

### Retorno esperado:
```
{
  "Produtos": [
    {
      "id produto": 1,
      "nome produto": "Camiseta"
    },
    ...
  ]
}
```

### [POST] /registerProducts
Cria um novo produto.<br>

### JSON de exemplo:
```
{
  "nome": "Camiseta",
  "descricao": "Camiseta preta M",
  "valor": 49.90,
  "quantidade": 10
}

```

### Retorno esperado:
```
{
  "Produto cadastrado": "Produto criado",
  "ID Produto": 1,
  "Nome produto": "Camiseta",
  "Descriçao produto": "Camiseta preta M",
  "Valor do produto": 49.9,
  "Qtd": 10
}

```

### [PATCH] /changeProdutos/<id>
Atualiza campos específicos de um produto.<br>

### JSON exemplo:
```
{
  "quantidade": 5
}

```

## [DELETE] /deleteProduct/<id>
Deleta um produto pelo ID.<br><br>


### Retorno esperado:
```
{
    "Message": "Produto deletado", 
    "Nome do produto": nome_produto, 
    "ID do produto": 1
    }
```

---

## 👥 Clientes
## [GET] /Clientes
Retorna todos os clientes cadastrados.<br>

### Retorno esperado:
```
{
  "clientes": [
    {
      "id cliente": 1,
      "nome cliente": "João"
    }
  ]
}

```

## [POST] /registerClientes
Registra um novo cliente.<br>

## JSON de exemplo:
```
{
  "nome": "João",
  "Telefone": "81999998888"
}

```

## [PATCH] /changeClientes/<id>
Atualiza dados de um cliente.<br>

## Exemplo:
```
{
  "Telefone": "81900001111"
}

```

## [DELETE] /delete/<id>
Deleta um cliente pelo ID.<br><br>

### Retorno esperado:
```
{
    "Message": "Cliente deletado", 
"Nome do cliente": nome, 
"ID do cliente": id
}
```

---

## 💳 Itens de Venda
## [GET] /itensVendas/<id_venda>
Busca os itens de uma venda específica.<br>

### Retorno esperado:
```
[
  {
    "id": 1,
    "quantidade": 2,
    "valor_produto": 49.9,
    "id_venda": 3,
    "id_produto": 1,
    "nome_produto": "Camiseta"
  }
]

```

## [DELETE] /deleteitensVendas/<id_iten>
Deleta um item da venda pelo ID do produto vinculado à venda.<br><br>

### Retorno esperado:
```
{
    "Message": "Item deletado com sucesso!"
}
```

---

##💾 Conexão com o MySQL (connection.py)
```
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='seu_usuario',
        password='sua_senha',
        database='vendas'
    )

```

## ⚠️ Substitua com suas credenciais do banco.<br><br>

---

## made by: github.com/webarthu