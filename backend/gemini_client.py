import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY não configurada no arquivo .env")

# URL direta da API REST do Gemini
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"

def generate_response(system_prompt: str, history: list, new_message: str) -> str:
    """
    Gera a resposta usando a API REST do Gemini 1.5 Flash.
    """
    
    # Formata o histórico
    contents = []
    
    # Injeta a instrução de sistema (já que a v1beta REST systemInstruction é complexa)
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
    
    payload = {
        "contents": contents
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    payload_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(GEMINI_API_URL, data=payload_bytes, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        raise ValueError(f"Erro da API Gemini ({e.code}): {error_msg}")
    except (KeyError, IndexError):
        raise ValueError(f"Resposta inesperada da API: {data}")

def count_tokens(text: str) -> int:
    """
    Estima os tokens usando a API REST de contagem do modelo.
    """
    count_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:countTokens?key={API_KEY}"
    payload_bytes = json.dumps({"contents": [{"parts": [{"text": text}]}]}).encode('utf-8')
    req = urllib.request.Request(count_url, data=payload_bytes, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("totalTokens", 0)
    except Exception:
        return len(text) // 4

