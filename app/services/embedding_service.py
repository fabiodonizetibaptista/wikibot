import os
import numpy as np
from sentence_transformers import SentenceTransformer

# Obtém o caminho absoluto para o diretório do projeto
PROJETO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CONHECIMENTO_PATH = os.path.join(PROJETO_DIR, 'data', 'conhecimento.txt')
EMBEDDING_PATH = os.path.join(PROJETO_DIR, 'data', 'embedding.npy')

modelo = SentenceTransformer('all-MiniLM-L6-v2')


def gerar_embeddings():

    if os.path.exists(EMBEDDING_PATH):

        print("Embeddings já existem.")
        return

    with open(CONHECIMENTO_PATH, "r", encoding="utf-8") as arquivo:

        textos = arquivo.readlines()

    embeddings = modelo.encode(textos)

    np.save(EMBEDDING_PATH, embeddings)

    print("Embeddings gerados com sucesso.")