import sqlite3
import pandas as pd

def ver_jogos(db):
    print(db.head(60))

def adicionar_jogos(quantidade):
    for i in range(quantidade):
        nomes.append(input("Digite o nome do jogo que deseja adicionar: "))
        precos.append(float(input("Digite o preço do jogo: ")))
        estoque.append(int(input("Digite a quantidade de cópias disponíveis em estoque: ")))
        preco_fabrica.append(float(input("Digite o preço de fábrica do jogo: ")))
        vendas.append(int(input("Digite a quantidade de vendas do jogo: ")))
        aquisicoes_estoque.append(int(input("Digite a quantidade de aquisições feitas para o estoque: ")))
    for i in range(len(nomes)):
        cursor.execute(
            f''' INSERT INTO controle (nome, preco, estoque, preco_fabrica, vendas, aquisicoes_estoque) VALUES('{nomes[i]}', {precos[i]}, {estoque[i]}, {preco_fabrica[i]}, {vendas[i]}, {aquisicoes_estoque[i]})''')
    conexao.commit()
    return pd.read_sql("SELECT * FROM controle", conexao)

def remover_jogos(db):
    ver_jogos(db)
    remover_id = int(input("Digite o ID do item que deseja remover: "))
    conexao.execute('DELETE FROM controle WHERE id = ?', (remover_id,))
    saida = pd.read_sql("SELECT * FROM controle", conexao)
    conexao.commit()
    return saida

conexao = sqlite3.connect('controle.db')

cursor = conexao.cursor()

nomes = []
precos = []
estoque = []
preco_fabrica = []
vendas = []
aquisicoes_estoque = []

while True:
    print("Cybergames 2077")
    print("[1] Adicionar jogos | [2] Remover jogos | [3] Ver jogos disponíveis")
    opcao = int(input("Selecione uma ação: "))
    controle = pd.read_sql("SELECT * FROM controle", conexao)
    if opcao == 1:
        qtd_jogos = int(input("Digite a quantidade de jogos que deseja adicionar: "))
        print(adicionar_jogos(qtd_jogos))
        break
    elif opcao == 2:
        dataframe = pd.read_sql("SELECT * FROM controle", conexao)
        print(remover_jogos(dataframe))
        break
    elif opcao == 3:
        print(controle.head(60))
        break
    else:
        break

conexao.close()