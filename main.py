import sqlite3
import pandas as pd


def ver_jogos(db):
    print(db.head(60))


def adicionar_jogos(quantidade):
    nomes = []
    precos = []
    preco_fabrica = []
    for i in range(quantidade):
        nomes.append(input("Digite o nome do jogo que deseja adicionar: "))
        precos.append(float(input("Digite o preço do jogo: ")))
        preco_fabrica.append(float(input("Digite o preço de fábrica do jogo: ")))
    for i in range(len(nomes)):
        cursor.execute(
            f''' INSERT INTO controle (nome, preco, estoque, preco_fabrica, vendas, aquisicoes_estoque) VALUES('{nomes[i]}', {precos[i]}, 0, {preco_fabrica[i]}, 0, 0)''')
    conexao.commit()
    return pd.read_sql("SELECT * FROM controle", conexao)


def remover_jogos(db):
    ver_jogos(db)
    remover_id = int(input("Digite o ID do item que deseja remover: "))
    conexao.execute('DELETE FROM controle WHERE id = ?', (remover_id,))
    saida = pd.read_sql("SELECT * FROM controle", conexao)
    conexao.commit()
    return saida


def registrar_venda(banco, id_jogo, qtd_venda):
    df = pd.read_sql("SELECT * FROM controle", conexao)
    if int(df[df['id'] == id_jogo]['estoque'].iloc[0]) - qtd_venda >= 0:
        custos_totais = int(df[df['id'] == id_jogo]['preco'].iloc[0]) * qtd_venda
        qtd_nova = int(df[df['id'] == id_jogo]['estoque'].iloc[0]) - qtd_venda
        vendas_nova = int((df[df['id'] == id_jogo])['vendas'].iloc[0]) + qtd_venda
        banco.execute(f'UPDATE controle SET estoque = {qtd_nova} WHERE id = {id_jogo}')
        banco.execute(f'UPDATE controle SET vendas = {vendas_nova} WHERE id = {id_jogo}')
        df_novo = pd.read_sql("SELECT * FROM controle", conexao)
        print(df_novo.head(60))
        conexao.commit()
        print(f"Valor total da venda: R${custos_totais}")
        return custos_totais
    else:
        print("Não possuímos tal quantidade em estoque.")
        return 0


def compra_de_estoque(banco, id_jogo, qtd_compra):
    df = pd.read_sql("SELECT * FROM controle", conexao)
    custos_totais = int(df[df['id'] == id_jogo]['preco'].iloc[0]) * qtd_compra
    qtd_nova = int(df[df['id'] == id_jogo]['estoque'].iloc[0]) + qtd_compra
    aquisicoes =  int((df[df['id'] == id_jogo])['aquisicoes_estoque'].iloc[0]) + qtd_compra
    banco.execute(f'UPDATE controle SET estoque = {qtd_nova} WHERE id = {id_jogo}')
    banco.execute(f'UPDATE controle SET aquisicoes_estoque = {aquisicoes} WHERE id = {id_jogo}')
    df_novo = pd.read_sql("SELECT * FROM controle", conexao)
    print(df_novo.head(60))
    conexao.commit()
    print(f"Valor total da compra: R${custos_totais}")
    return custos_totais


conexao = sqlite3.connect('controle.db')
cursor = conexao.cursor()

controle = pd.read_sql("SELECT * FROM controle", conexao)
caixa = ((controle['preco'] * controle['vendas']).sum() - (controle['preco_fabrica'] * controle['aquisicoes_estoque']).sum()).round(2)

while True:
    print("Cybergames 2077")
    print(f"Valor em caixa: R${caixa}")
    print("[1] Adicionar jogos | [2] Remover jogos | [3] Registrar venda | [4] Compra de estoque | [5] Resumo da loja | [6] Sair")
    opcao = int(input("Selecione uma ação: "))
    if opcao == 1:
        qtd_jogos = int(input("Digite a quantidade de jogos que deseja adicionar: "))
        print(adicionar_jogos(qtd_jogos))
    elif opcao == 2:
        dataframe = pd.read_sql("SELECT * FROM controle", conexao)
        print(remover_jogos(dataframe))
    elif opcao == 3:
        print(controle.head(60))
        id_jogo_venda = int(input("Digite o id do jogo que deseja registrar a venda: "))
        qtd_jogo_venda = int(input("Digite a quantidade que deseja registrar a venda: "))
        caixa += registrar_venda(cursor, id_jogo_venda, qtd_jogo_venda)
        print(f"Valor em caixa: R${caixa}")
    elif opcao == 4:
        print(controle.head(60))
        id_jogo_compra = int(input("Digite o id do jogo que deseja comprar: "))
        qtd_jogo_compra = int(input("Digite a quantidade que deseja comprar: "))
        caixa -= compra_de_estoque(cursor, id_jogo_compra, qtd_jogo_compra)
        print(f"Valor em caixa: R${caixa}")
    elif opcao == 5:
        print(controle.head(60))
    else:
        print("Caixa fechado.")
    caixa = (controle['preco'] * controle['vendas']).sum() - (controle['preco_fabrica'] * controle['aquisicoes_estoque']).sum()
    break



conexao.close()