from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route("/")
def get_liturgy():
    url = "https://liturgia.up.railway.app/"

    response = requests.get(url)
    data = json.loads(response.text)

    titulos = [
        "data",
        "liturgia",
        "cor",
        "dia",
        "oferendas",
        "comunhao",
        "primeiraLeitura",
        "segundaLeitura",
        "salmo",
        "evangelho"
    ]

    correspondentes = []

    for titulo in titulos:
        correspondente = data.get(titulo, "")
        if isinstance(correspondente, dict):
            correspondente = tratamento_dados(correspondente, titulo)
        correspondentes.append((format_title(titulo), correspondente))

    return render_template('index.html', titulos_correspondentes=correspondentes)

def tratamento_dados(dados, titulo):
    correspondente = ""
    if "referencia" in dados:
        correspondente += dados["referencia"]
    if "titulo" in dados:
        correspondente += " - " + dados["titulo"]
    if "texto" in dados:
        correspondente += "<br><br>" + dados["texto"].replace("\n", "<br>")
    if titulo == "primeiraLeitura":
        correspondente += "<br><br>- Palavra do Senhor.<br>- Graças a Deus."
    elif titulo == "evangelho":
        correspondente += "<br>— Palavra da Salvação.<br>— Glória a vós, Senhor."
    return correspondente.replace("\n", "<br>")

def format_title(string):
    formatted = string[0].upper()
    for i in range(1, len(string)):
        if string[i].isupper():
            formatted += " " + string[i]
        else:
            formatted += string[i]
    return formatted

if __name__ == "__main__":
    app.run()
