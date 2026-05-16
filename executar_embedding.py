# -*- coding: utf-8 -*-
# Este script é para uso único para gerar os embeddings.
# Ele importa a função do serviço e a executa.

import sys
import os

# Adiciona o diretório raiz ao path para que possamos importar o módulo 'app'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.services import embedding_service

if __name__ == "__main__":
    print("Iniciando a geração de embeddings...")
    embedding_service.gerar_embeddings()
    print("Processo de geração de embeddings concluído.")