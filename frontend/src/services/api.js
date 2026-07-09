import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000', // Backend local
    headers: {
        'Content-Type': 'application/json'
    }
});

export const sendMessageToApi = async (sessionId, message, history) => {
    try {
        const response = await api.post('/chat', {
            session_id: sessionId,
            message: message,
            history: history.map(h => ({ role: h.role, content: h.content }))
        });
        return response.data.reply;
    } catch (error) {
        console.error("Erro na API:", error);
        throw new Error("Desculpe, ocorreu um erro ao se comunicar com o backend.");
    }
};
