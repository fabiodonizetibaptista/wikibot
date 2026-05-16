from flask import Flask, render_template, request, jsonify

from app.services.rag_service import buscar_contexto
from app.services.ia_service import gerar_resposta
from app.services.memoria_service import adicionar_mensagem, limpar_historico

# Ajuste para o Flask encontrar as pastas de templates e arquivos estáticos
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')


@app.route("/")
def index():
    """Rota principal que renderiza a interface do chat."""
    limpar_historico()  # Limpa o histórico a cada nova visita
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Rota que recebe as requisições do Dialogflow.
    Esta é a conexão principal entre o agente e a nossa IA.
    """
    try:
        # 1. Recebe a requisição JSON do Dialogflow
        dados = request.get_json(silent=True)
        if not dados:
            return jsonify({"fulfillmentText": "Erro: requisição sem dados."}), 400

        # 2. Extrai a pergunta do usuário
        pergunta = dados['queryResult']['queryText']

        # 3. Busca o contexto relevante para a pergunta (RAG)
        contexto = buscar_contexto(pergunta)

        # 4. Gera a resposta final usando a IA (com o contexto)
        resposta_ia = gerar_resposta(pergunta, contexto)

        # 5. Adiciona a pergunta e a resposta ao histórico da conversa
        adicionar_mensagem("user", pergunta)
        adicionar_mensagem("assistant", resposta_ia)

        # 6. Formata e retorna a resposta para o Dialogflow
        resposta_dialogflow = {"fulfillmentText": resposta_ia}
        
        return jsonify(resposta_dialogflow)

    except Exception as e:
        # Em caso de qualquer erro no processo, loga e envia uma resposta padrão.
        print(f"Erro no webhook: {e}")
        return jsonify({"fulfillmentText": "Desculpe, encontrei um problema ao processar sua pergunta. Tente novamente."})


@app.route("/chat", methods=["POST"])
def chat():
    """
    Rota para interação direta via interface web (sem Dialogflow).
    É útil para testes rápidos.
    """
    try:
        pergunta = request.json['pergunta']
        contexto = buscar_contexto(pergunta)
        resposta = gerar_resposta(pergunta, contexto)
        adicionar_mensagem("user", pergunta)
        adicionar_mensagem("assistant", resposta)
        return jsonify({"resposta": resposta})
    except Exception as e:
        print(f"Erro no chat: {e}")
        return jsonify({"resposta": "Ocorreu um erro."}), 500
