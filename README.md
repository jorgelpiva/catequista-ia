# Catequista IA ⛪

Um Chatbot Católico baseado em Inteligência Artificial, desenvolvido com o objetivo de responder dúvidas de fé, teologia e doutrina cristã com um tom amigável, didático e fundamentado **exclusivamente** na Sagrada Escritura e no Magistério da Igreja Católica.

Criado por **Jorge Leandro Piva** (Cientista de Dados Católico e Entusiasta de Inteligência Artificial).

---

## 🌟 Funcionalidades

- **Respostas Fundamentadas:** A IA atua como um "Catequista Virtual" instruído com base na Bíblia, Catecismo da Igreja Católica (CIC), Patrística e escritos dos Santos.
- **Histórico Offline-first:** Todas as conversas e históricos são salvos diretamente no navegador (IndexedDB) através da tecnologia **RxDB**, garantindo privacidade e que o histórico não seja perdido ao recarregar a página.
- **Pin & Exclusão de Chats:** Sistema para gerenciar os bate-papos diretamente pela barra lateral, permitindo fixar conversas favoritas e remover as desnecessárias.
- **Truncamento de Contexto:** Lógica inteligente no backend para resumir e truncar o histórico de mensagens e não estourar os limites de tokens da API do Gemini, sem perder a capacidade de ter uma conversa contínua.
- **Interface Premium:** Frontend desenhado em *Glassmorphism*, modo escuro e toques sutis no *Dourado do Vaticano*. Totalmente responsivo e renderizando código Markdown nativo no chat.

## 💻 Tech Stack

### Frontend
- **Vue.js 3** + **Vite**
- **RxDB** (com Storage *Dexie*) para persistência reativa local.
- **Axios** (Integração com API).
- **Marked & DOMPurify** para renderização segura de respostas em Markdown.

### Backend
- **Python 3.11+**
- **FastAPI** & **Uvicorn** (API assíncrona de altíssima performance).
- **Gemini 2.5 Flash** via integração REST (urllib nativo) para gerar respostas otimizadas e livres de bibliotecas propensas a conflito.

---

## 🚀 Como Rodar o Projeto Localmente

O projeto está dividido em duas partes: o **Backend** (Python) e o **Frontend** (Vue/Node.js). Siga os passos abaixo para iniciar ambos.

### 1. Configurando o Backend (Python)

1. Entre na pasta do backend:
   ```bash
   cd backend
   ```
2. Crie e ative um ambiente virtual (recomendado usar `conda` ou `venv`):
   ```bash
   conda create -n catequista python=3.11
   conda activate catequista
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure a chave de API:
   - Crie um arquivo `.env` na raiz da pasta `backend` com a sua chave do Google Gemini:
   ```env
   GEMINI_API_KEY=sua_chave_aqui
   ```
5. Inicie o servidor do FastAPI:
   ```bash
   uvicorn main:app --reload
   ```
   > O servidor iniciará em `http://127.0.0.1:8000`.

### 2. Configurando o Frontend (Vue)

1. Abra um novo terminal e entre na pasta do frontend:
   ```bash
   cd frontend
   ```
2. Instale as dependências do Node:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento do Vite:
   ```bash
   npm run dev
   ```
4. Abra o navegador na URL indicada (geralmente `http://localhost:5173`) e comece a conversar com seu Catequista Virtual!

---

## 📜 Licença

Desenvolvido para fins pastorais e de evangelização. Salve Maria!
