<template>
  <div class="chat-window" ref="scrollContainer">
    <div class="messages-container">
      <div v-if="messages.length === 0" class="welcome-message">
        <div class="welcome-icon">⛪</div>
        <h2>Louvado seja Nosso Senhor Jesus Cristo!</h2>
        <p>Sou o Catequista IA. Faça-me qualquer pergunta sobre a doutrina, a Bíblia, os sacramentos ou a vida dos santos.</p>
      </div>
      
      <MessageBubble 
        v-for="msg in messages" 
        :key="msg.id" 
        :message="msg" 
      />
      
      <div v-if="isLoading" class="message-bubble is-bot loading-bubble">
        <div class="avatar">⛪</div>
        <div class="content typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import MessageBubble from './MessageBubble.vue';

const props = defineProps({
  messages: {
    type: Array,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  }
});

const scrollContainer = ref(null);

const scrollToBottom = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight;
  }
};

// Faz scroll para baixo quando novas mensagens chegarem ou o loading mudar
watch(() => [props.messages, props.isLoading], () => {
  nextTick(() => {
    scrollToBottom();
  });
}, { deep: true });
</script>

<style scoped>
.chat-window {
  flex-grow: 1;
  overflow-y: auto;
  padding: 24px;
  scroll-behavior: smooth;
}

.messages-container {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.welcome-message {
  text-align: center;
  margin: 60px auto;
  max-width: 500px;
  animation: fadeIn 0.8s ease-out;
}

.welcome-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.welcome-message h2 {
  font-size: 1.5rem;
  color: var(--accent-color);
  margin-bottom: 12px;
}

.welcome-message p {
  color: var(--text-secondary);
  font-size: 1.05rem;
}

.loading-bubble {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  max-width: 85%;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 18px 24px !important;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background-color: var(--text-secondary);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
