historico_conversa = []


def adicionar_mensagem(role, content):

    historico_conversa.append({
        "role": role,
        "content": content
    })


def obter_historico():

    # Retorna as últimas 10 mensagens para não sobrecarregar o prompt
    return historico_conversa[-10:]


def limpar_historico():
    """Limpa o histórico da conversa."""
    global historico_conversa
    historico_conversa = []