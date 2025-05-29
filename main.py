import sqlite3
import pandas as pd
import hashlib

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def exibir(tabela, con):
    tabela = pd.read_sql(f"SELECT * FROM {tabela}", con)
    print(tabela)


def encode(text):
    text_bytes = text.encode('utf-8')
    encoded_text = hashlib.sha256(text_bytes)
    return encoded_text.hexdigest()


def cadastrar(db, con):
    print("\nCadastro:")
    data = pd.read_sql("SELECT * FROM usuarios", con)
    nome_valido = True
    username = input("Digite o seu nome de usuário: ")
    for i in data["username"]:
        if username == i:
            print("O nome de usuário já está sendo utilizado.")
            nome_valido = False
    while not nome_valido:
        username = input("Digite o seu nome de usuário: ")
        for i in data["username"]:
            if username == i:
                print("O nome de usuário já está sendo utilizado.")
                nome_valido = False
        nome_valido = True
    password = input("Digite a sua senha: ")
    confirm_password = input("Confirme a sua senha: ")
    while confirm_password != password:
        password = input("Senhas não coincidem. Digite a senha novamente: ")
        confirm_password = input("Confirme a sua senha: ")
    db.execute(f"""INSERT INTO usuarios (username, password, type) VALUES ('{username}', '{encode(password)}', 'ADM')""")
    con.commit()


def validar(db, con):
    print("\nLogin:")
    data = pd.read_sql("SELECT * FROM usuarios", con)
    username = input("Digite o seu nome de usuário: ")
    password = encode(input("Digite a sua senha: "))
    try:
        if password == data[data["username"] == username]["password"].iloc[0]:
            print("Acesso concedido.")
            return username
        else:
            print("Nome de usuário ou senha estão incorretos.")
            return False
    except IndexError:
        print("Usuário não encontrado.")
        return False


def ver_jogos(db):
    print(db.head(60))


def adicionar_jogos(quantidade, con):
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
    con.commit()
    return pd.read_sql("SELECT * FROM controle", con)


def remover_jogos(db, con):
    ver_jogos(db)
    remover_id = int(input("Digite o ID do item que deseja remover: "))
    con.execute('DELETE FROM controle WHERE id = ?', (remover_id,))
    saida = pd.read_sql("SELECT * FROM controle", con)
    con.commit()
    return saida


def registrar_venda(banco, id_jogo, qtd_venda, usuario, con):
    df = pd.read_sql("SELECT * FROM controle", con)
    if int(df[df['id'] == id_jogo]['estoque'].iloc[0]) - qtd_venda >= 0:
        preco = int(df[df['id'] == id_jogo]['preco'].iloc[0])
        custos_totais = preco * qtd_venda
        qtd_nova = int(df[df['id'] == id_jogo]['estoque'].iloc[0]) - qtd_venda
        vendas_nova = int((df[df['id'] == id_jogo])['vendas'].iloc[0]) + qtd_venda
        banco.execute(f'UPDATE controle SET estoque = {qtd_nova} WHERE id = {id_jogo}')
        banco.execute(f'UPDATE controle SET vendas = {vendas_nova} WHERE id = {id_jogo}')
        df_novo = pd.read_sql("SELECT * FROM controle", con)
        print(df_novo.head(60))
        print(f"Valor total da venda: R${custos_totais}")
        banco.execute(f"INSERT INTO vendas (jogo, preco, quantidade, valor_total, usuario) VALUES ('{df[df['id'] == id_jogo]["nome"].iloc[0]}', {preco}, {qtd_venda}, {custos_totais}, '{usuario}')")
        con.commit()
        tabela = pd.read_sql("SELECT * FROM vendas", con)
        print(tabela.head(60))
        return custos_totais
    else:
        print("Não possuímos tal quantidade em estoque.")
        return 0


