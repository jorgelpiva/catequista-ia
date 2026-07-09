import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { initDB } from './db/rxdb-setup'

// Inicializa o banco antes de montar o Vue
initDB().then(() => {
  createApp(App).mount('#app')
}).catch(err => {
  console.error("Falha ao inicializar o RxDB:", err)
  // Monta o app mesmo assim para exibir um erro se necessário
  createApp(App).mount('#app')
})
