import re, mysql.connector
from datetime import datetime
from flask import Flask, json, jsonify, request

app = Flask(__name__)

Finalizadas = []
Comandas = []


Empadas = {}
Tortas = {}
Sanduiche = {}
HotDog = {}
TSalgadas = {}
TDoces = {}
BAlcool = {}
BSemAlcool = {}
SucosDetox = {}

Lanches = {"Sanduiches": Sanduiche, "Hot-Dog": HotDog}
Salgados = {"Empadas": Empadas, "Tortas": Tortas}
Tapiocas = {"Salgadas": TSalgadas, "Doces": TDoces}
Bebidas = {"Alcoolico": BAlcool, "Nao-alcoolico": BSemAlcool, "Sucos-Detox": SucosDetox}
Porcoes = {}
Escondidinhos = {}
Caldos = {}

Cardapio = {"Lanches": Lanches, "Salgados": Salgados, "Escondidinhos": Escondidinhos, "Caldos": Caldos, "Tapiocas": Tapiocas, "Bebidas": Bebidas, "Porcoes": Porcoes}

EmpadasI = {}
TortasI = {}
SanduicheI = {}
HotDogI = {}
TSalgadasI = {}
TDocesI = {}
BAlcoolI = {}
BSemAlcoolI = {}
SucosDetoxI = {}

LanchesI = {"Sanduiches": SanduicheI, "Hot-Dog": HotDogI}
SalgadosI = {"Empadas": EmpadasI, "Tortas": TortasI}
TapiocasI = {"Salgadas": TSalgadasI, "Doces": TDocesI}
BebidasI = {"Alcoolico": BAlcoolI, "Nao-alcoolico": BSemAlcoolI, "Sucos-Detox": SucosDetoxI}
PorcoesI = {}
EscondidinhosI = {}
CaldosI = {}

Imagens = {"Lanches": LanchesI, "Salgados": SalgadosI, "Escondidinhos": EscondidinhosI, "Caldos": CaldosI, "Tapiocas": TapiocasI, "Bebidas": BebidasI, "Porcoes": PorcoesI}

Geral = [{"Cardapio": Cardapio}, Comandas]

con = mysql.connector.connect(host = 'us-cdbr-east-04.cleardb.com', database = 'heroku_b200452de328eaa', user = 'b29ac0776cb380', password = '68cf88e1')

cursor = con.cursor()
cursor.execute("select * from cardapio;")
linhas = cursor.fetchall()
print(linhas)
for linha in linhas:
    if linha[4] == "empadas":
        Empadas[linha[1]] = linha[2]
        EmpadasI[linha[1]] = linha[5]
    elif linha[4] == "tortas":
        Tortas[linha[1]] = linha[2]
        TortasI[linha[1]] = linha[5]
    elif linha[4] == "hot-dogs":
        HotDog[linha[1]] = linha[2]
        HotDogI[linha[1]] = linha[5]
    elif linha[4] == "sanduiches":
        Sanduiche[linha[1]] = linha[2]
        SanduicheI[linha[1]] = linha[5]
    elif linha[4] == "escondidinhos":
        Escondidinhos[linha[1]] = linha[2]
        EscondidinhosI[linha[1]] = linha[5]
    elif linha[4] == "caldos":
        Caldos[linha[1]] = linha[2]
        CaldosI[linha[1]] = linha[5]
    elif linha[4] == "salgadas":
        TSalgadas[linha[1]] = linha[2]
        TSalgadasI[linha[1]] = linha[5]
    elif linha[4] == "doces":
        TDoces[linha[1]] = linha[2]
        TDocesI[linha[1]] = linha[5]
    elif linha[4] == "alcoólicas":
        BAlcool[linha[1]] = linha[2]
        BAlcoolI[linha[1]] = linha[5]
    elif linha[4] == "não-alcoólicas":
        BSemAlcool[linha[1]] = linha[2]
        BSemAlcoolI[linha[1]] = linha[5]
    elif linha[4] == "sucos detox":
        SucosDetox[linha[1]] = linha[2]
        SucosDetoxI[linha[1]] = linha[5]
    elif linha[4] == "porções":
        Porcoes[linha[1]] = linha[2]
        PorcoesI[linha[1]] = linha[5]
    
    con.close()

@app.route('/', methods =['GET'])
def raiz():
    return jsonify(Geral)

@app.route('/MostraCardapio', methods =['GET'])
def GetCardapio():
    return jsonify(Cardapio)