def compra_de_estoque(banco, id_jogo, qtd_compra, usuario, con):
    df = pd.read_sql("SELECT * FROM controle", con)
    preco = df[df['id'] == id_jogo]['preco'].iloc[0]
    custos_totais = preco * qtd_compra
    qtd_nova = int(df[df['id'] == id_jogo]['estoque'].iloc[0]) + qtd_compra
    aquisicoes =  int((df[df['id'] == id_jogo])['aquisicoes_estoque'].iloc[0]) + qtd_compra
    banco.execute(f'UPDATE controle SET estoque = {qtd_nova} WHERE id = {id_jogo}')
    banco.execute(f'UPDATE controle SET aquisicoes_estoque = {aquisicoes} WHERE id = {id_jogo}')
    df_novo = pd.read_sql("SELECT * FROM controle", con)
    print(df_novo.head(60))
    print(f"Valor total da compra: R${custos_totais}")
    banco.execute(
        f"INSERT INTO compras (jogo, preco_fabrica, quantidade, valor_total, usuario) VALUES ('{df[df['id'] == id_jogo]["nome"].iloc[0]}', {preco}, {qtd_compra}, {custos_totais}, '{usuario}')")
    con.commit()
    tabela = pd.read_sql("SELECT * FROM compras", con)
    print(tabela.head(60))
    return custos_totais


conexao = sqlite3.connect('controle.db')
cursor = conexao.cursor()

controle = pd.read_sql("SELECT * FROM controle", conexao)
caixa = ((controle['preco'] * controle['vendas']).sum() - (controle['preco_fabrica'] * controle['aquisicoes_estoque']).sum()).round(2)

user = False
while not user:
    print("Deseja fazer login ou cadastrar-se? ")
    print("[1] Fazer Login | [2] Cadastrar-se")
    opcao_login = int(input("Selecione uma ação: "))
    if opcao_login == 1:
        user = validar(cursor, conexao)
    elif opcao_login == 2:
        cadastrar(cursor, conexao)
        user = validar(cursor, conexao)

while True:
    print(f"\nCybergames 2077\nUsuário: {user}")
    print(f"Valor em caixa: R${caixa}")
    print("[1] Adicionar jogos | [2] Remover jogos | [3] Registrar venda | [4] Compra de estoque | [5] Histórico | [6] Resumo da loja | [7] Sair")
    opcao = int(input("Selecione uma ação: "))
    if opcao == 1:
        qtd_jogos = int(input("Digite a quantidade de jogos que deseja adicionar: "))
        print(adicionar_jogos(qtd_jogos, conexao))
    elif opcao == 2:
        dataframe = pd.read_sql("SELECT * FROM controle", conexao)
        print(remover_jogos(dataframe, conexao))
    elif opcao == 3:
        print(controle.head(60))
        id_jogo_venda = int(input("Digite o id do jogo que deseja registrar a venda: "))
        qtd_jogo_venda = int(input("Digite a quantidade que deseja registrar a venda: "))
        caixa += registrar_venda(cursor, id_jogo_venda, qtd_jogo_venda, user, conexao)
        print(f"Valor em caixa: R${caixa}")
    elif opcao == 4:
        print(controle.head(60))
        id_jogo_compra = int(input("Digite o id do jogo que deseja comprar: "))
        qtd_jogo_compra = int(input("Digite a quantidade que deseja comprar: "))
        caixa -= compra_de_estoque(cursor, id_jogo_compra, qtd_jogo_compra, user, conexao)
        print(f"Valor em caixa: R${caixa}")
    elif opcao == 5:
        print("[1] Histórico de vendas | [2] Histórico de compras")
        escolha = int(input("Selecione uma ação: "))
        while escolha != 1 and escolha != 2:
            escolha = int(input("Selecione uma ação: "))
        if escolha == 1:
            exibir("vendas", conexao)
        elif escolha == 2:
            exibir("compras", conexao)
    elif opcao == 6:
        print(controle)
    else:
        print("Caixa fechado.")
        break
    caixa = round((controle['preco'] * controle['vendas']).sum() - (controle['preco_fabrica'] * controle['aquisicoes_estoque']).sum(), 2)


conexao.close()