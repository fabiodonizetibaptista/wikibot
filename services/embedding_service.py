import os
import numpy as np

from sentence_transformers import SentenceTransformer


modelo = SentenceTransformer('all-MiniLM-L6-v2')


def gerar_embeddings():

    caminho_embeddings = "data/embedding.npy"

    if os.path.exists(caminho_embeddings):

        print("Embeddings já existem.")
        return

    with open("data/conhecimento.txt", "r", encoding="utf-8") as arquivo:

        textos = arquivo.readlines()

    embeddings = modelo.encode(textos)

    np.save(caminho_embeddings, embeddings)

    print("Embeddings gerados com sucesso.")