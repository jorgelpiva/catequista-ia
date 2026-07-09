import logging

# Limite seguro do modelo (Gemini 1.5 Flash tem limite de ~1M, 
# mas vamos fixar um limite razoável para manter a agilidade e evitar custos,
# como 100k tokens por padrão ou um pouco menos dependendo da necessidade).
# Para este projeto inicial, um contexto de 8k ou 16k é excelente para chat.
MAX_CONTEXT_TOKENS = 8000 

def truncate_history(history: list, new_message: str, max_tokens: int = MAX_CONTEXT_TOKENS) -> list:
    """
    Retorna o histórico truncado para caber no max_tokens.
    O truncamento remove as mensagens mais antigas primeiro.
    O system_prompt NÃO está incluído neste history (é passado separadamente na API do Gemini).
    """
    # Abordagem simplificada para evitar circular import com o gemini_client
    # Considera ~4 caracteres = 1 token
    new_msg_tokens = len(new_message) // 4
    
    if new_msg_tokens > max_tokens:
        logging.warning("A nova mensagem é maior que o limite de tokens!")
        return []

    tokens_available = max_tokens - new_msg_tokens
    
    truncated_history = []
    current_tokens = 0
    
    for msg in reversed(history):
        msg_text = msg.get("content", "")
        msg_tokens = len(msg_text) // 4
        
        if current_tokens + msg_tokens <= tokens_available:
            truncated_history.insert(0, msg)
            current_tokens += msg_tokens
        else:
            break
            
    return truncated_history