@app.route('/MostraComandasAbertas', methods =['GET'])
def GetComandas():
    Comandas = []
    banco = mysql.connector.connect(host = 'us-cdbr-east-04.cleardb.com', database = 'heroku_b200452de328eaa', user = 'b29ac0776cb380', password = '68cf88e1')
    
    cursor2 = banco.cursor()
    cursor2.execute("select * from comandaAberta;")
    Linhas = cursor2.fetchall()
    print(Linhas)
    cursor3 = banco.cursor()
    cursor3.execute("select `idComanda`, `nomePessoa` as 'Nome', sum(`preco` * `qtdProduto`) as 'Preço final' from `comandaAberta` inner join `cardapio` on `comandaAberta`.`idProduto` = `cardapio`.`idProduto` group by `idComanda`;")
    Linhas2 = cursor3.fetchall()
    print(Linhas2)

    for linha2 in Linhas2:
        itens = []
        data = ""
        for linha1 in Linhas:
            if linha1[0] == linha2[0]:
                for linha in linhas:
                    if linha[0] == linha1[1]:
                        itens.append({"Nome": linha[1], "Quantidade": linha1[4], "Preco": linha[2], "Nome Imagem": linha[5], "Observacoes": linha1[2]})

        Comandas.append({"Nome":linha2[1], "Itens": itens, "Total": linha2[2]})

    banco.close()

    return jsonify(Comandas)

@app.route('/MostraComandaPorNome/<string:Ncomanda>', methods =['GET'])
def GetComandaPorNome(Ncomanda):
    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    return jsonify(indice_pessoas_por_nome[nome_procurado])

@app.route('/Pedido', methods = ['POST'])
def PedidoFeito():
    data = request.get_json()

    banco = mysql.connector.connect(host = 'us-cdbr-east-04.cleardb.com', database = 'heroku_b200452de328eaa', user = 'b29ac0776cb380', password = '68cf88e1')
    
    cursor2 = banco.cursor()
    cursor2.execute("select * from comandaAberta;")
    Linhas = cursor2.fetchall()
    print(Linhas)

    if Linhas == []:
        id = 1
    else:
        id = Linhas[len(Linhas) - 1][0] + 1

    ComandaParaAbrir = ""

    for a in data["Itens"]:
        for linha in linhas:
            if a["Nome"] == linha[1]:
                if float(a["Preco"]) == linha[2]:
                    if ComandaParaAbrir == "":
                        ComandaParaAbrir = str(ComandaParaAbrir) + "(" + str(id) + ", " + str(linha[0]) + ", '" + a["Observacoes"] + "', '" + data["Nome"] + "', " + str(a["Quantidade"]) + ")"
                    else:
                        ComandaParaAbrir = str(ComandaParaAbrir) + ", (" + str(id) + ", " + str(linha[0]) + ", '" + a["Observacoes"] + "', '" + data["Nome"] + "', " + str(a["Quantidade"]) + ")"

    ComandaParaAbrir = ComandaParaAbrir + ";"
    print("insert into `comandaAberta` (`idComanda`, `idProduto`, `obs`, `nomePessoa`, `qtdProduto`) values " + ComandaParaAbrir)

    bd = banco.cursor()
    bd.execute("insert into `comandaAberta` (`idComanda`, `idProduto`, `obs`, `nomePessoa`, `qtdProduto`) values " + ComandaParaAbrir)
    banco.commit()
    
    #Comandas.append(data)
    banco.close()
    
    return jsonify(Comandas)

@app.route('/LimparComanda/<string:Ncomanda>', methods = ['GET'])
def LimparPedido(Ncomanda):

    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    Comandas.remove(indice_pessoas_por_nome[nome_procurado])

    return jsonify(Comandas)

@app.route('/MostraFinalizadas', methods = ['GET'])
def ComandasFinalizadas():
    Finalizadas.clear()
    
    banco = mysql.connector.connect(host = 'us-cdbr-east-04.cleardb.com', database = 'heroku_b200452de328eaa', user = 'b29ac0776cb380', password = '68cf88e1')
    
    cursor2 = banco.cursor()
    cursor2.execute("select * from comandaFinalizada;")
    Linhas = cursor2.fetchall()
    print(Linhas)

    cursor3 = banco.cursor()
    cursor3.execute("select `idComanda`, `nomePessoa` as 'Nome', sum(`preco` * `qtdProduto`) as 'Preço final' from `comandaFinalizada` inner join `cardapio` on `comandaFinalizada`.`idProduto` = `cardapio`.`idProduto` group by `idComanda`;")
    Linhas2 = cursor3.fetchall()
    print(Linhas2)

    for linha2 in Linhas2:
        itens = []
        data = ""
        for linha1 in Linhas:
            if linha1[0] == linha2[0]:
                for linha in linhas:
                    if linha[0] == linha1[1]:
                        itens.append({"Nome": linha[1], "Quantidade": linha1[3], "Valor": linha[2], "Nome Imagem": linha[5]})
                data = linha1[4]

        Finalizadas.append({"Nome":linha2[1], "Itens": itens, "Total": linha2[2], "Data": data})

    banco.close()

    return jsonify(Finalizadas)

