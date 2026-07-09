import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY não configurada no arquivo .env")

# Lista de modelos para tentar na API gratuita
MODELS_TO_TRY = [
    "gemini-1.5-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-pro-latest",
    "gemini-2.0-flash"
]

def generate_response(system_prompt: str, history: list, new_message: str) -> str:
    """
    Gera a resposta usando a API REST do Gemini com fallback automático de modelos.
    """
    
    # Formata o histórico
    contents = []
    
    # Injeta a instrução de sistema
    contents.append({
        "role": "user",
        "parts": [{"text": f"INSTRUÇÃO DO SISTEMA:\n{system_prompt}\n\nAja estritamente de acordo com esta instrução."}]
    })
    contents.append({
        "role": "model",
        "parts": [{"text": "Entendido. Sou o Catequista IA e agirei conforme a instrução recebida."}]
    })

    # Adiciona as mensagens do histórico
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })
        
    # Adiciona a mensagem atual
    contents.append({
        "role": "user",
        "parts": [{"text": new_message}]
    })
    
    payload = {"contents": contents}
    headers = {"Content-Type": "application/json"}
    payload_bytes = json.dumps(payload).encode('utf-8')
    
    last_error = ""
    
    # Tenta cada modelo da lista
    for model in MODELS_TO_TRY:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        req = urllib.request.Request(url, data=payload_bytes, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            last_error = f"[{model}] {e.code}: {e.read().decode('utf-8')}"
            continue # Se falhou, tenta o próximo modelo
        except Exception as e:
            last_error = f"[{model}] {str(e)}"
            continue

    raise ValueError(f"Todos os modelos da cota gratuita falharam ou estão indisponíveis. Último erro: {last_error}")

def count_tokens(text: str) -> int:
    """
    Estima os tokens. Tenta contar no primeiro modelo disponível, ou aproxima por caractere se falhar.
    """
    payload_bytes = json.dumps({"contents": [{"parts": [{"text": text}]}]}).encode('utf-8')
    
    for model in MODELS_TO_TRY:
        count_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:countTokens?key={API_KEY}"
        req = urllib.request.Request(count_url, data=payload_bytes, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data.get("totalTokens", 0)
        except Exception:
            continue
            
    return len(text) // 4

