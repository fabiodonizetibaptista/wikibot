from services.rag_service import buscar_contexto
from services.ia_service import gerar_resposta


pergunta = "O que é RAG?"

contexto = buscar_contexto(pergunta)

resposta = gerar_resposta(pergunta, contexto)

print(resposta)