import re
from flask import Flask, json, jsonify, request

app = Flask(__name__)

Cardapio = {
        "Refrigerante" : 5.50,
        "Hamburguer" : 12.75,
        "Carne Louca": 13,
        "Caldo": 10
}

Finalizadas = []

Comandas = []

Geral = [{"Cardapio": Cardapio}, Comandas]


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

app.run()