@app.route('/ImagemItens', methods = ['GET'])
def ImagemDosItens():
    
    return jsonify(Imagens)

@app.route('/Finaliza/<string:Ncomanda>', methods = ['GET'])
def FinalizaComanda(Ncomanda):

    now = datetime.today()
    today = now.strftime("%d/%m/%Y")
    
    banco = mysql.connector.connect(host = 'us-cdbr-east-04.cleardb.com', database = 'heroku_b200452de328eaa', user = 'b29ac0776cb380', password = '68cf88e1')

    cursor2 = banco.cursor()
    cursor2.execute("select `idComanda`, `nomePessoa` as 'Nome', sum(`preco`) as 'Preço final' from `comandaFinalizada` inner join `cardapio` on `comandaFinalizada`.`idProduto` = `cardapio`.`idProduto` group by `idComanda`;")
    Linhas2 = cursor2.fetchall()

    if Linhas2 == []:
        id = 1
    else:
        id = Linhas2[len(Linhas2) - 1][0] + 1
    
    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    ComandaProcurada = indice_pessoas_por_nome[nome_procurado]

    ComandaParaFinalizar = ""

    for a in ComandaProcurada["Itens"]:
        for linha in linhas:
            if a["Nome"] == linha[1]:
                if float(a["Preco"]) == linha[2]:
                    if ComandaParaFinalizar == "":
                        ComandaParaFinalizar = str(ComandaParaFinalizar) + "(" + str(id) + ", " + str(linha[0]) + ", '" + Ncomanda + "', " + str(a["Quantidade"]) + ", '" + today + "')"
                    else:
                        ComandaParaFinalizar = str(ComandaParaFinalizar) + ", (" + str(id) + ", " + str(linha[0]) + ", '" + Ncomanda + "', " + str(a["Quantidade"]) + ", '" + today + "')"

    ComandaParaFinalizar = ComandaParaFinalizar + ";"
    print("insert into `comandaFinalizada` (`idComanda`, `idProduto`, `nomePessoa`, `qtdProduto`, `data`) values " + ComandaParaFinalizar)

    bd = banco.cursor()
    bd.execute("insert into `comandaFinalizada` (`idComanda`, `idProduto`, `nomePessoa`, `qtdProduto`, `data`) values " + ComandaParaFinalizar)
    banco.commit()
    
    Comandas.remove(indice_pessoas_por_nome[nome_procurado])

    banco.close()

    return jsonify(Finalizadas)

@app.route('/AddNaComanda/<string:Ncomanda>', methods = ['POST'])
def AddNaComanda(Ncomanda):
    data = request.get_json()
    
    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    ComandaProcurada = indice_pessoas_por_nome[nome_procurado]
    ComandaProcurada["Itens"].append(data)

    return jsonify(ComandaProcurada)

@app.route('/RemoveDaComanda/<string:Ncomanda>/<string:Item>', methods = ['GET'])
def RemoveDaComanda(Ncomanda,Item):

    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    ComandaProcurada = indice_pessoas_por_nome[nome_procurado]
    indice_item_por_nome = {a["Nome"]: a for a in ComandaProcurada["Itens"]}
    item_procurado = Item
    estrutura_do_item = indice_item_por_nome[item_procurado]
    ComandaProcurada["Itens"].remove(estrutura_do_item)

    return jsonify(ComandaProcurada)

@app.route('/EditaItem', methods = ['POST'])
def EditaItem():
    data = request.get_json()
    ItemAlterado = {}
    ItemAlterado.update(data)

    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = ItemAlterado["Nome"]
    ComandaProcurada = indice_pessoas_por_nome[nome_procurado]
    indice_item_por_nome = {a["Nome"]: a for a in ComandaProcurada["Itens"]}
    item_procurado = ItemAlterado["Item"]
    estrutura_do_item = indice_item_por_nome[item_procurado]
    estrutura_do_item.update({"Quantidade": ItemAlterado["Quantidade"]})

    return jsonify(Comandas)


@app.route('/AddNoCardapio', methods = ['POST'])
def ColocaNoCardapio():
    data = request.get_json()
    Cardapio.update(data)
    return(Cardapio)

@app.route('/RemoveDoCardapio/<string:Item>', methods = ['GET'])
def TiraDoCardapio(Item):
    del Cardapio[Item]
    return (Cardapio)
