<template>
  <div class="alerta-erro" v-if="temErro">
    <div class="erro-header">
      <span class="icon-erro">⚠️</span>
      <h4>{{ erro.mensagem }}</h4>
      <button @click="emit('fechar')" class="btn-fechar">×</button>
    </div>
    <p v-if="erro.detalhes" class="erro-detalhes">{{ erro.detalhes }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  erro: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['fechar']);

const temErro = computed(() => {
  return props.erro !== null;
});
</script>

<style scoped>
.alerta-erro {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 20px;
  animation: slideIn 0.3s ease-in-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.erro-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon-erro {
  font-size: 20px;
}

.erro-header h4 {
  margin: 0;
  color: #000;
  flex: 1;
}

.btn-fechar {
  background: none;
  border: none;
  font-size: 24px;
  color: #721c24;
  cursor: pointer;
  padding: 0;
  transition: opacity 0.2s;
}

.btn-fechar:hover {
  opacity: 0.7;
}

.erro-detalhes {
  margin: 10px 0 0 0;
  color: #000;
  font-size: 14px;
}
</style>
