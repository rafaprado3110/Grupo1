import re, mysql.connector
from flask import Flask, json, jsonify, request

app = Flask(__name__)

Cardapio = {}

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

Cardapio2 = {"Lanches": Lanches, "Salgados": Salgados, "Escondidinhos": Escondidinhos, "Caldos": Caldos, "Tapiocas": Tapiocas, "Bebidas": Bebidas, "Porcoes": Porcoes}

Geral = [{"Cardapio": Cardapio2}, Comandas]

con = mysql.connector.connect(host = 'us-cdbr-east-04.cleardb.com', database = 'heroku_b200452de328eaa', user = 'b29ac0776cb380', password = '68cf88e1')

cursor = con.cursor()
cursor.execute("select * from cardapio;")
linhas = cursor.fetchall()
print(linhas)
for linha in linhas:
    if linha[4] == "empadas":
        Empadas[linha[1]] = linha[2]
    elif linha[4] == "tortas":
        Tortas[linha[1]] = linha[2]
    elif linha[4] == "hot-dogs":
        HotDog[linha[1]] = linha[2]
    elif linha[4] == "sanduiches":
        Sanduiche[linha[1]] = linha[2]
    elif linha[4] == "escondidinhos":
        Escondidinhos[linha[1]] = linha[2]
    elif linha[4] == "caldos":
        Caldos[linha[1]] = linha[2]
    elif linha[4] == "salgadas":
        TSalgadas[linha[1]] = linha[2]
    elif linha[4] == "doces":
        TDoces[linha[1]] = linha[2]
    elif linha[4] == "alcoólicas":
        BAlcool[linha[1]] = linha[2]
    elif linha[4] == "não-alcoólicas":
        BSemAlcool[linha[1]] = linha[2]
    elif linha[4] == "sucos detox":
        SucosDetox[linha[1]] = linha[2]
    elif linha[4] == "porções":
        Porcoes[linha[1]] = linha[2]

@app.route('/', methods =['GET'])
def raiz():
    return jsonify(Geral)

@app.route('/MostraCardapio', methods =['GET'])
def GetCardapio():
    return jsonify(Cardapio)

@app.route('/MostraComandasAbertas', methods =['GET'])
def GetComandas():
    return jsonify(Comandas)

@app.route('/MostraComandaPorNome/<string:Ncomanda>', methods =['GET'])
def GetComandaPorNome(Ncomanda):
    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    return jsonify(indice_pessoas_por_nome[nome_procurado])

@app.route('/Pedido', methods = ['POST'])
def PedidoFeito():
    data = request.get_json()

    Comandas.append(data)
    
    return jsonify(Geral)

@app.route('/LimparComanda/<string:Ncomanda>', methods = ['GET'])
def LimparPedido(Ncomanda):

    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    Comandas.remove(indice_pessoas_por_nome[nome_procurado])

    return jsonify(Geral)

@app.route('/MostraFinalizadas', methods = ['GET'])
def ComandasFinalizadas():
    return jsonify(Finalizadas)

@app.route('/Finaliza/<string:Ncomanda>', methods = ['GET'])
def FinalizaComanda(Ncomanda):

    ComandaF = {}

    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    ComandaF = indice_pessoas_por_nome[nome_procurado].copy()
    Finalizadas.append(ComandaF)
    Comandas.remove(indice_pessoas_por_nome[nome_procurado])
    
    return jsonify(Finalizadas)

@app.route('/AddNaComanda/<string:Ncomanda>', methods = ['POST'])
def AddNaComanda(Ncomanda):
    data = request.get_json()
    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    indice_pessoas_por_nome[nome_procurado].update(data)

    return jsonify(indice_pessoas_por_nome[nome_procurado])

@app.route('/RemoveDaComanda/<string:Ncomanda>/<string:Item>', methods = ['GET'])
def RemoveDaComanda(Ncomanda,Item):
    indice_pessoas_por_nome = {d["Nome"]: d for d in Comandas}
    nome_procurado = Ncomanda
    Comanda = indice_pessoas_por_nome[nome_procurado]
    del Comanda[Item]
    

    return jsonify(indice_pessoas_por_nome[nome_procurado])


@app.route('/AddNoCardapio', methods = ['POST'])
def ColocaNoCardapio():
    data = request.get_json()
    Cardapio.update(data)
    return(Cardapio)

@app.route('/RemoveDoCardapio/<string:Item>', methods = ['GET'])
def TiraDoCardapio(Item):
    del Cardapio[Item]
    return (Cardapio)
