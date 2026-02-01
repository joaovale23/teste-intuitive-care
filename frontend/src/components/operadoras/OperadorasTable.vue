<template>
  <div class="tabela-container">
    <!-- Barra de busca -->
    <div class="busca-section">
      <div class="busca-controles">
        <select v-model="campoBusca" class="select-busca" @change="emitirBusca">
          <option value="razao_social">Razão social</option>
          <option value="cnpj">CNPJ</option>
        </select>
        <input
          v-model="buscaLocal"
          type="text"
          :placeholder="placeholderBusca"
          class="input-busca"
          @input="emitirBusca"
        />
      </div>
      <span v-if="buscaLocal" class="resultado-busca">
        {{ operadorasFiltradas.length }} resultado(s)
      </span>
    </div>

    <!-- Estado: Loading -->
    <div v-if="loading" class="estado-loading">
      <div class="spinner"></div>
      <p>Carregando operadoras...</p>
    </div>

    <!-- Estado: Vazio -->
    <div v-else-if="operadorasFiltradas.length === 0" class="estado-vazio">
      <p>Nenhuma operadora encontrada</p>
    </div>

    <!-- Tabela: Dados -->
    <table v-else class="tabela-operadoras">
      <thead>
        <tr>
          <th>
            Razão Social
          </th>
          <th>
            CNPJ
          </th>
          <th>
            Modalidade
          </th>
          <th>
            UF
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="op in operadorasOrdenadas" :key="op.cnpj" class="linha-tabela" @click="emit('visualizar', op.cnpj)">
          <td class="coluna-razao-social">{{ op.razao_social }}</td>
          <td class="coluna-cnpj">{{ formatarCNPJ(op.cnpj) }}</td>
          <td class="coluna-modalidade">{{ op.modalidade || '-' }}</td>
          <td class="coluna-uf">{{ op.uf }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Paginação -->
    <div v-if="operadorasFiltradas.length > 0" class="paginacao">
      <button
        :disabled="page === 1"
        @click="emit('pagina-anterior')"
        class="btn-pagina"
      >
        ← Anterior
      </button>

      <div class="paginacao-controles">
        <span class="info-pagina">
          Página 
          <input 
            v-model.number="paginaInput" 
            type="number" 
            min="1" 
            :max="totalPaginas"
            @keyup.enter="irParaPagina"
            @keyup.space="irParaPagina"
            class="input-pagina"
          />
          de {{ totalPaginas }}
        </span>
      </div>

      <button
        :disabled="page === totalPaginas"
        @click="emit('proxima-pagina')"
        class="btn-pagina"
      >
        Próxima →
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { formatarCNPJ } from '../../utils/formatadores';

const props = defineProps({
  operadoras: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  page: {
    type: Number,
    default: 1,
  },
  totalPaginas: {
    type: Number,
    default: 1,
  },
});

watch(() => props.operadoras, (novasOperadoras) => {
  console.log("OperadorasTable recebeu:", novasOperadoras?.length, "operadoras");
}, { immediate: true });

const emit = defineEmits(['buscar', 'visualizar', 'proxima-pagina', 'pagina-anterior', 'ir-pagina']);

const buscaLocal = ref('');
const campoBusca = ref('razao_social');
let debounceId = null;
const paginaInput = ref(props.page);
const ordenacao = ref({
  campo: null,
  direcao: 'asc',
});

watch(() => props.page, (novaPagina) => {
  paginaInput.value = novaPagina;
});

const operadorasFiltradas = computed(() => {
  return props.operadoras;
});

const placeholderBusca = computed(() => {
  return campoBusca.value === 'cnpj'
    ? 'Buscar por CNPJ...'
    : 'Buscar por razão social...';
});

const operadorasOrdenadas = computed(() => {
  if (!ordenacao.value.campo) {
    return operadorasFiltradas.value;
  }

  const copia = [...operadorasFiltradas.value];
  const campo = ordenacao.value.campo;
  const direcao = ordenacao.value.direcao;

  copia.sort((a, b) => {
    const aVal = a[campo];
    const bVal = b[campo];

    if (typeof aVal === 'string') {
      return direcao === 'asc' 
        ? aVal.localeCompare(bVal) 
        : bVal.localeCompare(aVal);
    }

    return direcao === 'asc' ? aVal - bVal : bVal - aVal;
  });

  return copia;
});

function ordenarPor(campo) {
  if (ordenacao.value.campo === campo) {
    ordenacao.value.direcao = ordenacao.value.direcao === 'asc' ? 'desc' : 'asc';
  } else {
    ordenacao.value.campo = campo;
    ordenacao.value.direcao = 'asc';
  }
}

function irParaPagina() {
  if (paginaInput.value >= 1 && paginaInput.value <= props.totalPaginas) {
    emit('ir-pagina', paginaInput.value);
  }
}

function emitirBusca() {
  if (debounceId) {
    clearTimeout(debounceId);
  }

  debounceId = setTimeout(() => {
    emit('buscar', buscaLocal.value, campoBusca.value);
  }, 300);
}
</script>

<style scoped>
.tabela-container {
  width: 100%;
  padding: 20px;
  background: var(--surface-muted);
  border-radius: 8px;
  border: 1px solid var(--border);
}

.busca-section {
  margin-bottom: 20px;
  position: relative;
}

.busca-controles {
  display: flex;
  gap: 10px;
  align-items: center;
}

.select-busca {
  padding: 10px 12px;
  border: 2px solid var(--border);
  border-radius: 6px;
  font-size: 14px;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
}

.select-busca:focus {
  outline: none;
  border-color: var(--primary);
}

.input-busca {
  width: 100%;
  flex: 1;
  padding: 12px;
  border: 2px solid var(--border);
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
  color: var(--text);
  background: var(--surface);
}

.input-busca::placeholder {
  color: var(--muted);
}

.input-busca:focus {
  outline: none;
  border-color: var(--primary);
}

.resultado-busca {
  position: absolute;
  right: 12px;
  top: 12px;
  color: var(--muted);
  font-size: 12px;
}

.estado-loading,
.estado-vazio {
  text-align: center;
  padding: 40px 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.tabela-operadoras {
  width: 100%;
  border-collapse: collapse;
  background: var(--surface);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border);
}

thead {
  background-color: var(--primary);
  color: #fff;
}

th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
}

.coluna-ordenavel {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.coluna-ordenavel:hover {
  background-color: var(--primary-600);
}

.ordenacao-icon {
  margin-left: 4px;
  font-size: 12px;
}

td {
  padding: 14px 12px;
  border-bottom: 1px solid var(--border);
  font-size: 14px;
  color: var(--text);
}

.linha-tabela:hover {
  background-color: var(--surface-muted);
  cursor: pointer;
}

.coluna-razao-social {
  font-weight: 500;
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.coluna-acoes {
  text-align: center;
}

.btn-detalhes {
  padding: 6px 12px;
  background-color: var(--primary);
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.2s;
}

.btn-detalhes:hover {
  background-color: var(--primary-600);
}

.paginacao {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

.paginacao-controles {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-pagina {
  font-size: 14px;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.input-pagina {
  width: 50px;
  padding: 4px 8px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 14px;
  text-align: center;
  background: var(--surface);
  color: var(--text);
}

/* Remove as setas do input number */
.input-pagina::-webkit-outer-spin-button,
.input-pagina::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.input-pagina[type=number] {
  appearance: textfield;
  -moz-appearance: textfield;
}

.btn-pagina {
  padding: 8px 16px;
  background-color: var(--primary);
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-pagina:hover:not(:disabled) {
  background-color: var(--primary-600);
}

.btn-pagina:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
