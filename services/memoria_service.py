historico_conversa = []


def adicionar_mensagem(role, content):

    historico_conversa.append({
        "role": role,
        "content": content
    })


def obter_historico():

    return historico_conversa[-10:]