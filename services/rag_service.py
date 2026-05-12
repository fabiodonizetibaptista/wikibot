import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


modelo = SentenceTransformer('all-MiniLM-L6-v2')


def buscar_contexto(pergunta):

    with open("data/conhecimento.txt", "r", encoding="utf-8") as arquivo:

        textos = arquivo.readlines()

    embeddings = np.load("data/embedding.npy")

    embedding_pergunta = modelo.encode([pergunta])

    similaridades = cosine_similarity(
        embedding_pergunta,
        embeddings
    )[0]

    indice_mais_similar = np.argmax(similaridades)

    contexto = textos[indice_mais_similar]

    return contexto