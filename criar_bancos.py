import sqlite3

conexao = sqlite3.connect("controle.db")
cursor = conexao.cursor()

cursor.execute(
    """CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )""")

cursor.execute(
    """CREATE TABLE controle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco FLOAT NOT NULL,
    estoque INT NOT NULL,
    preco_fabrica FLOAT NOT NULL,
    vendas INT NOT NULL,
    aquisicoes_estoque INT NOT NULL
    )""")

conexao.close()