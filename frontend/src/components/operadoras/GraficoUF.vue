<template>
  <div class="grafico-container">
    <div class="grafico-header">
      <h3>Distribuição de Despesas por UF</h3>
      <select v-model="tipoGrafico" class="tipo-grafico">
        <option value="bar">Barra</option>
        <option value="pie">Pizza</option>
        <option value="doughnut">Rosca</option>
      </select>
    </div>

    <div v-if="!temDados" class="sem-dados">
      <p>Nenhum dado disponível para exibir</p>
    </div>

    <canvas v-else ref="chartRef" class="canvas-grafico"></canvas>

    <div class="legenda">
      <p class="total-despesas">
        Total: <strong>{{ formatarMoeda(totalDespesas) }}</strong>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick, watchEffect } from 'vue';
import { Chart, registerables } from 'chart.js';
import { agruparDespesasPorUF, formatarMoeda } from '../../utils/formatadores';

Chart.register(...registerables);

const props = defineProps({
  operadoras: {
    type: Array,
    required: true,
  },
});

const chartRef = ref(null);
let chartInstance = null;
const tipoGrafico = ref('bar');

const temDados = computed(() => {
  const tem = props.operadoras && props.operadoras.length > 0;
  console.log("GraficoUF temDados:", tem, "operadoras:", props.operadoras?.length);
  return tem;
});

const chartData = computed(() => {
  if (!temDados.value) return null;
  const dados = agruparDespesasPorUF(props.operadoras);
  console.log("GraficoUF chartData:", dados);
  return dados;
});

const totalDespesas = computed(() => {
  if (!chartData.value) return 0;
  return chartData.value.datasets[0].data.reduce((a, b) => a + b, 0);
});

function criarGrafico() {
  if (!chartRef.value || !chartData.value) {
    console.log("Sem dados para gráfico");
    return;
  }

  console.log("Criando gráfico...");
  if (chartInstance) {
    chartInstance.destroy();
  }

  const config = {
    type: tipoGrafico.value,
    data: chartData.value,
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: tipoGrafico.value !== 'bar',
          position: 'bottom',
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label || '';
              const valor = formatarMoeda(context.parsed.y || context.parsed);
              return `${label}: ${valor}`;
            },
          },
        },
      },
      scales: tipoGrafico.value === 'bar' ? {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return 'R$ ' + value.toLocaleString('pt-BR');
            },
          },
        },
      } : undefined,
    },
  };

  chartInstance = new Chart(chartRef.value, config);
}

watch(tipoGrafico, () => {
  criarGrafico();
});

// Quando tipo de gráfico muda, recria
watch(() => props.operadoras, () => {
  nextTick(() => criarGrafico());
}, { deep: true, immediate: true });

onMounted(() => {
  console.log("GraficoUF montado, temDados:", temDados.value);
  // Usar watchEffect para garantir que o gráfico é criado quando dados chegam
  watchEffect(() => {
    if (temDados.value && chartData.value) {
      console.log("watchEffect disparado, criando gráfico");
      nextTick(() => criarGrafico());
    }
  });
});
</script>

<style scoped>
.grafico-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.grafico-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.grafico-header h3 {
  margin: 0;
  font-size: 18px;
  color: #000;
}

.tipo-grafico {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.canvas-grafico {
  max-height: 400px;
}

.sem-dados {
  text-align: center;
  padding: 40px 20px;
  color: #000;
}

.legenda {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  text-align: center;
}

.total-despesas {
  margin: 0;
  font-size: 16px;
  color: #000;
}
</style>
