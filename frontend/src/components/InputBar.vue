<template>
  <div class="input-container glass-panel">
    <form @submit.prevent="submit" class="input-form">
      <textarea
        v-model="text"
        ref="textareaRef"
        placeholder="Pergunte ao Catequista..."
        @keydown.enter.prevent="handleEnter"
        rows="1"
        :disabled="disabled"
      ></textarea>
      <button type="submit" :disabled="!text.trim() || disabled" class="send-btn">
        <svg v-if="!disabled" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
        <span v-else class="loading-spinner"></span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

const props = defineProps({
  disabled: Boolean
});

const emit = defineEmits(['send']);
const text = ref('');
const textareaRef = ref(null);

const adjustHeight = () => {
  const el = textareaRef.value;
  if (!el) return;
  el.style.height = 'auto';
  el.style.height = `${Math.min(el.scrollHeight, 120)}px`;
};

watch(text, () => {
  nextTick(adjustHeight);
});

const handleEnter = (e) => {
  if (e.shiftKey) {
    // Permite quebra de linha com shift+enter
    text.value += '\n';
  } else {
    submit();
  }
};

const submit = () => {
  if (!text.value.trim() || props.disabled) return;
  emit('send', text.value.trim());
  text.value = '';
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto';
    }
  });
};
</script>

<style scoped>
.input-container {
  padding: 20px;
  border-top: 1px solid var(--glass-border);
  border-right: none;
}

.input-form {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: var(--bg-tertiary);
  padding: 12px 16px;
  border-radius: 24px;
  border: 1px solid var(--glass-border);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: border-color 0.3s ease;
}

.input-form:focus-within {
  border-color: var(--accent-color);
}

textarea {
  flex-grow: 1;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-family: inherit;
  font-size: 1rem;
  resize: none;
  outline: none;
  max-height: 120px;
  padding: 4px 0;
  line-height: 1.5;
}

textarea::placeholder {
  color: var(--text-secondary);
}

.send-btn {
  background: var(--accent-color);
  color: #000;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.send-btn:disabled {
  background: var(--bg-secondary);
  color: var(--text-secondary);
  cursor: not-allowed;
}

.send-btn:not(:disabled):hover {
  background: var(--accent-hover);
  transform: scale(1.05);
  box-shadow: 0 0 15px var(--accent-glow);
}

.send-btn svg {
  width: 20px;
  height: 20px;
  transform: translateX(-1px) translateY(1px);
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid var(--text-secondary);
  border-top-color: var(--accent-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
