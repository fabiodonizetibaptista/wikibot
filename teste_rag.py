from services.rag_service import buscar_contexto

pergunta = "O que é recuperação aumentada por geração?"

resultado = buscar_contexto(pergunta)

print(resultado)