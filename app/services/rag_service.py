import numpy as np
import os
from fastembed import TextEmbedding
from sklearn.metrics.pairwise import cosine_similarity

# Obtém o caminho absoluto para o diretório do projeto
PROJETO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CONHECIMENTO_PATH = os.path.join(PROJETO_DIR, 'data', 'conhecimento.txt')
EMBEDDING_PATH = os.path.join(PROJETO_DIR, 'data', 'embedding.npy')

# Instância única do modelo (carrega apenas uma vez na inicialização)
modelo = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


def buscar_contexto(pergunta):

    with open(CONHECIMENTO_PATH, "r", encoding="utf-8") as arquivo:
        # Filtra linhas vazias para manter alinhamento correto com os embeddings
        textos = [linha.strip() for linha in arquivo.readlines() if linha.strip()]

    embeddings = np.load(EMBEDDING_PATH)

    embedding_pergunta = np.array(list(modelo.embed([pergunta])))

    similaridades = cosine_similarity(
        embedding_pergunta,
        embeddings
    )[0]

    indice_mais_similar = np.argmax(similaridades)

    contexto = textos[indice_mais_similar]

    return contexto