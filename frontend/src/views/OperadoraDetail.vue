<template>
  <div class="container">
    <div class="header">
      <router-link to="/" class="btn-voltar">← Voltar</router-link>
      <h1>{{ operadora?.razao_social || 'Carregando...' }}</h1>
    </div>

    <!-- Alerta de Erro -->
    <AlertaErro 
      :erro="erro" 
      @fechar="limparErro" 
    />

    <!-- Estado: Loading -->
    <div v-if="loading" class="estado-loading">
      <div class="spinner"></div>
      <p>Carregando detalhes...</p>
    </div>

    <!-- Dados: Operadora -->
    <div v-else-if="operadora" class="conteudo">
      <!-- Info Básica -->
      <div class="card info-basica">
        <h2>Informações Básicas</h2>
        <div class="info-grid">
          <div class="info-item">
            <label>Razão Social</label>
            <p>{{ operadora.razao_social }}</p>
          </div>
          <div class="info-item">
            <label>CNPJ</label>
            <p>{{ formatarCNPJ(operadora.cnpj) }}</p>
          </div>
          <div class="info-item">
            <label>Registro ANS</label>
            <p>{{ operadora.registro_ans }}</p>
          </div>
          <div class="info-item">
            <label>Modalidade</label>
            <p>{{ operadora.modalidade || '-' }}</p>
          </div>
          <div class="info-item">
            <label>UF</label>
            <p>{{ operadora.uf }}</p>
          </div>
          <div class="info-item">
            <label>Cidade</label>
            <p>{{ operadora.cidade || '-' }}</p>
          </div>
        </div>
      </div>

      <!-- Histórico de Despesas -->
      <div class="card historico-despesas">
        <h2>Histórico de Despesas</h2>
        
        <div v-if="!despesasDetail.historico || despesasDetail.historico.length === 0" class="estado-vazio estado-vazio-interno">
          <p>Nenhuma despesa registrada para esta operadora</p>
        </div>

        <div v-else>
          <div class="tabela-wrapper">
            <table class="tabela-despesas">
              <thead>
                <tr>
                  <th>
                    Ano
                  </th>
                  <th @click="ordenarDespesasPor('trimestre')" class="coluna-ordenavel">
                    Trimestre
                    <span v-if="ordenacaoDespesas.campo === 'trimestre'" class="ordenacao-icon">
                      {{ ordenacaoDespesas.direcao === 'asc' ? '▲' : '▼' }}
                    </span>
                  </th>
                  <th @click="ordenarDespesasPor('valor_despesas')" class="coluna-ordenavel">
                    Despesas
                    <span v-if="ordenacaoDespesas.campo === 'valor_despesas'" class="ordenacao-icon">
                      {{ ordenacaoDespesas.direcao === 'asc' ? '▲' : '▼' }}
                    </span>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(despesa, index) in despesasOrdenadas" :key="index">
                  <td class="coluna-ano">{{ despesa.ano }}</td>
                  <td class="coluna-trimestre">{{ despesa.trimestre }}º</td>
                  <td class="coluna-valor">{{ formatarMoeda(despesa.valor_despesas) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Estatísticas -->
          <div class="estatisticas">
            <div class="stat-item">
              <label>Total Despesas</label>
              <p class="valor-destaque">{{ formatarMoeda(totalDespesas) }}</p>
            </div>
            <div class="stat-item">
              <label>Média por Trimestre</label>
              <p class="valor-destaque">{{ formatarMoeda(mediaDespesas) }}</p>
            </div>
            <div class="stat-item">
              <label>Registros</label>
              <p class="valor-destaque">{{ despesasDetail.historico.length }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Estado: Não encontrado -->
    <div v-else class="card estado-vazio estado-vazio-pagina">
      <h2>Operadora não encontrada</h2>
      <p>Não há dados disponíveis para esta operadora.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useOperadorasStore } from '../stores/operadoras';
import { useErrorHandler } from '../composables/useErrorHandler';
import { formatarCNPJ, formatarMoeda } from '../utils/formatadores';
import AlertaErro from '../components/operadoras/AlertaErro.vue';

const route = useRoute();
const store = useOperadorasStore();
const { erro, definirErro, limparErro } = useErrorHandler();

const cnpj = route.params.cnpj;
const loading = ref(false);
const operadora = ref(null);
const ordenacaoDespesas = ref({
  campo: null,
  direcao: 'asc',
});

const despesasDetail = computed(() => store.despesasDetail);

const despesasOrdenadas = computed(() => {
  if (!despesasDetail.value.historico) return [];
  
  if (!ordenacaoDespesas.value.campo) {
    return despesasDetail.value.historico;
  }

  const copia = [...despesasDetail.value.historico];
  const campo = ordenacaoDespesas.value.campo;
  const direcao = ordenacaoDespesas.value.direcao;

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

const totalDespesas = computed(() => {
  if (!despesasDetail.value.historico) return 0;
  return despesasDetail.value.historico.reduce(
    (sum, d) => sum + parseFloat(d.valor_despesas || 0),
    0
  );
});

const mediaDespesas = computed(() => {
  if (!despesasDetail.value.historico || despesasDetail.value.historico.length === 0) return 0;
  return totalDespesas.value / despesasDetail.value.historico.length;
});

function ordenarDespesasPor(campo) {
  if (ordenacaoDespesas.value.campo === campo) {
    ordenacaoDespesas.value.direcao = ordenacaoDespesas.value.direcao === 'asc' ? 'desc' : 'asc';
  } else {
    ordenacaoDespesas.value.campo = campo;
    ordenacaoDespesas.value.direcao = 'asc';
  }
}

async function carregarDetalhes() {
  try {
    loading.value = true;
    
    // Carrega todos os dados da operadora (informações + despesas)
    await store.carregarDespesas(cnpj);
    
    // Usa os dados retornados pela API que incluem tudo
    operadora.value = store.despesasDetail;
    
    if (store.erro) {
      definirErro(new Error(store.erro.mensagem));
    }
  } catch (error) {
    definirErro(error);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  carregarDetalhes();
});
</script>

<style scoped>
.container {
  width: 1000px;
  margin: 0 auto;
  padding: 28px;
  background: var(--surface);
  min-height: 100vh;
  box-sizing: border-box;
  border-radius: 18px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

@media (max-width: 1040px) {
  .container {
    width: calc(100% - 40px);
    max-width: none;
  }
}

.header {
  margin-bottom: 30px;
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-voltar {
  display: inline-block;
  margin-bottom: 8px;
  padding: 9px 14px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: #fff;
  text-decoration: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.25);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-voltar:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 22px rgba(79, 70, 229, 0.35);
}

.header h1 {
  margin: 0;
  font-size: 30px;
  color: var(--text);
  word-break: break-word;
  overflow-wrap: break-word;
}

.estado-loading {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.conteudo {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
}

.card h2 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: var(--text);
  border-bottom: 2px solid rgba(79, 70, 229, 0.2);
  padding-bottom: 10px;
}

.info-basica {
  display: block;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
  padding: 12px;
  background: var(--surface-muted);
  border-radius: 10px;
  border: 1px solid var(--border);
}

.info-item label {
  display: block;
  font-size: 12px;
  color: var(--muted);
  text-transform: uppercase;
  margin-bottom: 8px;
}

.info-item p {
  margin: 0;
  font-size: 16px;
  color: var(--text);
  font-weight: 500;
}

.tabela-wrapper {
  overflow-x: auto;
  margin-bottom: 20px;
  border-radius: 12px;
  border: 1px solid var(--border);
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.06);
}

.tabela-despesas {
  width: 100%;
  border-collapse: collapse;
}

.tabela-despesas thead {
  background-color: var(--primary);
  color: #fff;
}

.tabela-despesas th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
}

.coluna-ordenavel {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.coluna-ordenavel:hover,
.coluna-ordenavel:active,
.coluna-ordenavel:focus {
  background-color: var(--primary-600);
  color: #fff;
}

.ordenacao-icon {
  margin-left: 4px;
  font-size: 12px;
}

.tabela-despesas td {
  padding: 12px;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}

.tabela-despesas tbody tr:hover {
  background-color: var(--surface-muted);
}

.coluna-ano {
  font-weight: 500;
  color: var(--text);
}

.coluna-valor {
  text-align: right;
  font-weight: 600;
  color: var(--success);
}

.estado-vazio {
  text-align: center;
  padding: 60px 20px;
  color: var(--muted);
  font-size: 16px;
  border-radius: 12px;
  border: 1px dashed var(--border);
}

.estado-vazio h2 {
  margin: 0 0 10px 0;
  font-size: 20px;
  color: var(--text);
}

.estado-vazio-pagina {
  padding: 40px 20px;
}

.estado-vazio-interno {
  background: var(--surface);
  border: 1px dashed var(--border);
}

.estatisticas {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
  background: var(--surface-muted);
  border-radius: 12px;
  padding: 20px;
}

.stat-item {
  text-align: center;
}

.stat-item label {
  display: block;
  font-size: 12px;
  color: var(--muted);
  text-transform: uppercase;
  margin-bottom: 8px;
}

.valor-destaque {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--primary);
}
</style>
