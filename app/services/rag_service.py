import numpy as np
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Obtém o caminho absoluto para o diretório do projeto
PROJETO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CONHECIMENTO_PATH = os.path.join(PROJETO_DIR, 'data', 'conhecimento.txt')
EMBEDDING_PATH = os.path.join(PROJETO_DIR, 'data', 'embedding.npy')

modelo = SentenceTransformer('all-MiniLM-L6-v2')


def buscar_contexto(pergunta):

    with open(CONHECIMENTO_PATH, "r", encoding="utf-8") as arquivo:

        textos = arquivo.readlines()

    embeddings = np.load(EMBEDDING_PATH)

    embedding_pergunta = modelo.encode([pergunta])

    similaridades = cosine_similarity(
        embedding_pergunta,
        embeddings
    )[0]

    indice_mais_similar = np.argmax(similaridades)

    contexto = textos[indice_mais_similar]

    return contexto