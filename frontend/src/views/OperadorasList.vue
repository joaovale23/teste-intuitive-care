<template>
  <div class="container">
    <div class="header">
      <h1>Operadoras ANS</h1>
      <p class="subtitle">Consulta de operadoras de saúde e análise de despesas</p>
    </div>

    <!-- Alerta de Erro -->
    <AlertaErro 
      :erro="erro" 
      @fechar="limparErro" 
    />

    <!-- Seção de Gráfico -->
    <div class="secao-grafico">
      <GraficoUF :operadoras="despesasUF" />
    </div>

    <!-- Seção de Tabela -->
    <div class="secao-tabela">
      <OperadorasTable
        :operadoras="operadoras"
        :loading="loading"
        :page="page"
        :totalPaginas="totalPaginas"
        @buscar="buscarOperadoras"
        @visualizar="abrirDetalhes"
        @proxima-pagina="irProxima"
        @pagina-anterior="irAnterior"
        @ir-pagina="irParaPagina"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useOperadorasStore } from '../stores/operadoras';
import { useRouter } from 'vue-router';
import OperadorasTable from '../components/operadoras/OperadorasTable.vue';
import GraficoUF from '../components/operadoras/GraficoUF.vue';
import AlertaErro from '../components/operadoras/AlertaErro.vue';

const store = useOperadorasStore();
const router = useRouter();

// Usar o store diretamente para manter reatividade
const operadoras = computed(() => store.operadoras);
const despesasUF = computed(() => store.despesasUF);
const loading = computed(() => store.loading);
const erro = computed(() => store.erro);
const page = computed(() => store.page);
const totalPaginas = computed(() => store.totalPaginas);
const carregarOperadoras = store.carregarOperadoras;
const buscarOperadoras = store.buscarOperadoras;
const limparErro = store.limparErro;

async function irProxima() {
  if (page.value < totalPaginas.value) {
    await carregarOperadoras(page.value + 1);
  }
}

async function irAnterior() {
  if (page.value > 1) {
    await carregarOperadoras(page.value - 1);
  }
}

async function irParaPagina(numeroPagina) {
  if (numeroPagina >= 1 && numeroPagina <= totalPaginas.value) {
    await carregarOperadoras(numeroPagina);
  }
}

function abrirDetalhes(cnpj) {
  router.push(`/operadora/${cnpj}`);
}

onMounted(() => {
  console.log("OperadorasList montado, carregando operadoras...");
  carregarOperadoras(1);
});
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: var(--surface);
  min-height: 100vh;
  border-radius: 16px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  margin: 0 0 10px 0;
  font-size: 32px;
  color: #000;
}

.subtitle {
  margin: 0;
  color: #333;
  font-size: 16px;
}

.secao-grafico {
  margin-bottom: 40px;
}

.secao-tabela {
  margin-bottom: 40px;
}
</style>
