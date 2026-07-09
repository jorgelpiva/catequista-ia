<template>
  <div class="app-layout">
    <Sidebar 
      :conversations="conversations" 
      :current-chat-id="currentSessionId"
      @new-chat="startNewChat"
      @select-chat="selectChat"
    />
    
    <main class="main-content">
      <header class="top-bar">
        <h1>{{ currentChatTitle || 'Nova Conversa' }}</h1>
        <div class="status" :class="{ 'online': !isLoading, 'typing': isLoading }">
          {{ isLoading ? 'Pensando...' : 'Online' }}
        </div>
      </header>
      
      <ChatWindow 
        :messages="currentMessages" 
        :is-loading="isLoading" 
      />
      
      <div class="input-wrapper">
        <InputBar 
          :disabled="isLoading" 
          @send="handleSendMessage" 
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import Sidebar from './components/Sidebar.vue';
import ChatWindow from './components/ChatWindow.vue';
import InputBar from './components/InputBar.vue';
import { getDB } from './db/rxdb-setup';
import { sendMessageToApi } from './services/api';

const db = ref(null);
const conversations = ref([]);
const allMessages = ref([]);
const currentSessionId = ref(null);
const isLoading = ref(false);

const currentChatTitle = computed(() => {
  const chat = conversations.value.find(c => c.id === currentSessionId.value);
  return chat ? chat.title : '';
});

const currentMessages = computed(() => {
  if (!currentSessionId.value) return [];
  return allMessages.value
    .filter(m => m.conversationId === currentSessionId.value)
    .sort((a, b) => a.createdAt - b.createdAt);
});

onMounted(async () => {
  try {
    db.value = await getDB();
    
    // Inscrever-se para mudanças nas coleções usando RxJS
    db.value.conversations.find().sort({ createdAt: 'desc' }).$.subscribe(results => {
      conversations.value = results.map(d => d.toJSON());
    });
    
    db.value.messages.find().$.subscribe(results => {
      allMessages.value = results.map(d => d.toJSON());
    });
    
  } catch (error) {
    console.error("Erro ao carregar banco:", error);
    alert("Erro crítico ao inicializar o banco de dados: " + error.message);
  }
});

const startNewChat = () => {
  currentSessionId.value = null;
};

const selectChat = (id) => {
  currentSessionId.value = id;
};

const handleSendMessage = async (text) => {
  if (!text.trim()) return;
  
  try {
    // Se não tem sessão atual, cria uma nova
    if (!currentSessionId.value) {
      if (!db.value) throw new Error("Banco de dados não foi inicializado.");
      const newId = uuidv4();
      const title = text.length > 30 ? text.substring(0, 30) + '...' : text;
      
      await db.value.conversations.insert({
        id: newId,
        title: title,
        createdAt: Date.now()
      });
      
      currentSessionId.value = newId;
    }
    
    const sessionId = currentSessionId.value;
    
    // Salva a mensagem do usuário
    const userMessage = {
      id: uuidv4(),
      conversationId: sessionId,
      role: 'user',
      content: text,
      createdAt: Date.now()
    };
    
    await db.value.messages.insert(userMessage);
    
    // Pega o histórico ATUAL para enviar
    const history = currentMessages.value
      .filter(m => m.id !== userMessage.id) 
      .map(m => ({
        role: m.role,
        content: m.content
      }));

    isLoading.value = true;
    
    try {
      // Chama o backend
      const replyText = await sendMessageToApi(sessionId, text, history);
      
      // Salva a resposta do bot
      await db.value.messages.insert({
        id: uuidv4(),
        conversationId: sessionId,
        role: 'assistant',
        content: replyText,
        createdAt: Date.now()
      });
      
    } catch (apiError) {
      // Insere mensagem de erro
      await db.value.messages.insert({
        id: uuidv4(),
        conversationId: sessionId,
        role: 'assistant',
        content: `**Erro da API**: ${apiError.message}`,
        createdAt: Date.now()
      });
    } finally {
      isLoading.value = false;
    }
  } catch (error) {
    alert("Erro interno no Frontend (verifique o console): " + error.message);
    console.error(error);
  }
};
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--bg-primary);
  background-image: 
    radial-gradient(circle at 15% 50%, rgba(255, 215, 0, 0.03), transparent 25%),
    radial-gradient(circle at 85% 30%, rgba(255, 215, 0, 0.03), transparent 25%);
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100%;
}

.top-bar {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--glass-border);
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 5;
}

.top-bar h1 {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0;
}

.status {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
}

.status::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #4CAF50;
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.5);
}

.status.typing::before {
  background-color: var(--accent-color);
  box-shadow: 0 0 8px var(--accent-glow);
  animation: pulse 1.5s infinite;
}

.input-wrapper {
  padding: 0 24px 24px;
  background: linear-gradient(to top, var(--bg-primary) 80%, transparent);
}

@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}
</style>
