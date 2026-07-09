<template>
  <aside class="sidebar glass-panel">
    <div class="sidebar-header">
      <h2>Catequista IA</h2>
      <button @click="$emit('new-chat')" class="new-chat-btn" title="Nova Conversa">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>
    </div>
    
    <div class="chat-list">
      <div 
        v-for="chat in conversations" 
        :key="chat.id"
        class="chat-item"
        :class="{ active: currentChatId === chat.id, pinned: chat.pinned }"
        @click="$emit('select-chat', chat.id)"
      >
        <span class="chat-icon">{{ chat.pinned ? '📌' : '💬' }}</span>
        <div class="chat-info">
          <div class="chat-title">{{ chat.title }}</div>
          <div class="chat-date">{{ formatDate(chat.createdAt) }}</div>
        </div>
        <div class="chat-actions">
          <button @click.stop="$emit('pin-chat', chat)" :title="chat.pinned ? 'Desafixar' : 'Fixar'" class="action-btn">
            {{ chat.pinned ? '📍' : '📌' }}
          </button>
          <button @click.stop="$emit('delete-chat', chat.id)" title="Excluir" class="action-btn delete">
            🗑️
          </button>
        </div>
      </div>
      
      <div v-if="conversations.length === 0" class="empty-state">
        Nenhuma conversa ainda. Comece uma nova!
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  conversations: {
    type: Array,
    required: true
  },
  currentChatId: {
    type: String,
    default: null
  }
});

defineEmits(['new-chat', 'select-chat', 'delete-chat', 'pin-chat']);

const formatDate = (timestamp) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
};
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  height: 100vh;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  z-index: 10;
}

.sidebar-header {
  padding: 24px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--glass-border);
}

.sidebar-header h2 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--accent-color);
  margin: 0;
}

.new-chat-btn {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--glass-border);
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.new-chat-btn:hover {
  background: var(--bg-tertiary);
  color: var(--accent-color);
  border-color: var(--accent-color);
}

.new-chat-btn svg {
  width: 18px;
  height: 18px;
}

.chat-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 12px;
}

.chat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}

.chat-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.chat-item.active {
  background: var(--bg-tertiary);
  border-left: 3px solid var(--accent-color);
}

.chat-icon {
  font-size: 1.1rem;
  opacity: 0.7;
}

.chat-info {
  overflow: hidden;
}

.chat-title {
  font-size: 0.9rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text-primary);
}

.chat-date {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 2px;
}

.empty-state {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.85rem;
  padding: 20px;
  font-style: italic;
}

.chat-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s ease;
  margin-left: auto;
}

.chat-item:hover .chat-actions {
  opacity: 1;
}

.action-btn {
  background: transparent;
  border: none;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s ease;
  color: var(--text-secondary);
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.action-btn.delete:hover {
  background: rgba(255, 0, 0, 0.2);
}

.chat-item.pinned {
  border-left: 3px solid #ff9800; /* Laranja para diferenciá-lo do chat ativo (amarelo) */
}
</style>
