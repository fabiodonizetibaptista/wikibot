from flask import Flask, render_template, request, jsonify

from services.rag_service import buscar_contexto
from services.ia_service import gerar_resposta
from services.memoria_service import adicionar_mensagem

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        dados = request.get_json()

        pergunta = dados["queryResult"]["queryText"]

        contexto = buscar_contexto(pergunta)

        resposta = gerar_resposta(pergunta, contexto)

        return jsonify({
            "fulfillmentText": resposta
        })

    except Exception as erro:

        return jsonify({
            "fulfillmentText": f"Erro: {str(erro)}"
        })


@app.route("/chat", methods=["POST"])
def chat():

    try:

        dados = request.get_json()

        pergunta = dados.get("pergunta")

        if not pergunta:

            return jsonify({
                "erro": "Pergunta não enviada."
            }), 400

        contexto = buscar_contexto(pergunta)

        adicionar_mensagem("user", pergunta)

        resposta = gerar_resposta(pergunta, contexto)

        adicionar_mensagem("assistant", resposta)

        return jsonify({
            "resposta": resposta
        })

    except Exception as erro:

        return jsonify({
            "erro": str(erro)
        }), 500


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)