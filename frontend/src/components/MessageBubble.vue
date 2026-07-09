<template>
  <div class="message-bubble" :class="{ 'is-user': isUser }">
    <div class="avatar">
      <span v-if="isUser">👤</span>
      <span v-else>⛪</span>
    </div>
    <div class="content">
      <div v-if="isUser" class="text">{{ message.content }}</div>
      <div v-else class="markdown-body" v-html="renderedContent"></div>
      <div class="time">{{ formattedTime }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
});

const isUser = computed(() => props.message.role === 'user');

const renderedContent = computed(() => {
  if (isUser.value) return props.message.content;
  const rawHtml = marked.parse(props.message.content);
  return DOMPurify.sanitize(rawHtml);
});

const formattedTime = computed(() => {
  const date = new Date(props.message.createdAt);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
});
</script>

<style scoped>
.message-bubble {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  max-width: 85%;
}

.message-bubble.is-user {
  margin-left: auto;
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  font-size: 1.2rem;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border: 1px solid var(--glass-border);
}

.is-user .avatar {
  background: var(--accent-color);
  color: #000;
}

.content {
  background: var(--bubble-bot);
  padding: 14px 18px;
  border-radius: 18px;
  border-top-left-radius: 4px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  border: 1px solid var(--glass-border);
  position: relative;
}

.is-user .content {
  background: var(--bubble-user);
  border-radius: 18px;
  border-top-right-radius: 4px;
}

.text {
  font-size: 0.95rem;
  white-space: pre-wrap;
}

.time {
  font-size: 0.7rem;
  color: var(--text-secondary);
  margin-top: 6px;
  text-align: right;
  opacity: 0.7;
}
</style>
