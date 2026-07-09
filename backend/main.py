from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import logging

from prompts import SYSTEM_PROMPT
from gemini_client import generate_response
from context_manager import truncate_history

app = FastAPI(title="Catequista IA API")

# Permitir CORS para o frontend local (Vue/Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, ajustar para o domínio correto do Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageInput(BaseModel):
    role: str # "user" ou "assistant"
    content: str

class ChatRequest(BaseModel):
    session_id: str
    message: str
    history: List[MessageInput] = []

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Catequista IA!"}

@app.post("/chat")
@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    try:
        # 1. Truncar o histórico para evitar estourar o limite de tokens
        # Converte a lista de objetos Pydantic em dicionários
        history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]
        
        truncated_history = truncate_history(history_dicts, request.message)
        
        # 2. Gerar resposta
        resposta = generate_response(
            system_prompt=SYSTEM_PROMPT,
            history=truncated_history,
            new_message=request.message
        )
        
        return {"reply": resposta}
    
    except Exception as e:
        logging.exception("Erro ao processar mensagem:")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

