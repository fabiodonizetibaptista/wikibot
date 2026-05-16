import os
import requests
from dotenv import load_dotenv

# Ajuste no import para a nova estrutura
from app.services.memoria_service import obter_historico

# Carrega variáveis de ambiente do arquivo .env na raiz do projeto
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def gerar_resposta(pergunta, contexto):
    prompt = f'''
    Você é um assistente corporativo especializado em inteligência artificial.

    Responda SOMENTE com base no contexto fornecido.

    Se a resposta não estiver no contexto, diga:
    "Não encontrei essa informação na base de conhecimento."

    Contexto:
    {contexto}

    Pergunta:
    {pergunta}
    '''

    historico = obter_historico()

    messages = [
        {
            "role": "system",
            "content": '''
            Você é um assistente corporativo especializado em inteligência artificial.
            '''
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

    try:
        resposta = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=30 # Adicionado timeout
        )
        resposta.raise_for_status() # Lança exceção para respostas de erro (4xx ou 5xx)
        dados = resposta.json()
        return dados["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"Erro ao contatar a API do Groq: {e}")
        return "Desculpe, estou com problemas para me conectar ao serviço de inteligência artificial."
    except (KeyError, IndexError) as e:
        print(f"Erro ao processar a resposta da API: {e}")
        return "Desculpe, recebi uma resposta inesperada do serviço de inteligência artificial."