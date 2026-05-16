import os
import numpy as np
from fastembed import TextEmbedding

# Obtém o caminho absoluto para o diretório do projeto
PROJETO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CONHECIMENTO_PATH = os.path.join(PROJETO_DIR, 'data', 'conhecimento.txt')
EMBEDDING_PATH = os.path.join(PROJETO_DIR, 'data', 'embedding.npy')

# Modelo leve via ONNX (mesma dimensão 384 do all-MiniLM-L6-v2, mas usa ~50MB de RAM)
modelo = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


def gerar_embeddings():

    if os.path.exists(EMBEDDING_PATH):
        print("Embeddings já existem.")
        return

    with open(CONHECIMENTO_PATH, "r", encoding="utf-8") as arquivo:
        textos = [linha.strip() for linha in arquivo.readlines() if linha.strip()]

    embeddings = np.array(list(modelo.embed(textos)))

    np.save(EMBEDDING_PATH, embeddings)

    print(f"Embeddings gerados com sucesso. Shape: {embeddings.shape}")