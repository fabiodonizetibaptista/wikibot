import os
import requests

from dotenv import load_dotenv

from services.memoria_service import obter_historico

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def gerar_resposta(pergunta, contexto):

    prompt = f"""
    Você é um assistente corporativo especializado em inteligência artificial.

    Responda SOMENTE com base no contexto fornecido.

    Se a resposta não estiver no contexto, diga:
    "Não encontrei essa informação na base de conhecimento."

    Contexto:
    {contexto}

    Pergunta:
    {pergunta}
    """

    historico = obter_historico()

    messages = [
        {
            "role": "system",
            "content": """
            Você é um assistente corporativo especializado em inteligência artificial.
            """
        }
    ]

    messages.extend(historico)

    messages.append({
        "role": "user",
        "content": prompt
    })

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.1-8b-instant",
        "messages": messages
    }

    resposta = requests.post(
        url,
        headers=headers,
        json=body
    )

    dados = resposta.json()

    return dados["choices"][0]["message"]["content"]