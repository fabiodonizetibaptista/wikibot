# 🤖 Wikibot — Assistente Corporativo com IA

> Chatbot corporativo especializado em Inteligência Artificial, construído com arquitetura RAG (Retrieval-Augmented Generation), integrado ao Google Dialogflow e hospedado na nuvem.

---

## 📌 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Ferramentas Utilizadas](#ferramentas-utilizadas)
- [Por que não usamos o Ollama localmente?](#por-que-não-usamos-o-ollama-localmente)
- [Como Acessar e Usar](#como-acessar-e-usar)
- [Como Executar Localmente](#como-executar-localmente)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Base de Conhecimento](#base-de-conhecimento)
- [Deploy](#deploy)

---

## Sobre o Projeto

O **Wikibot** é um assistente virtual corporativo focado em responder perguntas sobre **Inteligência Artificial**. Ele utiliza a técnica de **RAG (Retrieval-Augmented Generation)** para buscar informações relevantes em uma base de conhecimento interna antes de gerar uma resposta, garantindo que as respostas sejam sempre fundamentadas em conteúdo validado — e não em "alucinações" da IA.

O bot é integrado ao **Google Dialogflow** como interface conversacional e processa as perguntas em um backend Python/Flask hospedado no **Render**.

---

## Arquitetura

```
┌─────────────────┐       ┌──────────────────┐       ┌───────────────────────┐
│   Usuário       │──────▶│  Google          │──────▶│  Flask (Webhook)      │
│  (chat)         │       │  Dialogflow      │  POST  │  /webhook             │
└─────────────────┘       └──────────────────┘       └──────────┬────────────┘
                                                                 │
                                    ┌────────────────────────────▼────────────────────────────┐
                                    │                  Processamento RAG                       │
                                    │                                                          │
                                    │  1. fastembed converte a pergunta em embedding           │
                                    │  2. Cosine similarity busca o trecho mais relevante      │
                                    │     na base de conhecimento (conhecimento.txt)           │
                                    │  3. Contexto + pergunta são enviados ao Groq (LLaMA)    │
                                    │  4. Resposta é retornada ao Dialogflow                  │
                                    └──────────────────────────────────────────────────────────┘
```

---

## Ferramentas Utilizadas

### 🐍 Python 3.11
**O que faz:** Linguagem base de todo o projeto.  
**Por que foi escolhida:** Python é o padrão da indústria para projetos de IA e Machine Learning, com o ecossistema de bibliotecas mais rico disponível. Sua sintaxe clara facilita a manutenção e evolução do projeto.

---

### 🌐 Flask
**O que faz:** Framework web responsável por expor as rotas HTTP do projeto, incluindo o webhook que recebe as chamadas do Dialogflow (`/webhook`), a interface de chat direto (`/chat`) e o health check (`/health`).  
**Por que foi escolhido:** Flask é leve, minimalista e ideal para APIs e microsserviços. Não carrega overhead desnecessário, o que é fundamental para um serviço hospedado em plano gratuito com recursos limitados.

---

### 🤖 Google Dialogflow
**O que faz:** Interface conversacional do bot. Recebe as mensagens do usuário, processa a linguagem natural (NLU) e encaminha a pergunta ao webhook do backend para obtenção da resposta via IA.  
**Por que foi escolhido:** Dialogflow oferece um NLU robusto gratuitamente, com suporte nativo a intents, entities e integração com múltiplos canais (WhatsApp, Telegram, Web, etc.), sem necessidade de implementar o processamento de linguagem natural do zero.

---

### ⚡ Groq API (LLaMA 3.1 8B Instant)
**O que faz:** Serviço de inferência de LLM (Large Language Model) na nuvem. Recebe o contexto recuperado pelo RAG e a pergunta do usuário, e gera uma resposta em linguagem natural precisa e contextualizada.  
**Por que foi escolhido:** A Groq é atualmente a API de inferência de LLM mais rápida disponível no mercado, com latência extremamente baixa (~200ms). Oferece acesso gratuito ao modelo **LLaMA 3.1 8B Instant**, que é altamente capaz para tarefas de Q&A corporativo. A combinação velocidade + gratuidade + qualidade a torna a escolha ideal para este projeto.

---

### 🔍 fastembed + ONNX Runtime
**O que faz:** Biblioteca responsável por converter textos em vetores numéricos (embeddings) para a etapa de busca semântica do RAG. Utiliza o modelo `BAAI/bge-small-en-v1.5` via ONNX Runtime, sem necessidade do PyTorch.  
**Por que foi escolhido:** O `fastembed` foi escolhido por ser extremamente leve em comparação com alternativas como `sentence-transformers` + PyTorch (que consomem mais de 600MB de RAM). O `fastembed` com ONNX consome apenas ~80MB, tornando o deploy viável no plano gratuito do Render (limite de 512MB). A qualidade dos embeddings é equivalente, pois utiliza o mesmo modelo de 384 dimensões.

---

### 📐 scikit-learn (cosine_similarity)
**O que faz:** Calcula a similaridade de cosseno entre o embedding da pergunta do usuário e todos os embeddings da base de conhecimento, identificando o trecho mais relevante para responder à pergunta.  
**Por que foi escolhido:** scikit-learn é a biblioteca de machine learning mais consolidada do ecossistema Python. A função `cosine_similarity` é eficiente, bem testada e perfeita para busca semântica em bases de conhecimento de pequeno e médio porte.

---

### 🗄️ NumPy
**O que faz:** Armazena e manipula os vetores de embeddings da base de conhecimento no arquivo `embedding.npy`, e realiza as operações matriciais necessárias para o cálculo de similaridade.  
**Por que foi escolhido:** NumPy é o padrão para operações numéricas em Python. O formato `.npy` permite salvar e carregar embeddings pré-computados em milissegundos, evitando o reprocessamento a cada requisição.

---

### ☁️ Render
**O que faz:** Plataforma de cloud hosting onde o backend Flask está hospedado, fornecendo uma URL pública e permanente para o webhook do Dialogflow.  
**Por que foi escolhido:** O Render oferece um plano gratuito para serviços web Python com deploy automático via GitHub. É simples de configurar, suporta variáveis de ambiente seguras e possui integração nativa com `render.yaml` para configuração como código.

---

### 🟢 Gunicorn
**O que faz:** Servidor WSGI de produção que executa a aplicação Flask no Render. Gerencia múltiplos workers para lidar com requisições simultâneas de forma estável.  
**Por que foi escolhido:** O servidor de desenvolvimento do Flask não é adequado para produção. O Gunicorn é o servidor WSGI mais usado com Flask em produção, oferecendo estabilidade, performance e suporte nativo no Render.

---

### 🔐 python-dotenv
**O que faz:** Carrega as variáveis de ambiente do arquivo `.env` (como a `GROQ_API_KEY`) sem expô-las no código-fonte.  
**Por que foi escolhido:** Boa prática fundamental de segurança: nunca hardcodar chaves de API no código. O `python-dotenv` é o padrão da indústria para gerenciamento de variáveis de ambiente em projetos Python.

---

## Por que não usamos o Ollama localmente?

O exercício original propunha a utilização do **Ollama** para executar modelos de linguagem localmente (na própria máquina). Porém, optamos por uma arquitetura baseada em **API na nuvem (Groq)** por uma razão fundamental de **acessibilidade e portabilidade**:

> **O Wikibot foi projetado para funcionar em qualquer computador, independentemente das suas especificações de hardware.**

Modelos de linguagem grandes como o LLaMA, quando executados localmente via Ollama, exigem:

- **8GB a 16GB de RAM** para modelos de 7B/8B parâmetros
- Processadores modernos com múltiplos núcleos
- Preferencialmente uma **GPU dedicada** para performance aceitável
- **Espaço em disco significativo** (4GB a 8GB por modelo)

Essa exigência de hardware tornaria o projeto inacessível para grande parte dos usuários e ambientes corporativos com máquinas mais modestas. Ao utilizar a **Groq API**, o processamento pesado ocorre nos servidores da Groq, e o bot responde rapidamente em qualquer máquina — inclusive em computadores antigos com poucos recursos.

Além disso, a solução em nuvem oferece:

| Critério | Ollama Local | Groq API (escolhida) |
|---|---|---|
| Requisito de hardware | Alto (8GB+ RAM, GPU ideal) | Nenhum |
| Velocidade de resposta | Lenta sem GPU | Muito rápida (~200ms) |
| Portabilidade | Limitada | Universal |
| Custo de infraestrutura | Alto (hardware) | Gratuito |
| Disponibilidade | Apenas na máquina local | 24/7 na nuvem |
| Facilidade de deploy | Complexa | Simples |

Essa decisão arquitetural garante que o **Wikibot possa ser acessado por qualquer pessoa, de qualquer dispositivo, sem barreiras de hardware**.

---

## Como Acessar e Usar

### Acesso via Dialogflow (Produção)
O bot está integrado ao Google Dialogflow. Para interagir com ele, acesse o console do Dialogflow e utilize o painel **"Try it now"** ou integre a um canal de sua escolha.

**URL do Webhook (configurada no Dialogflow):**
```
https://wikibot-wbdj.onrender.com/webhook
```

### Acesso via API direta
Você pode também testar o webhook diretamente com qualquer cliente HTTP:

```bash
curl -X POST https://wikibot-wbdj.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"queryResult": {"queryText": "O que é machine learning?"}}'
```

**Resposta esperada:**
```json
{
  "fulfillmentText": "O machine learning é uma subárea da inteligência artificial..."
}
```

### Health Check
Para verificar se o serviço está operacional:
```
GET https://wikibot-wbdj.onrender.com/health
```

**Resposta:**
```json
{
  "status": "ok",
  "servico": "wikibot",
  "mensagem": "Serviço operacional."
}
```

---

## Como Executar Localmente

### Pré-requisitos
- Python 3.11+
- Conta na [Groq](https://console.groq.com) com uma API Key

### 1. Clone o repositório
```bash
git clone -b aplication https://github.com/fabiodonizetibaptista/wikibot.git
cd wikibot
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
GROQ_API_KEY=sua_chave_aqui
```

### 4. Gere os embeddings da base de conhecimento
> ⚠️ Necessário apenas na primeira execução ou ao alterar o `conhecimento.txt`
```bash
python executar_embedding.py
```

### 5. Inicie o servidor
```bash
flask run
```
O servidor estará disponível em `http://127.0.0.1:5000`

### 6. Teste o webhook
```bash
curl -X POST http://127.0.0.1:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"queryResult": {"queryText": "O que é IA generativa?"}}'
```

---

## Estrutura do Projeto

```
wikibot/
│
├── main.py                         # Entrypoint: rotas Flask (webhook, chat, health)
├── requirements.txt                # Dependências do projeto
├── render.yaml                     # Configuração de deploy no Render
├── runtime.txt                     # Versão do Python para o Render
├── .python-version                 # Versão do Python (pyenv/Render)
├── .env                            # Variáveis de ambiente (NÃO versionar)
├── .gitignore
│
├── executar_embedding.py           # Script para gerar/atualizar embeddings
├── teste_ia.py                     # Script de teste da IA isolada
├── teste_rag.py                    # Script de teste do RAG isolado
├── teste_embedding.py              # Script de teste dos embeddings
│
└── app/
    ├── data/
    │   ├── conhecimento.txt        # Base de conhecimento do bot
    │   └── embedding.npy           # Embeddings pré-computados (gerado automaticamente)
    │
    ├── services/
    │   ├── ia_service.py           # Integração com a API do Groq (LLaMA)
    │   ├── rag_service.py          # Busca semântica (RAG) com fastembed
    │   ├── embedding_service.py    # Geração de embeddings com fastembed
    │   └── memoria_service.py      # Gerenciamento do histórico de conversa
    │
    ├── routes/
    │   └── chat_routes.py          # Rotas alternativas de chat
    │
    └── templates/
        └── index.html              # Interface web do chat
```

---

## Base de Conhecimento

O arquivo `app/data/conhecimento.txt` é o coração do RAG. Cada linha representa um fragmento de conhecimento independente que o bot pode recuperar e usar como contexto para gerar respostas.

**Para adicionar novos conteúdos:**
1. Edite `app/data/conhecimento.txt` adicionando novas linhas
2. Delete o arquivo `app/data/embedding.npy`
3. Execute `python executar_embedding.py` para regenerar os embeddings
4. Faça commit e push — o Render redeploya automaticamente

---

## Deploy

O projeto está configurado para deploy automático no **Render** via `render.yaml`.

A cada `git push` na branch `aplication`, o Render automaticamente:
1. Clona o repositório
2. Instala as dependências (`pip install -r requirements.txt`)
3. Inicia o servidor com Gunicorn (`gunicorn main:app`)

### Variáveis de ambiente no Render
Configure no dashboard do Render (Settings → Environment):

| Variável | Descrição |
|---|---|
| `GROQ_API_KEY` | Chave de acesso à API do Groq |

### Keep-Alive (UptimeRobot)
Para evitar que o serviço "adormeça" no plano gratuito do Render, configure um monitor gratuito no [UptimeRobot](https://uptimerobot.com) para pingar a URL de health check a cada 5 minutos:
```
https://wikibot-wbdj.onrender.com/health
```

---

## 👨‍💻 Autor

**Fabio Donizete Baptista**  
Projeto desenvolvido como exercício prático de construção de chatbot corporativo com IA generativa e arquitetura RAG.

---

*Wikibot — Inteligência Artificial a serviço do conhecimento corporativo* 🤖